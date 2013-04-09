
from pprint import pprint
import requests
import json
import time
from urlparse import urlparse
from posixpath import basename
import os, sys

def login(username, password):
    """logs into reddit, saves cookie"""
 
    print 'begin log in'
    UP = {'user': username, 'passwd': password, 'api_type': 'json',}
    
    #POST with user/pwd
    client = requests.session()
 
    r = client.post('http://www.reddit.com/api/login', data=UP)
    
    #print r.text
    #print r.cookies
 
    #gets and saves the modhash
    j = json.loads(r.text)
 
    #client.modhash = j['json']['data']['modhash']
    #print '{USER}\'s modhash is: {mh}'.format(USER=username, mh=client.modhash)
    client.user = username

    def name():
        return '{}\'s client'.format(username)
 
    #pp2(j)
 
    return client
 
def getUserSaves( client, username, limit=100, after='' ):
    
    url = 'http://www.reddit.com/user/{u}/saved/.json'.format(u=username)
    parameters = {'limit': limit,}
    parameters['after'] = after
    
    r = client.get(url,params=parameters)
    j = json.loads(r.text)
    for link in j['data']['children']:
        
        location = link['data']['url']
        if 'imgur' in location:
            print link['data']['title']
            downloadImage(location, username)
        
    after = j['data']['after']
    #print 'After = {AFTER}'.format(AFTER=after)
    #pprint(j)
    
    if after is not None:
        getUserSaves(client, username, limit, after)
    
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
    
    r = requests.get(r'http://www.reddit.com/user/{u}/about/.json'.format(u=username))
    j = json.loads(r.text)  #turn the json response into a python dict
    #pprint(j)  #here's the final respone, printed out nice an readable format
    
    ##thetime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(j['data']['created']))
    ##print 'Account created on {TIME}'.format(TIME=thetime)
    
    client = login(username,password)
    #j = subredditInfo( client, limit=1, sr='programming' )
    #pprint(j)
    
    getUserSaves(client, username, after='')
    
