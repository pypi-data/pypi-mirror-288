import os
import json
import random

def print_success():
    print("安装 easytool 成功")

# I/O
def dump_json(obj, filepath):
    with open(filepath, "wt", encoding="utf-8") as fout:
        json.dump(obj, fout, ensure_ascii=False, indent=4)

def load_json(filepath, **kwargs):
    data = list()
    with open(filepath, "rt", encoding="utf-8") as fin:
        data = json.load(fin, **kwargs)
    return data

def load_jsonlines(filepath, **kwargs):
    data = list()
    with open(filepath, "rt", encoding="utf-8") as fin:
        for idx, line in enumerate(fin):
            line_data = json.loads(line.strip())
            data.append(line_data)
    return data

def load_json_or_jsonl(filepath):
    try:
        data_list = load_json(filepath)
    except :
        data_list = load_jsonlines(filepath)
    return data_list

def dump_jsonlines(obj, filepath, **kwargs):
    with open(filepath, "wt", encoding="utf-8") as fout:
        for d in obj:
            line_d = json.dumps(
                d, ensure_ascii=False, **kwargs
            )
            fout.write("{}\n".format(line_d))

def load_lines(filepath, split_by_line=False, combine_to_one=False):
    with open(filepath, 'r', encoding='utf-8') as fr:
        all_lines = fr.readlines()

    if split_by_line:
        return [line.strip() for line in all_lines]
    if combine_to_one:
        return ''.join(all_lines)
    return all_lines

def dump_lines(obj_list, filepath, with_size=True):
    if with_size:
        filepath = add_size_4_filepath(filepath, len(obj_list))

    with open(filepath, "wt", encoding="utf-8") as fout:
        for obj in obj_list:
            fout.write(str(obj) + '\n')

def add_size_4_filepath(filepath, size):
    _filepath, suffix =  filepath.split('.')[:-1], filepath.split('.')[-1]
    filepath = '.'.join(_filepath) + f"_{size}" + f".{suffix}"
    return filepath

def dump_json_or_jsonl_with_size(obj, filepath, out_type='json', with_size=True):
    if with_size:
        filepath = add_size_4_filepath(filepath, len(obj))

    if out_type == 'json':
        dump_json(obj, filepath)
    else:
        dump_jsonlines(obj, filepath)

def create_folder(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

def load_jsonfile_list(filepath_list):
    all_json_data_list = []
    for filepath in filepath_list:
        all_json_data_list.extend(load_json_or_jsonl(filepath=filepath))
    return all_json_data_list

def load_linefile_list(filepath_list, **kwargs):
    all_data_list = []
    for filepath in filepath_list:
        one_file_data = load_lines(filepath=filepath, **kwargs)
        all_data_list.extend(one_file_data)
    return all_data_list

def dump_jsonlines_append(obj, filepath, **kwargs):
    with open(filepath, "a", encoding="utf-8") as fout:
        for d in obj:
            line_d = json.dumps(
                d, ensure_ascii=False, **kwargs
            )
            fout.write("{}\n".format(line_d))

def devide_json_file(input_file, output_file_1, output_file_2, split_ratio=0.5, shuffle=True, **kwargs):
    all_data_list = load_json_or_jsonl(input_file)
    if shuffle:
        random.shuffle(all_data_list)
    
    split_point = int(len(all_data_list) * split_ratio)
    
    dump_json_or_jsonl_with_size(all_data_list[:split_point], output_file_1, **kwargs)
    dump_json_or_jsonl_with_size(all_data_list[split_point:], output_file_2, **kwargs)

# trans
def modify_error_jsonl(input_filepath, output_filepath, split_string='"}', **kwargs):
    ## 修正因为“格式化文档”导致错乱的jsonl文件
    all_lines = load_lines(input_filepath)
    all_lines = [line.strip() for line in all_lines]
    all_content = ''.join(all_lines)

    json_string_list = list(filter(lambda x: len(x)>0, all_content.split(split_string)))
    json_obj_list = [eval(item+split_string) for item in json_string_list if len(item)>0]

    dump_json_or_jsonl_with_size(json_obj_list, output_filepath, **kwargs)

def jsonl_2_json(input_filepath, output_filepath, **kwargs):
    json_obj_data = load_jsonlines(input_filepath)
    dump_json_or_jsonl_with_size(json_obj_data, output_filepath, out_type='json', **kwargs)

def json_2_jsonl(input_filepath, output_filepath, **kwargs):
    json_obj_data = load_json(input_filepath)
    dump_json_or_jsonl_with_size(json_obj_data, output_filepath, out_type='jsonl', **kwargs)

def combine_json_to_one_file(filepath_list, output_path):
    all_data_list = load_jsonfile_list(filepath_list)
    dump_json_or_jsonl_with_size(all_data_list, output_path)

def combine_lines_to_one_file(filepath_list, output_path):
    all_data_list = load_linefile_list(filepath_list, split_by_line=True)
    dump_lines(all_data_list, output_path)


if __name__ == "__main__":
    pass