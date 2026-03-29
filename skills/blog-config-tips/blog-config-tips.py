#!/usr/bin/env python3
"""
Blog Config Tips Skill
提供 Hexo 博客配置相关的实用功能
"""

import os
import sys
import json
import subprocess
from pathlib import Path

BLOG_DIR = os.environ.get('BLOG_DIR', '/var/www/myblog')

def run_shell(cmd, cwd=None):
    """运行 shell 命令"""
    result = subprocess.run(
        cmd, shell=True, cwd=cwd or BLOG_DIR,
        capture_output=True, text=True
    )
    return result.returncode, result.stdout, result.stderr

def check_performance():
    """检查博客性能"""
    tips = []
    
    # 检查包管理器
    if (Path(BLOG_DIR) / 'pnpm-lock.yaml').exists():
        tips.append("✅ 使用 pnpm - 依赖管理良好")
    else:
        tips.append("⚠️  建议切换到 pnpm 以获得更好的依赖管理")
    
    # 检查图片优化
    package_json = Path(BLOG_DIR) / 'package.json'
    if package_json.exists():
        import json
        with open(package_json) as f:
            pkg = json.load(f)
        if 'sharp' in pkg.get('dependencies', {}):
            tips.append("✅ 已安装 sharp - 图片优化就绪")
        else:
            tips.append("⚠️  未安装 sharp，建议: pnpm add sharp")
    
    # 检查主题配置
    config_path = Path(BLOG_DIR) / '_config.yml'
    if config_path.exists():
        content = config_path.read_text()
        if 'lazyload: true' in content:
            tips.append("✅ 图片懒加载已启用")
        if 'dark_mode: true' in content:
            tips.append("✅ 暗黑模式已启用")
    
    return "\n".join(tips) if tips else "未发现问题"

def optimize_nginx():
    """生成 Nginx 优化配置片段"""
    config = """# Hexo 博客 Nginx 优化配置
server {
    # 启用 gzip 压缩
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_types text/plain text/css text/xml text/javascript application/javascript application/xml+rss application/json;
    
    # 静态资源缓存
    location ~* \\.(jpg|jpeg|png|gif|ico|css|js|woff2|ttf)$ {
        expires 365d;
        add_header Cache-Control "public, immutable";
    }
    
    # 安全头
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
}
"""
    return config

def backup_config():
    """备份博客配置"""
    import datetime
    backup_dir = Path('/var/backups/blog-config') / datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
    backup_dir.mkdir(parents=True, exist_ok=True)
    
    files_to_backup = [
        '_config.yml',
        'package.json',
        'pnpm-lock.yaml',
        'package-lock.json'
    ]
    
    for f in files_to_backup:
        src = Path(BLOG_DIR) / f
        if src.exists():
            import shutil
            shutil.copy2(src, backup_dir / f)
    
    themes_backup = backup_dir / 'themes'
    themes_backup.mkdir(exist_ok=True)
    import shutil
    if (Path(BLOG_DIR) / 'themes').exists():
        for theme in os.listdir(Path(BLOG_DIR) / 'themes'):
            theme_src = Path(BLOG_DIR) / 'themes' / theme
            if theme_src.is_dir():
                shutil.copytree(theme_src, themes_backup / theme, dirs_exist_ok=True)
    
    return str(backup_dir)

def handle_request(intent, params=None):
    """处理用户请求"""
    responses = []
    
    if intent == 'check_performance':
        result = check_performance()
        responses.append(f"性能检查结果:\n{result}")
    
    elif intent == 'nginx_optimize':
        config = optimize_nginx()
        responses.append("Nginx 优化配置片段:")
        responses.append(f"```nginx\n{config}\n```")
        responses.append("建议将此配置添加到 /etc/nginx/conf.d/blog.conf 并运行 nginx -t && systemctl reload nginx")
    
    elif intent == 'backup':
        backup_path = backup_config()
        responses.append(f"✅ 配置已备份到: {backup_path}")
    
    elif intent == 'general_tips':
        responses.append("博客配置技巧:\n")
        responses.append("1. 使用 pnpm 管理依赖，更快更稳")
        responses.append("2. 启用 gzip 和缓存（Nginx）")
        responses.append("3. 安装 sharp 进行图片优化")
        responses.append("4. 配置懒加载加速首屏")
        responses.append("5. 定期备份 source/ 和 _config.yml")
        responses.append("6. 禁用不必要的主题功能")
        responses.append("7. 使用 CDN 托管静态资源（可选）")
    
    return "\n\n".join(responses)

# CLI 入口
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("用法: blog-config-tips.py <intent> [params]")
        sys.exit(1)
    
    intent = sys.argv[1]
    params = sys.argv[2:] if len(sys.argv) > 2 else None
    
    print(handle_request(intent, params))
