import time
start_time = time.time() #gets start time for later calculation
import random
from bs4 import BeautifulSoup 
import requests
import os
from azure.storage.blob import BlobServiceClient, __version__

try:
    print("Azure Blob Storage v" + __version__ + "working")
except Exception as ex:
    print("Exception:")
    print(ex)
    
connect_str = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
blob_service_client = BlobServiceClient.from_connection_string(connect_str)


container_client = blob_service_client.get_container_client("html")

#adds headers to avoid being flagged as a bot
headers = requests.utils.default_headers()
headers.update({'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',})

#total_sleep = 0 #keeps track of the amount throttled

#sleeps for a 0.00 - 3.00 seconds
def throttle(start):
    global total_sleep
    #print("\r" + 'Time (seconds): ' + str(round((time.time() - start), 2)))
    sleepy_time = round((random.random()*3), 2)
    #total_sleep += sleepy_time
    time.sleep(sleepy_time)

def job_search(position, location):
    global start_time
    jobs = {}
    description = []
    #this section pulls data from indeed for the position/location for the pages in the range and extracts
    #the url from the clickable results for each job post, adding them to the 'jobs' list 
    for page in range(0,50,10): #15 items per page, but page in link iterates by 10 
        url = 'https://www.indeed.com/jobs?q={}&l={}&sort=date&start='.format(position, location)+str(page)
        result = requests.get(url, headers=headers)
        #throttle(start_time)
        content = result.text
        soup = BeautifulSoup(content, 'html.parser')
        #searches the page for links in each post
        for tap_Items in soup.find_all(class_='tapItem'):
            for links in tap_Items.find_all('a', href=True):
                if ('fromjk=' in links['href']):
                    start = links['href'].find('fromjk=') + 4
                    stop = start + 19 #all the links so far have a set length of 19 characters as of 1/10/22
                    job_url = "https://www.indeed.com/viewjob?"+links['href'][start:stop]
                    short_key = links['href'][start+3:stop]
                    #jobs += [job_url, short_key]
                    jobs[short_key] = job_url
                    print(short_key)
                    print(job_url)
                    
                    throttle(start_time)

    
#grabs all text in the job description from every page found above and makes a dictionary of word counts

    for short_key in jobs: #used to be url'
        result = requests.get(jobs[short_key], headers=headers)
        throttle(start_time)
        content = result.text 
        soup = BeautifulSoup(content, 'html.parser')
        description = str(soup.text) #pulls the full text from each job 
        container_client.upload_blob(short_key, description, overwrite=True)
        word_count = ['']

    return word_count

# #runs a job search for data science and one for accounting, and generates a wordcloud from the data unique to the DS search
data_science = job_search('Data Science -analyst -engineer -entry'.replace(' ', '%20'), 'United States')
