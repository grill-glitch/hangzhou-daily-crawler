# Blog Config Tips Skill

Hexo 博客配置技巧与优化指南。

## 快速开始

```bash
# 检查博客性能和配置
BLOG_DIR=/var/www/myblog python3 blog-config-tips.py check_performance

# 生成 Nginx 优化配置
BLOG_DIR=/var/www/myblog python3 blog-config-tips.py nginx_optimize

# 备份博客配置
BLOG_DIR=/var/www/myblog python3 blog-config-tips.py backup

# 查看通用技巧
BLOG_DIR=/var/www/myblog python3 blog-config-tips.py general_tips
```

## 功能

- ✅ 性能检查（包管理器、图片优化、主题配置）
- ✅ Nginx 优化配置生成（gzip、缓存、安全头）
- ✅ 一键备份（配置 + 主题）
- ✅ 通用配置技巧汇总

## 文件结构

```
skills/blog-config-tips/
├── SKILL.md              # 技能定义
├── blog-config-tips.py   # 主脚本
├── scripts/
│   └── check-blog.sh     # Shell 检查脚本
└── references/
    └── CONFIG_TIPS.md    # 详细配置参考
```

## 与 OpenClaw 集成

此 Skill 通过自然语言触发，例如：
- "博客配置技巧"
- "Hexo 优化"
- "博客性能"
- "Nginx 配置"
- "主题定制"

## 注意事项

- 所有操作默认针对 `/var/www/myblog`
- 可通过 `BLOG_DIR` 环境变量修改路径
- 危险操作（如备份）会自动确认
- Nginx 配置生成后需要手动应用

## 更新日志

**2026-03-21** - 初始版本
- 创建基本性能检查
- 添加 Nginx 优化模板
- 实现配置备份功能
