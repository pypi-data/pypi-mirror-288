import datetime
import re
import http.client
from json import loads
import asyncio
import aiohttp
import json
import requests
import time


class BaseLive:
    def __init__(self, url: str, path: str, refresh_interval: int = 10):
        self.url = url
        self.path = path
        self._data = {}
        self.refresh_interval = refresh_interval
        self._last_fetch_time = 0
        self.refresh_data()  # Initial data fetch

    def _fetch_data(self) -> dict:
        try:
            connection = http.client.HTTPSConnection(self.url)
            connection.request("GET", self.path)
            response = connection.getresponse()

            if response.status == 200:
                data = loads(response.read().decode())
                return data.get('content', {})  # Default to empty dict if 'content' is missing
            else:
                print(f"Error: {response.status} - {response.reason}")
                return {}

        except Exception as e:
            print(f"Exception occurred: {e}")
            return {}

        finally:
            if connection is not None:
                connection.close()

    def refresh_data(self) -> None:
        """Refresh the data by fetching it again from the API."""
        self._data = self._fetch_data()
        self._last_fetch_time = time.time()

    def get_data(self) -> dict:
        """Return the latest data, refreshing if necessary."""
        current_time = time.time()
        if current_time - self._last_fetch_time > self.refresh_interval:
            self.refresh_data()
        return self._data

    def live_status(self) -> bool:
        data = self.get_data()
        status = data.get('status', '')  # Default to empty string if 'status' is missing
        return status == "OPEN"

    def _get_live_data_if_open(self, key: str):
        if self.live_status() is True:
            return self._data.get(key)
        else:
            print("Error: This stream is offline")
            return None

    def _get_fetch_live_data_if_close(self, key: str):
        if self.live_status() is False:
            return self._data.get(key)
        else:
            print("Error: This stream is online")
            return None

    def _get_channel_data_if_open(self, key: str):
        if self.live_status():
            channel_data = self._data.get('channel', {})
            return channel_data.get(key)
        else:
            print("Error: This stream is offline")
            return None

    def _get_channel_data_if_close(self, key: str):
        if not self.live_status():
            channel_data = self._data.get('channel', {})
            return channel_data.get(key)
        else:
            print("Error: This stream is online")
            return None


class BaseInfo:
    def __init__(self, channel_id: str, url: str, nid_aut: str, nid_ses: str, refresh_interval: int = 10):
        self.channel_id = channel_id
        self.url = url
        self.nid_aut = nid_aut
        self.nid_ses = nid_ses
        self._data = []
        self.refresh_interval = refresh_interval
        self._last_fetch_time = 0
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
            "Cache-Control": "no-cache",
            "Origin": "https://studio.chzzk.naver.com",
            "Pragma": "no-cache",
            "Referer": f"https://studio.chzzk.naver.com/{self.channel_id}/live",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
            "Cookie": f"NID_AUT={self.nid_aut}; NID_SES={self.nid_ses}",
            "Deviceid": "ed6c3c29-f184-4c7a-bd90-58011b5be74f",
            "Front-Client-Platform-Type": "PC",
            "Front-Client-Product-Type": "web"
        }
        self.refresh_data()  # Initial fetch

    def _fetch_data(self) -> list:
        """Fetch data from the API."""
        try:
            response = requests.get(self.url, headers=self.headers)
            if response.status_code == 200:
                result = response.json()
                content = result.get('content', {})
                data = content.get('data', [])
                if data:
                    return data  # Extract the list of data
                else:
                    return content
            else:
                print(f"Error: {response.status_code} - {response.reason}")
                return []

        except Exception as e:
            print(f"Exception occurred: {e}")
            return []

    def refresh_data(self) -> None:
        """Refresh the data by fetching it again from the API."""
        self._data = self._fetch_data()
        self._last_fetch_time = time.time()

    def get_data(self) -> list:
        """Return the latest data, refreshing if necessary."""
        if time.time() - self._last_fetch_time > self.refresh_interval:
            self.refresh_data()
        return self._data


class Live(BaseLive):
    def __init__(self, channel_id: str):
        url = "api.chzzk.naver.com"
        path = f"/service/v3/channels/{channel_id}/live-detail"
        super().__init__(url, path)

    def title(self) -> str:
        return self._get_live_data_if_open('liveTitle')

    def category(self) -> str:
        return self._get_live_data_if_open('liveCategory')

    def category_value(self) -> str:
        return self._get_live_data_if_open('liveCategoryValue')

    def tags(self) -> list:
        return self._get_live_data_if_open('tags')

    def id(self) -> int:
        return self._get_live_data_if_open('liveId')

    def channel_id(self) -> int:
        return self._get_channel_data_if_open("channelId")

    def concurrent_view_count(self) -> int:
        return self._get_live_data_if_open('concurrentUserCount')

    def accumulate_view_count(self) -> int:
        return self._get_live_data_if_open('accumulateCount')

    def clip_active(self) -> bool:
        return self._get_live_data_if_open('clipActive')

    def type(self) -> str:
        return self._get_live_data_if_open('categoryType')

    def default_thumbnail_url(self) -> str:
        return self._get_live_data_if_open('defaultThumbnailImageUrl')

    def image_url(self) -> str:
        return self._get_live_data_if_open('liveImageUrl')

    def adult(self) -> bool:
        return self._get_live_data_if_open('adult')

    def open_date(self) -> str:
        return self._get_live_data_if_open('openDate')

    def open_day(self) -> str:
        date = self.open_date()
        return date.split()[0] if date else ''

    def open_time(self) -> str:
        date = self.open_date()
        return date.split()[1] if date else ''


