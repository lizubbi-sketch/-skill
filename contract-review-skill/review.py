#!/usr/bin/env python3
"""
contract-review-skill
Lightweight contract reviewer for agent/agency/service-provider agreements.
Usage:
  python review.py --contract examples/sample_contract.txt --rules rules/default_rules.yaml --out report.json
"""
import argparse, json, sys, re
from pathlib import Path
from difflib import SequenceMatcher

try:
    import yaml
except Exception:
    print("Missing dependency 'pyyaml'. Install with: pip install pyyaml")
    sys.exit(1)

def load_text(path):
    return Path(path).read_text(encoding='utf-8')

def load_rules(path):
    return yaml.safe_load(Path(path).read_text(encoding='utf-8'))

def normalize_text(s):
    # 简单正则清洗，保留中文与英数标点等
    s = s.replace('\r\n', '\n')
    s = re.sub(r'\s+', ' ', s)
    return s.strip()

def presence_check(text, keywords):
    hits = []
    for k in keywords:
        if re.search(re.escape(k), text, flags=re.I):
            hits.append({'keyword': k, 'found': True})
        else:
            hits.append({'keyword': k, 'found': False})
    return hits

def forbidden_check(text, keywords):
    hits = []
    for k in keywords:
        m = re.search(re.escape(k), text, flags=re.I)
        hits.append({'keyword': k, 'found': bool(m), 'snippet': m.group(0) if m else None})
    return hits

def split_sentences(text):
    # 基本中文/英文句子切分（轻量）
    text = text.replace('。', '。\n').replace('；', '；\n').replace(';', ';\n').replace('\n', '\n')
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    return lines

def duplication_check(text, threshold=0.85):
    sentences = split_sentences(text)
    dup_pairs = []
    n = len(sentences)
    for i in range(n):
        for j in range(i+1, n):
            a,b = sentences[i], sentences[j]
            if len(a) < 10 or len(b) < 10:
                continue
            ratio = SequenceMatcher(None, a, b).ratio()
            if ratio >= threshold:
                dup_pairs.append({'a': a, 'b': b, 'ratio': round(ratio,3)})
    return dup_pairs

def taxonomy_checks(text, rules):
    report = {}
    report['required'] = presence_check(text, rules.get('required_keywords', []))
    report['forbidden'] = forbidden_check(text, rules.get('forbidden_keywords', []))
    report['attribution'] = presence_check(text, rules.get('attribution_terms', []))
    report['cps_cpa'] = presence_check(text, rules.get('cps_cpa_terms', []))
    return report

def definitions_conflict_check(text, defined_terms):
    # 简单检测同义或重复定义出现多次（在合同定义章节重复出现词）
    defs = {}
    # heuristic: lines that contain '定义' or '指' are candidate definition lines
    lines = split_sentences(text)
    for ln in lines:
        for term in defined_terms:
            if term in ln and ('指' in ln or '定义' in ln or ':' in ln):
                defs.setdefault(term, []).append(ln)
    conflicts = {k:v for k,v in defs.items() if len(v) > 1}
    return conflicts

def tax_duplication_check(text, tax_terms):
    hits = []
    for t in tax_terms:
        cnt = len(re.findall(re.escape(t), text, flags=re.I))
        if cnt > 1:
            hits.append({'term': t, 'count': cnt})
    return hits

def termination_settlement_check(text, phrases):
    hits = []
    for p in phrases:
        if re.search(re.escape(p), text, flags=re.I):
            hits.append({'phrase': p, 'found': True})
        else:
            hits.append({'phrase': p, 'found': False})
    return hits

def run_checks(contract_text, rules):
    t = normalize_text(contract_text)
    out = {}
    out['meta'] = {'length_chars': len(t)}
    out['duplication'] = duplication_check(t, threshold=rules.get('duplication_threshold', 0.88))
    out['taxonomy'] = taxonomy_checks(t, rules)
    out['definitions_conflict'] = definitions_conflict_check(t, rules.get('defined_terms', []))
    out['tax_duplication'] = tax_duplication_check(t, rules.get('tax_terms', []))
    out['termination_settlement'] = termination
