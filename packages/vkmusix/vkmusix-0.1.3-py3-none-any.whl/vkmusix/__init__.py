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

import time
import httpx
import base64

from typing import Union as _Union, Type as _Type, List as _List

from .models import Artist as _Artist, Album as _Album, Track as _Track, Playlist as _Playlist
from .config import VKAPI as _VKAPI, VKAPIVersion as _VKAPIVersion, RuCaptchaAPI as _RuCaptchaAPI
from .errors import errorsDict as _errorsDict, createErrorClass as _createErrorClass
from .cookies import getCookies as _getCookies, checkCookies as _checkCookies
from .utils.another import objectToDict as _objectToDict, checkFile as _checkFile

from .utils.requests import Client as _ReqClient
from .methods.another import Utils as _Utils
from .methods.search import Search as _Search
from .methods.update import Update as _Update
from .methods.get import Get as _Get

from .aio.utils.requests import Client as _ReqClientAsync
from .aio.methods.another import Utils as _UtilsAsync
from .aio.methods.search import Search as _SearchAsync
from .aio.methods.update import Update as _UpdateAsync
from .aio.methods.get import Get as _GetAsync


class _Init:
    def __init__(self, VKToken: str = None, RuCaptchaKey: str = None, errorsLanguage: str = None, responseType: str = "model", login: str = None, password: str = None, cookieFilename: str = None, asyncMode: bool = True) -> None:
        if not VKToken:
            VKToken = input("Получите токен с правами на аудио и доступ в любое время на `https://vkhost.github.io/` (приложение VK Admin) и отправьте его: ")

        self._RuCaptchaKey = RuCaptchaKey
        self._errorsLanguage = errorsLanguage.lower() if errorsLanguage and isinstance(errorsLanguage, str) and errorsLanguage.lower() in ["ru", "en"] else None
        self._responseType = responseType.lower() if responseType and isinstance(responseType, str) and responseType.lower() in ["model", "json"] else "model"

        if login or cookieFilename:
            cookieFileExist = False
            if not cookieFilename:
                cookieFilename = login

            if _checkFile(f"{cookieFilename}.VKCookie"):
                cookieFileExist = True

            if not cookieFileExist:
                if login and password:
                    cookieFilename = _getCookies(login, password, cookieFilename)

                else:
                    self._raiseError("VKCookieFileNotFound")

            self._cookies = _checkCookies(cookieFilename)

        self._asyncMode = asyncMode
        if self._asyncMode:
            self._clientSession = httpx.AsyncClient()
            self._client = _ReqClientAsync(self._clientSession)

        else:
            self._clientSession = httpx.Client()
            self._client = _ReqClient(self._clientSession)

        self._defaultParams = {"access_token": VKToken, "v": _VKAPIVersion}
        self._closed = False


    def _raiseError(self, errorType: _Union[str, None]) -> _Union[dict, None]:
        if not errorType:
            return

        if errorType not in _errorsDict:
            errorType = "unknown"

        errorClass = _createErrorClass(errorType)

        error = _errorsDict.get(errorType)
        errorText = getattr(error, self._errorsLanguage) if self._errorsLanguage else "🇷🇺: " + error.ru + " 🇬🇧: " + error.en

        if error.critical:
            raise errorClass(errorText)

        return {"error": {"code": error.code, "type": errorClass, "message": errorText}}


    def _finalizeResponse(self, response: _List[dict], objectType: _Type[_Union[_Artist, _Album, _Track, _Playlist]]) -> _Union[_List[dict], dict, None]:
        if not (response or response is False):
            return

        if not isinstance(response, list):
            response = [response]

        for index, obj in enumerate(response):
            if objectType is _Playlist:
                playlistType = obj.get("type")

                if playlistType in [0, 5]:
                    response[index] = objectType(obj, False if obj.get("original") else True)

                elif playlistType == 1:
                    response[index] = _Album(obj, True)

            else:
                response[index] = objectType(obj)

            if self._responseType == "json":
                response[index] = _objectToDict(response[index])

        return response if len(response) > 1 else response[0]


