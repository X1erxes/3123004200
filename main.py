import sys


def read_file(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read().strip()
        return content
    except FileNotFoundError:
        print(f"错误：找不到文件 {filename}")
        return None


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


if __name__ == "__main__":
    main()
