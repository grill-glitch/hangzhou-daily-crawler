# 博客配置技巧参考

## Hexo Magzine 主题完整配置指南

来源：https://2am.top/2026/01/28/magzine%E4%B8%BB%E9%A2%98%E6%8C%87%E5%8C%97/

### 安装

```bash
# 从 GitHub
git clone https://github.com/forever218/hexo-theme-magzine.git themes/magzine

# 或从 Gitee（可能稍滞后）
git clone https://gitee.com/ran_brother/hexo-theme-magzine.git themes/magzine
```

### 升级

```bash
cd themes/magzine
git pull
# 建议升级前备份 _config.yml
```

### 评论系统（Twikoo）

在主题 `_config.yml` 中配置：

```yaml
comments:
  enable: true
  type: twikoo
  twikoo:
    envId: your_env_id    # 必填
    region: ap-guangzhou  # 你的服务区域
    path: window.location.pathname
    visitor: true
```

部署方法见 [twikoo.js.org](https://twikoo.js.org/)

### AI 摘要功能

**注意**：新版方案需通过 Workers 实现 API 白名单（原方案不安全）。

配置示例：

```yaml
ai_summary:
  enable: true
  api_key: ""            # 留空，使用白名单方式
  summary_directly: false
  ai_name: "然-AI"
  ai_introduce: "我是文章辅助AI..."
  ai_version: "deepseekv3"
  buttons:
    - "介绍自己"
    - "来点灵感"
    - "生成AI简介"
```

详细配置：[Workers 实现 Api 白名单](https://2am.top/2025/12/22/Workers%E5%AE%9E%E7%8E%B0Api%E7%99%BD%E5%90%8D%E5%8D%95/)

### 必需页面

```bash
# 标签页
hexo new page tags
# 编辑 source/tags/index.md
---
title: tags
layout: tag
---

# 分类页
hexo new page categories
# 编辑 source/categories/index.md
---
title: categories
layout: categories
---

# 友链页
hexo new page link
# 编辑 source/link/index.md
---
title: link
layout: link
---

# 关于页
hexo new page about
# 可选：编辑 themes/magzine/layout/about.pug 自定义样式
```

### 友链配置

创建 `source_data/link.yml`（YAML 格式）：

```yaml
- name: 未来的回忆
  link: https://2am.top
  avatar: https://2am.top/images/0.gif
  description: 人生而自由，却无往不在枷锁之中

# 后续友链条目...
```

### 标签插件（短代码）

#### 1. note - 提示块

**两种样式**：`modern`（现代）、`simple`（简易）

```markdown
{% note modern %}
基础标签
{% endnote %}

{% note 'fas fa-bullhorn' modern %}
带图标的标签
{% endnote %}

{% note default modern %}default{% endnote %}
{% note info modern %}info{% endnote %}
{% note success modern %}success{% endnote %}
{% note warning modern %}warning{% endnote %}
{% note danger modern %}danger{% endnote %}
```

**simple 样式**：将 `modern` 替换为 `simple`

#### 2. btn - 按钮

```markdown
{% btn 'https://2am.top',我的博客,far fa-hand-point-right,blue larger %}
{% btn 'https://2am.top',我的博客,far fa-hand-point-right,purple outline %}
{% btn 'https://2am.top',我的博客,far fa-hand-point-right,pink block %}
```

参数：`url, 文本, 图标, [颜色] [样式]`

颜色可选：`default blue pink red purple orange green`

样式可选：`outline center block larger`

#### 3. tabs - 标签页

```markdown
{% tabs 标签id %}
<!-- tab 标签1 -->
内容1
<!-- endtab -->
<!-- tab 标签2 -->
内容2
<!-- endtab -->
{% endtabs %}
```

#### 4. hideToggle - 折叠内容

```markdown
{% hideToggle 点击展开 %}
这里是隐藏的内容...
{% endhideToggle %}
```

#### 5. video - 视频嵌入

```markdown
{% video https://www.bilibili.com/video/BV1jzYXzVECb %}
```

支持平台：Bilibili、AcFun、西瓜视频、虎牙、YouTube、Twitter/X、Instagram、Twitch

#### 6. timeline - 时间线

```markdown
{% timeline 2026年 %}
<!-- timeline 1-20 -->
准备起飞
<!-- endtimeline -->
<!-- timeline 1-21 -->
正在起飞
<!-- endtimeline -->
{% endtimeline %}
```

#### 7. hideInline - 内联隐藏

```markdown
{% hideInline [隐藏文字],[显示文字],[背景色],[字体色] %}
测试字段{% hideInline 不嘻嘻😠,嘻嘻🤭,#FF7242,#fff %}测试字段
```

#### 8. label - 标签

```markdown
{% label 测试样例 red %}
{% label 测试样例 info %}
```

颜色：`default primary success info warning danger important` 或自定义十六进制

---

## 性能优化

### Nginx 配置

启用 gzip 和缓存：

```nginx
gzip on;
gzip_vary on;
gzip_min_length 1024;
gzip_types text/plain text/css text/xml text/javascript application/javascript application/xml+rss application/json;

location ~* \.(jpg|jpeg|png|gif|ico|css|js|woff2|ttf)$ {
    expires 365d;
    add_header Cache-Control "public, immutable";
}
```

### Hexo 构建

- 使用 pnpm（比 npm 更快）
- 安装 `sharp` 依赖加速图片处理
- 关闭不必要的插件

```bash
pnpm add sharp
```

### 主题配置

```yaml
# 启用懒加载
lazyload: true
# 启用暗黑模式
dark_mode: true
```

## 安全建议

1. 定期备份 `source/` 和 `_config.yml`
2. 使用版本锁（pnpm-lock.yaml）
3. 及时更新 Hexo 和主题
4. 禁用不必要的第三方 API
5. 配置 Nginx 安全头

```nginx
add_header X-Frame-Options "SAMEORIGIN" always;
add_header X-Content-Type-Options "nosniff" always;
```

---

*最后更新：2026-03-21*
