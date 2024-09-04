from bs4 import BeautifulSoup
from functools import wraps
import json
import requests


def cache_to_file(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        try:
            with open(kwargs['filename'], 'r') as f:
                return f.read()
        except FileNotFoundError:
            text = func(*args, **kwargs)
            with open(kwargs['filename'], 'w', encoding="utf-8") as f:
                f.write(text)
            return text
    return decorated


def fetch_chapter_urls() -> list[str]:
    text = get_parsed_urls(filename="./output/urls.txt")
    return text.strip().split("\n")


@cache_to_file
def get_html(*args, **kwargs) -> str:
    response = requests.get(kwargs['url'])
    return response.text


@cache_to_file
def get_parsed_urls(*args, **kwargs) -> str:
    html = get_html(
        url="https://www.heritage-history.com/index.php?c=read&author=macgregor&book=rome&story=_front",
        filename="./output/html/_front.html",
    )
    
    s = BeautifulSoup(html, 'html.parser')
    urls = set()
    out = ""
    for tag in s.find_all('a'):
        href = tag.get('href')
        if href and 'book' in href and 'story' in href and href not in urls:
            out += f"{href}\n"
            urls.add(href)
    return out


def summarize_chapters(urls: list[str]) -> str:
    summary = ""
    for url in urls:
        ch_name = url[url.find("story=")+len("story="):]

        summary_fn = f"./output/summary/{ch_name}.txt"
        summary += generate_chapter_summary(url=url, filename=summary_fn) + '\n\n'
    return summary


@cache_to_file
def generate_chapter_summary(*args, **kwargs) -> str:
    url = kwargs['url']
    ch_name = url[url.find("story=")+len("story="):]
    filename = f"./output/html/{ch_name}.html"
    html = get_html(url=url, filename=filename)
    
    s = BeautifulSoup(html, 'html.parser')
    title = s.h1.text
    chapter_text = "".join(elem.text for elem in s.find_all('p'))

    prompt = f"Summarize the following text into a single paragraph. Do not include a header or leading sentence:\n{chapter_text}"
    summary = format_line_breaks(llama3_1(prompt))
    return f"{title}\n{summary}"


def llama3_1(prompt:str) -> str:
    """ 
    Adapted from https://llama.meta.com/docs/llama-everywhere/running-meta-llama-on-mac/
    """
    data = {
        "model": "llama3.1",
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "stream": False,
    }

    headers = {
        "Content-Type": "application/json"
    }

    ollama_url = "http://localhost:11434/api/chat"
    response = requests.post(ollama_url, headers=headers, json=data)
    return response.json()["message"]["content"]


def format_line_breaks(text: str, line_len=80) -> str:
    out = ""
    i = 0
    while i+80 < len(text):
        next = text.rfind(" ", i, i + line_len)
        out += text[i:next] + '\n'
        i = next + 1
    out += text[i:]
    return out


if __name__ == '__main__':

    chapter_urls = fetch_chapter_urls()
    summary = summarize_chapters(chapter_urls)
    print(summary)
