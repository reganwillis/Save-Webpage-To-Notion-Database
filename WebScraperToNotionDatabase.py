import sys
import requests
import configparser
from rich import print
from bs4 import BeautifulSoup

scraped_text = ""

print('Welcome to the Web Scraper to Notion Database App!')

# read database variables from configuration file
try:
    config_file = 'config.txt'
    config = configparser.ConfigParser()
    config.read(config_file)
    auth = config['notionAPI']['INTEGRATION_AUTH']
    db_id = config['notionAPI']['DATABASE_ID']
except:
    sys.exit('ERROR: unable to read configuration file \'' + config_file + '\'')

# input (required) - secret key, database key, URL
# input (optional) - name of new database, option to save web-scraped data to local text file
save_locally = False  # TODO: change default to false

# user can scrape as many URLs as they want
while True:
    url = input("Enter URL or type \'EXIT\' to quit: ")

    # allow user to quit
    if url.upper() == 'EXIT':
        break

    try:
        # scrape HTML of URL provided by user
        html = requests.get(url)
    except:
        print('ERROR: unable scrape HTML from \'' + url + '\'')
        continue

    try:
        # parse HTML
        soup = BeautifulSoup(html.content, "html.parser")

        # TODO: create folder for output
        # TODO: option to save just HTML in output file

        # TODO: grab title from html
        title = "test title"

        # default - raw text
        raw_text = soup.get_text()
        scraped_text = raw_text

        # TODO: spread text out by tag for readability
        #strs = [text for text in soup.stripped_strings]
        #print(strs)

        # TODO: medium compatable
        # if https://medium.com/ is in url
        # convert code chunks to code block

        # TODO: save to local text file
        if save_locally:

            with open('webscraped_html.txt', 'w') as file:
                file.write(scraped_text)

        # handle limit by splitting text into multiple blocks
        print(len(scraped_text))
        max_block_length = 2000 - 1
        blocks = []
        if len(scraped_text) > max_block_length:
            length_count = 0
            block = ""
            for char in scraped_text:
                block = block + char
                length_count = length_count + 1
                if length_count == max_block_length:
                    blocks.append(block)
                    block = ""
                    length_count = 0

        children = []
        for block in blocks:
            print(block + '\n')
            new_block = {
                "paragraph": {
                    "text": [
                        {
                            "text": {
                                "content": block
                            }
                        }
                    ]
                }
            }
            children.append(new_block)

        # TODO: save web-scraped data to notion
        notion_url = "https://api.notion.com/v1/pages/"
        # TODO: create new database if none exists
        # TODO: link property with link to article
        properties = {
            "title": {
                "title": [
                    {
                        "text": {
                            "content": title
                        }
                    }
                ]
            }
        }

        # post scraped data to notion database
        response = requests.post(notion_url,
            headers = {
                "Content-Type": "application/json",
                "Notion-Version": "2021-08-16",
                "Authorization": "Bearer " + auth
            },
            json = {
            "parent": {
                "database_id": db_id
            },
            "properties": properties,
            "children": children
            }
        )

        # get id of new page
        response_json = response.json()
        print(response_json)
        new_page_id = response_json.get("id")
        print(new_page_id)
    except:
        print('unknown error')
sys.exit('Thanks for using the Web Scraper to Notion Database App. Goodbye!')