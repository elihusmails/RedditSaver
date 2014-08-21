
from urlparse import urlparse
from posixpath import basename
import os, sys
import requests
import praw
import praw.errors
from imguralbum import ImgurAlbumDownloader
from imguralbum import ImgurAlbumException
from pprint import pprint
from urlparse import urlparse
from markdown.inlinepatterns import LINK_RE
import argparse
import re


def get_comments(submission, limit=None, threshold=0):
    submission.replace_more_comments(limit=limit, threshold=threshold)
    return praw.helpers.flatten_tree(submission.comments)

def extract_urls(md):
    urls = re.findall(LINK_RE, md)
    if urls:
        urls = [u[7].strip() for u in urls]

    return urls

def scanCommentsForLinks( submission ):
    
    print submission.title
    print submission.url
#     flat_comments = praw.helpers.flatten_tree(submission.comments)
    comments = get_comments(submission)
    
    links = []
      
    for comment in comments:
        
        if not isinstance(comment, praw.objects.Comment):
            print "Comment is not an instance of praw.Comment"
            continue
        
#        if no hasattr(comment, 'body'):
#            continue
        
#         print 'Author: ' + str(comment.author)
        print 'Comment: ' + comment.body

        # First pass.  This will process the comment using markdown
        urls = extract_urls(comment.body)
        links.extend(urls)
        
        # Second pass.  Just look for "http://" in the comment
        text = comment.body.split()
        for word in text:
            if 'http://' in word:
                links.append(word)
                
    print "Links = " + str(links)
    return links

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

    r = praw.Reddit(user_agent=username)
    r.config._ssl_url = None
    r.login(username, password)
    submissions = r.user.get_saved( limit=1000 )
    
    for s in submissions:

        #print s.subreddit
        #print dir(s)

        if not hasattr(s, 'url'):
            continue

        if 'imgur.com' in s.url:
            print 'Found a match ' + s.url
            theUrl = s.url.encode('ascii','ignore')
            
            if theUrl.endswith('.jpg') or theUrl.endswith('.gif') or theUrl.endswith('.png') or theUrl.endswith('jpeg'):
                
                path = username + '/' + str(s.subreddit)
                downloadImage( s.url, path )
            else:
                
                path = username + '/' + str(s.subreddit)
                
                try:
                    downloader = ImgurAlbumDownloader(s.url)
                    downloader.save_images(path)
                except ImgurAlbumException:
                    downloadImage( s.url+'.jpg', path )
            
            urls = scanCommentsForLinks( s )
            print urls
            for u in urls:
                try:
                    r.submit(sys.argv[3], url=u, title=s.title)
                except praw.errors.APIException:
                    print "Most likely an invalid URL"
                except praw.errors.AlreadySubmitted:
                    print "Link already submitted"
            #s.unsave()
            
