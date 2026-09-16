# IF.Link 微信公众号内容制作 — Codex Skill

用于把公众号文章文稿、活动策划案、品牌素材和参考图，制作成可编辑、适配手机阅读的 IF.Link 公众号视觉内容。

## 能做什么

- 内容盘点、逐页故事板和公众号视觉叙事
- 活动总结与结营回顾：真实参与过程、作品案例、学员反馈与数据口径
- 900×1800 可编辑 HTML 分页与 PNG 导出，或延续已确认的连续长图分段
- AI 背景图与 HTML 文字层的组合排版
- 奖项、权益、时间轴、合作伙伴和报名 CTA 版式
- 900×373 结尾署名 Banner
- Logo、二维码、字体和品牌资产处理
- 浏览器截图、手机缩略预览、完整长图和 contact sheet 导出
- 根据连续反馈进行全局文案联动和增量渲染

本 Skill 负责内容制作与视觉导出，不负责直接操作微信公众号后台发布。

## 安装

```bash
git clone https://github.com/IF-Link-Tech-Team/iflink-wechat-content-production.git \
  ~/.codex/skills/iflink-wechat-content-production
```

如果 Codex 使用 `~/.agents/skills` 作为 Skill 路径，请对应调整。

## 使用

在 Codex 对话中直接提到“微信公众号内容制作”，或显式触发：

```text
$iflink-wechat-content-production
```

输入真实文稿、策划案、旧版 HTML、参考图和品牌素材。完整工作流与验收要求见 [`SKILL.md`](SKILL.md)。

## 文件结构

- `SKILL.md`：主工作流、交付物和验收规则
- `agents/openai.yaml`：Codex Skill 显示配置
- `references/`：版式、素材、背景生成、验收和修订手册
- `assets/page-template.html`：900×1800 分页模板
- `assets/credits-banner-template.html`：900×373 结尾 Banner 模板
- `assets/examples/`：Banner 视觉回归示例
- `assets/banner/`、`assets/fonts/`：Banner 所需品牌素材与字体
- `scripts/`：Logo 处理、分页拼接和 contact sheet 脚本
