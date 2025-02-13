import re
import time
from typing import TypedDict

from aiohttp import ClientSession

from yutto._typing import AId, AvId, BvId, CId, EpisodeId
from yutto.exceptions import NotFoundError
from yutto.utils.fetcher import Fetcher
from yutto.utils.console.logger import Logger


class VideoInfo(TypedDict):
    avid: AvId
    aid: AId
    bvid: BvId
    episode_id: EpisodeId
    is_bangumi: bool
    cid: CId
    picture: str
    title: str
    pubdate: str


_info_cache: dict[AvId, VideoInfo] = {}


async def get_video_info(session: ClientSession, avid: AvId) -> VideoInfo:
    # 对于 video_info 的请求数量过于离谱，因此必须加上一个 cache 了
    if avid in _info_cache:
        Logger.debug("get_video_info cache 命中！")
        return _info_cache[avid]
    regex_ep = re.compile(r"https?://www\.bilibili\.com/bangumi/play/ep(?P<episode_id>\d+)")
    info_api = "http://api.bilibili.com/x/web-interface/view?aid={aid}&bvid={bvid}"
    res_json = await Fetcher.fetch_json(session, info_api.format(**avid.to_dict()))
    res_json_data = res_json.get("data")
    if res_json["code"] == 62002:
        raise NotFoundError(f"无法下载该视频 {avid}，原因：{res_json['message']}")
    assert res_json_data is not None, "响应数据无 data 域"
    episode_id = EpisodeId("")
    if res_json_data.get("redirect_url") and (ep_match := regex_ep.match(res_json_data["redirect_url"])):
        episode_id = EpisodeId(ep_match.group("episode_id"))
    video_info: VideoInfo = {
        "avid": BvId(res_json_data["bvid"]),
        "aid": AId(str(res_json_data["aid"])),
        "bvid": BvId(res_json_data["bvid"]),
        "episode_id": episode_id,
        "is_bangumi": bool(episode_id),
        "cid": CId(str(res_json_data["cid"])),
        "picture": res_json_data["pic"],
        "title": res_json_data["title"],
        "pubdate": time.strftime("%Y-%m-%d", time.localtime(res_json_data["pubdate"])),
    }
    _info_cache[avid] = video_info
    return video_info


async def is_vip(session: ClientSession) -> bool:
    info_api = "https://api.bilibili.com/x/web-interface/nav"
    res_json = await Fetcher.fetch_json(session, info_api)
    res_json_data = res_json.get("data")
    if res_json_data.get("vipStatus") == 1:
        return True
    return False
