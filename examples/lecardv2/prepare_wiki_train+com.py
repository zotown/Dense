import json
import os
from argparse import ArgumentParser

from transformers import AutoTokenizer,LongformerTokenizerFast
from tqdm import tqdm
import random

def deal_input(record, args, fact=None,item=None):
    if args.type == "common":
        assert fact!=None
        return fact
    elif args.type == "+com":
        return load_input(record) + fact
    elif args.type == "4ele":
        return load_input(record)
    elif args.type == "+crime":
        return load_input(record, add_crime=True)
    elif args.type == "+typecrime":
        if "charge" not in item:
            return load_input(record, add_crime=True)
        else:#对于candidate 加入标准罪名
            data=load_input(record)
            crime="罪名:"+" ".join(item['charge'])
            return data+crime




def load_input(data,add_crime=False):
    def dict_to_string(d,i):
        return f"\t罪名{str(i)}: "+', '.join(f'{key}: {value}' for key, value in d.items())
    try:
        if "json" in data:
            data = data[8:-3]
        data = json.loads(data)
        crime = ""
        crime2="\t罪名:"
        i=1
        if type(data) == list:
            for item in data:
                if '犯罪的四要件' in item:
                    crime+=dict_to_string(item["犯罪的四要件"],i)
                    if add_crime == True:
                        crime2 += f"{item['罪名']}\t"
                    i+=1
                else:
                    for key in item:
                        crime+=dict_to_string((item[key]["犯罪的四要件"]),i)
                        if add_crime == True:
                            crime2 += f"{item[key]['罪名']}\t"
                        i += 1
        else:
            for key in data:
                crime+=dict_to_string(data[key]["犯罪的四要件"],i)
                if add_crime == True:
                    crime2 += f"{data[key]['罪名']}\t"
                i += 1
        if add_crime == True:
            return crime+crime2
        else:
            return crime
    except Exception:
        print(Exception)
        return []

def build_pos_neg(candidate,can4ele,args):
    positives = []
    negatives = []
    for item in candidate:
        positives.append(deal_input(item["can_4element"],args,item["fact"],item))
    for element in can4ele:
        if element not in positives:
            negatives.append(element)
    negatives = random.sample(negatives, 100 - len(positives))  # todo:改为相似罪名
    return positives,negatives

#'/root/autodl-tmp/PollyZhao/bert-base-chinese/'
parser = ArgumentParser()
parser.add_argument('--input', type=str, default='sample15_result_gpt-4o-2024-08-06-train15.json')
parser.add_argument('--output', type=str, default='lecard-train-Lawformer')
parser.add_argument('--tokenizer', type=str, required=False, default='/root/autodl-tmp/Lawformer')
parser.add_argument('--minimum-negatives', type=int, required=False, default=8)
parser.add_argument('--type', type=str, required=False, default='+crime')
args = parser.parse_args()

#tokenizer = AutoTokenizer.from_pretrained(args.tokenizer)
tokenizer = LongformerTokenizerFast.from_pretrained(args.tokenizer)
tokenizer._tokenizer.model.save("tmp_law")
args.output=args.output+args.type

data = []
can4ele = []
with open(args.input, 'r', encoding='utf-8') as f:
    for line in f:
        record=json.loads(line)
        data.append(record)
        for candidate in record.get("candidate", []):
            candidate_4element = deal_input(candidate["can_4element"],args,candidate["fact"],candidate)
            can4ele.append(candidate_4element)

if not os.path.exists(args.output):
    os.makedirs(args.output)
with open(os.path.join(args.output, 'train_data.json'), 'w') as f:
    for idx, item in enumerate(tqdm(data)):
        group = {}
        query = deal_input(item["query_4element"],args,item["fact"],item)
        group['query'] = tokenizer.encode(query, add_special_tokens=False,
                                 max_length=512, truncation=True)
        positives,negatives = build_pos_neg(item['candidate'],can4ele,args)
        group['positives'] = []
        group['negatives'] = []
        for pos in positives:
            text = pos
            text = tokenizer.encode(text, add_special_tokens=False, max_length=512, truncation=True)
            group['positives'].append(text)
        for neg in negatives:
            text = neg
            text = tokenizer.encode(text, add_special_tokens=False, max_length=512, truncation=True)
            group['negatives'].append(text)
        if len(group['negatives']) >= args.minimum_negatives and len(group['positives']) >= 1:
            f.write(json.dumps(group) + '\n')
