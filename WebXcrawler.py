import os
import requests
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
from collections import deque

def print_banner():
    banner = """
    ╔═════════════════════════════════════════╗
    ║                                         ║
    ║             ███╗   ██╗                  ║
    ║             ████╗  ██║                  ║
    ║             ██╔██╗ ██║                  ║
    ║             ██║╚██╗██║                  ║
    ║             ██║ ╚████║                  ║
    ║             ╚═╝  ╚═══╝                  ║
    ║                                         ║
    ║             WebXCrawler                 ║
    ║                                         ║
    ║            Author: Lovegraphy           ║
    ║                                         ║
    ║  GitHub: https://github.com/lovegraphy  ║
    ║                                         ║
    ╚═════════════════════════════════════════╝
    """
    print(banner)

def download_page(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.content
        else:
            print(f"Failed to download {url}. Status code: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error downloading {url}: {e}")
        return None

def save_page(url, content, output_dir):
    parsed_url = urlparse(url)
    path = parsed_url.path
    if path == '' or path == '/':
        path = '/index.html'
    elif path.endswith('/'):
        path += 'index.html'
    
    filename = os.path.join(output_dir, path.lstrip('/'))
    
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'wb') as f:
        f.write(content)
    print(f"Saved {url} to {filename}")

def filter_and_organize_files(output_dir):
    js_dir = os.path.join(output_dir, 'javascript_files')
    php_dir = os.path.join(output_dir, 'php_files')
    other_dir = os.path.join(output_dir, 'other_files')

    for root, _, files in os.walk(output_dir):
        if root in [js_dir, php_dir, other_dir]:
            continue
        for file in files:
            filepath = os.path.join(root, file)
            if file.endswith('.js'):
                os.makedirs(js_dir, exist_ok=True)
                os.replace(filepath, os.path.join(js_dir, file))
                print(f"Moved {file} to javascript_files directory.")
            elif file.endswith('.php'):
                os.makedirs(php_dir, exist_ok=True)
                os.replace(filepath, os.path.join(php_dir, file))
                print(f"Moved {file} to php_files directory.")
            else:
                os.makedirs(other_dir, exist_ok=True)
                os.replace(filepath, os.path.join(other_dir, file))
                print(f"Moved {file} to other_files directory.")

def crawl(url, max_depth, output_dir, visited, queue):
    while queue:
        current_url, current_depth = queue.popleft()
        if current_depth > max_depth or current_url in visited:
            continue

        print(f"Crawling {current_url}")
        content = download_page(current_url)
        if content:
            save_page(current_url, content, output_dir)
            visited.add(current_url)
            soup = BeautifulSoup(content, 'html.parser')
            for link in soup.find_all('a', href=True):
                next_url = urljoin(current_url, link['href'])
                if urlparse(next_url).scheme in ('http', 'https') and next_url.startswith(url):
                    queue.append((next_url, current_depth + 1))

def should_crawl(url):
    try:
        robots_txt = requests.get(urljoin(url, '/robots.txt')).text
        lines = robots_txt.split('\n')
        for line in lines:
            if line.strip().startswith('Disallow:'):
                path = line.split(': ')[1].strip()
                if urlparse(url).path.startswith(path):
                    return False
        return True
    except requests.exceptions.RequestException:
        return True

if __name__ == "__main__":
    print_banner()
    start_url = input("Enter the starting URL: ")
    if not start_url.startswith(('http://', 'https://')):
        start_url = 'http://' + start_url

    print("Enter the maximum depth to crawl (1-5):")
    max_depth = int(input("Enter the maximum depth to crawl: "))
    while max_depth < 1 or max_depth > 5:
        print("Please enter a value between 1 and 5.")
        max_depth = int(input("Enter the maximum depth to crawl: "))

    base_output_directory = os.getcwd()  # Current working directory

    parsed_start_url = urlparse(start_url)
    domain = parsed_start_url.netloc
    output_directory = os.path.join(base_output_directory, domain)

    if should_crawl(start_url):
        visited = set()
        queue = deque([(start_url, 0)])
        crawl(start_url, max_depth, output_directory, visited, queue)
        filter_and_organize_files(output_directory)
    else:
        print("Crawling disallowed by robots.txt.")
