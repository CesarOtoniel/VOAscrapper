"""
Author: Cesar Guevara

This script scraps the mp3 file for the program 
Buenos Días América to use in a local radio station.

Make sure you have permit from VOA to broadcast the program.
"""
import os
from urllib.request import urlopen, urlretrieve
from xml.etree.ElementTree import parse
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from urllib.parse import quote  # Add import statement for quote function

savePath = '/home/$USER/Documents/'  #Linux filepath
targetFormat = ".mp3"
program1 = "Buenos Días América"


# Fetching URL from API
api_url = 'https://www.vozdeamerica.com/api/'
var_url = urlopen(api_url)
xmldoc = parse(var_url)

def remove_download_param(url):
    if url.endswith("?download=1"):
        return url[:-len("?download=1")]
    else:
        return url
# Print out titles for debugging
for item in xmldoc.iterfind('channel/item'):
    title = item.findtext('title')
    print(title)

# Extracting URL from XML
link = None
for item in xmldoc.iterfind('channel/item'):
    title = item.findtext('title')
    if program1 in title:
        link = item.findtext('link')
        break

# If link is found, proceed to scrape and download MP3
if link:
    link_encoded = quote(link, safe=':/')
    html_doc = urlopen(link_encoded).read()
    soup = BeautifulSoup(html_doc, 'html.parser') 

    # Look for links with "?download=1" in href attribute
    for a_tag in soup.find_all('a', href=lambda href: href and "?download=1" in href):
        mp3_link = a_tag.get('href')
        mp3_link = remove_download_param(mp3_link)

        if mp3_link.endswith('.mp3'):
            print("MP3 Link:", mp3_link)

            complete_name = os.path.join(savePath, program1 + ".mp3")
            if os.path.exists(complete_name):
                os.remove(complete_name)
            urlretrieve(mp3_link, complete_name)
            print("File downloaded successfully.")
            break
else:
    print("Program URL not found.")

