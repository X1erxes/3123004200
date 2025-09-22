import sys
import jieba

def read_file(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read().strip()
        return content
    except FileNotFoundError:
        print(f"�����Ҳ����ļ� {filename}")
        return None


def preprocess_text(text):
    words = jieba.lcut(text)

    punctuation = '������������""''��������������'
    stop_words = ['��', '��', '��', '��', '��', '��', '��', '��', '��', '��', '��', 'һ', 'һ��', '��', 'Ҳ', '��',
                  '��', '˵', 'Ҫ', 'ȥ', '��', '��', '��', 'û��', '��', '��', '�Լ�', '��']

    filtered_words = []
    for word in words:
        if word not in punctuation and word not in stop_words and len(word) > 0:
            filtered_words.append(word)

    return filtered_words


def main():
    if len(sys.argv) != 4:
        print("�������")
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


if __name__ == "__main__":
    main()
