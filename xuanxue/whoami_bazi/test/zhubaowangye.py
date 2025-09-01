import requests


def save_webpage_to_txt(url, filename="webpage_content.txt", headers=None):
    """
    抓取网页内容并保存到TXT文件
    :param url: 目标网页URL
    :param filename: 保存的文件名
    :param headers: 请求头信息
    :return: 成功返回True，失败返回False
    """
    # 设置默认请求头，模拟浏览器访问
    if headers is None:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/114.0.0.0 Safari/537.36"
        }

    try:
        # 发送GET请求
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # 检查请求是否成功

        # 设置正确的编码（避免中文乱码）
        response.encoding = response.apparent_encoding

        # 将内容写入TXT文件
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"网页标题: {response.url}\n\n")  # 写入URL
            f.write("网页内容:\n")
            f.write(response.text)  # 写入网页HTML内容

        print(f"网页内容已成功保存到 {filename}")
        return True

    except Exception as e:
        print(f"保存失败: {str(e)}")
        return False


def main():
    # 目标网页URL
    target_url = "https://www.52fhz.com/jipin/"

    # 调用函数保存网页内容
    save_webpage_to_txt(
        url=target_url,
        filename="example_page.txt"  # 自定义保存的文件名
    )


if __name__ == "__main__":
    main()
