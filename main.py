import sys
import jieba
from collections import Counter


def read_file(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read().strip()
        return content
    except FileNotFoundError:
        print(f"错误：找不到文件 {filename}")
        return None


def preprocess_text(text):
    words = jieba.lcut(text)

    punctuation = '，。！？；：""''（）【】《》、'
    stop_words = ['的', '了', '在', '是', '我', '有', '和', '就', '不', '人', '都', '一', '一个', '上', '也', '很',
                  '到', '说', '要', '去', '你', '会', '着', '没有', '看', '好', '自己', '这']

    filtered_words = []
    for word in words:
        if word not in punctuation and word not in stop_words and len(word) > 0:
            filtered_words.append(word)

    return filtered_words


def calculate_similarity(original_words, plagiarized_words):
    original_counter = Counter(original_words)
    plagiarized_counter = Counter(plagiarized_words)

    intersection = sum((original_counter & plagiarized_counter).values())
    union = sum((original_counter | plagiarized_counter).values())

    if union == 0:
        similarity = 0
    else:
        similarity = intersection / union

    return similarity


def write_result(filename, similarity):
    """将结果写入文件"""
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(f"{similarity:.2f}\n")


def main():
    if len(sys.argv) != 4:
        print("输入错误")
        return

    original_file = sys.argv[1]
    plagiarized_file = sys.argv[2]
    output_file = sys.argv[3]

    original_text = read_file(original_file)
    if original_text is None:
        return

    plagiarized_text = read_file(plagiarized_file)
    if plagiarized_text is None:
        return

    original_words = preprocess_text(original_text)
    plagiarized_words = preprocess_text(plagiarized_text)

    similarity = calculate_similarity(original_words, plagiarized_words)
    write_result(output_file, similarity)
    print(f"论文相似度: {similarity:.2f}")


def test_identical():
    ori_text = read_file("./test_/identical_orig.txt")
    plag_text = read_file("./test_/identical_test.txt")
    ori_words = preprocess_text(ori_text)
    plag_words = preprocess_text(plag_text)
    similarity = calculate_similarity(ori_words, plag_words)
    similarity = round(similarity, 2)
    assert similarity == 1.0


def test_completely_different():
    ori_text = read_file("./test_/completely_orig.txt")
    plag_text = read_file("./test_/completely_test.txt")
    ori_words = preprocess_text(ori_text)
    plag_words = preprocess_text(plag_text)
    similarity = calculate_similarity(ori_words, plag_words)
    similarity = round(similarity, 2)
    assert similarity == 0


def test_partial_overlap():
    ori_text = read_file("./test_/partial_orig.txt")
    plag_text = read_file("./test_/partial_test.txt")
    ori_words = preprocess_text(ori_text)
    plag_words = preprocess_text(plag_text)
    similarity = calculate_similarity(ori_words, plag_words)
    similarity = round(similarity, 2)
    assert similarity >= 0.5


def test_empty_orig():
    ori_text = read_file("./test_/ept_orig.txt")
    plag_text = read_file("./test_/ept_test.txt")
    ori_words = preprocess_text(ori_text)
    plag_words = preprocess_text(plag_text)
    similarity = calculate_similarity(ori_words, plag_words)
    similarity = round(similarity, 2)
    assert similarity == 0


def test_empty_plag():
    ori_text = read_file("./test_/empty_orig.txt")
    plag_text = read_file("./test_/empty_test.txt")
    ori_words = preprocess_text(ori_text)
    plag_words = preprocess_text(plag_text)
    similarity = calculate_similarity(ori_words, plag_words)
    similarity = round(similarity, 2)
    assert similarity == 0


def test_close():
    ori_text = read_file("./test_/close_orig.txt")
    plag_text = read_file("./test_/close_test.txt")
    ori_words = preprocess_text(ori_text)
    plag_words = preprocess_text(plag_text)
    similarity = calculate_similarity(ori_words, plag_words)
    similarity = round(similarity, 2)
    assert similarity >= 0.5


def test_substring():
    ori_text = read_file("./test_/substring_orig.txt")
    plag_text = read_file("./test_/substring_test.txt")
    ori_words = preprocess_text(ori_text)
    plag_words = preprocess_text(plag_text)
    similarity = calculate_similarity(ori_words, plag_words)
    similarity = round(similarity, 2)
    assert similarity >= 0.5


def test_long_text():
    ori_text = read_file("./test_/long_orig.txt")
    plag_text = read_file("./test_/long_test.txt")
    ori_words = preprocess_text(ori_text)
    plag_words = preprocess_text(plag_text)
    similarity = calculate_similarity(ori_words, plag_words)
    similarity = round(similarity, 2)
    assert similarity >= 0.6


def test_special_chars():
    ori_text = read_file("./test_/special_orig.txt")
    plag_text = read_file("./test_/special_test.txt")
    ori_words = preprocess_text(ori_text)
    plag_words = preprocess_text(plag_text)
    similarity = calculate_similarity(ori_words, plag_words)
    similarity = round(similarity, 2)
    assert similarity >= 0.1


def test_unsimplified():
    ori_text = read_file("./test_/unsimplified_orig.txt")
    plag_text = read_file("./test_/unsimplified_test.txt")
    ori_words = preprocess_text(ori_text)
    plag_words = preprocess_text(plag_text)
    similarity = calculate_similarity(ori_words, plag_words)
    similarity = round(similarity, 2)
    assert similarity == 0


if __name__ == "__main__":
    main()
