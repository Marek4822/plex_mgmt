from plexapi.server import PlexServer
from website.update import *
import os
from website.env import token, url_plex

def create_playlist():
    playlist_path = get_playlist_path()
    print(playlist_path)

    plex = PlexServer(url_plex, token)
    try:
        print("Connected to: " + str(plex.myPlexAccount()))
    except:
        print("Unable to connect!")
        return None

    
    def extract_name(playlist_path):
        prefix = '/home/plex_music/playlists/'
        playlist_name = playlist_path.removeprefix(prefix)

        return playlist_name

    playlist_name = extract_name(playlist_path)


    def check_playlists(plex, playlist_name):
        for playlist in plex.playlists():
            if playlist.title == playlist_name:
                print(playlist.title)
                return True
            
    is_playlist = check_playlists(plex, playlist_name)


    def get_songs_list_dir(playlist_path):
        song_dir_list = []
        for song in os.listdir(playlist_path):
            if song.endswith('.m4a'):
                song = song.replace('.m4a', '')
                song_dir_list.append(song)

        return song_dir_list
    

    def get_songs_list_playlist(plex, playlist_name):
        song_playlist_list = []
        for song in plex.playlist(playlist_name):
            song_playlist_list.append(song.title)

        return song_playlist_list
    


    def songs_diff(song_dir_list, song_playlist_list):
        song_dir_list = sorted(song_dir_list)
        song_playlist_list = sorted(song_playlist_list)
        song_diff_list = []

        for difference in song_dir_list:
            if difference not in song_playlist_list:
                song_diff_list.append(difference)
        
        return song_diff_list


    def create_playlist(plex, is_playlist, playlist_name):
        plex.library.refresh()
        if is_playlist:
            song_to_add_diff = []
            added_titles_diff = set()

            song_dir_list = get_songs_list_dir(playlist_path)
            song_playlist_list = get_songs_list_playlist(plex, playlist_name)
            song_diff_list = songs_diff(song_dir_list, song_playlist_list)
            print(song_diff_list)

            if len(song_diff_list) > 0:
                for song_i in plex.playlist('All Music'):
                    song_title = song_i.title
                    if song_title in song_diff_list and song_title not in added_titles_diff:
                        song_to_add_diff.append(song_i)
                        added_titles_diff.add(song_title)
                        print(f'Song added: {song_i}')

                plex.playlist(playlist_name).addItems(song_to_add_diff)
                print(f'added songs to playlist: {song_to_add_diff}')
            else:
                print('no songs to add')
        else:
            song_dir_list = get_songs_list_dir(playlist_path)
            added_titles_new = set()
            song_to_add_new = []
            print(song_dir_list)
            
            for song_j in plex.playlist('All Music'):
                song_title = song_j.title
                if song_title in song_dir_list and song_title not in added_titles_new:
                    song_to_add_new.append(song_j)
                    added_titles_new.add(song_j.title)
                    print(f'song added {song_j}')

            plex.createPlaylist(playlist_name, items=song_to_add_new)

    create_playlist(plex, is_playlist, playlist_name)
