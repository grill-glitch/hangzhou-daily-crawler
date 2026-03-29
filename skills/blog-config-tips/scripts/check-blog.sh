#!/usr/bin/env bash

# Blog Config Tips - 示例脚本
# 演示如何使用此 Skill 执行常见配置任务

set -e

BLOG_DIR="${1:-/var/www/myblog}"

echo "=== Hexo 博客配置检查 ==="
echo "博客目录: $BLOG_DIR"

# 1. 检查依赖管理
echo -e "\n[1] 检查包管理器..."
if [ -f "$BLOG_DIR/pnpm-lock.yaml" ]; then
    echo "✓ 使用 pnpm"
elif [ -f "$BLOG_DIR/package-lock.json" ]; then
    echo "✓ 使用 npm"
else
    echo "⚠ 未检测到锁文件"
fi

# 2. 检查主题
echo -e "\n[2] 检查主题..."
if [ -L "$BLOG_DIR/current-theme" ]; then
    echo "✓ 软链接主题: $(readlink $BLOG_DIR/current-theme)"
else
    echo "主题: $(grep '^theme:' $BLOG_DIR/_config.yml | cut -d' ' -f2)"
fi

# 3. 构建时间测试
echo -e "\n[3] 测试构建速度..."
time (cd "$BLOG_DIR" && hexo clean > /dev/null 2>&1 && hexo g > /dev/null 2>&1)
echo "✓ 构建完成"

# 4. 检查图片优化
echo -e "\n[4] 图片优化建议..."
if grep -q "sharp" "$BLOG_DIR/package.json" 2>/dev/null; then
    echo "✓ 已安装 sharp (图片优化)"
else
    echo "⚠ 未安装 sharp，建议: pnpm add sharp"
fi

# 5. Nginx 配置检查（如果存在）
if [ -f "/etc/nginx/conf.d/blog.conf" ]; then
    echo -e "\n[5] Nginx 配置文件存在"
    echo "   建议启用 gzip 压缩和缓存"
fi

echo -e "\n=== 检查完成 ==="
echo "更多配置技巧请参考 Skill 文档"