class ClientAsync(_Init, _UtilsAsync, _SearchAsync, _GetAsync, _UpdateAsync):
    """
    Класс для асинхронного взаимодействия с VK Music.

    Аргументы:
        VKToken (str, optional): Токен доступа к VK API.\n
        RuCaptchaKey (str, optional): Ключ для решения капчи через сервис RuCaptcha. Если не указан, капча может потребовать ручного решения.\n
        errorsLanguage (str, optional): Язык ошибок (например, `ru` для русского, `en` для английского). Если не указан, используются оба языка.\n
        responseType (str, optional): Формат данных ответа. Доступные варианты: `model` для объектов классов и `json`. По умолчанию `model`.\n
        login (str, optional): Логин аккаунта ВКонтакте. Нужен для получения cookie, нужных для некоторых методов.\n
        password (str, optional): Пароль аккаунта ВКонтакте. Нужен для получения cookie, нужных для некоторых методов.\n
        cookieFilename (str, optional): Название файла c расширением .VKCookie. По умолчанию введённый логин.

    Пример использования:
        client = ClientAsync(VKToken="yourVKToken", RuCaptchaKey="yourRuCaptchaKey", errorsLanguage="ru", responseType="json", login="admin@vkmusix.ru", password="vkmusix.ru", cookieFilename="admin")
        result = await client.searchArtists("prombl")
        print(result)
    """


    def __init__(self, VKToken: str = None, RuCaptchaKey: str = None, errorsLanguage: str = None, responseType: str = "model", login: _Union[str, int] = None, password: _Union[str, int] = None, cookieFilename: _Union[str, int] = None) -> None:
        super().__init__(VKToken, RuCaptchaKey, errorsLanguage, responseType, login, password, cookieFilename, asyncMode=True)


    async def __aenter__(self):
        return self


    async def __aexit__(self, exc_type, exc_value, traceback):
        await self.close()


    async def close(self):
        """
        Закрывает текующую сессию. Для отправки новых запросов потребуется создать новый объект класса `ClientAsync`.
        """

        self._closed = True
        await self._clientSession.aclose()


    def __enter__(self):
        self._raiseError("usingAsyncClientInSyncContext")


    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


    async def _VKReq(self, method: str, params: dict = None) -> dict or None:
        if self._closed:
            self._raiseError("sessionClosed")

        if not params:
            params = {}

        if "." not in method:
            method = "audio." + method

        url = _VKAPI + method
        fullParams = {**params, **self._defaultParams}

        req = await self._client.sendReq(url, fullParams)

        while isinstance(req, dict) and req.get("error"):
            error = req.get("error")
            errorCode = error.get("error_code")

            if errorCode == 3:
                return self._raiseError("VKInvalidMethod")

            elif errorCode == 5:
                self._raiseError("VKInvalidToken")

            elif errorCode == 10 and method == "createChatPlaylist":
                return self._raiseError("chatNotFound")

            elif errorCode == 14:
                captchaImg = error.get("captcha_img")
                if self._ruCaptchaKey:
                    solve = await self._solveCaptcha(captchaImg)

                else:
                    solve = input(captchaImg + "\nВведите решение капчи: ")

                fullParams.update({"captcha_sid": error.get("captcha_sid"), "captcha_key": solve})

                req = await self._client.sendReq(url, fullParams)

            elif errorCode in [15, 201, 203]:
                if ": can not restore too late" in error.get("error_msg"):
                    return self._raiseError("trackRestorationTimeEnded")

                else:
                    return self._raiseError("accessDenied")

            elif errorCode == 18:
                return self._raiseError("userWasDeletedOrBanned")

            elif errorCode == 104:
                return self._raiseError("notFound")

            else:
                return error

        if isinstance(req, list) and len(req) == 1:
            req = req[0]

        return req


    async def _solveCaptcha(self, captchaImg: str) -> str:
        imageBytes = await self._client.sendReq(captchaImg, responseType="file")
        captchaImageInBase64 = base64.b64encode(imageBytes).decode("utf-8")

        RuCaptchaParams = {
            "clientKey": self._RuCaptchaKey,
            "task": {
                "type": "ImageToTextTask",
                "body": captchaImageInBase64
            },
            "languagePool": "rn"
        }

        taskId = (await self._client.sendReq(_RuCaptchaAPI + "createTask", params=RuCaptchaParams, method="POST")).get("taskId")

        while True:
            time.sleep(5)
            taskResult = await self._client.sendReq(_RuCaptchaAPI + "getTaskResult", params={"clientKey": self._RuCaptchaKey, "taskId": taskId}, method="POST")
            errorId = taskResult.get("errorId")

            if errorId == 0 and taskResult.get("status") == "ready":
                return taskResult.get("solution").get("text")

            elif errorId == 1:
                self._raiseError("RuCaptchaInvalidKey")

            elif errorId == 10:
                self._raiseError("RuCaptchaZeroBalance")

            elif errorId == 12:
                taskId = (await self._client.sendReq(_RuCaptchaAPI + "createTask", params=RuCaptchaParams, method="POST")).get("taskId")

            elif errorId == 21:
                self._raiseError("RuCaptchaBannedIP")

            elif errorId == 55:
                self._raiseError("RuCaptchaBannedAccount")