class Status(BaseInfo):
    def __init__(self, channel_id: str, nid_aut: str, nid_ses: str):
        url = f"https://api.chzzk.naver.com/manage/v1/channels/{channel_id}/live-setting/normal"
        super().__init__(channel_id, url, nid_aut, nid_ses)

    def title(self) -> str:
        data = self.get_data()
        if data:
            return data.get('defaultLiveTitle', '')  # Assuming first item in list
        return ''

    def get_category(self, key: str):
        """Retrieve specific user data."""
        if self.get_data():
            channel_data = self.get_data().get('category', {})
            return channel_data.get(key, None)  # Default to None if key is not found
        return None

    def type(self) -> str:
        return self.get_category('categoryType')

    def category(self) -> str:
        return self.get_category('categoryId')

    def category_value(self) -> str:
        return self.get_category('categoryValue')

    def poster_image_url(self) -> str:
        return self.get_category('posterImageUrl')

    def category_tags(self) -> str:
        return self.get_category('tags')

    def paid_promotion(self) -> bool:
        data = self.get_data()
        if data:
            return data.get('paidPromotion', False)  # Assuming first item in list
        return False

    def adult(self) -> bool:
        data = self.get_data()
        if data:
            return data.get('adult', False)  # Assuming first item in list
        return False

    def kr_only_viewing(self) -> bool:
        data = self.get_data()
        if data:
            return data.get('krOnlyViewing', False)  # Assuming first item in list
        return False

    def tags(self) -> list:
        data = self.get_data()
        if data:
            return data.get('tags', [])  # Assuming first item in list
        return None

    def clip_active(self) -> bool:
        data = self.get_data()
        if data:
            return data.get('clipActive', False)  # Assuming first item in list
        return False

    def replay_publish_type(self) -> str:
        data = self.get_data()
        if data:
            return data.get('replayPublishType', "")  # Assuming first item in list
        return ""

    async def edit(self, title: str = None, category: str = None, category_type: str = None, tags: list = None,
                   adult: bool = False, clip_active: bool = False) -> None:
        adult = True if adult is not False else self.adult()
        title = title if title is not None else self.title()
        category_type = category_type if category_type is not None else self.type()
        tags = tags if tags is not None else self.tags()
        clip_active = True if clip_active is not False else self.clip_active()

        if category is None:
            category = self.category()

        elif category == "talk":
            category = "talk"
            category_type = "ETC"
            tags = self.tags()

        elif category == "종합 게임":
            category = "various_games"
            category_type = "ETC"
            tags = self.tags()

        else:
            if not category == "talk" or not category == "종합 게임":
                url = f"https://api.chzzk.naver.com/manage/v1/auto-complete/categories?keyword={category}&size=1"
                response = requests.get(url)
                category = loads(response.text)['content']['results'][0]['categoryId']
                category_type = loads(response.text)['content']['results'][0]['categoryType']
                tags = self.tags()

        data = {
            "adult": adult,
            "defaultLiveTitle": title,
            "categoryType": category_type,
            "liveCategory": category,
            "tags": tags,
            "clipActive": clip_active,
            "replayPublishType": self.replay_publish_type()
        }

        async with aiohttp.ClientSession() as session:
            async with session.put(self.url, headers=self.headers, data=json.dumps(data)) as response:
                if response.status == 200:
                    print("Successful")

                else:
                    if response.status == 401:
                        print("Error", response.status, "인증정보가 유효하지 않습니다.")

                    elif response.status == 403:
                        print("Error", response.status, "방송상태를 바꿀 수 있는 권한이 없습니다 (채널관리자 권한 필요)")

                    else:
                        print("Error", response.status, await response.text())


class Restrict(BaseInfo):
    def __init__(self, channel_id: str, nid_aut: str, nid_ses: str):
        url = f"https://api.chzzk.naver.com/manage/v1/channels/{channel_id}/restrict-users"
        super().__init__(channel_id, url, nid_aut, nid_ses)

    async def ban(self, name: str) -> None:
        data = {
            "targetId": name
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(self.url, headers=self.headers, data=json.dumps(data)) as response:
                if response.status == 200:
                    print("success")
                else:
                    await self._handle_error(response)

    async def unban(self, name: str) -> None:
        user_info = await self._fetch_user_info(name)
        if not user_info:
            return None

        user_id = user_info['userIdHash']
        unban_url = f"{self.url}/{user_id}"

        async with aiohttp.ClientSession() as session:
            async with session.delete(unban_url, headers=self.headers) as response:
                if response.status == 200:
                    print("success")
                else:
                    await self._handle_error(response)

    async def _fetch_user_info(self, name: str) -> dict:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.url}?page=0&size=50&userNickname={name}", headers=self.headers) as response:
                if response.status == 200:
                    result = await response.json()
                    users = result.get('content', {}).get('data', [])
                    if users:
                        return users[0]  # 첫 번째 유저 정보 반환
                    else:
                        return None
                else:
                    print(f"유저 정보를 가져오는 중 에러 발생: {response.status}")
                    return None

    async def _handle_error(self, response):
        if response.status == 401:
            print("Error", response.status, "인증정보가 유효하지 않습니다.")
        elif response.status == 403:
            print("Error", response.status, "사용자를 활동정지 할 수 있는 권한이 없습니다 (채널관리자 권한 필요)")
        else:
            print("Error", response.status, await response.text())


