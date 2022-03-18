import os, re, json
from azure.storage.blob import ContainerClient
from wordcloud import WordCloud
import matplotlib.pyplot as plt


connect_str = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
json_container = ContainerClient.from_connection_string(conn_str=connect_str, container_name="json")
final_data = {}
data_science = json.loads(json_container.download_blob("dictionary").content_as_text())
data_filter = list(json_container.download_blob("filter.csv").content_as_text().split("\r"))

for i, word in enumerate(data_filter):
    data_filter[i] = word[1:]

#print(data_science)
#print(data_filter)


#final_data = {data_science for key in data_filter if key in data_science}

# for key in data_science:
#     #print(key)
#     if len(key) > 1 and key in data_filter:
#         #print(key)
#         final_data.update({key: data_science[key]})
# print(final_data)

for key in data_filter:
    if key != "" and key in data_science:
        #print(entry)
        final_data.update({key: data_science[key]})
print(final_data)

word_cloud = {key: value 
                for key, value in final_data.items()
                if value > 0}

final_output_cloud = WordCloud(width = 1920, height = 1080).generate_from_frequencies(word_cloud)

#displays the wordcloud
plt.figure(figsize=(15,8))
plt.imshow(final_output_cloud)
