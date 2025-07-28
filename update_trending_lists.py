import os
import json
import datetime
import requests

# FOR LOCAL TESTING
#print("Loading API key")
#with open('.env/api_key', 'r') as fd:
#    YT_API_KEY = fd.read().strip()
#
#print("API key loaded")

# first argument is right after script name
YT_API_KEY = os.environ.get('API_KEY')


print("Retreiving trending data...")

vid_list = list()

headers = {'Content-Type': 'application/json', 'X-goog-api-key': YT_API_KEY}
PARAMS = {'part': 'snippet', 'chart': 'mostPopular', 'regionCode': 'US'}
response = requests.get('https://youtube.googleapis.com/youtube/v3/videos', headers=headers, params=PARAMS)

if response.status_code != 200:
    raise Exception(str(response.json()))

data = response.json()
items = data["items"]
for vid in items:
    vid_list.append({'id': vid["id"], 
                    'title': vid["snippet"]["title"], 
                    'channel': vid["snippet"]["channelTitle"],
                    'categoryId': vid["snippet"]["categoryId"],
                    'thumbnail': vid["snippet"]["thumbnails"]["high"]["url"]})

while data.get('nextPageToken'):
    PARAMS['pageToken'] = data['nextPageToken']
    response = requests.get('https://youtube.googleapis.com/youtube/v3/videos', headers=headers, params=PARAMS)

    if response.status_code != 200:
        raise Exception(str(response.json()))

    data = response.json()
    items = data["items"]
    for vid in items:
        vid_list.append({'id': vid["id"], 
            'title': vid["snippet"]["title"], 
            'channel': vid["snippet"]["channelTitle"],
            'categoryId': vid["snippet"]["categoryId"],
            'thumbnail': vid["snippet"]["thumbnails"]["high"]["url"]})


print("Finished retreiving trending data")


print("Generating trending pages...")
with open('docs/trending/US.md', 'w') as fd:
    fd.write("# YT Trending - US\n\n\n")
    fd.write("Last updated " + datetime.datetime.utcnow().ctime() + " UTC\n\n")
    for vid in vid_list:
        vid_url = "https://www.youtube.com/watch?v=" + vid['id']
        vid_img = '[![' + vid['title'] + '](' + vid['thumbnail'] + ')](' + vid_url + ')'
        vid_title = '##[' + vid['title'] + '](' + vid_url +')'
        # fd.write(vid['id'] + "\n")
        
        fd.write(vid_img + "\n")
        fd.write(vid_title + "\n\n")
        fd.write('by ' + vid['channel'] + "\n\n")
        fd.write('---\n')
        fd.write("\n\n")


print("Finished generating trending pages")
