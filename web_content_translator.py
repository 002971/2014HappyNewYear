import requests
from bs4 import BeautifulSoup
from googletrans import Translator
import pdfkit

def translate_web_content(url):
    # 创建一个Translator对象
    translator = Translator(service_urls=['translate.google.com'])

    # 发送GET请求获取网页内容
    response = requests.get(url)
    content = response.text

    # 创建一个BeautifulSoup对象并解析网页内容
    soup = BeautifulSoup(content, 'html.parser')

    # 提取前10个页面链接
    links = soup.select("a[href]")
    top_10_links = [link.get("href") for link in links][:10]

    # 翻译每个链接的内容并保存到临时文件中
    for link in top_10_links:
        # 获取链接的内容
        link_response = requests.get(link)
        link_content = link_response.text

        # 翻译内容
        translation = translator.translate(link_content, src='en', dest='zh-CN')

        # 保存翻译后的内容到临时文件
        with open('translated.txt', 'a') as file:
            file.write(f"Original Text:\n{link_content}\n\nTranslated Text:\n{translation.text}\n\n")

    # 合并所有临时文件为一个PDF文件
    pdfkit.from_file('translated.txt', 'output.pdf')

# 主函数
if __name__ == '__main__':
    url = 'https://medium.com/?tag=software-engineering'
    translate_web_content(url)
