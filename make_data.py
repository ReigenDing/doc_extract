import json
import os
import re


def get_data(file_path):
    text = []
    _id = os.path.splitext(os.path.basename(file_path))[0]
    print(_id)
    with open(file_path, 'r', encoding='utf8') as fp:
        for line in fp:
            line = re.sub(r'[\uf070\uf0d8\uf0fc]', '', line)
            line = line.strip()
            if line:
                text.append(line)
    data = {'id': _id, 'text': '|'.join(text)}
    print(data)
    return data


def save_data(file_path, data):
    with open(file_path, 'a', encoding='utf8') as fp:
        fp.write(json.dumps(data, ensure_ascii=False) + '\n')


def main():
    file_list = os.listdir('./data/input/')
    for file in file_list:
        file_path = os.path.join('./data/input/', file)
        data = get_data(file_path)
        save_data(r'D:\work\文档解析\data\output\test_data.txt', data)


if __name__ == '__main__':
    main()
    # data = get_data('D:\work\文档解析\data\input\知识图谱构建方法研究.txt')
    # save_data(r'D:\work\文档解析\data\output\test_data.txt', data)