class Client(_Init, _Utils, _Search, _Get, _Update):
    """
    Класс для взаимодействия с VK Music.

    Аргументы:
        VKToken (str, optional): Токен доступа к VK API.\n
        RuCaptchaKey (str, optional): Ключ для решения капчи через сервис RuCaptcha. Если не указан, капча может потребовать ручного решения.\n
        errorsLanguage (str, optional): Язык ошибок (например, `ru` для русского, `en` для английского). Если не указан, используются оба языка.\n
        responseType (str, optional): Формат данных ответа. Доступные варианты: `model` для объектов классов и `json`. По умолчанию `model`.\n
        login (str, optional): Логин аккаунта ВКонтакте. Нужен для получения cookie, нужных для некоторых методов.\n
        password (str, optional): Пароль аккаунта ВКонтакте. Нужен для получения cookie, нужных для некоторых методов.\n
        cookieFilename (str, optional): Название файла c расширением .VKCookie. По умолчанию введённый логин.

    Пример использования:
        client = Client(VKToken="yourVKToken", RuCaptchaKey="yourRuCaptchaKey", errorsLanguage="ru", responseType="json", login="admin@vkmusix.ru", password="vkmusix.ru", cookieFilename="admin")
        result = client.searchArtists("prombl")
        print(result)
    """

    def __init__(self, VKToken: str = None, ruCaptchaKey: str = None, errorsLanguage: str = None, responseType: str = "model", login: str = None, password: str = None, cookieFilename: str = None) -> None:
        super().__init__(VKToken, ruCaptchaKey, errorsLanguage, responseType, login, password, cookieFilename, asyncMode=False)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def close(self):
        """
        Закрывает текующую сессию. Для отправки новых запросов потребуется создать новый объект класса `Client`.
        """

        self._closed = True
        self._clientSession.close()


    def __aenter__(self):
        self._raiseError("usingSyncClientInAsyncContext")


    def __aexit__(self, exc_type, exc_val, exc_tb):
        pass


    def _VKReq(self, method: str, params: dict = None) -> dict or None:
        if self._closed:
            self._raiseError("sessionClosed")

        if not params:
            params = {}

        if "." not in method:
            method = "audio." + method

        url = _VKAPI + method
        fullParams = {**params, **self._defaultParams}

        req = self._client.sendReq(url, fullParams)

        while isinstance(req, dict) and req.get("error"):
            error = req.get("error")
            errorCode = error.get("error_code")

            if errorCode == 3:
                return self._raiseError("VKInvalidMethod")

            elif errorCode == 5:
                self._raiseError("VKInvalidToken")

            elif errorCode == 10 and method == "createChatPlaylist":
                return self._raiseError("chatNotFound")

            elif errorCode == 14:
                captchaImg = error.get("captcha_img")
                if self._ruCaptchaKey:
                    solve = self._solveCaptcha(captchaImg)

                else:
                    solve = input(captchaImg + "\nВведите решение капчи: ")

                fullParams.update({"captcha_sid": error.get("captcha_sid"), "captcha_key": solve})

                req = self._client.sendReq(url, fullParams)

            elif errorCode in [15, 201, 203]:
                if ": can not restore too late" in error.get("error_msg"):
                    return self._raiseError("trackRestorationTimeEnded")

                else:
                    return self._raiseError("accessDenied")

            elif errorCode == 18:
                return self._raiseError("userWasDeletedOrBanned")

            elif errorCode == 104:
                return self._raiseError("notFound")

            else:
                return error

        if isinstance(req, list) and len(req) == 1:
            req = req[0]

        return req


    def _solveCaptcha(self, captchaImg: str) -> str:
        imageBytes = self._client.sendReq(captchaImg, responseType="file")
        captchaImageInBase64 = base64.b64encode(imageBytes).decode("utf-8")

        RuCaptchaParams = {
            "clientKey": self._RuCaptchaKey,
            "task": {
                "type": "ImageToTextTask",
                "body": captchaImageInBase64
            },
            "languagePool": "rn"
        }

        taskId = (self._client.sendReq(_RuCaptchaAPI + "createTask", params=RuCaptchaParams, method="POST")).get("taskId")

        while True:
            time.sleep(5)
            taskResult = self._client.sendReq(_RuCaptchaAPI + "getTaskResult", params={"clientKey": self._RuCaptchaKey, "taskId": taskId}, method="POST")
            errorId = taskResult.get("errorId")

            if errorId == 0 and taskResult.get("status") == "ready":
                return taskResult.get("solution").get("text")

            elif errorId == 1:
                self._raiseError("RuCaptchaInvalidKey")

            elif errorId == 10:
                self._raiseError("RuCaptchaZeroBalance")

            elif errorId == 12:
                taskId = (self._client.sendReq(_RuCaptchaAPI + "createTask", params=RuCaptchaParams, method="POST")).get("taskId")

            elif errorId == 21:
                self._raiseError("RuCaptchaBannedIP")

            elif errorId == 55:
                self._raiseError("RuCaptchaBannedAccount")