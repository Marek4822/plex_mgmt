def checker(playlist_link):
    base_url = "https://www.youtube.com/playlist?list="
    if playlist_link.startswith(base_url):
        playlist_id = playlist_link[len(base_url):]
        if playlist_id:
            return True
    return False