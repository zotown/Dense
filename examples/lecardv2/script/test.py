import json

# 读取 JSON 文件
papers = []
with open('../lecard-train-bert-base-chinese-common/train_data_common.json', 'r', encoding='utf-8') as f:
    for line in f.readlines():
        dic = json.loads(line)
        papers.append(dic)

non_string_elements = []
for item in papers:
    for key, values in item.items():
        if key=="query":
            for value in values:
                if not isinstance(value, int):
                    non_string_elements.append(value)
        else:
            for value in values:
                for v in value:
                    if not isinstance(v, int):
                        non_string_elements.append(v)

print(non_string_elements)