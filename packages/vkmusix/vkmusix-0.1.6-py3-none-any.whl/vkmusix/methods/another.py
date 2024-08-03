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

from typing import Union, List

from ..utils.another import addHTTPsToUrl


class Utils:
    def APIReq(self, method: str, params: dict = {}) -> Union[dict, List[dict], bool, int]:
        """
        Отправляет запрос к методу VK API с указанными параметрами.

        Пример использования для создания поста на своей страничке с текстом «Примет, мир!»:\n
        result = client.APIReq(method="wall.post", params={"message": "Привет, мир!"})\n
        print(result)

        :param method: метод, к которому необходимо отправить запрос. (str)
        :param params: параметры запроса в виде словаря. Ключи и значения зависят от метода API. (dict, необязательно)
        :return: результат выполнения запроса, тип и структура данных зависят от метода API.
        """

        return self._VKReq(method, params)


    def getSelf(self) -> dict:
        """
        Получает информацию о текущем пользователе.

        Пример использования:\n
        result = client.getSelf()\n
        print(result)

        :return: словарь с информацией о текущем пользователе с гарантированными ключами: `id`, `first_name` и `last_name`.
        """

        return self._VKReq("users.get")


    def createVKccUrl(self, url: str) -> str:
        """
        Создаёт сокращённую ссылку с доменом «vk.cc».

        Пример использования:\n
        result = client.createVKccUrl(url="google.com")\n
        print(result)

        :param url: ссылка, которую необходимо сократить. (str)
        :return: сокращённая ссылка с доменом «vk.cc».
        """

        url = addHTTPsToUrl(url)

        return self._VKReq("utils.getShortLink", {"url": url}).get("short_url")