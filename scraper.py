import requests
from lxml import html

page_directories = {
                    "G": "http://www.imdb.com/search/title?title_type=feature&certificates=US%3Ag&languages=en&count=100", 
                    "PG" : "http://www.imdb.com/search/title?title_type=feature&certificates=US%3Apg&languages=en&count=100", 
                    "PG-13" : "http://www.imdb.com/search/title?title_type=feature&certificates=US%3Apg_13&languages=en&count=100", 
                    "R": "http://www.imdb.com/search/title?title_type=feature&certificates=US%3Ar&languages=en&count=100", 
                    "NC-17": "http://www.imdb.com/search/title?title_type=feature&certificates=US%3Anc_17&languages=en&count=100"
                    }

for key in page_directories.keys():
    print("Grabbing URL List - " + key)
    webpage = requests.get(page_directories[key])
    tree = html.fromstring(webpage.content)

    urls = tree.xpath('//h3[@class="lister-item-header"]//a/@href')
    titles = tree.xpath('//h3[@class="lister-item-header"]//a/text()')

    for i in range(0,len(urls)):
        print("\tGrabbing - " + titles[i]);
        text_file = open("Training/"+key+ "-" + titles[i] + ".txt", "w")
        
        # Writes movies title
        text_file.write(titles[i])

        # Grabs description
        movie_page = requests.get('http://www.imdb.com/'+urls[i])
        movie_tree = html.fromstring(movie_page.content)
        movie_description = movie_tree.xpath('//div[@itemprop="description"]//p/text()')
        text_file.write(movie_description[0])

        # Grabs Synopsis
        synopsis_url = movie_tree.xpath('//div[@id="titleStoryLine"]//span[@class="see-more inline"]//a/@href')[0]
        synopsis_page = requests.get('http://www.imdb.com/'+synopsis_url)
        synopsis_tree = html.fromstring(synopsis_page.content)
        synopsis = ''.join(synopsis_tree.xpath('//ul[@class="ipl-zebra-list"]//li/text()')).lstrip()
        text_file.write('\n'+synopsis)
        text_file.close()






