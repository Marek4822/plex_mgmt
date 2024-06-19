import os

def view_file_list(playlist):
    path = f'/home/plex_music/playlists/{playlist}'
    file_list = []
    count_file = 0
    for file in os.listdir(path):
        if file.endswith('m4a'):
            file_list.append(file)
            count_file += 1

    return file_list, count_file

def view_dir():
    path = '/home/plex_music/playlists'
    dir_list = []
    dirs = os.listdir(path)
    count_dir = 0
    for dir_name in dirs:
        dir_path = os.path.join(path, dir_name) 
        if os.path.isdir(dir_path):  
            dir_list.append(dir_name)
            count_dir += 1
    
    return dir_list, count_dir

