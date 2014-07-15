
import praw
from markdown.inlinepatterns import LINK_RE
import argparse
import re


def scanCommentsForLinks( submission ):
    
    print submission.title
    print submission.url
    flat_comments = praw.helpers.flatten_tree(submission.comments)
    
    links = []
      
    for comment in flat_comments:
        
        if not isinstance(comment, praw.objects.Comment):
            print "Comment is not an instance of praw.Comment"
            continue
        
#        if no hasattr(comment, 'body'):
#            continue
        
        print 'Author: ' + str(comment.author)
        print 'Comment: ' + comment.body

        urls = re.findall(LINK_RE, comment.body)
        print "URLs = " + str(urls)
        if urls:
            urls = [u[7].strip() for u in urls]
            links.extend(urls)
            
    return links