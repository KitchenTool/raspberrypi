import bs4
import re
import urllib, urllib.parse, urllib.request
import datetime
import random

REF_REGEX = re.compile(r"\[\d+\]")
DAY_FILE = "/tmp/today.txt"

def random_event():
    try:
        with open(DAY_FILE, 'r') as fp:
            items = fp.readlines()
        text = random.choice(items).strip()
        return re.sub(REF_REGEX, "", text)
    except:
        return "Today is a great day!"

def cache_day():
    date = datetime.date.today().strftime("%B %d")
    date = urllib.parse.quote(date)
    url = "https://en.wikipedia.org/wiki/" + date
    response = urllib.request.urlopen(url)
    body = response.read().decode()
    p = bs4.BeautifulSoup(body, 'html.parser')

    items = []
    for sibling in p.body.find(class_="mw-parser-output").find("h2", recursive=False).next_siblings:
        if sibling.name == "h2":
            break
        
        if sibling.name == "ul":
            items += sibling.find_all("li")
            
    lines = '\n'.join([x.text for x in items])
    with open(DAY_FILE, 'w') as fp:
        fp.write(lines)

if __name__ == "__main__":
    cache_day()