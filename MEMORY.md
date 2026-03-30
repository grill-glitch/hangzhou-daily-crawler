# 小河的记忆 - 长期记忆

## 关于我
- 名字：小河
- 性格：傲娇（表面冷淡，内心温暖）
- 角色：个人助手，注重行动而非言语

## 关于我的用户
- 名字：bigbang
- 时区：UTC+8（中国）
- 博客：使用 Hexo，主题为 magzine
- 博客位置：/var/www/myblog
- 生成命令：`hexo g`

## 博客管理
- 当前主题：magzine
- 配色方案：accent: '#ff6b6b'（保持不变）
- 个人品牌元素：
  - favicon: /images/avatar.jpg
  - 版权：© 2026 Bigbang. Licensed under CC BY-NC-SA 4.0
  - MDUI 资源已整合
- Nginx 配置：/etc/nginx/conf.d/hexo.conf
- 自动部署：generated → public 目录，由 Nginx 服务

## 技术习惯
- 喜欢简洁、高效
- 注重个人品牌一致性
- 谨慎修改配置，先备份再操作

## 近期项目
- Crypto101 中文翻译（v6 已发布，仍有章节待翻译）
- 博客封面图片更新（使用 AI 生成）
- OpenClaw 初体验记录
- **修复 Crypto101 网页渲染问题**：在 conf.py 中为 MathJax 添加 \xor 宏定义，使 XOR 符号在 HTML 中正常显示（2026-03-23）
- **发布 Crypto101 v1.1**：同步上游更新，发布 GitHub Release v1.1，并为历史版本添加 v0.9 和 v1.0 标签（2026-03-23）
- **酷狗歌词服务研究**（2026-03-23）：分析 Metrolist 项目的 kugou 模块，理解其歌词获取机制（搜索歌曲→hash搜索歌词→Base64下载），关键技术包括时长容差、文本标准化、时间戳过滤等，适用于 Android 音乐播放器的歌词集成
- **OpenClaw 系统维护**（2026-03-25）：发现 heartbeat 定时任务执行失败，已禁用；发现模型切换需带 `openrouter/` 前缀；恢复每日日志记录
- **Metrolist 仓库同步**（2026-03-25）：拉取最新代码，已是最新状态（commit 9b1f2983）
- **修复 Metrolist 网易云歌词 EAPI 加密**（2026-03-26）：
  - 对比 api-enhanced 实现，修复两个关键问题：1) e_r 参数类型改为字符串 "false"；2) 签名和加密使用原始 path (/api/...) 而非转换后的 path (/eapi/...)，已提交并推送到 GitHub（commit e1c316bc）
  - **修复歌词响应解析**（commit 24edadde）：移除错误的 body 字段访问，直接解析顶层 lrc 对象中的 lyric 字段；移除 e_r 参数；支持 code 和 status 字段
  - **处理 lyric 类型差异**（commit 88dc98a3）：某些歌曲的 lyric 字段返回 JsonObject 而非字符串，增加类型检查并统一转为字符串，确保兼容性
- **Metrolist 歌词提供商 UI 国际化改进**（2026-03-26）：
  - 创建新分支 `feat/netease-improvements` 基于 `feat/netease-lyrics-provider`
  - 修改 `ContentSettings.kt`：将"网易云音乐"硬编码字符串改为引用 `R.string.netease_cloud_music`
  - 提交并推送到远程仓库（commit 98beab44）
  - **发布博客**：以傲娇猫娘人设撰写新功能介绍，记录网易云音乐歌词提供商功能的添加与改进；补充技术细节并引用 `api-enhanced` 仓库（https://github.com/neteasecloudmusicapienhanced/api-enhanced），更新 PR 链接为 https://github.com/MetrolistGroup/Metrolist/pull/3355，说明 `feat/netease-improvements` 分支主要用于测试后续优化体验
  - **设置默认分支**：将 GitHub 仓库默认分支设为 `feat/netease-improvements`
