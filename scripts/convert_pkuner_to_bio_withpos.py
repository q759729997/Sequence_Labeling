'''PKU 命名实体识别转换为bio标签的数据;
源数据，分割符号为\t：
台湾/ns#S-Ns	是/v#O	中国/ns#S-Ns	领土/n#O	不可分割/i#O	的/u#O	一/m#O	部分/n#O	。/wp#O 
转换后数据，分割符号为\t：
台	B-LOC
湾	I-LOC
是	O
中	B-LOC
国	I-LOC
领	O
土	O
不	O
可	O
分	O
割	O
的	O
一	O
部	O
分	O
。	O
'''
import re
import codecs
import traceback
# 日志初始化
import logging

logging.basicConfig(
    format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
logging.info('logging test')


# tag转换配置,nr、ns、ni
ner_tag_config = {
    'S-Nh': 'PER',  # PER WHO
    'B-Nh': 'PER',
    'I-Nh': 'PER',
    'E-Nh': 'PER',
    'S-Ns': 'LOC',
    'B-Ns': 'LOC',
    'I-Ns': 'LOC',
    'E-Ns': 'LOC',
    'S-Ni': 'ORG',
    'B-Ni': 'ORG',
    'I-Ni': 'ORG',
    'E-Ni': 'ORG'
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
            tokens = line.split('\t')
            for token in tokens:
                if len(token) == 0:
                    continue
                ne_split_index = token.rfind('#')
                pos_split_index = token.rfind('/')
                if ne_split_index == -1 or pos_split_index == -1:
                    continue
                word_text = token[:pos_split_index]
                pos_tag = token[pos_split_index+1:ne_split_index]
                word_tag = token[ne_split_index+1:]
                ner_tag = ner_tag_config.get(word_tag, 'o')
                if ner_tag == 'o':
                    for char_index in range(len(word_text)):
                        if char_index == 0:
                            ner_list.append('{} B-{} {}\n'.format(word_text[char_index], pos_tag, 'O'))
                        else:
                            ner_list.append('{} I-{} {}\n'.format(word_text[char_index], pos_tag, 'O'))
                else:
                    for char_index in range(len(word_text)):
                        if char_index == 0:
                            if word_tag.startswith('S-') or word_tag.startswith('B-'):
                                ner_list.append('{} B-{} B-{}\n'.format(word_text[char_index], pos_tag, ner_tag))
                            else:
                                ner_list.append('{} B-{} I-{}\n'.format(word_text[char_index], pos_tag, ner_tag))
                        else:
                            ner_list.append('{} I-{} I-{}\n'.format(word_text[char_index], pos_tag, ner_tag))
            ner_list.append('\n')
            ner_text = ''.join(ner_list)
            fo.write(ner_text)
        except Exception:
            traceback.print_exc()
            continue


if __name__ == "__main__":
    input_files = {
        'test': 'data/pku-test.ner',
        'train': 'data/pku-train.ner',
        'val': 'data/pku-holdout.ner',
    } 
    output_file = 'data/pkuner_pos_{}_bio.txt'
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
