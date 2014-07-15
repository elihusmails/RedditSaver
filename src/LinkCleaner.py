
import os, sys
import praw
import urllib2

from GetLinksInComments import scanCommentsForLinks

def get_status_code(url):
    """ This function retreives the status code of a website by requesting
        HEAD data from the host. This means that it only requests the headers.
        If the host cannot be reached or something else goes wrong, it returns
        None instead.
    """
    code = 0
    
    try:
        connection = urllib2.urlopen(url)
        code = connection.getcode()
        connection.close()
    except (urllib2.HTTPError, urllib2.URLError) as e:
        code = 404
    
    return code

if __name__ == '__main__':
    username = sys.argv[1]
    password = sys.argv[2]
    
    r = praw.Reddit(user_agent=username)
    r.login(username, password)
    submissions = r.user.get_saved( limit=1000 )
    
    for s in submissions:
    
        if not hasattr(s, 'url'):
            continue
        
        status = get_status_code(s.url)
        
        if status != 200:
            print s.subreddit
            print s.title
            print s.url
            print "Status = {0}".format(status)
        
            #urls = scanCommentsForLinks( s )
            #for u in urls:
            #    r.submit(sys.argv[3], url=u, title=s.title)
        
            #s.unsave()
        