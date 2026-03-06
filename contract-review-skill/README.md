# contract-review-skill

轻量级合同审阅工具（面向电子商务平台法务，代理/服务商/推广类合同优先）
- 自动识别合同中常见风险点（计费/归因/反作弊/结算/数据与IP/终止等）
- 依据可配置规则生成详细 redline 建议（三档强度模板：mild/balanced/strong）
- 输出：控制台报告 / JSON 报告 / 红线文本（unified diff 或 inline 标记）

安装
1. 克隆或复制本仓库
2. 创建虚拟环境并安装依赖：
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt

用法
基本命令：
  python review.py --contract examples/sample_contract.txt --rules rules/default_rules.yaml --templates templates/redline_templates.yaml --out output/report.json --intensity balanced

主要参数
  --contract   合同文本（UTF-8 txt）
  --rules      规则 YAML（匹配项、优先级等）
  --templates  替换模板 YAML（按强度提供替换建议）
  --out        输出 JSON 报告路径
  --redline    redline 输出文件（可选，生成 unified diff 文本）
  --format     redline 格式： unified / inline (default unified)
  --intensity  替换文本强度： mild / balanced / strong (default balanced)

规则与模板
- rules/default_rules.yaml：定义要检查的规则（用正则匹配关键词/段落）
- templates/redline_templates.yaml：按规则ID和强度给出建议修改文本
可按需扩展/修改规则与模板

输出示例
- output/report.json: 包含检测到的问题、每项匹配的原文片段、建议替换文本、diff
- output/redline.diff: unified diff（可在 git 等工具中查看）
- output/redline_inline.txt: inline 标注的合同文本（<<DELETE>> / <<ADD>>）

设计原则
- 可配置：规则和替换模板均为 YAML，便于法务团队维护
- 面向实务：聚焦计费归因、反作弊、结算/追溯、证据/对账、数据与IP、终止/善后等业务痛点
- 非律师工具：本工具提供合同改动建议和定位，最终条文由法务/业务共同确认

许可
MIT
