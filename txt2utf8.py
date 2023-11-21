import chardet
import tqdm
import argparse
import os
import time

def get_args():
    parser = argparse.ArgumentParser(description="这是一个检测和转换txt文件编码的工具")
    parser.add_argument("-i", "--input", required=True, help="指定输入文件的路径")
    parser.add_argument("-o", "--output", required=True, help="指定输出文件的路径")
    return parser.parse_args()

def convert_encoding(input_file, output_file):
    detector = chardet.UniversalDetector()
    with open(input_file, "rb") as f:
        data = f.read(10240)
        detector.feed(data)
        detector.close()
    encoding = detector.result["encoding"]
    if encoding == "GB2312":
        encoding = "GB18030"
    confidence = detector.result["confidence"]
    print(f"输入文件的编码为：{encoding}，置信度为：{confidence}")

    start_time = time.time()
    with tqdm.tqdm(total=os.path.getsize(input_file)) as pbar:
        with open(input_file, "r", encoding=encoding, errors="replace") as fin, \
             open(output_file, "w", encoding="utf-8", errors="replace") as fout:              
            for line in fin:
                try:
                    fout.write(line)
                    pbar.update(len(line.encode(encoding)))
                except UnicodeEncodeError as e:
                    print(f"编码错误：{e}")
                    print(line)
                    continue     
    print(f"转换完成!\n用时：{time.time() - start_time}秒")

args = get_args()
input_file = args.input
output_file = args.output
convert_encoding(input_file, output_file)