class CheckSubscribers(BaseInfo):
    def __init__(self, channel_id: str, nid_aut: str = None, nid_ses: str = None):
        url = f"https://api.chzzk.naver.com/manage/v1/channels/{channel_id}/subscribers"
        super().__init__(channel_id, url, nid_aut, nid_ses)

    def fetch_subscript_data(self, name: str) -> dict:
        response = requests.get(f"{self.url}?page=0&size=50&nickname={name}&sortType=RECENT", headers=self.headers)
        try:
            if response.status_code == 200:
                result = response.json()
                content = result.get('content', {})
                data = content.get('data', [])
                if data:
                    return data  # Extract the list of data
                else:
                    return content
            else:
                print(f"Error: {response.status_code} - {response.reason}")
                return []

        except Exception as e:
            print(f"Exception occurred: {e}")
            return []

    def user_id(self, name) -> str:
        data = self.fetch_subscript_data(name)
        if data:
            return data[0].get('userIdHash', '')  # Assuming first item in list
        return ''

    def user_name(self, name) -> str:
        data = self.fetch_subscript_data(name)
        if data:
            return data[0].get('nickname', '')  # Assuming first item in list
        return ''

    def profile_image_url(self, name) -> str:
        data = self.fetch_subscript_data(name)
        if data:
            return data[0].get('profileImageUrl', '')  # Assuming first item in list
        return ''

    def verified_mark(self, name) -> bool:
        data = self.fetch_subscript_data(name)
        if data:
            return data[0].get('verifiedMark', False)  # Assuming first item in list
        return False

    def total_month(self, name) -> int:
        data = self.fetch_subscript_data(name)
        if data:
            return data[0].get('totalMonth', 0)  # Assuming first item in list
        return 0

    def twitch_month(self, name) -> int:
        data = self.fetch_subscript_data(name)
        if data:
            return data[0].get('twitchMonth', 0)
        return 0

    def tier(self, name) -> str:
        data = self.fetch_subscript_data(name)
        if data:
            return data[0].get('tier', '')  # Assuming first item in list
        return ''

    def publish_period(self, name) -> int:
        data = self.fetch_subscript_data(name)
        if data:
            return data[0].get('publishPeriod', 0)  # Assuming first item in list
        return 0

    def created(self, name) -> str:
        data = self.fetch_subscript_data(name)
        if data:
            return data[0].get('createdDate', '')  # Assuming first item in list
        return ''


class CheckFollowers(BaseInfo):
    def __init__(self, channel_id: str, nid_aut: str = None, nid_ses: str = None):
        url = f"https://api.chzzk.naver.com/manage/v1/channels/{channel_id}/followers"
        super().__init__(channel_id, url, nid_aut, nid_ses)

    def fetch_follow_data(self, name: str) -> dict:
        response = requests.get(f"{self.url}?page=0&size=50&userNickname={name}", headers=self.headers)
        try:
            if response.status_code == 200:
                result = response.json()
                content = result.get('content', {})
                data = content.get('data', [])
                if data:
                    return data  # Extract the list of data
                else:
                    return content
            else:
                print(f"Error: {response.status_code} - {response.reason}")
                return []

        except Exception as e:
            print(f"Exception occurred: {e}")
            return []

    def get_user(self, key: str, name: str):
        """Retrieve specific user data."""
        if self.fetch_follow_data(name):
            # Assuming the user data is inside the first item
            channel_data = self.fetch_follow_data(name)[0].get('user', {})
            return channel_data.get(key, None)  # Default to None if key is not found
        return None

    def get_following(self, key: str, name: str):
        """Retrieve specific user data."""
        if self.fetch_follow_data(name):
            # Assuming the user data is inside the first item
            channel_data = self.fetch_follow_data(name)[0].get('following', {})
            return channel_data.get(key, None)  # Default to None if key is not found
        return None

    def get_channel_following(self, key: str, name: str):
        """Retrieve specific user data."""
        if self.fetch_follow_data(name):
            # Assuming the user data is inside the first item
            channel_data = self.fetch_follow_data(name)[0].get('channelFollowing', {})
            return channel_data.get(key, None)  # Default to None if key is not found
        return None

    def user_id(self, name: str) -> str:
        return self.get_user('userIdHash', name=name)

    def user_name(self, name: str) -> str:
        return self.get_user('nickname', name=name)

    def profile_image_url(self, name: str) -> str:
        return self.get_user('profileImageUrl', name=name)

    def verified_mark(self, name: str) -> bool:
        return self.get_user('verifiedMark', name=name)

    def following(self, name: str) -> bool:
        return self.get_following('following', name=name)

    def notification(self, name: str) -> bool:
        return self.get_following('notification', name=name)

    def follow_date(self, name: str) -> str:
        return self.get_following('followDate', name=name)

    def channel_following(self, name: str) -> bool:
        return self.get_channel_following('following', name=name)

    def channel_notification(self, name: str) -> bool:
        return self.get_channel_following('notification', name=name)

    def channel_follow_date(self, name: str) -> str:
        return self.get_channel_following('followDate', name=name)


