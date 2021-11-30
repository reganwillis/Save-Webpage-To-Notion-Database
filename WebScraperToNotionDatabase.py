import sys
import requests
import configparser
from rich import print
from bs4 import BeautifulSoup

print('[underline yellow]Welcome to the Web Scraper to Notion Database App!')

# print formatted progress and error messages
def print_formatted(string, message_type=('progress', 'error')):

    if message_type == 'progress':
        print('[blue]' + string + '...[/blue]')

    if message_type == 'error':
        print('[red][bold]ERROR:[/bold] ' + string + '[/red]')

# read database variables from configuration file
# TODO: add any default variables to configuration file
try:
    print_formatted('Reading configuration file', 'progress')

    config_file = 'config.txt'
    config = configparser.ConfigParser()
    config.read(config_file)
    auth = config['notionAPI']['INTEGRATION_AUTH']
    db_id = config['notionAPI']['DATABASE_ID']
except:
    print_formatted('unable to read configuration file \'' + config_file + '\'', 'error')
    print_formatted('Exiting program', 'progress')
    sys.exit()

# user can scrape as many URLs as they want
while True:
    url = input("Enter URL or type \'EXIT\' to quit: ")
    scraped_text = []

    # allow user to quit
    if url.upper() == 'EXIT':
        break

    # scrape HTML of URL provided by user
    try:
        print_formatted('Scraping HTML from \'' + url + '\'', 'progress')

        html = requests.get(url)
        soup = BeautifulSoup(html.content, "html.parser")

        # default values
        title = "New Entry Saved from Web Scraper"
        scraped_text.append(soup.get_text())
    except:
        print_formatted('unable scrape HTML from \'' + url + '\'', 'error')
        continue

    # format HTML for readability
    try:
        print_formatted('Formatting HTML for readability', 'progress')

        scraped_text = []

        # grab title from head
        title = soup.title.string

        # only work with text in article tag
        article = soup.article
        #print(article.get_text())
        scraped_text.append(article.get_text())
        # TODO: spread text out by tag for readability
        #strs = [text for text in soup.stripped_strings]
        #print(strs)
        #for i in soup.prettify().split('\n'):
        #    print(i)

        # TODO: medium compatable
        # if https://medium.com/ is in url
        
        # extract all links
        links = []
        for link in article.find_all('a'):
            stripped_link = str(link.string) + '\t' + link.get('href')
            links.append(stripped_link)
            #print(stripped_link)
            scraped_text.append(stripped_link)
        # add them as notion inline links
        # add separate link section at the bottom

        # extract images

        # turn gists into code blocks
    except Exception as e:
        print_formatted('unable to format HTML', 'error')
        print(e)
        print_formatted('Continuing with raw text', 'progress')

    # save scraped HTML locally
    try:
        # input (optional) - name of new database, option to save web-scraped data to local text file
        save_locally = False  # TODO: change default to false
        local_location = ''

        # TODO: create folder for output
        # TODO: option to save just HTML in output file

        # TODO: save to local text file
        if save_locally:

            with open('webscraped_html.txt', 'w') as file:
                file.write(scraped_text)
    except:
        print_formatted('unable to save HTML locally to \'' + local_location + '\'', 'error')

    # save scraped HTML to notion database
    try:
        # handle limit by splitting text into multiple blocks
        #print(len(scraped_text))
        max_block_length = 2000 - 1
        blocks = []

        for item in scraped_text:
            if len(item) > max_block_length:
                length_count = 0
                block = ""

                for char in item:
                    block = block + char
                    length_count = length_count + 1

                    if length_count == max_block_length:
                        blocks.append(block)
                        #print(block + '\n')
                        block = ""
                        length_count = 0
                blocks.append(block)
            else:
                blocks.append(item)

        children = []
        for block in blocks:
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

        # save to notion
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

        # print response to user
        #print(response.json())

        # get id of new page
        #response_json = response.json()
        #print(response_json)
        #new_page_id = response_json.get("id")
        #print(new_page_id)
    except:
        print_formatted('unable to save to Notion', 'error')

print('[yellow]Thanks for using the Web Scraper to Notion Database App. Goodbye!')
sys.exit()