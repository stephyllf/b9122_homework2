#!/usr/bin/env python
# coding: utf-8

# In[1]:


from bs4 import BeautifulSoup
import urllib.request
#from urllib.request import Request


# In[2]:


seed_url = "https://www.sec.gov/news/pressreleases"


# In[3]:


urls = [seed_url]    #queue of urls to crawl
seen = [seed_url]    #stack of urls seen so far
charges_list = []          #collect pages that contain word "charges"


# In[4]:


maxNumUrl = 20; #set the maximum number of urls to find 'charges'
print("Starting with url="+str(urls))
while len(urls) > 0 and len(charges_list) < maxNumUrl:
    # DEQUEUE A URL FROM urls AND TRY TO OPEN AND READ IT
    try:
        curr_url=urls.pop(0)
        print("num. of URLs in stack: %d " % len(urls))
        print("Trying to access= "+curr_url)
        req = urllib.request.Request(curr_url,headers={'User-Agent': 'Mozilla/5.0'})
        webpage = urllib.request.urlopen(req).read()
        charges_list.append(curr_url)
        if 'charges' in webpage.lower().decode():  # collect pages that contain word "charges"
            charges_list.append(curr_url)

    except Exception as ex:
        print("Unable to access= "+curr_url)
        print(ex)
        continue    #skip code below


# In[5]:


# IF URL OPENS, CHECK WHICH URLS THE PAGE CONTAINS
# ADD THE URLS FOUND TO THE QUEUE url AND seen
soup = BeautifulSoup(webpage)  #creates object soup
# Put child URLs into the stack
for tag in soup.find_all('a', href = True): #find tags with links
    childUrl = tag['href'] #extract just the link
    o_childurl = childUrl
    childUrl = urllib.parse.urljoin(seed_url, childUrl)
    print("seed_url=" + seed_url)
    print("original childurl=" + o_childurl)
    print("childurl=" + childUrl)
    print("seed_url in childUrl=" + str(seed_url in childUrl))
    print("Have we seen this childUrl=" + str(childUrl in seen))
    if seed_url in childUrl and childUrl not in seen:
        print("***urls.append and seen.append***")
        urls.append(childUrl)
        seen.append(childUrl)
    else:
        print("######")

print("num. of URLs seen = %d, and scanned = %d" % (len(seen), len(charges_list)))
print("List of charges URLs:")
for charges_url in charges_list:
    print(charges_url)


# In[ ]:




