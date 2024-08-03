#  VKMusix — VK Music API Client Library for Python
#  Copyright (C) 2024—present to4no4sv <https://github.com/to4no4sv/VKMusix>
#
#  This file is part of VKMusix.
#
#  VKMusix is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  VKMusix is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with VKMusix. If not, see <http://www.gnu.org/licenses/>.

import re

from .config import VK
from .utils.another import unixToDatetime


class Artist:
    """
    Класс, представляющий артиста.

    Атрибуты:
        nickname (str): псевдоним артиста.\n
        photo (dict, optional): словарь с размерами и URL фотографий артиста, отсортированный по размеру.\n
        albums (list[Album], optional): список альбомов артиста, представленных объектами класса Album.\n
        tracks (list[Track], optional): список треков артиста, представленных объектами класса Track.\n
        id (str): идентификатор артиста.\n
        url (str): URL страницы артиста.
    """

    def __init__(self, artist: dict) -> None:
        self.nickname = artist.get("name")

        photo = artist.get("photo")
        if photo:
            photoDict = {f"{photo.get('width')}": re.sub(r"\.(j|jp|jpg)$", "", photo.get("url")[:photo.get("url").rfind("&c_uniq_tag=")]) for photo in photo}
            self.photo = dict(sorted(photoDict.items(), key=lambda item: (int(item[0]))))

        else:
            photo = artist.get("photos")
            if photo:
                photoDict = {f"{photo.get('width')}": photo.get("url") for photo in photo[0]["photo"]}
                self.photo = dict(sorted(photoDict.items(), key=lambda item: (int(item[0]))))

        albums = artist.get("albums")
        if albums:
            self.albums = [Album(album) for album in albums]

        tracks = artist.get("tracks")
        if tracks:
            self.tracks = [Track(track) for track in tracks]

        if self.nickname != "Various Artists":
            self.id = artist.get("id")
            domain = artist.get("domain")
            self.url = VK + "artist/" + (domain if domain else self.id)


class Album:
    """
    Класс, представляющий альбом.

    Атрибуты:
        title (str): название альбома.\n
        subtitle (str, optional): подзаголовок альбома, если он присутствует.\n
        description (str, optional): описание альбома, если оно присутствует.\n
        artists (list[Artist]): список основных артистов альбома, представленных объектами класса Artist.\n
        featuredArtists (list[Artist], optional): список приглашённых артистов альбома, представленных объектами класса Artist.\n
        releaseYear (int, optional): год выпуска альбома.\n
        genres (list[Genre], optional): список жанров альбома, представленных объектами класса Genre.\n
        plays (int, optional): количество прослушиваний альбома.\n
        uploadedAt (datetime, optional): дата и время загрузки альбома.\n
        updatedAt (datetime, optional): дата и время последнего обновления информации об альбоме.\n
        photo (dict, optional): словарь с размерами и URL фотографий альбома, отсортированный по размеру.\n
        tracks (list[Track], optional): список треков альбома, где каждый трек представлен объектом класса Track.\n
        exclusive (bool, optional): флаг, указывающий, является ли альбом эксклюзивным.\n
        ownerId (str): идентификатор владельца альбома.\n
        albumId (str): идентификатор альбома.\n
        id (str): комбинированный идентификатор в формате "ownerId_albumId".\n
        url (str): URL страницы альбома.
    """

    def __init__(self, album: dict, playlist: bool = False) -> None:
        title = album.get("title")
        if title:
            self.title = title
        subtitle = album.get("subtitle")
        if subtitle:
            self.subtitle = subtitle

        description = album.get("description")
        if description:
            self.description = description

        mainArtists = album.get("main_artists")
        if mainArtists:
            self.artists = [Artist(mainArtist) for mainArtist in mainArtists]

        featuredArtists = album.get("featured_artists")
        if featuredArtists:
            self.featuredArtists = [Artist(featuredArtist) for featuredArtist in featuredArtists]

        releaseYear = album.get("year")
        if releaseYear:
            self.releaseYear = releaseYear

        genres = album.get("genres")
        if genres:
            for index, genre in enumerate(genres):
                genres[index] = Genre(genre)
            self.genres = genres

        plays = album.get("plays")
        if plays:
            self.plays = plays

        uploadedAt = album.get("create_time")
        if uploadedAt:
            self.uploadedAt = unixToDatetime(uploadedAt)

        updatedAt = album.get("update_time")
        if updatedAt:
            self.updatedAt = unixToDatetime(updatedAt)

        photo = album.get("photo")
        if not photo:
            photo = album.get("thumb")

        if photo:
            self.photo = {key.split("_")[1]: value[:value.rfind("&c_uniq_tag=")] for key, value in photo.items() if key.startswith("photo_")}

        original = album.get("original")
        if original:
            self.original = Album(original)

        tracks = album.get("tracks")
        if tracks:
            self.tracks = tracks

        exclusive = album.get("exclusive")
        if exclusive is not None:
            self.exclusive = exclusive

        self.ownerId = album.get("owner_id")
        if not playlist:
            self.albumId = album.get("id") or album.get("playlist_id")
            self.id = f"{self.ownerId}_{self.albumId}"
            self.url = VK + "music/album/" + self.id

        else:
            self.playlistId = album.get("id")
            self.id = f"{self.ownerId}_{self.playlistId}"
            self.url = VK + "music/playlist/" + self.id


