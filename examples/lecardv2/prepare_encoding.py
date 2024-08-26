# @Time : 2024/8/25 15:05 
# @Author : LiuHuanghai
# @File : prepare_encoding.py 
# @Project: PyCharm
import json
import os

#{text_id: "xxx", 'text': TEXT_TYPE}

def save_to_json(data, file_path):
    with open(file_path, 'w', encoding='utf-8') as f:
        for item in data:
            json.dump(item, f, ensure_ascii=False)
            f.write('\n')

def load_input(data):
    def dict_to_string(d):
        return ', '.join(f'{key}: {value}' for key, value in d.items())
    try:
        if "json" in data:
            data = data[8:-3]
        data = json.loads(data)
        crime = []
        if type(data) == list:
            for item in data:
                if '犯罪的四要件' in item:
                    crime.append(dict_to_string(item["犯罪的四要件"]))
                else:
                    for key in item:
                        crime.append(dict_to_string(item[key]["犯罪的四要件"]))
        else:
            for key in data:
                crime.append(dict_to_string(data[key]["犯罪的四要件"]))
        return crime
    except Exception:
        print(Exception)
        return []

def read_data(file_path):
    file_path = file_path
    data = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            data.append(json.loads(line))
    query4ele = []
    can4ele = []
    for record in data[-4:]:
        query_4element ={'text_id': record.get("id", ""), 'text': load_input(record.get("query_4element", ""))}
        query4ele.append(query_4element)
        for candidate in record.get("candidate", []):
            candidate_4element = {'text_id': candidate.get("pid", ""), 'text': load_input(candidate.get("can_4element", ""))}
            can4ele.append(candidate_4element)
    return query4ele, can4ele

def read_common_data(file_path):
    file_path = file_path
    data = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            data.append(json.loads(line))
    query4ele = []
    can4ele = []
    for record in data:
        query_4element = record.get("fact", "")
        query4ele.append(query_4element)
        for candidate in record.get("candidate", []):
            candidate_4element = candidate.get("fact", "")
            can4ele.append(candidate_4element)
    return query4ele, can4ele

def read_common_data(file_path):
    file_path = file_path
    data = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            data.append(json.loads(line))
    query4ele = []
    can4ele = []
    for record in data[-4:]:
        query_4element = {'text_id': record.get("id", ""), 'text': record.get("fact", "")}
        query4ele.append(query_4element)
        for candidate in record.get("candidate", []):
            candidate_4element = {'text_id': candidate.get("doc_id", ""), 'text': candidate.get("fact", "")}
            can4ele.append(candidate_4element)
    return query4ele, can4ele

def main():
    query4ele, can4ele = read_data('sample10_result_gpt-4o-2024-08-06.json')
    corpus_dir = 'corpus'
    if not os.path.exists(corpus_dir):
        os.makedirs(corpus_dir)
    save_to_json(can4ele, os.path.join(corpus_dir, 'corpus.json'))
    save_to_json(query4ele, os.path.join(corpus_dir, 'query.json'))


if __name__ == "__main__":
    main()
