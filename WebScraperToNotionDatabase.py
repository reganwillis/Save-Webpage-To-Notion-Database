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

def add_block():
    pass

# user can scrape as many URLs as they want
while True:
    url = input("Enter URL or type \'EXIT\' to quit: ")
    scraped_text = []
    new_children = []

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

        # TODO: different method if no article tag available
        # only work with text in article tag
        article = soup.article
        #scraped_text.append(article.get_text())

        # TODO: turn scraped text into dictionary with key as text or link.
        # TODO: clear out all empty strings from scraped_text
        # TODO: save in block format
        one_string = ""
        block_to_be_added = ""
        type_of_block_to_be_added = ""
        subtype_of_block_to_be_added = ""
        curr_block = {}
        max_block_length = 2000
        for tag in article.strings:
            #print(tag.parent.name)
            if tag.parent.name == 'h1':
                new_children.append(curr_block)
                curr_block = {}
                #scraped_text.append(one_string)
                #scraped_text.append(tag)
                # start new block

                heading = {
                    "type": "heading_1",
                    "heading_1": {
                        "text": [{
                            "type": "text",
                            "text": {
                                "content": tag
                            }
                        }]
                    }
                }
                new_children.append(heading)
            elif tag.parent.name == 'h2':
                new_children.append(curr_block)
                curr_block = {}
                heading = {
                    "type": "heading_2",
                    "heading_2": {
                        "text": [{
                            "type": "text",
                            "text": {
                                "content": tag
                            }
                        }]
                    }
                }
                new_children.append(heading)
            elif tag.parent.name == 'p':
                #new_children.append(curr_block)
                #curr_block = {}
                #type_of_block_to_be_added = "text"
                #subtype_of_block_to_be_added = "content"
                if curr_block.get("type") == "paragraph":
                    # different action if link or not
                    pass
                para = {
                    "type": "paragraph",
                    "paragraph": {
                        "text": [{
                            "type": "text",
                            "text": {
                                "content": tag
                            }
                        }]
                    }
                }
                if curr_block == {}:
                    curr_block = para
                else:
                    curr_content = curr_block.get("paragraph").get("text")
                    curr_content.append({"type": "text", "text": {"content": tag}})
                    curr_block = {
                        "type": "paragraph",
                        "paragraph": {
                            "text": curr_content
                        }
                    }
                #if tag.parent.name == 'span':
                #    pass
                #if tag.parent.name == 'em':
                #    pass
            elif tag.parent.name == 'a':
                if curr_block.get("type") == "paragraph":
                    # different action if link or not
                    # TODO: user can customize link color
                    curr_content = curr_block.get("paragraph").get("text")
                    curr_content.append({"type": "text", "text": {"content": tag, "link": None}, "annotations": {"color": "blue"}})
                    curr_block = para = {
                        "type": "paragraph",
                        "paragraph": {
                            "text": curr_content
                        }
                    }
                    #curr_content = curr_content + tag
                
                # TODO: place text inline
                # TODO: change color of text
                # TODO: change text to link
                #print(tag)
                #print(tag.parent.get('href'))
                #scraped_text.append(tag + ' (' + tag.parent.get('href') + ') ')
            else:
                #scraped_text.append(tag)
                # TODO: handle missed text in a better way
                print_formatted('if statements failed to catch ' + tag.parent.name, 'error')
                new_children.append(curr_block)
                curr_block = {}
    
                """
                new_block = {
                    "paragraph": {
                        "text": [
                            {
                                "text": {
                                    "content": tag
                                }
                                "text": {
                                    "content": "link text",
                                    "link": {
                                        "type": "url",
                                        "url": ""
                                    }
                                }
                            }
                        ]
                    }
                }
                children.append(new_block)
                """
        #new_children.append(curr_block)
        # TODO: spread text out by tag for readability
        #strs = [text for text in soup.stripped_strings]
        #print(strs)
        #for i in soup.prettify().split('\n'):
        #    print(i)

        # TODO: medium compatable
        # if https://medium.com/ is in url
        # split title by pipes (title | by author | publisher)
        
        # extract all links
        # TODO: add them as notion inline links
        #links = []
        #for link in article.find_all('a'):
        #    stripped_link = str(link.string) + '\t' + link.get('href')
        #    links.append(stripped_link)
        #    # add separate link section at the bottom
        #    scraped_text.append(stripped_link)

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
        print_formatted('Saving to Notion database', 'progress')
        # handle limit by splitting text into multiple blocks
        # TODO: more simple way to format this code block
        # TODO: cycle through all blocks and split if greater than max length
        max_block_length = 2000 - 1
        blocks = []
        smaller_new_children = []

        for c in new_children:
            if c == {}:
                print('passing')
            else:
                smaller_new_children.append(c)

        """
        for c in new_children:
            print(c)
            if c == {}:
                print('passing')
                #continue
                #print(c)
                #print('new child')
            elif c.get("type") == "paragraph":
                # TODO: loop through each curr
                for curr in c.get("paragraph").get("text")[0].get("text").get("content"):
                    #curr = c.get("paragraph").get("text")[0].get("text").get("content")
                    #print(c.get('paragraph').get('text'))
                    chunks = []
                    #print(len(curr))
                    if len(curr) > max_block_length:
                        print('splitting child')
                        length_count = 0
                        new_content = ""
                        for char in curr:
                            new_content = new_content + char
                            length_count = length_count + 1
                            if length_count == max_block_length:
                                chunks.append(new_content)
                                length_count = 0
                                new_content = ""
                        chunks.append(new_content)
                    else:
                        chunks.append(curr)
                    for chunk in chunks:
                        para = {
                            "type": "paragraph",
                            "paragraph": {
                                "text": [{
                                    "type": "text",
                                    "text": {
                                        "content": chunk
                                    }
                                }]
                            }
                        }
                        smaller_new_children.append(para)
                    #else:
                    #    smaller_new_children.append(c)
            else:
                smaller_new_children.append(c)
        """
        """
        for item in scraped_text:
            if len(item) > max_block_length:
                length_count = 0
                block = ""

                for char in item:
                    block = block + char
                    length_count = length_count + 1

                    if length_count == max_block_length:
                        blocks.append(block)
                        block = ""
                        length_count = 0
                blocks.append(block)
            else:
                blocks.append(item)
        """
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

        print_formatted('printing body', 'progress')
        print(smaller_new_children)
        #for i in smaller_new_children:
        #    print(i)

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
                "children": smaller_new_children
            }
        )

        # print response to user
        print(response.json())

        # get id of new page
        #response_json = response.json()
        #print(response_json)
        #new_page_id = response_json.get("id")
        #print(new_page_id)
    except Exception as e:
        print(e)
        print_formatted('unable to save to Notion', 'error')

print('[yellow]Thanks for using the Web Scraper to Notion Database App. Goodbye!')
sys.exit()