class Track:
    """
    Класс, представляющий трек.

    Атрибуты:
        title (str): название трека.\n
        subtitle (str, optional): подзаголовок трека, если он присутствует.\n
        artists (list[Artist], optional): список основных артистов трека, представленных объектами класса Artist.\n
        artist (Artist, optional): основной артист трека, если список артистов отсутствует.\n
        featuredArtists (list[Artist], optional): список приглашённых артистов трека, представленных объектами класса Artist.\n
        genre (Genre, optional): жанр трека, представленный объектом класса Genre.\n
        explicit (bool, optional): флаг, указывающий, есть ли в треке ненормативная лексика.\n
        duration (int): продолжительность трека в секундах.\n
        fileUrl (str, optional): ссылка на MP3-файл.\n
        lyrics (str, optional): текст трека.\n
        hasLyrics (bool, optional): имеет ли трек текст.\n
        uploadedAt (datetime, optional): дата и время загрузки трека.\n
        album (Album, optional): альбом, к которому принадлежит трек, представленный объектом класса Album.\n
        ownerId (str): идентификатор владельца трека.\n
        trackId (str): идентификатор трека.\n
        id (str): комбинированный идентификатор в формате "ownerId_trackId".\n
        url (str): URL страницы трека.
    """

    def __init__(self, track: dict) -> None:
        self.title = track.get("title")
        subtitle = track.get("subtitle")
        if subtitle:
            self.subtitle = subtitle

        mainArtists = track.get("main_artists")
        if mainArtists:
            self.artists = [Artist(mainArtist) for mainArtist in mainArtists]

        else:
            self.artist = track.get("artist")

        featuredArtists = track.get("featured_artists")
        if featuredArtists:
            self.featuredArtists = [Artist(featuredArtist) for featuredArtist in featuredArtists]

        genreId = track.get("genre_id")
        if genreId:
            self.genre = Genre(genreId=genreId)

        explicit = track.get("is_excplicit")
        if explicit is not None:
            self.explicit = explicit

        self.duration = track.get("duration")

        fileUrl = track.get("url")
        if fileUrl:
            self.fileUrl = fileUrl[:fileUrl.rfind("?siren=1")]

        lyrics = track.get("lyrics")
        if lyrics:
            self.lyrics = lyrics

        else:
            hasLyrics = track.get("has_lyrics")
            if hasLyrics is not None:
                self.hasLyrics = hasLyrics

        uploadedAt = track.get("date")
        if uploadedAt:
            self.uploadedAt = unixToDatetime(uploadedAt)

        album = track.get("album")
        if album:
            self.album = Album(album)

        licensed = track.get("is_licensed")
        if licensed is not None:
            self.licensed = licensed

        self.ownerId = track.get("owner_id")
        self.trackId = track.get("id")
        self.id = f"{self.ownerId}_{self.trackId}"

        releaseAudioId = track.get("release_audio_id")
        self.url = VK + "audio" + (self.id if not releaseAudioId else releaseAudioId)


