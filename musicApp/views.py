from django.shortcuts import render, redirect, get_object_or_404
from .models import Album, Song,Like
from django.contrib.auth.decorators import login_required
from .forms import SongForm,AlbumForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout


def upload_song(request):
    if request.method == 'POST':
        form = SongForm(request.POST, request.FILES)
        if form.is_valid():
            album_list = form.cleaned_data['albums']
            # Save the song object and assign the selected albums to it
            song = form.save(commit=False)
            song.uploader = request.user
            song.save()
            song.albums.set(album_list)
            song.save()
            return redirect('music_index')
    else:
        form = SongForm()
    return render(request, 'music_upload.html', {'form': form})

def music_index(request):
    query = request.GET.get('q')
    if query:
        albums = Album.objects.filter(album_title__icontains=query)
        songs = Song.objects.filter(title__icontains=query)
    else:
        albums = Album.objects.all()
        songs = Song.objects.all()
    return render(request, 'music_index.html', {'albums': albums, 'songs': songs})

def create_album(request):
    if request.method == 'POST':
        form = AlbumForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('music_index')
    else:
        form = AlbumForm()
    return render(request, 'create_album.html', {'form': form})

def album_detail(request, album_id):
    album_id = album_id
    album = Album.objects.get(id=album_id)
    #get songs that have the Album as model
    songs = Song.objects.filter(albums=album_id)
    return render(request, 'album_detail.html', {'album': album, 'songs': songs})

def like_song(request, song_id):
    song = get_object_or_404(Song, id=song_id)
    Like.objects.create(user=request.user, song=song)
    return redirect('song_detail', song_id=song_id)

def unlike_song(request, song_id):
    song = get_object_or_404(Song, id=song_id)
    Like.objects.filter(user=request.user, song=song).delete()
    return redirect('song_detail', song_id=song_id)

def song_detail(request, song_id):
    song = get_object_or_404(Song, id=song_id)
    user = request.user
    is_liked = False

    if request.method == 'POST':
        like, created = Like.objects.get_or_create(Song=song, user=user)
        if not created:
            like.delete()
            is_liked = False
        else:
            is_liked = True
    
    context = {
        'song': song,
        'is_liked': is_liked,
    }

    return render(request, 'song_detail.html', context)


#song edit or delete page
def song_edit(request, song_id):
    song = Song.objects.get(id=song_id)
    if request.method == 'POST':
        form = SongForm(request.POST, request.FILES, instance=song)
        if form.is_valid():
            form.save()
            return redirect('music_index')
    else:
        form = SongForm(instance=song)
    return render(request, 'song_edit.html', {'form': form})

#song delete confirm page
def song_delete(request, song_id):
    song = get_object_or_404(Song, id=song_id)
    if request.method == 'POST':
        song.delete()
        return redirect('music_index')
    return render(request, 'song_delete.html', {'song': song})

#album edit
def album_edit(request, album_id):
    album = Album.objects.get(id=album_id)
    if request.method == 'POST':
        form = AlbumForm(request.POST, request.FILES, instance=album)
        if form.is_valid():
            form.save()
            return redirect('music_index')
    else:
        form = AlbumForm(instance=album)
    return render(request, 'album_edit.html', {'form': form})

#album delete
def album_delete(request, album_id):
    album = get_object_or_404(Album, id=album_id)
    if request.method == 'POST':
        album.delete()
        return redirect('music_index')
    return render(request, 'album_delete.html', {'album': album})


# user page show albums and songs user uploaded
def user_page(request, user_id):
    user = User.objects.get(id=user_id)
    albums = Album.objects.filter(uploader=user_id)
    songs = Song.objects.filter(uploader=user_id)
    likes = Like.objects.filter(user=user_id)
    return render(request, 'user_page.html', {'user': user, 'albums': albums, 'songs': songs, 'likes': likes})