class Prohibit_Words(BaseInfo):
    def __init__(self, channel_id: str, nid_aut: str, nid_ses: str):
        url = f"https://api.chzzk.naver.com/manage/v1/channels/{channel_id}/chats/prohibit-words"
        super().__init__(channel_id, url, nid_aut, nid_ses)

    def get_prohibit_words(self) -> list:
        """Retrieve all prohibited words."""
        data = self.get_data()
        if data:
            return data.get('prohibitWordList', [])
        return []

    def prohibit_words(self) -> list:
        prohibited_words = self.get_prohibit_words()
        return [word["prohibitWord"] for word in prohibited_words]

    def find_prohibit_word_no(self, word: str) -> int:
        """Find the prohibitWordNo for a given prohibited word."""
        prohibited_words = self.get_prohibit_words()
        for item in prohibited_words:
            if item["prohibitWord"] == word:
                return item["prohibitWordNo"]
        return None

    async def add(self, word: str) -> None:
        data = {
            "prohibitWord": word
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(self.url, headers=self.headers, data=json.dumps(data)) as response:
                if response.status == 200:
                    print("success")
                else:
                    await self._handle_error(response)

    async def delete(self, word: str) -> None:
        word_no = self.find_prohibit_word_no(word)
        if not word_no:
            return None

        delete_url = f"{self.url}/{word_no}"

        async with aiohttp.ClientSession() as session:
            async with session.delete(delete_url, headers=self.headers) as response:
                if response.status == 200:
                    print("success")
                else:
                    await self._handle_error(response)

    async def _handle_error(self, response):
        if response.status == 401:
            print("Error", response.status, "인증정보가 유효하지 않습니다.")
        elif response.status == 403:
            print("Error", response.status, "사용자를 활동정지 할 수 있는 권한이 없습니다 (채널관리자 권한 필요)")
        else:
            print("Error", response.status, await response.text())


class FetchLive(BaseLive):
    def __init__(self, channel_id: str):
        url = "api.chzzk.naver.com"
        path = f"/service/v3/channels/{channel_id}/live-detail"
        super().__init__(url, path)

    def title(self) -> str:
        return self._get_fetch_live_data_if_close('liveTitle')

    def category(self) -> str:
        return self._get_fetch_live_data_if_close('liveCategoryValue')

    def tags(self) -> list:
        return self._get_fetch_live_data_if_close('tags')

    def id(self) -> int:
        return self._get_fetch_live_data_if_close('liveId')

    def concurrent_view_count(self) -> int:
        return self._get_fetch_live_data_if_close('concurrentUserCount')

    def accumulate_view_count(self) -> int:
        return self._get_fetch_live_data_if_close('accumulateCount')

    def clip_active(self) -> bool:
        return self._get_fetch_live_data_if_close('clipActive')

    def type(self) -> str:
        return self._get_fetch_live_data_if_close('categoryType')

    def default_thumbnail_url(self) -> str:
        return self._get_fetch_live_data_if_close('defaultThumbnailImageUrl')

    def image_url(self) -> str:
        return self._get_fetch_live_data_if_close('liveImageUrl')

    def adult(self) -> bool:
        return self._get_fetch_live_data_if_close('adult')

    def close_date(self) -> str:
        return self._get_fetch_live_data_if_close('closeDate')

    def close_day(self) -> str:
        date = self.close_date()
        return date.split()[0] if date else ''

    def close_time(self) -> str:
        date = self.close_date()
        return date.split()[1] if date else ''


class Channel(BaseLive):
    def __init__(self, channel_id: str):
        url = "api.chzzk.naver.com"
        path = f"/service/v1/channels/{channel_id}"
        super().__init__(url, path)

    def id(self) -> int:
        return self._data.get('channelId', 0)

    def description(self) -> str:
        return self._data.get('channelDescription', '')

    def follower(self) -> int:
        return self._data.get('followerCount', 0)

    def image_url(self) -> str:
        return self._data.get('channelImageUrl', '')

    def name(self) -> str:
        return self._data.get('channelName', '')

    def subscript(self) -> bool:
        return self._data.get('subscriptionAvailability', False)

    def type(self) -> str:
        return self._data.get('channelType', '')

    def ad_monetization(self) -> bool:
        return self._data.get('adMonetizationAvailability', False)

    def verified(self) -> bool:
        return self._data.get('verifiedMark', False)


class Clip(BaseInfo):
    def __init__(self, channel_id: str, nid_aut: str = None, nid_ses: str = None):
        url = f"https://api.chzzk.naver.com/manage/v1/channels/{channel_id}/clips?page=0&size=50&dateFilter=ALL&orderFilter=LATEST"
        super().__init__(channel_id, url, nid_aut, nid_ses)

    def uid(self, count: int = 1) -> str:
        value = count - int(1)
        data = self.get_data()
        if data:
            return data[value].get('clipUID', '')  # Assuming first item in list
        return ''

    def clip_url(self, count: int = 1) -> str:
        uid = self.uid(count)
        base_url = "https://chzzk.naver.com/embed/clip/"
        clip_url = f"{base_url}{uid}"
        if clip_url:
            return clip_url

        else:
            return ''

    def title(self, count: int = 1) -> str:
        value = count - int(1)
        data = self.get_data()
        if data:
            return data[value].get('clipTitle', '')  # Assuming first item in list
        return ''

    def thumbnail_image_url(self, count: int = 1) -> str:
        value = count - int(1)
        data = self.get_data()
        if data:
            return data[value].get('thumbnailImageUrl', '')  # Assuming first item in list
        return ''

    def duration(self, count: int = 1) -> int:
        value = count - int(1)
        data = self.get_data()
        if data:
            return data[value].get('duration', 0)  # Assuming first item in list
        return 0

    def adult(self, count: int = 1) -> bool:
        value = count - int(1)
        data = self.get_data()
        if data:
            return data[value].get('audlt', False)  # Assuming first item in list
        return False

    def vod_status(self, count: int = 1) -> str:
        value = count - int(1)
        data = self.get_data()
        if data:
            return data[value].get('vodStatus', '')  # Assuming first item in list
        return ''

    def created(self, count: int = 1) -> str:
        value = count - int(1)
        data = self.get_data()
        if data:
            return data[value].get('createdDate', '')  # Assuming first item in list
        return ''

    def make_channel(self, key: str, count: int = 1):
        value = count - int(1)
        """Retrieve specific user data."""
        if self.get_data():
            # Assuming the user data is inside the first item
            channel_data = self.get_data()[value].get('makeChannel', {})
            return channel_data.get(key, None)  # Default to None if key is not found
        return None

    def make_channel_id(self, count: int = 1) -> str:
        return self.make_channel('channelId', count)

    def make_channel_name(self, count: int = 1) -> str:
        return self.make_channel('channelName', count)


class Follow(BaseInfo):
    def __init__(self, channel_id: str, nid_aut: str = None, nid_ses: str = None):
        url = f"https://api.chzzk.naver.com/manage/v1/channels/{channel_id}/news-feeds?size=20&typeFilters=FOLLOW"
        super().__init__(channel_id, url, nid_aut, nid_ses)

    def news_feed_no(self, count: int = 1) -> int:
        value = count - int(1)
        data = self.get_data()
        if data:
            return data[value].get('newsFeedNo', 0)  # Assuming first item in list
        return 0

    def news_feed_type(self, count: int = 1) -> str:
        value = count - int(1)
        data = self.get_data()
        if data:
            return data[value].get('newsFeedType', '')  # Assuming first item in list
        return ''

    def message(self, count: int = 1) -> str:
        value = count - int(1)
        data = self.get_data()
        if data:
            return data[value].get('message', '')  # Assuming first item in list
        return ''

    def get_user(self, key: str, count: int = 1):
        value = count - int(1)
        """Retrieve specific user data."""
        if self.get_data():
            # Assuming the user data is inside the first item
            channel_data = self.get_data()[value].get('user', {})
            return channel_data.get(key, None)  # Default to None if key is not found
        return None

    def user_id_hash(self) -> str:
        return self.get_user('userIdHash')

    def nickname(self) -> str:
        return self.get_user('nickname')

    def profile_image_url(self) -> str:
        return self.get_user('profileImageUrl')

    def verified_mark(self) -> bool:
        return self.get_user('verifiedMark')  # Default to False if 'verifiedMark' is not found

    def created(self, count: int = 1) -> str:
        value = count - int(1)
        data = self.get_data()
        if data:
            return data[value].get('createdDate', '')  # Assuming first item in list
        return ''


class Donation(BaseInfo):
    def __init__(self, channel_id: str, nid_aut: str = None, nid_ses: str = None):
        url = f"https://api.chzzk.naver.com/manage/v1/channels/{channel_id}/news-feeds?size=20&typeFilters=DONATION"
        super().__init__(channel_id, url, nid_aut, nid_ses)

    def news_feed_no(self, count: int = 1) -> int:
        value = count - int(1)
        data = self.get_data()
        if data:
            return data[value].get('newsFeedNo', 0)  # Assuming first item in list
        return 0

    def news_feed_type(self, count: int = 1) -> str:
        value = count - int(1)
        data = self.get_data()
        if data:
            return data[value].get('newsFeedType', '')  # Assuming first item in list
        return ''

    def message(self, count: int = 1) -> str:
        value = count - int(1)
        data = self.get_data()
        if data:
            return data[value].get('message', '')  # Assuming first item in list
        return ''

    def get_user(self, key: str, count: int = 1):
        value = count - int(1)
        """Retrieve specific user data."""
        if self.get_data():
            # Assuming the user data is inside the first item
            channel_data = self.get_data()[value].get('user', {})
            return channel_data.get(key, None)  # Default to None if key is not found
        return None

    def user_id_hash(self) -> str:
        return self.get_user('userIdHash')

    def nickname(self) -> str:
        return self.get_user('nickname')

    def profile_image_url(self) -> str:
        return self.get_user('profileImageUrl')

    def verified_mark(self) -> bool:
        return self.get_user('verifiedMark')  # Default to False if 'verifiedMark' is not found

    def created(self, count: int = 1) -> str:
        value = count - int(1)
        data = self.get_data()
        if data:
            return data[value].get('createdDate', '')  # Assuming first item in list
        return ''

    def id(self, count: int = 1) -> str:
        value = count - int(1)
        data = self.get_data()
        if data:
            return data[value].get('donationId', '')  # Assuming first item in list
        return ''

    def text(self, count: int = 1) -> str:
        value = count - int(1)
        data = self.get_data()
        if data:
            return data[value].get('donationText', '')  # Assuming first item in list
        return ''

    def pay_amount(self, count: int = 1) -> int:
        value = count - int(1)
        data = self.get_data()
        if data:
            extra_json_str = data[value].get('extraJson', '{}')
            extra_json = json.loads(extra_json_str)
            return extra_json.get('payAmount', 0)
        return 0

    def anonymous(self, count: int = 1) -> bool:
        value = count - int(1)
        data = self.get_data()
        if data:
            return data[value].get('anonymous')  # Assuming first item in list
        return False


class MissionDonation(BaseInfo):
    def __init__(self, channel_id: str, nid_aut: str = None, nid_ses: str = None):
        url = f"https://api.chzzk.naver.com/manage/v1/channels/{channel_id}/news-feeds?size=20&typeFilters=DONATION"
        super().__init__(channel_id, url, nid_aut, nid_ses)

    def news_feed_no(self, count: int = 1) -> int:
        value = count - int(1)
        data = self.get_data()
        if data:
            return data[value].get('newsFeedNo', 0)  # Assuming first item in list
        return 0

    def news_feed_type(self, count: int = 1) -> str:
        value = count - int(1)
        data = self.get_data()
        if data:
            return data[value].get('newsFeedType', '')  # Assuming first item in list
        return ''

    def message(self, count: int = 1) -> str:
        value = count - int(1)
        data = self.get_data()
        if data:
            return data[value].get('message', '')  # Assuming first item in list
        return ''

    def get_user(self, key: str, count: int = 1):
        value = count - int(1)
        """Retrieve specific user data."""
        if self.get_data():
            # Assuming the user data is inside the first item
            channel_data = self.get_data()[value].get('user', {})
            return channel_data.get(key, None)  # Default to None if key is not found
        return None

    def user_id_hash(self) -> str:
        return self.get_user('userIdHash')

    def nickname(self) -> str:
        return self.get_user('nickname')

    def profile_image_url(self) -> str:
        return self.get_user('profileImageUrl')

    def verified_mark(self) -> bool:
        return self.get_user('verifiedMark')  # Default to False if 'verifiedMark' is not found

    def created(self, count: int = 1) -> str:
        value = count - int(1)
        data = self.get_data()
        if data:
            return data[value].get('createdDate', '')  # Assuming first item in list
        return ''

    def id(self, count: int = 1) -> str:
        value = count - int(1)
        data = self.get_data()
        if data:
            return data[value].get('donationId', '')  # Assuming first item in list
        return ''

    def text(self, count: int = 1) -> str:
        value = count - int(1)
        data = self.get_data()
        if data:
            return data[value].get('donationText', '')  # Assuming first item in list
        return ''

    def pay_amount(self, count: int = 1) -> int:
        value = count - int(1)
        data = self.get_data()
        if data:
            extra_json_str = data[value].get('extraJson', '{}')
            extra_json = json.loads(extra_json_str)
            return extra_json.get('payAmount', 0)
        return 0

    def get_mission(self, key: str, count: int = 1):
        value = count - int(1)
        """Retrieve specific user data."""
        if self.get_data():
            # Assuming the user data is inside the first item
            channel_data = self.get_data()[value].get('missionDonation', {})
            return channel_data.get(key, None)  # Default to None if key is not found
        return None

    def mission_type(self) -> str:
        return self.get_mission('missionType')

    def amount(self) -> int:
        return self.get_mission('amount')

    def fail_cheering_rate(self) -> int:
        return self.get_mission('failCheeringRate')

    def status(self) -> str:
        return self.get_mission('status')

    def success(self) -> bool:
        return self.get_mission('success')

    def duration(self) -> int:
        return self.get_mission('missionDurationTime')

    def start(self) -> str:
        return self.get_mission('missionStartTime')

    def end(self) -> str:
        return self.get_mission('missionEndTime')

    def anonymous(self, count: int = 1) -> bool:
        value = count - int(1)
        data = self.get_data()
        if data:
            return data[value].get('anonymous')  # Assuming first item in list
        return False


class VideoDonation(BaseInfo):
    def __init__(self, channel_id: str, nid_aut: str = None, nid_ses: str = None):
        url = f"https://api.chzzk.naver.com/manage/v1/channels/{channel_id}/news-feeds?size=20&typeFilters=VIDEO"
        super().__init__(channel_id, url, nid_aut, nid_ses)

    def news_feed_no(self, count: int = 1) -> int:
        value = count - int(1)
        data = self.get_data()
        if data:
            return data[value].get('newsFeedNo', 0)  # Assuming first item in list
        return 0

    def news_feed_type(self, count: int = 1) -> str:
        value = count - int(1)
        data = self.get_data()
        if data:
            return data[value].get('newsFeedType', '')  # Assuming first item in list
        return ''

    def message(self, count: int = 1) -> str:
        value = count - int(1)
        data = self.get_data()
        if data:
            return data[value].get('message', '')  # Assuming first item in list
        return ''

    def get_user(self, key: str, count: int = 1):
        value = count - int(1)
        """Retrieve specific user data."""
        if self.get_data():
            # Assuming the user data is inside the first item
            channel_data = self.get_data()[value].get('user', {})
            return channel_data.get(key, None)  # Default to None if key is not found
        return None

    def user_id_hash(self) -> str:
        return self.get_user('userIdHash')

    def nickname(self) -> str:
        return self.get_user('nickname')

    def profile_image_url(self) -> str:
        return self.get_user('profileImageUrl')

    def verified_mark(self) -> bool:
        return self.get_user('verifiedMark')  # Default to False if 'verifiedMark' is not found

    def created(self, count: int = 1) -> str:
        value = count - int(1)
        data = self.get_data()
        if data:
            return data[value].get('createdDate', '')  # Assuming first item in list
        return ''

    def donation_id(self, count: int = 1) -> str:
        value = count - int(1)
        data = self.get_data()
        if data:
            return data[value].get('donationId', '')  # Assuming first item in list
        return ''

    def video_id(self, count: int = 1) -> str:
        value = count - int(1)
        data = self.get_data()
        if data:
            return data[value].get('videoId', '')  # Assuming first item in list
        return ''

    def video_type(self, count: int = 1) -> str:
        value = count - int(1)
        data = self.get_data()
        if data:
            return data[value].get('videoType', '')  # Assuming first item in list
        return ''

    def video_url(self, count: int = 1) -> str:
        video_id = self.video_id(count)
        video_type = self.video_type(count)
        base_url = None

        if video_type == "YOUTUBE":
            base_url = "https://www.youtube.com/watch?v="

        elif video_type == "CHZZK_CLIP":
            base_url = "https://chzzk.naver.com/embed/clip/"

        if base_url and video_id:
            url = f"{base_url}{video_id}"
            return url

        else:
            return ""  # Or handle the error as needed

    def start(self, count: int = 1) -> int:
        value = count - int(1)
        data = self.get_data()
        if data:
            return data[value].get('startSecond', 0)  # Assuming first item in list
        return 0

    def end(self, count: int = 1) -> int:
        value = count - int(1)
        data = self.get_data()
        if data:
            return data[value].get('endSecond', 0)  # Assuming first item in list
        return 0

    def is_played(self, count: int = 1) -> bool:
        value = count - int(1)
        data = self.get_data()
        if data:
            return data[value].get('isPlayed', True)  # Assuming first item in list
        return True

    def is_playing(self, count: int = 1) -> bool:
        value = count - int(1)
        data = self.get_data()
        if data:
            return data[value].get('isPlaying', False)  # Assuming first item in list
        return False

    def pay_amount(self, count: int = 1) -> int:
        value = count - int(1)
        data = self.get_data()
        if data:
            extra_json_str = data[value].get('extraJson', '{}')
            extra_json = json.loads(extra_json_str)
            return extra_json.get('payAmount', 0)
        return 0

    def text(self, count: int = 1) -> str:
        value = count - int(1)
        data = self.get_data()
        if data:
            return data[value].get('donationText', '')  # Assuming first item in list
        return ''

    def anonymous(self, count: int = 1) -> bool:
        value = count - int(1)
        data = self.get_data()
        if data:
            return data[value].get('anonymous')  # Assuming first item in list
        return False


class Subsciption(BaseInfo):
    def __init__(self, channel_id: str, nid_aut: str = None, nid_ses: str = None):
        url = f"https://api.chzzk.naver.com/manage/v1/channels/{channel_id}/news-feeds?size=20&typeFilters=DONATION"
        super().__init__(channel_id, url, nid_aut, nid_ses)

    def news_feed_no(self, count: int = 1) -> int:
        value = count - int(1)
        data = self.get_data()
        if data:
            return data[value].get('newsFeedNo', 0)  # Assuming first item in list
        return 0

    def news_feed_type(self, count: int = 1) -> str:
        value = count - int(1)
        data = self.get_data()
        if data:
            return data[value].get('newsFeedType', '')  # Assuming first item in list
        return ''

    def message(self, count: int = 1) -> str:
        value = count - int(1)
        data = self.get_data()
        if data:
            return data[value].get('message', '')  # Assuming first item in list
        return ''

    def get_user(self, key: str, count: int = 1):
        value = count - int(1)
        """Retrieve specific user data."""
        if self.get_data():
            # Assuming the user data is inside the first item
            channel_data = self.get_data()[value].get('user', {})
            return channel_data.get(key, None)  # Default to None if key is not found
        return None

    def user_id_hash(self) -> str:
        return self.get_user('userIdHash')

    def nickname(self) -> str:
        return self.get_user('nickname')

    def profile_image_url(self) -> str:
        return self.get_user('profileImageUrl')

    def verified_mark(self) -> bool:
        return self.get_user('verifiedMark')  # Default to False if 'verifiedMark' is not found

    def created(self, count: int = 1) -> str:
        value = count - int(1)
        data = self.get_data()
        if data:
            return data[value].get('createdDate', '')  # Assuming first item in list
        return ''

    def text(self, count: int = 1) -> int:
        value = count - int(1)
        data = self.get_data()
        if data:
            extra_json_str = data[value].get('extraJson', '{}')
            extra_json = json.loads(extra_json_str)
            return extra_json.get('subscriptionText', 0)
        return 0

    def month(self, count: int = 1) -> int:
        value = count - int(1)
        data = self.get_data()
        if data:
            extra_json_str = data[value].get('extraJson', '{}')
            extra_json = json.loads(extra_json_str)
            return extra_json.get('subscriptionMonth', 0)
        return 0

    def tier_no(self, count: int = 1) -> int:
        value = count - int(1)
        data = self.get_data()
        if data:
            extra_json_str = data[value].get('extraJson', '{}')
            extra_json = json.loads(extra_json_str)
            return extra_json.get('subscriptionTierNo', 0)
        return 0

    def tier_name(self, count: int = 1) -> int:
        value = count - int(1)
        data = self.get_data()
        if data:
            extra_json_str = data[value].get('extraJson', '{}')
            extra_json = json.loads(extra_json_str)
            return extra_json.get('subscriptionTierName', 0)
        return 0

    def anonymous(self, count: int = 1) -> bool:
        value = count - int(1)
        data = self.get_data()
        if data:
            return data[value].get('anonymous')  # Assuming first item in list
        return False


class Ad(BaseInfo):
    def __init__(self, channel_id: str, nid_aut: str = None, nid_ses: str = None):
        url = f"https://api.chzzk.naver.com/manage/v1/channels/{channel_id}/news-feeds?size=20&typeFilters=DONATION"
        super().__init__(channel_id, url, nid_aut, nid_ses)

    def news_feed_no(self, count: int = 1) -> int:
        value = count - int(1)
        data = self.get_data()
        if data:
            return data[value].get('newsFeedNo', 0)  # Assuming first item in list
        return 0

    def news_feed_type(self, count: int = 1) -> str:
        value = count - int(1)
        data = self.get_data()
        if data:
            return data[value].get('newsFeedType', '')  # Assuming first item in list
        return ''

    def message(self, count: int = 1) -> str:
        value = count - int(1)
        data = self.get_data()
        if data:
            return data[value].get('message', '')  # Assuming first item in list
        return ''

    def created(self, count: int = 1) -> str:
        value = count - int(1)
        data = self.get_data()
        if data:
            return data[value].get('createdDate', '')  # Assuming first item in list
        return ''

    def anonymous(self, count: int = 1) -> bool:
        value = count - int(1)
        data = self.get_data()
        if data:
            return data[value].get('anonymous')  # Assuming first item in list
        return False


class Chzzk:
    def __init__(self, channel_id: str, nid_aut: str = None, nid_ses: str = None):
        self.channel_id = channel_id
        self.nid_aut = nid_aut
        self.nid_ses = nid_ses
        self.live = Live(channel_id)
        self.status = Status(channel_id, nid_aut, nid_ses)
        self.fetch_live = FetchLive(channel_id)
        self.channel = Channel(channel_id)
        self.follow = Follow(channel_id, nid_aut, nid_ses)
        self.donation = Donation(channel_id, nid_aut, nid_ses)
        self.mission_donation = MissionDonation(channel_id, nid_aut, nid_ses)
        self.video_donation = VideoDonation(channel_id, nid_aut, nid_ses)
        self.subscription = Subsciption(channel_id, nid_aut, nid_ses)
        self.ad = Ad(channel_id, nid_aut, nid_ses)
        self.restrict = Restrict(channel_id, nid_aut, nid_ses)
        self.prohibit_words = Prohibit_Words(channel_id, nid_aut, nid_ses)
        self.clip = Clip(channel_id, nid_aut, nid_ses)
        self.check_followers = CheckFollowers(channel_id, nid_aut, nid_ses)
        self.check_subscribers = CheckSubscribers(channel_id, nid_aut, nid_ses)

    def get_live(self) -> Live:
        return self.live

    def get_fetch_live(self) -> FetchLive:
        return self.fetch_live

    def get_channel(self) -> Channel:
        return self.channel

    def get_follow(self) -> Follow:
        return self.follow

    def get_donation(self) -> Donation:
        return self.donation

    def get_mission_donation(self) -> MissionDonation:
        return self.mission_donation

    def get_video_donation(self) -> VideoDonation:
        return self.video_donation

    def get_subscription(self) -> Subsciption:
        return self.subscription

    def get_ad(self) -> Ad:
        return self.ad

    def get_restrict(self) -> Restrict:
        return self.restrict

    def get_prohibit_words(self) -> Prohibit_Words:
        return self.prohibit_words

    def get_clip(self) -> Clip:
        return self.clip

    def get_check_followers(self) -> CheckFollowers:
        return self.check_followers

    def get_check_subscribers(self) -> CheckSubscribers:
        return self.check_subscribers

    def refresh_all(self):
        self.live.refresh_data()
        self.fetch_live.refresh_data()
        self.channel.refresh_data()
        self.follow.refresh_data()
        self.donation.refresh_data()
        self.mission_donation.refresh_data()
        self.video_donation.refresh_data()
        self.subscription.refresh_data()
        self.ad.refresh_data()
        self.prohibit_words()
        self.clip()
        self.check_followers()
        self.check_subscribers()
