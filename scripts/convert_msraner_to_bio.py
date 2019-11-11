'''MSRANER 命名实体识别转换为bio标签的数据;
数据来源：<https://github.com/chineseGLUE/chineseGLUE>
源数据：
中共中央/nt 致/o 中国致公党十一大/nt 的贺词/o 
转换后数据：
中	B-ORG
共	I-ORG
中	I-ORG
央	I-ORG
致	O
中	B-ORG
国	I-ORG
致	I-ORG
公	I-ORG
党	I-ORG
十	I-ORG
一	I-ORG
大	I-ORG
的	O
贺	O
词	O
'''
import re
import codecs
import traceback
# 日志初始化
import logging

logging.basicConfig(
    format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
logging.info('logging test')


# tag转换配置,nr、ns、nt
ner_tag_config = {
    'nr': 'PER',
    'ns': 'LOC',
    'nt': 'ORG'
}


def data_parse_write_io(fi, fo):
    """根据文件对象，执行相应bio转换处理"""
    line_index = 0
    for line in fi:
        line_index += 1
        if line_index % 100 == 0:
            logging.info('processed lines:{}'.format(line_index))
        try:
            ner_list = []
            line = re.sub('\n', '', line)
            if len(line) == 0:
                continue
            # 句子预处理与切分
            tokens = line.split(' ')
            for token in tokens:
                if len(token) == 0:
                    continue
                split_index = token.rfind('/')
                if split_index == -1:
                    continue
                word_text = token[:split_index]
                word_tag = token[split_index+1:].lower()
                ner_tag = ner_tag_config.get(word_tag, 'o')
                if ner_tag == 'o':
                    for char_index in range(len(word_text)):
                        ner_list.append('{}\t{}\n'.format(word_text[char_index], 'O'))
                else:
                    for char_index in range(len(word_text)):
                        if char_index == 0:
                            ner_list.append('{}\t{}{}\n'.format(word_text[char_index], 'B-', ner_tag))
                        else:
                            ner_list.append('{}\t{}{}\n'.format(word_text[char_index], 'I-', ner_tag))
            ner_list.append('\n')
            ner_text = ''.join(ner_list)
            fo.write(ner_text)
        except Exception:
            traceback.print_exc()
            continue


if __name__ == "__main__":
    input_files = {
        'test': 'data/testright1.txt',
        'train': 'data/train1.txt'
    } 
    output_file = 'data/msraner_{}_bio.txt'
    # 提取数据集中的数据
    # title_list = ('news_id', 'category_code', 'category', 'title', 'keywords')
    for data_type, input_file_name in input_files.items():
        logging.info('start to process file : {}'.format(input_file_name))
        output_file_name = output_file.format(data_type)
        # 输入输出文件对象获取
        with codecs.open(input_file_name, 'r', encoding='utf-8') as fi:
            with codecs.open(output_file_name, 'w', encoding='utf-8') as fo:
                data_parse_write_io(fi, fo)
            logging.info('end to process file : {}'.format(input_file_name))
