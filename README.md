# musicWebWith0css
this is django web project without any style, so that everyone can apply their style.css to it with ease

simple music web server

if no database:
clone to local - python manage.py runserver - Ctrl+C - python manage.py  makemigrations - python manage.py  migrate

if yes:
clone to local - python manage.py runserver

========================================================================================================================================================================================
first page:
showing albums and song

in the detail page of albums and songs:
  albums_detail page:
    songs that in the albums
  song_detail page:
    song details and playable song access

in create album page:
  form: artist , name of album , and cover of the album(optional)
in upload song page:
  form: artist , title of the song , upload file ,  and cover of the album(optional)
  
in user page:
  access of both editing pages of albums and songs
  delete method of both albums and songs
