import requests
import os
import string
from lxml import html
import random
page_directories = {
                    #"G": "http://www.imdb.com/search/title?title_type=feature&certificates=US%3Ag&languages=en&count=800", 
                    #"PG" : "http://www.imdb.com/search/title?title_type=feature&certificates=US%3Apg&languages=en&count=800", 
                    #"PG-13" : "http://www.imdb.com/search/title?title_type=feature&certificates=US%3Apg_13&languages=en&count=800", 
                    #"R": "http://www.imdb.com/search/title?title_type=feature&certificates=US%3Ar&languages=en&count=800", 
                    #"NC-17": "http://www.imdb.com/search/title?title_type=feature&certificates=US%3Anc_17&languages=en&count=400"
                   }
training_dir = "Training/"
test_dir = "Testing/"

for key in page_directories.keys():
    print("Grabbing URL List - " + key)
    webpage = requests.get(page_directories[key])
    tree = html.fromstring(webpage.content)

    urls = tree.xpath('//h3[@class="lister-item-header"]//a/@href')
    titles = tree.xpath('//h3[@class="lister-item-header"]//a/text()')

    printable = set(string.printable)

    for i in range(0,len(urls)):
        print("\tGrabbing - " + titles[i]);
        text_file = open(training_dir+key + "-" + titles[i].replace('/','-') + ".txt", "w")
        
        # Writes movies title
        text_file.write('\n'+filter(lambda x: x in printable, titles[i]))

        # Grabs description
        movie_page = requests.get('http://www.imdb.com/'+urls[i])
        movie_tree = html.fromstring(movie_page.content)
        movie_description = movie_tree.xpath('//div[@itemprop="description"]//p/text()')
        if len(movie_description) > 0:
            #    print(movie_description)
            text_file.write(filter(lambda x: x in printable, movie_description[0]))
        else:
            print("\t\t *** ERROR Omitting")
            text_file.close()
            continue

        # Grabs Synopsis
        synopsis_url = movie_tree.xpath('//div[@id="titleStoryLine"]//span[@class="see-more inline"]//a/@href')[0]
        synopsis_page = requests.get('http://www.imdb.com/'+synopsis_url)
        synopsis_tree = html.fromstring(synopsis_page.content)
        synopsis = ''.join(synopsis_tree.xpath('//ul[@class="ipl-zebra-list"]//li/text()')).lstrip()

        text_file.write('\n'+filter(lambda x: x in printable, synopsis))
        text_file.close()

# Create Testing Set
print("Creating Test Set in: " + test_dir)

all_titles = os.listdir(training_dir)
test_files = random.sample(all_titles, 25)
for i in test_files:
    os.rename(training_dir + i, test_dir + i)
