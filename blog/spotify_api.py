import os
import sys
import base64
from requests import post, get
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

if os.path.isfile(os.path.join(BASE_DIR, 'env.py')):
    import env

CLIENT_ID = os.getenv('CLIENT_ID', '')
CLIENT_SECRET = os.getenv('CLIENT_SECRET', '')

# CREDIT - This video got me started with python based Spotify APIs:
# https://www.youtube.com/watch?v=WAmEZBEeNmg
def get_access_token():
    auth_string = CLIENT_ID + ':' + CLIENT_SECRET
    auth_bytes = auth_string.encode('utf-8')
    auth_base64 = str(base64.b64encode(auth_bytes), 'utf-8')

    url = 'https://accounts.spotify.com/api/token'
    headers = {
        'Authorization': 'Basic ' + auth_base64,
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    data = {'grant_type': 'client_credentials'}
    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    access_token = json_result['access_token']
    return access_token


def get_auth_header(access_token):
    return {'Authorization': 'Bearer ' + access_token}


def search_for_item(access_token, item, params):
    headers = get_auth_header(access_token)
    query_url = f'https://api.spotify.com/v1/search?q={item}&type={params}'
    results = get(query_url, headers=headers)

    if results.status_code == 401:
        access_token = get_access_token()
        return search_for_item(access_token, item, params)
    
    elif results.status_code == 429:
        return 'Spotify API limit is reached, please try again later!'
    
    elif results.status_code != 200:
        return f'Error: {results.status_code}'

    
    json_data = json.loads(results.content)
    json_results = json_data['playlists']['items']        

    all_playlists = []

    for playlist in json_results:
        playlist_id = playlist['id']
        playlist_name = playlist['name']
        playlist_image = playlist['images'][0]['url']

        all_playlists.append(
            {
                'playlist_id': playlist_id,
                'playlist_name': playlist_name,
                'playlist_image': playlist_image,
            }
        )

    return all_playlists
    

# access_token = get_access_token()
# item = 'Rocket League!'
# params = 'playlist,album'
# search_results = search_for_item(access_token, item, params)

# print(search_results)