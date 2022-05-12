# JobCloudAzure
Rework of the [JobCloud project](https://github.com/botmalka/JobCloud) using Azure blob storage

Part 1: JobScraper scrapes Indeed using BeautifulSoup and reads all posts for data science jobs and uploads that to blob storage. Each job post is stored separately 

Part 2: JobParser takes the blob data for the jobs, takes counts of all words, put them into a dictionary, and stores that info in Azure as json data

Part 3: WordCloud takes the json data from Azure, filters the words found in Filter.csv and outputs word cloud based on the prevalence of those words

an example:

![](https://github.com/botmalka/JobCloudAzure/blob/main/Figure%202022-03-17%20120629.png)
