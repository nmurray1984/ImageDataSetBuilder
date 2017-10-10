from bs4 import BeautifulSoup
import requests
import re
import urllib3
import os
import argparse
import sys
import json

# adapted from http://stackoverflow.com/questions/20716842/python-download-images-from-google-image-search
# source URL https://gist.github.com/genekogan/ebd77196e4bf0705db51f86431099e57

# Disable insecure request warning - see https://stackoverflow.com/a/28002687
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_soup(url,header):
    http = urllib3.PoolManager()
    response = http.request('GET', url,headers=header)
    return BeautifulSoup(response.data,'html.parser')

def main(args):
    parser = argparse.ArgumentParser(description='Scrape Google images')
    parser.add_argument('-s', '--search', default='bananas', type=str, help='search term')
    parser.add_argument('-n', '--num_images', default=10, type=int, help='num images to save')
    parser.add_argument('-d', '--directory', default='images', type=str, help='save directory')
    args = parser.parse_args()
    query = args.search#raw_input(args.search)
    max_images = args.num_images
    save_directory = args.directory
    image_type="Action"
    query= query.split()
    query='+'.join(query)
    url="https://www.google.co.in/search?q="+query+"&source=lnms&tbm=isch"
    header={'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"}
    soup = get_soup(url,header)
    ActualImages=[]# contains the link for Large original images, type of  image
    for a in soup.find_all("div",{"class":"rg_meta"}):
        link , Type =json.loads(a.text)["ou"]  ,json.loads(a.text)["ity"]
        ActualImages.append((link,Type))
    for i , (img , Type) in enumerate( ActualImages[0:max_images]):
        #try:
            path = os.path.join(save_directory , "img" + "_"+ str(i)+".jpg")
            http = urllib3.PoolManager()
            print(img)
            r = http.request('GET', img,headers=header, preload_content=False)
            with open(path, 'wb') as out:
                while True:
                    data = r.read(2048)
                    if not data:
                        break
                    out.write(data)
            r.release_conn()
        #except Exception as e:
        #    print("could not load : "+img)
        #    print(e)

if __name__ == '__main__':
    from sys import argv
    try:
        main(argv)
    except KeyboardInterrupt:
        pass
    sys.exit()