"""
论文查重程序
功能：比较两个文本文件的相似度，使用Jaccard相似度算法
使用方法：python main.py [原文文件] [抄袭版论文的文件] [答案文件]
"""

import sys
import jieba
from collections import Counter


def read_file(filename):
    """
    读取文件内容

    参数:
        filename (str): 要读取的文件路径

    返回:
        str: 文件内容字符串，如果文件不存在返回None
    """
    try:
        # 以UTF-8编码打开文件并读取内容
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read().strip()  # 读取全部内容并去除首尾空白
        return content
    except FileNotFoundError:
        # 文件不存在时打印错误信息
        print(f"错误：找不到文件 {filename}")
        return None


def preprocess_text(text):
    """
    文本预处理：分词并去除标点符号和停用词

    参数:
        text (str): 待处理的文本

    返回:
        list: 处理后的词汇列表
    """
    # 使用jieba进行中文分词
    words = jieba.lcut(text)

    # 定义要过滤的标点符号
    punctuation = '，。！？；：""''（）【】《》、'

    # 定义中文停用词列表
    stop_words = ['的', '了', '在', '是', '我', '有', '和', '就', '不', '人', '都', '一', '一个', '上', '也', '很',
                  '到', '说', '要', '去', '你', '会', '着', '没有', '看', '好', '自己', '这']

    # 过滤标点符号和停用词，只保留有意义的词汇
    filtered_words = []
    for word in words:
        # 如果单词不是标点符号且不是停用词且长度大于0，则保留
        if word not in punctuation and word not in stop_words and len(word) > 0:
            filtered_words.append(word)

    return filtered_words


def calculate_similarity(original_words, plagiarized_words):
    """
    使用Jaccard相似度算法计算两个文本的相似度

    参数:
        original_words (list): 原文分词后的词汇列表
        plagiarized_words (list): 抄袭版分词后的词汇列表

    返回:
        float: 相似度值，范围0-1
    """
    # 使用Counter统计两个文本中各词汇的出现频率
    original_counter = Counter(original_words)
    plagiarized_counter = Counter(plagiarized_words)

    # 计算交集：两个文本中共同词汇的词频最小值之和
    intersection = sum((original_counter & plagiarized_counter).values())

    # 计算并集：两个文本中所有词汇的词频最大值之和
    union = sum((original_counter | plagiarized_counter).values())

    # 计算Jaccard相似度：交集/并集
    if union == 0:
        similarity = 0  # 避免除零错误
    else:
        similarity = intersection / union

    return similarity


def write_result(filename, similarity):
    """
    将相似度结果写入文件

    参数:
        filename (str): 输出文件路径
        similarity (float): 相似度值
    """
    # 以UTF-8编码打开文件并写入结果
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(f"{similarity:.2f}\n")  # 保留两位小数


def main():
    """
    主函数：处理命令行参数并执行查重流程
    """
    # 检查命令行参数数量是否正确（程序名 + 3个参数 = 4个）
    if len(sys.argv) != 4:
        print("输入错误")
        return

    # 获取命令行参数
    original_file = sys.argv[1]  # 原文文件路径
    plagiarized_file = sys.argv[2]  # 抄袭版文件路径
    output_file = sys.argv[3]  # 输出结果文件路径

    # 读取原文文件
    original_text = read_file(original_file)
    if original_text is None:
        return  # 文件读取失败则退出

    # 读取抄袭版文件
    plagiarized_text = read_file(plagiarized_file)
    if plagiarized_text is None:
        return  # 文件读取失败则退出

    # 对两个文本进行预处理（分词、去停用词等）
    original_words = preprocess_text(original_text)
    plagiarized_words = preprocess_text(plagiarized_text)

    # 计算相似度
    similarity = calculate_similarity(original_words, plagiarized_words)

    # 将结果写入输出文件
    write_result(output_file, similarity)

    # 打印结果到控制台
    print(f"论文相似度: {similarity:.2f}")


def test_identical():
    """
    测试完全相同的文本
    预期相似度：1.0
    """
    ori_text = read_file("./test_/identical_orig.txt")
    plag_text = read_file("./test_/identical_test.txt")
    ori_words = preprocess_text(ori_text)
    plag_words = preprocess_text(plag_text)
    similarity = calculate_similarity(ori_words, plag_words)
    similarity = round(similarity, 2)
    assert similarity == 1.0


