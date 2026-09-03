---
name: iflink-wechat-content-production
description: Create, revise, render, and export editable IF.Link WeChat official-account content packages from article copy, campaign plans, local brand assets, reference posters, or existing HTML. Use for IF.Link event announcements, competition campaigns, community recruitment posts, article visual sequences, AI-generated backgrounds with HTML typography, mobile-readability revisions, Logo/QR/credits treatment, and final long-image exports.
---

# IF.Link 微信公众号内容制作

把文稿、策划案、品牌素材和参考图转化为可编辑 HTML、分页图片、结尾 Banner、手机预览及完整长图。始终交付真实文件，并以手机端可读性、品牌一致性和后续可修改性为优先级。

## 开始前

1. 读取用户给出的真实文稿、飞书页面、策划案、旧版 HTML、参考图和素材目录。
2. 优先延续项目中已经确认的文案、字体、Logo、二维码、署名与视觉语言，不凭记忆重建。
3. 将反馈区分为：
   - 全局规则：正文字号、行高、页边距、字体、对比度、Logo 处理方式。
   - 局部修订：某页位置、某个 Logo、某条文案或某个时间节点。
4. 若项目已有 HTML，做最小范围的可编辑修改；不要退回到不可编辑的整图文字。
5. 迭代现有长图时读取 [references/revision-playbook.md](references/revision-playbook.md)，先确定反馈影响范围，再修改、增量渲染和回拼，避免旧文案或旧分页残留。

## 核心交付物

至少交付：

- 可编辑 HTML 源文件；
- 每页 900px 宽的 PNG；
- 一张按顺序拼接的完整长图；
- 手机缩略总览或 contact sheet；
- 独立、可编辑的结尾署名 Banner（用户需要时）。

不要只给设计建议或代码片段。完成渲染、检查和导出。

## 标准工作流

### 1. 做内容盘点

从源文稿提取：标题、开场情景、活动介绍、奖项、参与权益、产品介绍、时间轴、联合主办、生态伙伴、报名 CTA、免责声明和署名。

建立逐页故事板。内容过多时增加纵向空间或页数，不要通过缩小正文硬塞。参考顺序：

`封面 → 情景带入 → 活动介绍 → 奖项 → 产品/工具介绍 → 参与权益 → 时间轴 → 主办与合作伙伴 → 报名 CTA → 署名 Banner`

### 2. 选择版式方向

- 需要模块化信息、奖项卡片或结构化权益时，可使用 Bento。
- 需要更从容的阅读节奏、较长正文或杂志感时，优先使用非 Bento 编辑部版式。
- 用户要求两个版本时，共享同一内容结构、字体规范和素材处理规则，仅改变信息组织方式。

读取 [references/brand-and-layout.md](references/brand-and-layout.md) 后确定画布、字体、间距和首屏结构。

### 3. 生成或整理背景

需要 AI 背景时，先读取当前可用的 image generation Skill，并遵循它的调用规范。

- 每个背景只生成环境、器物、材质、声波和留白。
- 禁止让模型生成中文、Logo、二维码、表格、奖项数字或时间轴。
- 在提示词中明确 HTML 文字区的位置、占比与负空间。
- 分段生成背景，保持同一纸张材质、橙色声波、黑色台座和器物语言。
- 生成后逐张检查畸变、背景干扰和可用留白；不合格则重做背景，不用半透明文字勉强补救。

需要提示词结构时读取 [references/image-generation.md](references/image-generation.md)。

### 4. 用 HTML 排文字和信息

从 [assets/page-template.html](assets/page-template.html) 复制起始结构，或在项目现有 HTML 中继续工作。

- 使用真实 HTML 文本，禁止把正文烘焙进背景图。
- 固定每个分页画布为 `900 × 1800`，允许完整长图包含任意数量的分页。
- 为每页提供 `#capture-N` 锚点，只显示目标页，便于确定性截图。
- 统一中文正文的字体、字号、字重和行高；不要对中文字形做横向或纵向拉伸。
- 首屏大标题使用具有明确性格的中文衬线体；正文使用思源黑体等可读性稳定的无衬线体。
- 先保证最小字号、左右安全边距和对比度，再处理装饰。
- 大标题、说明、正文、数字和注释分别建立 CSS token，避免同级文字忽大忽小。

### 5. 处理 Logo、二维码和合作伙伴

读取 [references/asset-treatment.md](references/asset-treatment.md)。

- 优先使用官方 SVG 或透明 PNG。
- 以可见墨迹边界而非图片画布边界做对齐。
- 清理白边、整块底色和多余透明画布，但不要裁掉 Logo 正式图形。
- 浅色背景优先使用透明底纯黑 Logo；深色 Banner 使用透明底白色 Logo/二维码。
- 四个合作伙伴优先采用左对齐的 2×2 排列，使 Logo 更大且避开背景器物。
- 按视觉体量校准 Logo，不能只给所有文件相同 CSS 宽高。
- 二维码去除装饰白框时，仍须保留清晰、均匀的 quiet zone，并实测可扫描。

处理栅格 Logo 时可运行：

```bash
python3 scripts/normalize_logo.py INPUT OUTPUT --mode preserve-alpha
python3 scripts/normalize_logo.py INPUT OUTPUT --mode light-on-dark --low 165 --high 245
python3 scripts/normalize_logo.py INPUT OUTPUT --mode dark-on-light --low 10 --high 245
```

SVG 保持矢量优先；若源文件包含大画布留白，在 HTML 中使用裁切容器或修正副本的 `viewBox`，不要低清栅格化。

### 6. 制作结尾署名 Banner

