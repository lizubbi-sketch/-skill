# 案例：图片版权违规审核示例

## 用户输入 (设计方提交)
> "为了迎接春节，我们设计了一张海报，画面中间是一个可爱的粉色海狸（Loopy）穿着唐装，手里拿着 1688 的红包，背景有一些 Nike 的鞋子作为年货展示。"

## AI 审核过程
1. **识别素材类型**：图片/海报设计概念。
2. **匹配规则**：
   - 规则 1.2：禁止使用知名卡通形象（Loopy）。
   - 规则 1.2：禁止使用知名大牌产品（Nike）。
3. **判定**：高风险禁止。

## AI 输出报告

### 审核结论：高风险禁止

### 问题详情列表
1. **[版权侵权]**: 使用了知名卡通形象"Loopy"（赞萌露比）。
   - *引用条款*: 一.(二).2.高危禁止 - 图片中有知名卡通形象（如 loopy...）。
2. **[商标侵权]**: 背景展示了"Nike"品牌鞋子。
   - *引用条款*: 一.(二).2.高危禁止 - 图片中有知名大牌 Logo、产品。

### 🔧 修改建议：生成合规图片 Prompt

由于原图核心元素均侵权，建议放弃原图，使用 AI 重新生成一张原创的春节海报素材。

**推荐生成 Prompt:**
> **Positive Prompt**: "A cute original anthropomorphic animal character (not a bear or known IP), wearing traditional Chinese Tang suit, holding a red envelope with '1688' text, festive Spring Festival atmosphere, lanterns in background, generic sports shoes on the table without any logos, 3d render, pixar style, bright lighting, high detail, 4k."
>
> **Negative Prompt**: "Loopy, Pororo, Disney characters, Nike logo, Adidas logo, any brand logo, trademark, copyright character, real human face, low quality, blurry."

### 给设计师的提示
- 请不要绘制任何现有的卡通明星。
- 背景中的鞋子必须是通用的、无 Logo 的款式，或者进行模糊/遮挡处理。
- 角色形象需完全原创，避免与现有 IP 撞脸。
