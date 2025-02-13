import argparse
import asyncio
import re
from typing import Optional

import aiohttp

from yutto._typing import AId, AvId, BvId, EpisodeData
from yutto.api.acg_video import get_acg_video_pubdate, get_acg_video_title
from yutto.exceptions import HttpStatusError, NoAccessPermissionError, NotFoundError, UnSupportedTypeError
from yutto.extractor._abc import SingleExtractor
from yutto.extractor.common import extract_acg_video_data
from yutto.utils.console.logger import Badge, Logger


class AcgVideoExtractor(SingleExtractor):
    """投稿视频单视频"""

    REGEX_AV = re.compile(r"https?://www\.bilibili\.com/video/av(?P<aid>\d+)(\?p=(?P<page>\d+))?")
    REGEX_BV = re.compile(r"https?://www\.bilibili\.com/video/(?P<bvid>(bv|BV)\w+)(\?p=(?P<page>\d+))?")

    REGEX_AV_ID = re.compile(r"av(?P<aid>\d+)(\?p=(?P<page>\d+))?")
    REGEX_BV_ID = re.compile(r"(?P<bvid>(bv|BV)\w+)(\?p=(?P<page>\d+))?")

    page: int
    avid: AvId

    def resolve_shortcut(self, id: str) -> tuple[bool, str]:
        matched = False
        url = id
        if match_obj := self.REGEX_AV_ID.match(id):
            page: int = 1
            if match_obj.group("page") is not None:
                page = int(match_obj.group("page"))
            url = f"https://www.bilibili.com/video/av{match_obj.group('aid')}?p={page}"
            matched = True
        elif match_obj := self.REGEX_BV_ID.match(id):
            page: int = 1
            if match_obj.group("page") is not None:
                page = int(match_obj.group("page"))
            url = f"https://www.bilibili.com/video/{match_obj.group('bvid')}?p={page}"
            matched = True
        return matched, url

    def match(self, url: str) -> bool:
        if (match_obj := self.REGEX_AV.match(url)) or (match_obj := self.REGEX_BV.match(url)):
            self.page: int = 1
            if "aid" in match_obj.groupdict().keys():
                self.avid = AId(match_obj.group("aid"))
            else:
                self.avid = BvId(match_obj.group("bvid"))
            if match_obj.group("page") is not None:
                self.page = int(match_obj.group("page"))
            return True
        else:
            return False

    async def extract(self, session: aiohttp.ClientSession, args: argparse.Namespace) -> Optional[EpisodeData]:
        title, pubdate = await asyncio.gather(
            get_acg_video_title(session, self.avid),
            get_acg_video_pubdate(session, self.avid),
        )
        Logger.custom(title, Badge("投稿视频", fore="black", back="cyan"))
        try:
            return await extract_acg_video_data(
                session,
                self.avid,
                self.page,
                None,
                args,
                {"title": title, "pubdate": pubdate},
                "{title}",
            )
        except (NoAccessPermissionError, HttpStatusError, UnSupportedTypeError, NotFoundError) as e:
            Logger.error(e.message)
            return None
