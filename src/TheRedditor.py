
from urlparse import urlparse
from posixpath import basename
import os, sys
import requests
from praw import Reddit
from imguralbum import ImgurAlbumDownloader
from imguralbum import ImgurAlbumException
def downloadImage( url, username ):
        
    o = urlparse(url)
    filename = basename(o.path)
    
    r = requests.get(url)
    
    if not os.path.exists(username):
        os.makedirs(username)
    
    thefile = username+'/'+filename
    f = open(thefile, 'w')
    f.write(r.content)
    f.close()

if __name__ == '__main__':
    username = sys.argv[1]
    password = sys.argv[2]

    r = Reddit(user_agent=username)
    r.login(username, password)
    submissions = r.user.get_saved( limit=1000 )
    
    for s in submissions:

        if 'imgur.com' in s.url:
            print 'Found a match ' + s.url
            theUrl = s.url.encode('ascii','ignore')
            
            if theUrl.endswith('.jpg') or theUrl.endswith('.gif'):
                downloadImage( s.url, username )
            else:
                try:
                    downloader = ImgurAlbumDownloader(s.url)
                    downloader.save_images(username)
                except ImgurAlbumException:
                    downloadImage( s.url+'.jpg', username )
                
            s.unsave()
            
