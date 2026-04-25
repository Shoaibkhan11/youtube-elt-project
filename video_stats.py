import requests
import json
import os
from dotenv import load_dotenv
from datetime import date,datetime

load_dotenv(dotenv_path='./.env')

api_key=os.getenv("API_KEY")
channel_handle="MrBeast"
max_results=50


def get_playlist_id():
    try:
        url=f"https://youtube.googleapis.com/youtube/v3/channels?part=contentDetails&forHandle={channel_handle}&key={api_key}"

        response=requests.get(url)
        response.raise_for_status()
        #print(response)

        data=response.json()

        #print(json.dumps(data,indent=4))

        channel_playlist_id=data['items'][0]['contentDetails']['relatedPlaylists']['uploads']

        #print(channel_playlist_id)
        return channel_playlist_id
    
    except requests.exceptions.RequestException as e:
        raise e

def get_video_ids(playlist_id):
    
    base_url=f"https://youtube.googleapis.com/youtube/v3/playlistItems?part=contentDetails&maxResults={max_results}&playlistId={playlist_id}&key={api_key}"
    url_for_next_page="https://youtube.googleapis.com/youtube/v3/playlistItems?part=contentDetails&maxResults={max_results}&pageToken={page_token}&playlistId={playlist_id}&key={api_key}"
    video_ids=[]
    page_token=None
    try:
        while True:
            url=base_url
            if page_token:
                url+=f"&pageToken={page_token}"
            response=requests.get(url)
            response.raise_for_status()
            data=response.json()
            for item in data.get('items',[]):
                video_id=item['contentDetails']['videoId']
                video_ids.append(video_id)
            page_token=data.get('nextPageToken')

            if not page_token:
                break
        return video_ids
    except requests.exceptions.RequestException as e:
        raise e



def extract_video_data(video_id_list):
    extracted_data=[]
    def batch_list(video_id_list,batch_size):
        for video_id in range(0,len(video_id_list),batch_size):
            yield video_id_list[video_id : video_id + batch_size]
    
    try:
        for batch in batch_list(video_id_list,max_results):
            video_ids_str=','.join(batch)
            url=f"https://youtube.googleapis.com/youtube/v3/videos?part=contentDetails&part=snippet&part=statistics&id={video_ids_str}&key={api_key}"
            response=requests.get(url)
            response.raise_for_status()
            data=response.json()
            for item in data.get('items',[]):
                id=item['id']
                snippet=item['snippet']
                content_details=item['contentDetails']
                statistics=item['statistics']
                video_data={
                    'video_id':id,
                    'title':snippet.get('title'),
                    'published_at':snippet.get('publishedAt'),
                    'duration':content_details.get('duration'),
                    'view_count':statistics.get('viewCount',None),
                    'like_count':statistics.get('likeCount',None),
                    'comment_count':statistics.get('commentCount',None)
                }
                extracted_data.append(video_data)
        return extracted_data
    except requests.exceptions.RequestException as e:
        raise e

def save_to_json(extracted_data):
    file_path=f'./data/YT_data_{channel_handle}_{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.json'
    with open(file_path,'w',encoding='utf-8') as file_to_write:
        json.dump(extracted_data,file_to_write,indent=4,ensure_ascii=False)

if __name__=="__main__":
    playlist_id=get_playlist_id()
    video_ids=get_video_ids(playlist_id)
    video_data=extract_video_data(video_id_list=video_ids)
    save_to_json(video_data)