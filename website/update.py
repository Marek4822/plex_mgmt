from googleapiclient.discovery import build
import os
import re
from website.env import api_key


def update_app(playlist_link):

    def extract_id(playlist_link):
        pattern = r'(?:list=)([a-zA-Z0-9_-]+)'
        match = re.search(pattern, playlist_link)
        if match:
            return match.group(1)
        else:
            return None
        
    def playlist_name(playlist_id):
        youtube = build('youtube', 'v3', developerKey=api_key)
        request = youtube.playlists().list(
        part="snippet",
        id=playlist_id)
        
        response = request.execute()
        data_name = response['items'][0]['snippet']['title']

        return data_name
    

    def format_name(data_name):
        rep = r"-"
        data_name = data_name.replace(" ", rep).replace("'", rep).replace('"', rep)

        return data_name


    def create_dir(playlists_path):
        if not os.path.exists(playlists_path):
            print('Couldnt find a directory, Creating new one')
            os.mkdir(playlists_path)


    def get_playlist(youtube, playlist_id):
        request = youtube.playlistItems().list(
        part="snippet,contentDetails",
        maxResults=50,
        playlistId=playlist_id)

        response = request.execute()

        video_urls = []
        for i in range(len(response['items'])):
            video_urls.append(response['items'][i]['contentDetails']['videoId'])
        
        next_page_token = response.get('nextPageToken')
        more_pages = True

        while more_pages:
            if next_page_token is None:
                more_pages = False
            else:
                request = youtube.playlistItems().list( 
                        part="snippet,contentDetails",
                        maxResults=50,
                        playlistId=playlist_id,
                        pageToken = next_page_token)
                
                response = request.execute()
                for i in range(len(response['items'])):
                    video_urls.append(response['items'][i]['contentDetails']['videoId'])

                next_page_token = response.get('nextPageToken')

        return video_urls


    def get_urls(playlist_path):
        def extract_urls(filename):
            rm_extension = filename.rsplit('.', 1)[0]
            
            match = re.search(r'\[([-\w]+)\]$', rm_extension)
            if match:
                return match.group(1)
            else:
                return None

        video_id_list = []
        for file in os.listdir(playlist_path):
            if file.endswith('.m4a'):
                video_id = extract_urls(file)
                if video_id:
                    video_id_list.append(video_id)
                else:
                    return None
        return video_id_list


    def compare_urls(video_id_list, video_urls):
        playlist_on_disk = sorted(video_id_list)
        playlist_on_yt = sorted(video_urls)

        diff_urls = []
        for diff in playlist_on_yt:
            if diff not in playlist_on_disk:
                diff_urls.append(diff)

        if not diff_urls:
            print('Playlist is up to date')
        else:
            print(f'Missing songs in playlist: {len(diff_urls)}')
        
        return diff_urls


    def save_diff_urls(diff_urls, playlists_path):
        if diff_urls is None:
            diff_urls = []
            return diff_urls 

        urls_list = []

        for video_id in diff_urls:
            url = f"https://www.youtube.com/watch?v={video_id}" 
            urls_list.append(url)

        with open(f'{playlists_path}/diff_urls.txt', 'w') as f:
            for url in urls_list:
                f.write(url + '\n')


    def download(playlists_path):
        os.system(f'cd {playlists_path} && sudo /home/linuxbrew/.linuxbrew/bin/yt-dlp --skip-unavailable-fragments --ignore-errors --continue -R 10 -f 140 -i -a diff_urls.txt')



    # def change_song_name(playlists_path):
    #     for file in os.listdir(playlists_path):
    #         if file.endswith('.m4a'):
    #             os.rename(f'{playlists_path}/{file}', f'{playlists_path}/plex-{file}')
        

    def main():

        # playlists_id = 'PLpid-WNSSQAs01HGVMHSIu0molIRvsjGO'           # playlist id you want to download
        # playlists_path = '/home/marek/python/py_playlist/bangiers'    # place where u store files, destination where files will be saved
                                                                        # only files will be downloaded if there is a difference 
                                                                        # between playlist on yt(playlist_id) and files in your file dir(playlist_path)
    
        
        playlist_id = extract_id(playlist_link)
        data_name = playlist_name(playlist_id)
        dir_name = format_name(data_name)
        youtube = build('youtube', 'v3', developerKey=api_key)
        default_destination = '/home/plex_music/playlists/' # Default destination

        global playlists_path
        playlists_path = f'{default_destination}{dir_name}'
        create_dir(playlists_path)

        count = 0
        retries = True
        while retries:
            if count <= 2:
                video_urls = get_playlist(youtube, playlist_id)
                video_id_list = get_urls(playlists_path)
                diff_urls = compare_urls(video_id_list, video_urls)
                save_diff_urls(diff_urls, playlists_path)
                download(playlists_path)
                count += 1
                print(f'RETRIES: {count}')
            else:
                retries = False

        # change_song_name(playlists_path)
    
    main()

def get_playlist_path():
    return playlists_path

# yt-dlp --skip-unavailable-fragments --ignore-errors --continue -R 10 -f 140 -i -a diff_urls.txt
