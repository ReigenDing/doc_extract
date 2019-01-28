# encoding:utf-8

from hanziconv import HanziConv
import re
import argparse
import codecs
import chardet
import pathlib
from binaryornot.check import is_binary
import textract


class EncodingException(Exception):
    def __init__(self, err='Failed to detect encoding of input file'):
        Exception.__init__(self, err)


def fullwidth_to_halfwidth(s):
    """全角转半角"""
    n = []
    for char in s:
        num = ord(char)
        if num == 0x3000:
            num = 32
        elif 0xFF01 <= num <= 0xFF5E:
            num -= 0xfee0
        num = chr(num)
        n.append(num)
    return ''.join(n)

def filter_symbol(s):
    s = re.sub(r'[\s +.\-!\\/_,$%^*\"\'()]+|[+—?【】“”！，。？、~@#￥%…&*]+', '', s)
    return s

def decode_data(s):
    source_encoding = chardet.detect(s)['encoding']
    if not source_encoding:
        raise EncodingException()
    if source_encoding == 'GB2312' or source_encoding == 'GBK':
        source_encoding = 'GB18030'
    s = s.decode(source_encoding, 'ignore')
    return s


def filter_symbol(s):
    s = re.sub(r'[\s +.\-!\\/_,$%^*\"\'()]+|[+—?【】“”！，。？、~@#￥%…&*]+', '', s)
    return s

def preprocess_pipeline(s):
    s = decode_data(s)
    s = fullwidth_to_halfwidth(s)
    s = HanziConv.toSimplified(s)
    # s = filter_symbol(s)
    return s

def get_text(infile, output):
    support_ext = ('.doc', '.docx', '.ppt', '.pptx', '.xls', '.xlsx', '.pdf', '.txt')
    infile = pathlib.Path(infile)
    assert infile.is_file()
    assert infile.stat().st_size <= 3e8
    if infile.suffix not in support_ext and is_binary(str(infile)):
        raise Exception('Unsupported binary file')
    data = textract.process(str(infile))
    print(data)
    # data = preprocess_pipeline(data)
    with codecs.open(output, 'w', 'utf-8') as outfile:
        outfile.write(data)
    return data

def main():
    parser = argparse.ArgumentParser(description="extract plain text from file")
    parser.add_argument('-input', required=True, help='file to be extracted(support format: word、ppt、excel、pdf、txt)')
    parser.add_argument('-output', required=True, help='file to save the result')
    args = parser.parse_args()
    with codecs.open(args.output, 'w', 'utf-8') as outfile:
        data = get_text(args.input)
        outfile.write(data)




if __name__ == '__main__':
    # main()
    print(get_text(r'D:\work\搜索demo-文档\原始数据\数据底座数据主题联接元数据注册指南(试行)-通知【2017】001.docx',
                   'D:\work\文档解析\data\input\数据底座数据主题联接元数据注册指南(试行)-通知【2017】001.txt'))
