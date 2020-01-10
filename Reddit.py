import requests
from lxml import html
import sys

image_exts = ['.jpg', '.jpeg', '.gif', '.png']
def is_image(url):
    if any(image_ext in url for image_ext in image_exts):
        return True
    return False

def save_image(image_file, image_name, image_extension):
    directory = args.root_directory + image_name + image_extension
    f = open(directory, 'w')
    f.write(image_file)
    f.close()
    print 'Saving image as ' + directory

def return_links(page): 
    page = requests.get(page)
    if page.status_code == 200:
        page = html.fromstring(page.text)
        urls = page.xpath('//a/@href')
        return urls
    else:
        print 'Bad response from server.'
        sys.exit()

def get_imgur_gallery_links(gallery_address):
    image_urls = []
    gallery = requests.get(gallery_address)
    if gallery.status_code == 200:
        gallery_page = html.fromstring(gallery.text)
        gallery_image_urls = gallery_page.xpath('//div[@class="image textbox "]/a/@href')
        
        gallery_image_urls = ['http:' + i for i in gallery_image_urls]
        return gallery_image_urls
    else:
        print 'Bad response from gallery server.'
        sys.exit()

def return_image_links(page):
    
    page = requests.get(page)
    
    if page.status_code == 200:
        
        page = html.fromstring(page.text)
        
        urls = page.xpath('//p[@class="title"]/a/@href')
        image_urls = []
        for url in urls:
            if is_image(url):
                image_urls.append(url)                      
            else:
                image_urls.extend(get_imgur_gallery_links(url))
        return image_urls 
    else:
        print 'Bad response from reddit server.'
        sys.exit()

def get_top_pics(subreddit):
    urls = return_image_links('http://www.reddit.com/r/' + subreddit + '/top')
    print 'Saving ' + str(len(urls)) + ' images...zzz'
    
    count = 0
    for i in urls:
        while not is_image(i):
            i = i[:-1]
        count += 1
        image_file = requests.get(i)
        filename = 'image-' + str(count)
        if i.endswith('.jpg'):
            save_image(image_file.content, filename, '.jpg')
        elif i.endswith('.jpeg'):
            save_image(image_file.content, filename, '.jpeg')
        elif i.endswith('.gif'):
            save_image(image_file.content, filename, '.gif')
        elif i.endswith('.png'):
            save_image(image_file.content, filename, '.png')

if __name__ == '__main__':
    import argparse
    import os
    
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--directory', type=str, dest='root_directory',
                        default=os.getcwd(), help='Designate desination direcotry for images')
    parser.add_argument('-s', '--subreddit', type=str, dest='subreddit', required=True,
                        help='Designate target subreddit')
    args = parser.parse_args()
    
    if not args.root_directory.endswith('/'):
        args.root_directory += '/'

    get_top_pics(args.subreddit)