class Playlist:
    """
    Класс, представляющий плейлист.

    Атрибуты:
        title (str): название плейлиста.\n
        subtitle (str, optional): подзаголовок плейлиста, если он присутствует.\n
        description (str, optional): описание плейлиста, если оно присутствует.\n
        plays (int, optional): количество прослушиваний плейлиста.\n
        createdAt (datetime, optional): дата и время создания плейлиста.\n
        updatedAt (datetime, optional): дата и время последнего добавления аудиотрека в плейлист (или удаления из него).\n
        photo (dict, optional): словарь с размерами и URL фотографий плейлиста, отсортированный по размеру.\n
        tracks (list[Track], optional): список треков альбома, где каждый трек представлен объектом класса Track.\n
        ownerId (str): идентификатор владельца плейлиста.\n
        playlistId (str): идентификатор плейлиста.\n
        id (str): комбинированный идентификатор в формате "ownerId_playlistId".\n
        url (str): URL страницы плейлиста.
    """

    def __init__(self, playlist: dict, isOwn: bool = False) -> None:
        title = playlist.get("title")
        if title:
            self.title = title
        subtitle = playlist.get("subtitle")
        if subtitle:
            self.subtitle = subtitle

        description = playlist.get("description")
        if description:
            self.description = description

        plays = playlist.get("plays")
        if plays:
            self.plays = plays

        createddAt = playlist.get("create_time")
        if createddAt:
            self.createdAt = unixToDatetime(createddAt)

        updatedAt = playlist.get("update_time")
        if updatedAt:
            self.updatedAt = unixToDatetime(updatedAt)

        photo = playlist.get("photo")
        if not photo:
            photo = playlist.get("thumb")

        if photo:
            self.photo = {key.split("_")[1]: value[:value.rfind("&c_uniq_tag=")] for key, value in photo.items() if key.startswith("photo_")}

        original = playlist.get("original")
        if original:
            self.original = Playlist(original)

        tracks = playlist.get("tracks")
        if tracks:
            self.tracks = tracks

        self.ownerId = playlist.get("owner_id")
        self.playlistId = playlist.get("id") or playlist.get("playlist_id")
        self.id = f"{self.ownerId}_{self.playlistId}"
        self.url = VK + "music/playlist/" + self.id

        self.own = isOwn


trackGenres = {
    1: "Рок",
    2: "Поп",
    3: "Рэп и Хип-хоп",
    4: "Расслабляющая",
    5: "House и Танцевальная",
    6: "Инструментальная",
    7: "Метал",
    8: "Дабстеп",
    10: "Drum & Bass",
    11: "Транс",
    12: "Шансон",
    13: "Этническая",
    14: "Акустическая",
    15: "Регги",
    16: "Классическая",
    17: "Инди-поп",
    18: "Другая",
    19: "Скит",
    21: "Альтернатива",
    22: "Электро-поп и Диско",
    1001: "Джаз и Блюз"
}


class Genre:
    """
    Класс, представляющий жанр трека или альбома.

    Атрибуты:
        title (str): название жанра.\n
        id (str): идентификатор жанра.\n
    """

    def __init__(self, genre: dict = None, genreId: int = None) -> None:
        if genreId:
            self.title = trackGenres.get(genreId, "Неизвестен")

            self.id = genreId

        else:
            self.title = genre.get("name")

            self.id = genre.get("id")
