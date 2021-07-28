import bs4
import re
import urllib
import datetime
import random

REF_REGEX = re.compile(r"\[\d+\]")

def random_event():
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
            
    event = random.choice(items)
    text = event.text
    return re.sub(REF_REGEX, "", text)
