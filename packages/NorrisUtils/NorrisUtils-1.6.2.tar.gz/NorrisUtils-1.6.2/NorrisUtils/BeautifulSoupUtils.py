import requests
from bs4 import BeautifulSoup
import bs4
import re
import json
import NorrisUtils.RequestUtils

FEATURE_PARSER = 'html.parser'


def find_links_with_keyword(url, keyword):
    """
    在给定URL的网页中查找包含特定关键字的链接。

    参数:
    url (str): 要爬取的网页URL。
    keyword (str): 要查找的关键字。

    返回:
    str: 如果找到包含关键字的链接，则返回该链接的URL；否则返回空字符串。
    """
    try:
        # 发送HTTP请求获取网页内容
        response = requests.get(url)

        # 检查请求是否成功
        if response.status_code == 200:
            # 使用BeautifulSoup解析网页内容
            soup = BeautifulSoup(response.text, FEATURE_PARSER)
            # 查找所有链接标签
            # 查找所有a标签
            links = soup.find_all('a')
            for link in links:
                # 获取链接的URL
                # 获取链接的href属性
                href = link.get('href')
                # 检查链接内容和链接URL是否包含关键字
                # 检查链接中是否包含特定日期字符串
                for item in link.contents:
                    if keyword in item:
                        href = NorrisUtils.RequestUtils.valid_url(href)
                        print(href)
                        return href
                if keyword in link:
                    href = NorrisUtils.RequestUtils.valid_url(href)
                    print(href)
                    return href
        else:
            # 请求失败，打印错误信息
            print(f"请求网页时发生错误，状态码：{response.status_code}")
            return ''
    except Exception as e:
        # 发生异常，打印错误信息
        print(f"发生错误：{e}")
        return ''


def find_tags_by_query(url, query, regex, tag="a"):
    """
    根据给定的URL、查询字符串、正则表达式和标签名称，从网页中查找匹配的标签。

    参数:
    url: 字符串，要查询的网页URL。
    query: 字符串，查询字符串，用于在网页内容中进行匹配。
    regex: 字符串，正则表达式，用于筛选匹配的标签文本。
    tag: 字符串，指定的HTML标签名称，默认为"a"，表示查找链接标签。

    返回:
    匹配正则表达式的标签列表，如果请求失败或没有找到匹配项，则返回空列表。
    """
    try:
        # 发送HTTP请求获取网页内容
        response = requests.get(url)
        response.encoding = 'utf-8'  # 设置编码为 utf-8
        print(response.text)
        # 检查请求是否成功
        if response.status_code == 200:
            # 使用BeautifulSoup解析网页内容
            soup = BeautifulSoup(response.text, 'html.parser')
            # 查找所有指定标签的元素
            # 查找所有a标签
            elements = soup.find_all(tag)
            # 如果未提供正则表达式，则根据查询字符串生成一个默认的正则表达式
            regex = regex if (regex is not None and regex != "") else f".*{query}.*"
            # 筛选匹配正则表达式的元素
            filtered_elements = [element for element in elements if
                                 element.text is not None and re.match(regex, element.text)]
            # 递归处理每个匹配元素的子元素
            for link in filtered_elements:
                deep_traverse(link, url)
            # 将匹配的元素转换为字符串列表并返回
            stringfy_elements = [str(link) for link in elements if link.text is not None and re.match(regex, link.text)]
            return stringfy_elements
        else:
            # 请求失败时打印错误信息并返回空列表
            print(f"请求网页时发生错误，状态码：{response.status_code}")
            return []
    except Exception as e:
        # 发生异常时打印错误信息并返回空列表
        print(f"发生错误：{e}")
        return []


def find_tags_by_regex(query, regex, tag="a", **kwargs):
    try:
        kwargs.setdefault("url", None)
        kwargs.setdefault("src", None)
        url = kwargs["url"]
        src = kwargs["src"]
        if (url is None or url == '') and (src is None or src == ''):
            return []
        if src is None or src == '':
            response = requests.get(url)
            response.encoding = 'utf-8'  # 设置编码为 utf-8
            print(response.text)
            # 检查请求是否成功
            if response.status_code == 200:
                # 使用BeautifulSoup解析网页内容
                soup = BeautifulSoup(response.text, 'html.parser')
                print(soup)
            else:
                # 请求失败时打印错误信息并返回空列表
                print(f"请求网页时发生错误，状态码：{response.status_code}")
                return []
        else:
            soup = BeautifulSoup(src, 'html.parser')
        # 查找所有指定标签的元素
        # 查找所有a标签
        elements = soup.find_all(tag)
        # 如果未提供正则表达式，则根据查询字符串生成一个默认的正则表达式
        regex = regex if (regex is not None and regex != "") else f".*{query}.*"
        # 筛选匹配正则表达式的元素
        filtered_elements = [element for element in elements if
                             element.text is not None and re.match(regex, element.text)]
        # 递归处理每个匹配元素的子元素
        for link in filtered_elements:
            deep_traverse(link, url)
        # 将匹配的元素转换为字符串列表并返回
        stringfy_elements = [str(link) for link in elements if link.text is not None and re.match(regex, link.text)]
        return stringfy_elements
    except Exception as e:
        # 发生异常时打印错误信息并返回空列表
        print(f"发生错误：{e}")
        return []


def process_element(element, url):
    """
    处理HTML元素，尤其是链接<a>标签，以确保它们的URL是完整的。

    参数:
    - element: BeautifulSoup对象，表示一个HTML元素，尤其是<a>标签。
    - url: 字符串，表示当前页面的URL，用于确定链接的协议（http或https）。

    该函数尝试更新元素的href属性，以确保链接是绝对URL，并且协议与当前页面一致。
    """
    """处理元素，这里仅作为示例，您可以根据需要定义具体的逻辑"""
    if element.name == 'a':  # 检查当前元素是否为<a>标签
        # 在此处添加针对<a>标签的具体逻辑处理
        try:
            if element.attrs is not None and element.attrs['href'] is not None:
                element.attrs['href'] = NorrisUtils.RequestUtils.valid_url(element.attrs['href'])
        except:
            pass
        print(f"Processing a tag with text: {element.get_text(strip=True)} and href: {element.get('href')}")


def deep_traverse(soup_element, url):
    """
    深度遍历 BeautifulSoup 对象。

    递归地遍历给定的 BeautifulSoup 对象的所有子元素，对每个元素调用 process_element 函数。

    参数:
    - soup_element: BeautifulSoup 对象的子元素，可以是标签、文本等。
    - url: 相关的 URL，用于处理元素时的上下文信息。
    """
    """深度优先遍历 BeautifulSoup 对象中的所有元素"""
    for child in soup_element.children:
        # 只处理标签类型的子元素
        if isinstance(child, bs4.element.Tag):  # 确保处理的是标签元素
            process_element(child, url)  # 对当前元素进行处理
            # 递归处理当前标签的子元素
            deep_traverse(child, url)  # 递归遍历子元素

# url = (find_links_with_keyword('https://www.zrfan.com/category/zhinan/', '2024-7-31'))
#
# tags = find_tags_by_regex(query='京东', regex='', tag="blockquote", url=url)
# print('\n aaaaa:' + str(tags))
