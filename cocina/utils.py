from bs4 import BeautifulSoup


def clean_html(raw_html):
    soup = BeautifulSoup(raw_html)
    tag_list = soup.find_all(lambda tag: len(tag.attrs) > 0)
    for t in tag_list:
        for attr, val in t.attrs:
            del t[attr]
    return soup.get_text()


def clean_whitespaces(text):
    return ' '.join(text.split())
