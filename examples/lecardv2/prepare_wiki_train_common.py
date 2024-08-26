import json
import os
from argparse import ArgumentParser

from transformers import AutoTokenizer
from tqdm import tqdm

def build_pos_neg(candidate,can4ele):
    positives = []
    negatives = []
    for item in candidate:
        positives.append(item['fact'])

    for element in can4ele:
        if element not in positives:
            negatives.append(element)
    return positives,negatives


parser = ArgumentParser()
parser.add_argument('--input', type=str, required=True)
parser.add_argument('--output', type=str, required=True)
parser.add_argument('--tokenizer', type=str, required=False, default='bert-base-uncased')
parser.add_argument('--minimum-negatives', type=int, required=False, default=8)
args = parser.parse_args()

tokenizer = AutoTokenizer.from_pretrained(args.tokenizer)


data = []
can4ele = []
with open(args.input, 'r', encoding='utf-8') as f:
    for line in f:
        record=json.loads(line)
        data.append(record)
        for candidate in record.get("candidate", []):
            candidate_4element = candidate.get("fact", "")
            can4ele.append(candidate_4element)

if not os.path.exists(args.output):
    os.makedirs(args.output)
with open(os.path.join(args.output, 'train_data.json'), 'w') as f:
    for idx, item in enumerate(tqdm(data)):
        group = {}
        query = tokenizer.encode(item['fact'], add_special_tokens=False, max_length=256, truncation=True)
        group['query'] = query
        positives,negatives = build_pos_neg(item['candidate'],can4ele)
        group['positives'] = []
        group['negatives'] = []
        for pos in positives:
            text = pos
            text = tokenizer.encode(text, add_special_tokens=False, max_length=256, truncation=True)
            group['positives'].append(text)
        for neg in negatives:
            text = neg
            text = tokenizer.encode(text, add_special_tokens=False, max_length=256, truncation=True)
            group['negatives'].append(text)
        if len(group['negatives']) >= args.minimum_negatives and len(group['positives']) >= 1:
            f.write(json.dumps(group) + '\n')