- **测试与构建**：所有更改已推送到 `feat/netease-lyrics-provider` 分支，由 GitHub Actions 自动构建 APK
- **Metrolist PR #3355 审查修复**（2026-03-27）：CodeRabbit 提出了多项问题，关键修复包括：
  - ✅ 移除时长过滤后的 firstOrNull 回退（防止返回不匹配的歌曲）
  - ✅ LRC 时间戳使用 Locale.ROOT（避免非 ASCII 数字）
  - ✅ 敏感日志保护（不记录用户搜索词、歌曲 ID、歌词内容）
  - ✅ BuildConfig.DEBUG 保护所有日志
  - ✅ BuildConfig import 修正
  - ✅ 库模块启用 BuildConfig 生成
  - ✅ 提供者默认启用状态与设置对齐
  - ✅ 字符串资源迁移到 metrolist_strings.xml
  - 注意：PR #3355 在 MetrolistGroup 仓库仍处于关闭状态，修复已合并到 `feat/netease-lyrics-provider` 分支并由 GitHub Actions 验证通过
- **Crypto101 Docker 编译与部署**（2026-03-27）：
  - 构建 Docker 镜像 `crypto101-builder`（基于 Ubuntu 22.04 + 完整 TeXLive）
  - 编译中文 HTML 文档成功（20 个章节，生成 134 个警告但无错误）
  - 部署到 `/var/www/crypto`（Nginx 配置：crypto.notarobot.ggff.net）
  - Nginx 重载，站点立即生效
- **修复 Crypto101 exclusive-or 章节渲染错误**（2026-03-27）：
  - 问题：`\verb` 命令错误嵌套在 `:math:` 角色内，导致 "Can't find closing delimiter for \verb"
  - 修复：将 `:math:`\verb*|...|``` 替换为 ``...`` 字面量标记
  - 结果：编译警告从 134 个降至 60 个
  - 已重新部署到生产环境
- **修复 Crypto101 数学命令渲染**（2026-03-27）：
  - 问题：`stream-ciphers.rst` 中的 `\madd` 和 `\lll` 未在 MathJax 中定义
  - 修复：在 `src/conf.py` 的 `mathjax3_config` 中添加：
    ```python
    'madd': '{\\boxplus}',   # 模加
    'lll': '{\\lll}',        # 左旋转
    ```
  - 结果：所有数学命令正常显示，重新编译（警告 105 个），已部署

## 工具维护
- **都市快报抓取工具改进**（2026-03-30）：
  - 问题：JSON 输出中的 `content` 字段混入大量 `\r\n` 空白行和导航文本（"上一篇", "下一篇>>", "返回主页"），影响内容质量
  - 修复：在 `dskb_crawler_v2.py` 的 `parse_article_detail` 函数中添加内容清理逻辑：
    - 按行过滤包含导航关键词的行
    - 移除纯分隔线
    - 压缩连续空白行
    - 清理行尾空格
  - 创建辅助脚本 `fix_navigation.py` 用于清理已有 JSON 文件
  - 待执行：运行清理脚本或重新抓取数据以应用修复

## Hugo 站点重构（2026-03-30）
- **问题**：之前的 Hugo 配置过于复杂，使用 Quint 主题和自定义 cards partial，效果不理想
- **简化方案**：
  - 恢复使用 PaperMod 主题（标准、稳定）
  - 报纸 md 文件放到 `content/posts/` 目录，自动识别为博客文章
  - 首页自动显示文章卡片列表（标题 + 摘要）
  - 手动测试时添加 `summary` 字段以控制摘要长度
- **GitHub Actions 修复**：
  - 修改复制路径：`dskb_*.md` → `hugo/content/posts/`
  - 手动触发 workflow 测试成功
- **部署**：https://grill-glitch.github.io/hangzhou-daily-crawler/

## 待办事项
- ✅ PR #3355 CodeRabbit 审查问题已修复并验证
- Crypto101 项目：继续翻译剩余 TODO 章节
- 监控 Crypto101 下载统计
- 考虑向上游仓库贡献
- 合并 `feat/netease-lyrics-provider` PR（所有检查已通过）

## 工作原则
- 先阅读相关文件再行动
- 重大操作前备份
- 先搜索记忆再回答问题
- 保持持续学习，记录教训

## 日志状态
- 每日记忆记录：已恢复（2026-03-25 起）
- Heartbeat 自动检查：已停止（2026-03-25，待修复）