def test_completely_different():
    """
    测试完全不同的文本
    预期相似度：0.0
    """
    ori_text = read_file("./test_/completely_orig.txt")
    plag_text = read_file("./test_/completely_test.txt")
    ori_words = preprocess_text(ori_text)
    plag_words = preprocess_text(plag_text)
    similarity = calculate_similarity(ori_words, plag_words)
    similarity = round(similarity, 2)
    assert similarity == 0


def test_partial_overlap():
    """
    测试部分重叠的文本
    预期相似度：>= 0.5
    """
    ori_text = read_file("./test_/partial_orig.txt")
    plag_text = read_file("./test_/partial_test.txt")
    ori_words = preprocess_text(ori_text)
    plag_words = preprocess_text(plag_text)
    similarity = calculate_similarity(ori_words, plag_words)
    similarity = round(similarity, 2)
    assert similarity >= 0.5


def test_empty_orig():
    """
    测试原文为空的情况
    预期相似度：0.0
    """
    ori_text = read_file("./test_/ept_orig.txt")
    plag_text = read_file("./test_/ept_test.txt")
    ori_words = preprocess_text(ori_text)
    plag_words = preprocess_text(plag_text)
    similarity = calculate_similarity(ori_words, plag_words)
    similarity = round(similarity, 2)
    assert similarity == 0


def test_empty_plag():
    """
    测试抄袭版为空的情况
    预期相似度：0.0
    """
    ori_text = read_file("./test_/empty_orig.txt")
    plag_text = read_file("./test_/empty_test.txt")
    ori_words = preprocess_text(ori_text)
    plag_words = preprocess_text(plag_text)
    similarity = calculate_similarity(ori_words, plag_words)
    similarity = round(similarity, 2)
    assert similarity == 0


def test_close():
    """
    测试相近文本的相似度
    预期相似度：>= 0.5
    """
    ori_text = read_file("./test_/close_orig.txt")
    plag_text = read_file("./test_/close_test.txt")
    ori_words = preprocess_text(ori_text)
    plag_words = preprocess_text(plag_text)
    similarity = calculate_similarity(ori_words, plag_words)
    similarity = round(similarity, 2)
    assert similarity >= 0.5


def test_substring():
    """
    测试子字符串情况
    预期相似度：>= 0.5
    """
    ori_text = read_file("./test_/substring_orig.txt")
    plag_text = read_file("./test_/substring_test.txt")
    ori_words = preprocess_text(ori_text)
    plag_words = preprocess_text(plag_text)
    similarity = calculate_similarity(ori_words, plag_words)
    similarity = round(similarity, 2)
    assert similarity >= 0.5


def test_long_text():
    """
    测试长文本的相似度
    预期相似度：>= 0.6
    """
    ori_text = read_file("./test_/long_orig.txt")
    plag_text = read_file("./test_/long_test.txt")
    ori_words = preprocess_text(ori_text)
    plag_words = preprocess_text(plag_text)
    similarity = calculate_similarity(ori_words, plag_words)
    similarity = round(similarity, 2)
    assert similarity >= 0.6


def test_special_chars():
    """
    测试包含特殊字符的文本
    预期相似度：>= 0.1
    """
    ori_text = read_file("./test_/special_orig.txt")
    plag_text = read_file("./test_/special_test.txt")
    ori_words = preprocess_text(ori_text)
    plag_words = preprocess_text(plag_text)
    similarity = calculate_similarity(ori_words, plag_words)
    similarity = round(similarity, 2)
    assert similarity >= 0.1


def test_unsimplified():
    """
    测试繁简体转换情况
    预期相似度：0.0（区分简中和繁中）
    """
    ori_text = read_file("./test_/unsimplified_orig.txt")
    plag_text = read_file("./test_/unsimplified_test.txt")
    ori_words = preprocess_text(ori_text)
    plag_words = preprocess_text(plag_text)
    similarity = calculate_similarity(ori_words, plag_words)
    similarity = round(similarity, 2)
    assert similarity == 0


# 程序入口点
if __name__ == "__main__":
    main()
