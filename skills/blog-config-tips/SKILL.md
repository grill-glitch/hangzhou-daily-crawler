# blog-config-tips

提供 Hexo 博客配置技巧、性能优化、主题定制和故障排除。

## 描述

此技能帮助用户：
- 优化博客构建速度
- 配置 Nginx/SSL
- 管理主题和插件
- SEO 优化
- 评论系统集成
- 图片懒加载与压缩
- 安全加固与隐私保护

## 触发器

- "博客配置技巧"
- "Hexo 优化"
- "博客性能"
- "Nginx 配置"
- "主题定制"
- "SEO 设置"
- "评论系统"
- "图片优化"
- "博客安全"
- "备份策略"

## 输入

用户请求与博客配置相关的帮助。

## 输出

提供具体、可执行的配置建议、命令行操作、配置文件示例，并询问是否需要执行。

## 实现

- 主脚本: `blog-config-tips.py`
- 辅助脚本: `scripts/check-blog.sh`
- 参考文档: `references/CONFIG_TIPS.md`

## 使用方式

当用户请求博客配置帮助时，调用此 Skill 的 Python 脚本：
```bash
python3 skills/blog-config-tips/blog-config-tips.py <intent> [params]
```

支持 intents:
- `check_performance` - 检查博客性能并给出建议
- `nginx_optimize` - 生成 Nginx 优化配置
- `backup` - 备份博客配置
- `general_tips` - 提供通用配置技巧

## 注意事项

- 操作前自动备份配置文件
- 危险操作（如清空数据库）需用户确认
- Nginx 配置修改后自动测试语法并重载
- 所有操作在用户博客目录 `/var/www/myblog` 中进行

## 权限

需要：
- 文件读写权限（博客目录）
- Shell 执行权限（hexo、nginx 命令）
- Nginx 配置重载权限（可选，通过 sudo）
