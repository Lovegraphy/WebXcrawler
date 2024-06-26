# WebXcrawler
( a simple python tool for recursively crawling web pages )

WebXcrawler is a Python tool for recursively crawling web pages and organizing retrieved content into files based on their types. It provides basic functionality to initiate a web crawl from a specified starting URL and allows customization of the maximum depth of the crawl.


## Features

- Crawls web pages recursively starting from a specified URL.
- Organizes crawled content into directories (`javascript_files`, `php_files`, `other_files`).
- Handles URLs without `http` or `https` prefix.
- Validates crawl depth input (1-5).

## Installation

Clone the repository:

```bash
git clone https://github.com/lovegraphy/WebXcrawler.git
cd WebXcrawler
```
Install dependencies:
```bash
pip install requests beautifulsoup4
```
## Usage
Run the script
```bash
python WebXcrawler.py
```
## Example
```bash
python WebXcrawler.py
Enter the starting URL: https://example.com
Enter the maximum depth to crawl (1-5):
Enter the maximum depth to crawl: 3
```
## Directory Structure
After crawling, the directory structure will look like this:
```bash
example.com/
│
├── javascript_files/
│   ├── script1.js
│   ├── script2.js
│   └── ...
│
├── php_files/
│   ├── file1.php
│   ├── file2.php
│   └── ...
│
└── other_files/
    ├── index.html
    ├── image.jpg
    └── ...

```
Screenshots:
![Screenshot (81)](https://github.com/Lovegraphy/WebXcrawler/assets/108510677/ecfdc069-4555-4c30-87fa-4937cf2ee7d9)
