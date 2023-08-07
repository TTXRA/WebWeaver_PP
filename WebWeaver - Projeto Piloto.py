from bs4 import BeautifulSoup
import requests
import re
import json
import datetime

def WebWeaver_PP(query):
    query = query.replace(' ', '+')
    url = f"https://scholar.google.com/scholar?q={query}"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    results = soup.find_all('div', class_='gs_r gs_or gs_scl')

    scp_data = []

    if len(results) != 0:
        for result in results:
            title_element = result.find('h3', class_='gs_rt')
            title = result.find('h3', class_='gs_rt').text.strip()
            title = re.sub(r'\[.*?]', '', title)
            title = title.lstrip()

            authors = result.find('div', class_='gs_a').text.strip()

            if ' - ' in authors:
                authors_split = authors.split(' - ')
                if len(authors_split) > 0:
                    author = authors_split[0].strip()
                if len(authors_split) > 1:
                    publication = authors_split[1].strip()
            else:
                authors_split = authors.split(' - ')
                if len(authors_split) > 0:
                    author = authors_split[0].strip()
                if len(authors_split) > 2:
                    publication = authors_split[1].strip()

            fragment_elem = result.find('div', class_='gs_rs')
            if fragment_elem:
                fragment = fragment_elem.text.strip()
            else:
                fragment = "Fragment not available."

            link = title_element.find('a')['href']

            result_data = {
                "Title": title,
                "Author(s)": author,
                "Publication": publication,
                "Fragment": fragment.replace('\n', ''),
                "Link": link
            }

            scp_data.append(result_data)

        current_date = datetime.date.today()
        date = current_date.strftime("%Y-%m-%d")
        with open(query + '_' + date + '.json', 'w', encoding='utf8') as outfile:
            json.dump(scp_data, outfile, indent=4, ensure_ascii=False)

        print("--------")
        print("Data saved in '" + query + "_" + date + ".json'.")
    else:
        print("The query did not return any results.")

query = "web scraping"
WebWeaver_PP(query)