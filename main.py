import os
import sys
import json
from multiprocessing import Pool
import test_xunfei
import tqdm

bar = None

def get_file_list(path_prefix):
    file_list = os.listdir(path_prefix)
    for file_name in file_list:
        file_path = os.path.join(path_prefix, file_name)
        if os.path.isdir(file_path):
            for item in get_file_list(file_path):
                yield item
        else:
            yield file_path


def run_request(args):
    wav_path, output_json_path = args
    try:
        res = test_xunfei.request_lfasr_result(wav_path)
    except:
        res = {"err": "internal unknown error, in python."}

    output_path, filename = os.path.split(output_json_path)
    os.makedirs(output_path, exist_ok=True)
    json.dump(res, open(output_json_path, 'w'))
    bar.update()
    return int(res.get('err_no', '-1'))


def main():
    wav_list = list(get_file_list(sys.argv[1]))
    json_list = [os.path.join('log', wav_path + '.log') for wav_path in wav_list]

    global bar
    bar = tqdm.tqdm(total=len(wav_list))
    with Pool(processes=3) as pool:
        result_summary = pool.map(run_request, zip(wav_list, json_list))

    bar.close()
    print('result_summary:', result_summary)


if __name__ == '__main__':
    main()