统一使用可编辑的 [assets/credits-banner-template.html](assets/credits-banner-template.html) 制作结尾 Banner，画布为 `900 × 373px`。模板按最新署名版参考实现的坐标、字体、混排基线和素材尺寸复刻；[assets/examples/IF.Link_推送banner_署名版_900px.png](assets/examples/IF.Link_推送banner_署名版_900px.png) 作为视觉回归基准。

模板中的英文/数字与中文必须继续使用 `.latin`、`.cjk` 分段，以复现最新示例的 Google Sans Flex + 思源黑体混排效果。修改署名、二维码标签或右下角介绍时只替换 HTML 文本，不改变坐标和字号；最终按 `900 × 373px` 截图导出真实 PNG。

- 署名、设计、审核使用用户确认的姓名和组织前缀。
- 使用官方 IF.Link Logo，不用文字临摹 Logo。
- 二维码与左侧人员信息大致处于同一高度。
- 平台名靠近二维码，不加多余圆点或图标。
- 当前模板使用黑底、白字、橙色署名标签、99px 二维码、左下 Logo/口号和右下社区介绍；若项目确认其他视觉方向，HTML 模板和示例图必须一起更新。

### 7. 浏览器渲染和视觉检查

启动本地服务器，用浏览器自动化对每页做关键截图。前端修改必须截图验收。

建议直接截取页面坐标：

```text
clip: { x: 0, y: 0, width: 900, height: 1800 }
```

不要依赖超长页面 `fullPage` 拼接；它可能在固定画布或哈希目标页面上重复内容。若截图接口返回 JPEG 字节，即使扩展名写成 `.png`，也先转码成真实 PNG 再拼接。

读取 [references/qa-and-export.md](references/qa-and-export.md) 完成手机端、Logo、二维码、背景和尺寸检查。

### 8. 拼接完整长图

按页面顺序拼接，并把署名 Banner 放在最后：

```bash
python3 scripts/compose_long_image.py \
  --pages output/page-1.png output/page-2.png output/page-3.png \
  --banner output/credits-banner.png \
  --output output/完整长图.png \
  --contact-sheet previews/contact-sheet.png
```

脚本会校验宽度、顺序和输入存在性。输出后再次读取完整长图尺寸并检查首尾。

默认完整保留每个 `900 × 1800` 分页的上下留白。不要为了让页面接缝更“连续”而擅自裁掉页首、页尾或纯色呼吸区；只有用户明确要求无缝裁切时才制作裁切版，并同时保留完整分页版。

### 9. 处理连续反馈与紧急发布

- 用户修改一个名称或术语时，同步检查标题、正文、说明、脚注、二维码替代文字、两个版式和 Banner，不做局部字符串替换后就结束。
- 用户提供最终句子、奖项说明、姓名、组织前缀或金额时，逐字采用；相关单位、汇总和上下文语义一并联动。
- 只重渲染受影响分页，但必须重新拼接完整长图并更新 contact sheet；Banner 改动则重渲染 Banner 和所有引用它的长图。
- 用户撤回某项视觉反馈时，恢复到最近一次确认的基线，不保留折中裁切或隐性补偿。
- 用户表示即将发布或要求“直接输出”时，进入快速交付：完成必要渲染、尺寸确认和旧术语检索后，直接给最终图片路径，省略扩展性检查和长篇说明。

## 不可妥协的验收规则

- 所有正文在手机缩放后仍清晰；不得靠浅灰小字维持层级。
- 文字不得叠在声波、器物、植物或高对比纹理上。
- 同级正文必须使用一致字号和字形比例。
- 中文装饰引号使用成对的 `“` 与 `”`，并锁定中文宋体/思源宋体字形；若作为段落装饰，分别放在整段文字上方和下方，不塞入句头句尾，也不擅自改变已确认的正文换行。
- 左右留出稳定安全边距，纵向宁可更长，不要横向拥挤。
- 封面保留大面积呼吸空间；情景带入语句作为下一段落，不挤进主海报。
- Logo 必须来自真实资产并做光学对齐；乘号与 Logo 的可见边界居中。
- 时间轴节点必须在轴线上。
- 奖项名称、数量和金额在手机端应优先可读。
- 不自动添加页码、白色 Logo 承托层、证书文案或二维码框；仅在用户明确要求或扫描可靠性需要时加入。
- 每次修改同时更新 HTML、分页图、完整长图和预览，不留下版本漂移。
- 完整长图默认高度必须等于全部完整分页高度与 Banner 高度之和，不默认裁剪页间留白。

## 资源导航

- [references/brand-and-layout.md](references/brand-and-layout.md)：尺寸、字体、首屏、正文和版式经验。
- [references/image-generation.md](references/image-generation.md)：背景提示词结构与负空间策略。
- [references/asset-treatment.md](references/asset-treatment.md)：Logo、二维码、合作伙伴和署名处理。
- [references/qa-and-export.md](references/qa-and-export.md)：浏览器截图、手机验收、拼接和交付清单。
- [references/revision-playbook.md](references/revision-playbook.md)：连续反馈、术语联动、分页回退、增量渲染和紧急发布规则。
- [assets/page-template.html](assets/page-template.html)：900×1800 可编辑分页模板。
- [assets/credits-banner-template.html](assets/credits-banner-template.html)：可编辑结尾 Banner 模板。
- [assets/examples/IF.Link_推送banner_署名版_900px.png](assets/examples/IF.Link_推送banner_署名版_900px.png)：最新参考实现生成的署名 Banner 示例。
- `assets/banner/`：Banner 专用 Logo 与微信公众号/小红书二维码。
- `assets/fonts/`：Banner 混排使用的 Google Sans Flex 与思源黑体字体。
- `scripts/normalize_logo.py`：栅格 Logo 黑色透明化与裁边。
- `scripts/compose_long_image.py`：分页拼接和 contact sheet 生成。
