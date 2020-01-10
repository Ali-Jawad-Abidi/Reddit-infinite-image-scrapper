import requests
import shutil
import json
import sys


#download handler once the url to image has been extracted
def downloadUrl(url , name):
	response=requests.get(url, stream=True)
	with open(name, 'wb') as f:
		for chunk in response.iter_content(chunk_size=1024): 
			    if chunk: # filter out keep-alive new chunks
				f.write(chunk)


urls=[]
"""
PrettyGirls


https://gateway.reddit.com/desktopapi/v1/subreddits/prettygirls?rtj=only&redditWebClient=web2x&app=web2x-client-production&after=t3_byea6s&dist=25&layout=card&sort=hot&allow_over18=1&include=prefsSubreddit"""


headers={'Host': 'gateway.reddit.com',
'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0',
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
'Accept-Language': 'en-US,en;q=0.5',
'Cookie':'',
'Connection': 'keep-alive',
'Upgrade-Insecure-Requests': '1'
}

ext=""
after=""
#change the proxies as you see fit or dont use at all
http_proxy  = "http://95.88.192.108:3128"
https_proxy = "https://95.88.192.108:3128"
#ftp_proxy   = "ftp://10.10.1.10:3128"

proxyDict = { 
              "http"  : http_proxy, 
              "https" : https_proxy
            }
subreddit=sys.argv[2];


if sys.argv[1]=="Reddit":
	new_url="https://gateway.reddit.com/desktopapi/v1/subreddits/"+subreddit+"?dist=25&layout=card&sort=hot&allow_over18=1&include=prefsSubreddit"
	for i in range(0,5):
		p=requests.get(new_url,headers=headers,proxies=proxyDict)
		s=json.loads(p.text)				
		for posts in s["posts"]:
			try:
				try:
					url = s["posts"][posts]["source"]["url"]
				except:
					url=s["posts"][posts]["preview"]["url"]					
			except:
				continue
			
			name = (s["posts"][posts]["title"]).replace(" ","").split("/")[0]
			downloadUrl(url,name)
		after=s["postIds"][-1]
		new_url="https://gateway.reddit.com/desktopapi/v1/subreddits/UHDnsfw?after="+after+"&dist=25&layout=card&sort=hot&allow_over18=1&include=prefsSubreddit"

else:
	new_url="https://9gag.com/v1/group-posts/group/funny/type/hot?"
	for i in range(0,1):
		p=requests.get(new_url)#,headers=headers)
		s=json.loads(p.text)		
		for posts in s["data"]["posts"]:
			if(posts["type"]=="Photo"):
				ext=".jpg"
				url=posts["images"]["image700"]["url"]
			elif(posts["type"]=="Animated"):
				ext=".mp4"
				url=posts["images"]["image460sv"]["url"]
			name=(posts["title"]).replace(" ","")+ext
			
			downloadUrl(url,name)



			urls.append(str((posts["images"]["image700"]["url"]).split("/")[-1].split("_")[0]))
		new_url="https://9gag.com/v1/group-posts/group/nsfw/type/hot?"
		new_url+=s["data"]["nextCursor"]
#print urls
