import os
os.makedirs("crawler", exist_ok=True)

import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from classifier.rule_based_filter import is_valid_blog as rule_based_is_valid_blog
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from bs4.element import Tag
import time # used to pause the script(js to load)
import json


def save_blog(data ,  i):
    with open(f"crawler/blog_{i}.json" , "w" , encoding="utf-8") as f:
        json.dump(data , f , ensure_ascii=False , indent = 2)

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()


        base_url = "https://towardsdatascience.com/"
        page.goto(base_url)
        time.sleep(5) #wait for js to load 

        content = page.content()
        soup = BeautifulSoup(content, "html.parser")

        #extract blog post links from homepage
        links = [
            str(a['href']) for a in soup.find_all('a', href=True)
            if isinstance(a, Tag) and isinstance(a['href'], (str, list)) and str(a['href']).startswith('https://towardsdatascience.com/')
        ]


        #remove duplicates
        links = list(set(links))[:10] #limit of 10 

        for i, link in enumerate(links):

            try:
                page.goto(link)
                time.sleep(3)
                post = BeautifulSoup(page.content(),"html.parser")

                h1_tag = post.find("h1")
                title = h1_tag.text if h1_tag else "No Title"
                
                paragraphs = post.find_all("p")

                content = "\n".join([p.text for p in paragraphs])

                author_tag = post.find("meta" , {"name":"author"})

                author = author_tag["content"] if author_tag and isinstance(author_tag, Tag) and "content" in author_tag.attrs else "Unknown"
                
                date_tag = post.find("time")

                date = date_tag["datetime"] if date_tag and isinstance(date_tag, Tag) and "datetime" in date_tag.attrs else "Unknown"

                blog_data = {
                    "title": title,
                    "author": author,
                    "date": date,
                    "content": content,
                    "url": link
                }

                if rule_based_is_valid_blog(blog_data):
                    save_blog(blog_data, i)
                    print(f"✅ Saved blog {i+1}: {title}")
                else:
                    print(f"❌ Skipped blog {i+1}: not valid by rules")

            except Exception as e:
                print(f"Error on blog {i+1}:{e}")
                continue

        browser.close()

if __name__ == "__main__":
    run()