#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
contract-review-skill review tool
Author: ecom-legal team template
"""

import argparse
import json
import re
from pathlib import Path
from difflib import unified_diff

try:
    import yaml
except Exception:
    print("Missing dependency 'pyyaml'. Install with: pip install pyyaml")
    raise

def load_text(path):
    return Path(path).read_text(encoding='utf-8')

def load_yaml(path):
    return yaml.safe_load(Path(path).read_text(encoding='utf-8'))

def split_paragraphs(text):
    # 按空行分段，保留顺序
    paras = [p.strip() for p in re.split(r'\n\s*\n', text) if p.strip()]
    return paras

def find_matches(paragraphs, pattern):
    hits = []
    prog = re.compile(pattern, flags=re.I | re.S)
    for idx, p in enumerate(paragraphs):
        if prog.search(p):
            hits.append({'index': idx, 'paragraph': p})
    return hits

def apply_template(template_text, context):
    # 简单替换占位符
    out = template_text.format(**context)
    return out.strip()

def make_unified_diff(original, replacement, name='contract'):
    # returns unified diff string
    orig_lines = original.splitlines(keepends=True)
    rep_lines = replacement.splitlines(keepends=True)
    diff_lines = list(unified_diff(orig_lines, rep_lines, fromfile=f'{name}.orig', tofile=f'{name}.mod', lineterm=''))
    return ''.join(diff_lines)

def make_inline_redline(original, replacement):
    # inline style: mark whole paragraph delete and insert (simple)
    out = []
    out.append("<<DELETE>>")
    out.append(original)
    out.append("<<END DELETE>>")
    out.append("<<ADD>>")
    out.append(replacement)
    out.append("<<END ADD>>")
    return '\n'.join(out)

def review_contract(contract_path, rules_path, templates_path, intensity='balanced', out_json=None, redline_path=None, redline_format='unified'):
    text = load_text(contract_path)
    paragraphs = split_paragraphs(text)
    rules_doc = load_yaml(rules_path)
    templates_doc = load_yaml(templates_path)
    defaults = templates_doc.get('defaults', {})
    report = {
        'contract': str(contract_path),
        'summary': {
            'paragraphs': len(paragraphs),
            'issues_found': 0
        },
        'matches': []
    }
    used_paragraphs = set()
    for rule in rules_doc.get('rules', []):
        rid = rule.get('id')
        desc = rule.get('description')
        pattern = rule.get('pattern')
        severity = rule.get('severity', 'info')
        matches = find_matches(paragraphs, pattern)
        for m in matches:
            idx = m['index']
            orig_par = m['paragraph']
            # prepare suggestion
            template_map = templates_doc.get('templates', {}).get(rid, {})
            suggestion_template = template_map.get(intensity) or template_map.get('balanced') or ("建议文本（缺省）: 请人工审阅")
            context = {
                'platform_name': defaults.get('platform_name', '平台'),
                'tax_rate': defaults.get('tax_rate', '')
            }
            suggestion = apply_template(suggestion_template, context)
            # create diffs
            if redline_format == 'unified':
                diff = make_unified_diff(orig_par + '\n', suggestion + '\n', name=f'para_{idx}_{rid}')
                redline_text = diff
            else:
                redline_text = make_inline_redline(orig_par, suggestion)
            report['matches'].append({
                'rule_id': rid,
                'description': desc,
                'severity': severity,
                'paragraph_index': idx,
                'original_paragraph': orig_par,
                'suggested_replacement': suggestion,
                'redline': redline_text
            })
            used_paragraphs.add(idx)
    report['summary']['issues_found'] = len(report['matches'])

    # Output JSON
    if out_json:
        Path(out_json).write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')

    # Output redline aggregated file (if provided)
    if redline_path:
        lines = []
        for item in report['matches']:
            header = f"=== Rule: {item['rule_id']} ({item['severity']}) ===\nDescription: {item['description']}\nParagraph index: {item['paragraph_index']}\n"
            lines.append(header)
            lines.append(item['redline'])
            lines.append('\n\n')
        Path(redline_path).write_text('\n'.join(lines), encoding='utf-8')

    return report

def main():
    parser = argparse.ArgumentParser(description='contract-review-skill: review and suggest redlines for agent contracts')
    parser.add_argument('--contract', '-c', required=True, help='contract txt file path (utf-8)')
    parser.add_argument('--rules', '-r', default='rules/default_rules.yaml', help='rules yaml path')
    parser.add_argument('--templates', '-t', default='templates/redline_templates.yaml', help='templates yaml path')
    parser.add_argument('--intensity', choices=['mild','balanced','strong'], default='balanced', help='suggestion strength')
    parser.add_argument('--out', help='output json report path (optional)')
    parser.add_argument('--redline', help='output redline file path (optional)')
    parser.add_argument('--format', choices=['unified','inline'], default='unified', help='redline format')
    args = parser.parse_args()

    report = review_contract(args.contract, args.rules, args.templates, args.intensity, args.out, args.redline, args.format)
    print("Review complete. Issues found:", report['summary']['issues_found'])
    if args.out:
        print("JSON report:", args.out)
    if args.redline:
        print("Redline file:", args.redline)

if __name__ == '__main__':
    main()
