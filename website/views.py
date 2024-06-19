from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from . import db 
from website.update_checker import *
from website.view_playlist import *
from website.update import *
from website.plex_mgmt import *
import time


views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    return render_template("home.html", user=current_user)

@views.route("/update", methods=['GET', 'POST'])
@login_required
def update():
    if request.method == 'POST':
        playlist_link = request.form['playlist_link']

        if playlist_link:
            if checker(playlist_link):
                update_app(playlist_link)
                time.sleep(5)
                create_playlist()
                flash('Playlist updated!', 'success')
            else:
                flash('Invalid link!', 'error')
        else:
            flash('Error: input is empty', 'error')

    return render_template('update.html', user=current_user)

@views.route("/view_playlist", methods=['GET', 'POST'])
@login_required
def view_playlist():
    dir_list, count_dir = view_dir()
    if request.method == 'POST':
        playlist = request.form['playlist']
        if playlist:
            file_list, count_file = view_file_list(playlist)
            flash('Playlist selected!', 'success')
            return render_template('view_playlist.html', select_list=dir_list, file_list=file_list, count_dir=count_dir, count_file=count_file, user=current_user)

        else:
            flash('Please select playlist!', 'error')


    return render_template('view_playlist.html', select_list=dir_list, count_dir=count_dir, user=current_user)   

