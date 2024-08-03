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

from typing import Type, Union, List

from ..models import Artist, Album, Track, Playlist
from ..config import VK, headers, playlistsPerReq, playlistsOwnerId


class Get:
    def get(self, ownerId: int, trackId: int, includeLyrics: bool = False) -> Union[Track, dict]:
        """
        Получает информацию об аудиотреке по его идентификатору.

        Пример использования:\n
        result = client.get(ownerId=474499244, trackId=456638035, includeLyrics=True)\n
        print(result)

        :param ownerId: идентификатор владельца аудиотрека (пользователь или группа). (int)
        :param trackId: идентификатор аудиотрека, информацию о котором необходимо получить. (int)
        :param includeLyrics: флаг, указывающий, необходимо ли включать текст трека в ответ. (bool, по умолчанию `False`)
        :return: информация об аудиотреке в виде объекта модели `Track` или словаря.
        """

        id = f"{ownerId}_{trackId}"

        tasks = [self._VKReq("getById", {"audios": id})]

        if includeLyrics:
            tasks.append(self._VKReq("getLyrics", {"audio_id": id}))

        track = tasks[0]
        if not track:
            return self._raiseError("trackNotFound")

        if includeLyrics:
            lyrics = tasks[1]
            if not lyrics.get("error"):
                lyrics = lyrics.get("lyrics")

                timestamps = lyrics.get("timestamps")
                if timestamps:
                    lyrics = [line.get("line") for line in timestamps]

                else:
                    lyrics = lyrics.get("text")

                track["lyrics"] = "\n".join(lyrics)

        return self._finalizeResponse(track, Track)


    def getTracks(self, groupId: int = None) -> Union[List[Union[Track, dict]], Track, dict, None]:
        """
        Получает треки пользователя или группы по его (её) идентификатору. (Временно не работает)

        Пример использования:\n
        result = client.getTracks(groupId=-215973356)\n
        print(result)

        :param groupId: идентификатор пользователя или группы. (int, по умолчанию текущий пользователь)
        :return: список аудиотреков в виде объектов класса `Track` или словарей, аудиотрек в виде объекта модели `Track` (если он единственный), или `None` (если треки отсутствуют).
        """

        if not groupId:
            groupId = self.getSelf().get("id")

        tracks = self._client.sendReq(VK + "audios" + str(groupId), cookies=self._cookies if hasattr(self, "_cookies") else None, headers=headers, responseType="code")
        tracks = self._getTracks(tracks)

        return tracks


    def getArtist(self, artistId: int, includeAlbums: bool = False, includeTracks: bool = False) -> Union[Artist, dict]:
        """
        Получает информацию об артисте по его идентификатору.

        Пример использования:\n
        result = client.getArtist(artistId=5696274288194638935, includeAlbums=True, includeTracks=True)\n
        print(result)

        :param artistId: идентификатор артиста, информацию о котором необходимо получить. (int)
        :param includeAlbums: флаг, указывающий, необходимо ли включать альбомы артиста в ответ. (bool, по умолчанию `False`)
        :param includeTracks: флаг, указывающий, необходимо ли включать треки артиста в ответ. (bool, умолчанию `False`)
        :return: информация об артисте в виде объекта модели `Artist` или словаря.
        """

        params = {"artist_id": artistId}

        tasks = [self._VKReq("getArtistById", params)]

        if includeAlbums:
            tasks.append(self._VKReq("getAlbumsByArtist", params))

        if includeTracks:
            tasks.append(self._VKReq("getAudiosByArtist", params))

        artist = tasks[0]
        if not artist.get("name"):
            return self._raiseError("artistNotFound")

        if includeAlbums:
            artist["albums"] = tasks[1].get("items")

        if includeTracks:
            artist["tracks"] = tasks[2].get("items")

        return self._finalizeResponse(artist, Artist)


    def getRelatedArtists(self, artistId: int, limit: int = 10) -> Union[List[Union[Artist, dict]], Artist, dict, None]:
        """
        Получает похожих артистов.

        Пример использования:\n
        result = client.getRelatedArtists(artistId=5696274288194638935, limit=5)\n
        print(result)

        :param artistId: идентификатор артиста, похожих на которого необходимо получить. (int)
        :param limit: максимальное количество артистов, которое необходимо вернуть. (bool, по умолчанию 10)
        :return: список артистов в виде объектов модели `Artist` или словарей, артист в виде объекта модели `Artist` или словаря (если он единственственный), или None (если `artistId` неверный или похожие артисты отсутствуют).
        """

        return self._finalizeResponse(self._VKReq("getRelatedArtistsById", {"artist_id": artistId, "count": limit}).get("artists"), Artist)


    def _getTracks(self, tracks: str, objectType: Union[Type[Union[Album, Playlist]], None] = None) -> dict:
        tracks = re.sub(r"\\/", "/", re.sub(r"false", "False", re.sub(r"true", "True", tracks)))
        try:
            if objectType:
                tracks = eval(tracks[tracks.rfind("[["): tracks.rfind("]]") + 2])

            else:
                tracks = []

        except SyntaxError:
            tracks = self._raiseError("accessDenied" + ("WithoutCookie" if not hasattr(self, "_cookies") else ""))

        if isinstance(tracks, list):
            for index, track in enumerate(tracks):
                tracks[index] = Track({"owner_id": track[1], "id": track[0], "title": track[3], "subtitle": track[16], "main_artists": track[17], "duration": track[5]}) if len(track) > 3 else None

            if not tracks or all(track is None for track in tracks):
                tracks = None

        return tracks


    def getAlbum(self, ownerId: int, albumId: int, includeTracks: bool = False) -> Union[Album, dict]:
        """
        Получает информацию об альбоме по его идентификатору.

        Пример использования:\n
        result = client.getAlbum(ownerId=-2000837600, albumId=16837600, includeTracks=True)\n
        print(result)

        :param ownerId: идентификатор владельца альбома (пользователь или группа). (int)
        :param albumId: идентификатор альбома, информацию о котором необходимо получить. (int)
        :param includeTracks: флаг, указывающий, необходимо ли включать треки альбома в ответ. (bool, по умолчанию `False`)
        :return: информация об альбоме в виде объекта модели `Album` или словаря.
        """

        tasks = [self._VKReq("getPlaylistById", {"owner_id": ownerId, "playlist_id": albumId})]

        if includeTracks:
            tasks.append(self._client.sendReq(VK + "music/album/" + f"{ownerId}_{albumId}", headers=headers, responseType="code"))

        album = tasks[0]
        if not album:
            return self._raiseError("albumNotFound")

        if includeTracks:
            album["tracks"] = self._getTracks(tasks[1], Album)

        return self._finalizeResponse(album, Album)


    def getPlaylist(self, playlistId: int, ownerId: int = None, includeTracks: bool = False) -> Union[Playlist, dict]:
        """
        Получает информацию о плейлисте по его ID.

        Пример использования:\n
        result = client.getPlaylist(playlistId=1, ownerId=-215973356, includeTracks=True)\n
        print(result)

        :param playlistId: идентификатор плейлиста, информацию о котором необходимо получить. (int)
        :param ownerId: идентификатор владельца плейлиста (пользователь или группа). (int, по умолчанию текущий пользователь)
        :param includeTracks: флаг, указывающий, необходимо ли включать треки плейлиста в ответ. (bool, по умолчанию `False`)
        :return: информация о плейлисте в виде объекта модели `Playlist` или словаря.
        """

        if not ownerId:
            ownerId = self.getSelf().get("id")

        tasks = [self._VKReq("getPlaylistById", {"owner_id": ownerId, "playlist_id": playlistId})]

        if includeTracks:
            tasks.append(self._client.sendReq(VK + "music/playlist/" + f"{ownerId}_{playlistId}", cookies=self._cookies if hasattr(self, "_cookies") else None, headers=headers, responseType="code"))

        playlist = tasks[0]
        if playlist.get("error"):
            return playlist

        if includeTracks:
            playlist["tracks"] = self._getTracks(tasks[1], Playlist)
        return self._finalizeResponse(playlist, Playlist)


    def getPlaylists(self, ownerId: int = None, playlistTypes: Union[str, List[str]] = ["own", "foreign", "album"]) -> Union[List[Union[Playlist, Album, dict]], Playlist, Album, dict, None]:
        """
        Получает плейлисты пользователя или группы.

        Пример использования:\n
        result = client.getPlaylists(ownerId=-215973356, playlistTypes="own")\n
        print(result)

        :param ownerId: идентификатор пользователя или группы, плейлисты которого(ой) необходимо получить. (int, по умолчанию текущий пользователь)
        :param playlistTypes: типы плейлистов, которые необходимо получить: `own` — принадлежащий пользователю или группе, `foreign` — не принадлежащий пользователю или группе, `album` — альбом. (str или list, по умолчанию ["own", "foreign", "album"])
        :return: список плейлистов в виде объектов модели `Playlist` или `Album` или словарей, плейлист в виде объекта модели `Playlist` или `Album` или словаря (если он единственственный), или `None` (если плейлисты отсутствуют).
        """

        if not ownerId:
            ownerId = self.getSelf().get("id")

        if not isinstance(playlistTypes, list):
            playlistTypes = [playlistTypes]

        for index, playlistType in enumerate(playlistTypes):
            playlistTypes[index] = playlistType.lower()

        method, params = "getPlaylists", {"owner_id": ownerId, "count": playlistsPerReq}
        playlists_ = self._VKReq(method, params)
        if playlists_.get("error"):
            return playlists_

        playlists = [playlist for playlist in playlists_.get("items")]
        count = playlists_.get("count")
        offset = count if count < playlistsPerReq else playlistsPerReq

        if offset < count:
            tasks = []
            while offset < count:
                tasks.append(self._VKReq(method, {**params, **{"offset": offset}}))
                offset += playlistsPerReq

            for playlistGroup in tasks:
                for playlist in playlistGroup.get("items"):
                    playlists.append(playlist)

        playlists = self._finalizeResponse(playlists, Playlist)

        if not isinstance(playlists, list):
            playlists = [playlists]

        playlists = [playlist for playlist in playlists if (isinstance(playlist, dict) and not playlist.get("artists") and ("own" if playlist.get("own") else "foreign") in playlistTypes) or (isinstance(playlist, Playlist) and ("owm" if playlist.own else "foreign") in playlistTypes) or ((isinstance(playlist, Album) or (isinstance(playlist, dict) and playlist.get("artists"))) and "album" in playlistTypes)]

        return (playlists if len(playlists) > 1 else playlists[0]) if playlists else None


    def getCuratorTracks(self, curatorId: int, limit: int = 10, offset: int = 0) -> Union[List[Union[Track, dict]], Track, dict, None]:
        """
        Получает аудиотреки, принадлежащие куратору.

        Пример использования:\n
        result = client.getCuratorTracks(curatorId=28905875, limit=5)\n
        print(result)

        :param curatorId: идентификатор куратора (пользователь или группа). (int)
        :param limit: максимальное количество аудиотреков, которое необходимо вернуть. (int, по умолчанию 10)
        :param offset: количество результатов, которые необходимо пропустить. (int, необязательно)
        :return: список аудиотреков в виде объектов модели Track или словарей, аудиотрек в виде объекта модели `Track` или словаря (если он единственный), или `None` (если неверный `curatorId` или аудиотреки отсутствуют).
        """

        return self._finalizeResponse(self._VKReq("getAudiosByCurator", {"curator_id": curatorId, "count": limit, "offset": offset}).get("items"), Track)


    def getTracksFromFeed(self) -> List[dict]:
        """
        Получает все треки из новостной ленты.

        Пример использования:\n
        result = client.getTracksFromFeed()\n
        print(result)

        :return: список аудиотреков в виде словарей с ключами `ownerId` и `trackId`.
        """

        tracks = self._VKReq("getAudioIdsBySource", {"source": "feed"}).get("audios")
        for index, track in enumerate(tracks):
            ownerId, trackId = track.get("audio_id").split("_")[:2]
            tracks[index] = {"ownerId": int(ownerId), "trackId": int(trackId)}

        return tracks


    def getRecommendations(self, limit: int = 10, offset: int = 0, ownerId: int = None, trackId: int = None) -> Union[List[Union[Track, dict]], Track, dict, None]:
        """
        Получает рекомендации аудиотреков для пользователя или похожие на аудиотрек.

        Пример использования для рекомендаций пользователя:\n
        result = client.getRecommendations(limit=20)\n
        print(result)

        Пример использования для рекомендаций по аудиотреку:\n
        result = client.getRecommendations(limit=5, ownerId=474499156, trackId=456637846)\n
        print(result)

        :param limit: максимальное количество аудиотреков, которое необходимо вернуть. (int, по умолчанию 10, минимально для пользовательских рекомендаций 10)
        :param offset: количество результатов, которые необходимо пропустить. (int, необязательно)
        :param ownerId: идентификатор владельца аудиотрека (пользователь или группа).
        :param trackId: идентификатор аудиотрека, похожие на который необходимо получить.
        :return: список аудиотреков в виде объектов модели `Track` или словарей, аудиотрек в виде объекта модели `Track` или словаря (если он единственный), или `None` (если рекомендации или похожие треки отсутствуют).
        """

        if not all((ownerId, trackId)) and limit < 10:
            limit = 10

        return self._finalizeResponse(self._VKReq("getRecommendations", {"count": limit, "offset": offset, **({"target_audio": f"{ownerId}_{trackId}"} if all((ownerId, trackId)) else {})}).get("items"), Track)


    def getNew(self) -> List[Union[Track, dict]]:
        """
        Получает аудиотреки, вышедшие недавно.

        Пример использования:\n
        result = client.getNew()\n
        print(result)

        :return: список аудиотреков в виде объектов модели `Track` или словарей.
        """

        playlist = self.getPlaylist(2, playlistsOwnerId, True)

        return playlist.tracks if isinstance(playlist, Playlist) else playlist.get("tracks")


    def getPopular(self) -> List[Union[Track, dict]]:
        """
        Получает популярные аудиотреки.

        Пример использования:\n
        result = client.getPopular()\n
        print(result)

        :return: список аудиотреков в виде объектов модели `Track` или словарей.
        """

        playlist = self.getPlaylist(1, playlistsOwnerId, True)

        return playlist.tracks if isinstance(playlist, Playlist) else playlist.get("tracks")


    def getEditorsPicks(self) -> List[Union[Track, dict]]:
        """
        Получает аудиотреки, выбранные редакторами ВКонтакте.

        Пример использования:\n
        result = client.getEditorsPicks()\n
        print(result)

        :return: список аудиотреков в виде объектов модели `Track` или словарей.
        """

        playlist = self.getPlaylist(3, playlistsOwnerId, True)

        return playlist.tracks if isinstance(playlist, Playlist) else playlist.get("tracks")


    def getTrackCount(self, ownerId: int) -> int:
        """
        Получает количество аудиотреков, принадлежащих этому пользователю или группе.

        Пример использования:\n
        result = client.getTrackCount(ownerId=-215973356)\n
        print(result)

        :param ownerId: идентификатор пользователя или группы. (int)
        :return: количество аудиотреков, принадлежащих пользователю или группе, в виде целого числа.
        """

        return self._VKReq("getCount", {"owner_id": ownerId})


    def getSearchTrends(self, limit: int = 10, offset: int = 0) -> Union[List[str], str, None]:
        """
        Получает самые частые поисковые запросы в музыке.

        Пример использования:\n
        result = client.getSearchTrends(limit=5)\n
        print(result)

        :param limit: максимальное количество запросов, которое необходимо вернуть. (int, по умолчанию 10)
        :param offset: количество результатов, которые необходимо пропустить. (int, необязательно)
        :return: список строк, представляющих самые частые поисковые запросы в музыке, строка, представляющая запрос (если он единственный) или `None` (если запросы отсутствуют).
        """

        return [item.get("name") for item in self._VKReq("getSearchTrends", {"count": limit, "offset": offset}).get("items")]


    def getBroadcast(self, id: int = None, isGroup: bool = False) -> Union[Track, dict, None, bool]:
        """
        Получает аудиотрек, транслируемый в статус.

        Пример использования для текущего пользователя:\n
        result = client.getBroadcast()\n
        print(result)

        Пример использования для любого пользователя:\n
        result = client.getBroadcast(id=1)\n
        print(result)

        Пример использования для группы:\n
        result = client.getBroadcast(id=-215973356, isGroup=True)\n
        print(result)

        :param id: идентификатор пользователя или группы, аудиотрек из статуса которого(ой) необходимо получить. (int, по умолчанию текущий пользователь)
        :param isGroup: флаг, указывающий необходимо получить статус пользователя или группы (`True` для группы). (bool, по умолчанию `False`)
        :return: аудиотрек в виде объекта модели `Track` или словаря, `None` (если ничего не проигрывается), или `False` (если музыка не транслируется в статус, только для текущего пользователя).
        """

        if isGroup and id:
            id = id - (id * 2)

        broadcast = self._VKReq("status.get", {"user_id": id} if id else None)
        if broadcast.get("error"):
            return broadcast

        audio = broadcast.get("audio")
        if audio:
            return self.get(audio.get("owner_id"), audio.get("id"), True)

        else:
            if not id or id == self.getSelf().get("id"):
                isBroadcastEnabled = self._VKReq("getBroadcast").get("enabled")
                if not bool(isBroadcastEnabled):
                    return False

            return None