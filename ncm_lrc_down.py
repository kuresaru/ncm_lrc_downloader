# coding: utf-8
from urllib.request import Request
from urllib.request import urlopen
import json
import sys
import re


def get_lyric(mid):
    # 根据歌曲id取歌词(json)
    url = 'http://music.163.com/api/song/lyric?os=pc&id=%s&lv=-1&kv=-1&tv=-1' % mid
    headers = {
        'Cookie': 'appver=2.0.2',
        'Referer': 'http://music.163.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
    }
    req = Request(url, headers=headers)
    response = urlopen(req)
    ret = response.read().decode()
    return json.loads(ret)


def origin_lrc(lrc):
    # 取原歌词
    return lrc['lrc']['lyric']


def translate_lrc(lrc):
    # 取翻译歌词 不一定存在
    return lrc['tlyric']['lyric']


def kly_lrc(lrc):
    # 同步歌词??? 不知道干什么的
    return lrc['klyric']['lyric']


def save_lrcs(mid):
    lrc = get_lyric(mid)
    text = origin_lrc(lrc)
    if text:
        with open('%s.lrc' % mid, "w") as f:
            f.write(origin_lrc(lrc))
    trans = translate_lrc(lrc)
    if trans:
        with open('%s_translate.lrc' % mid, "w") as f:
            f.write(trans)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Please provides the song id or share link with command args.')
        sys.exit(1)

    arg = sys.argv[1]
    if re.match(r'^[0-9]+$', arg):
        #lrc = get_lyric('625573')
        save_lrcs(arg)
    else:
        m = re.match(r'.*\bid=([0-9]+).*', arg, re.M | re.I)
        if m:
            save_lrcs(m.group(1))
        else:
            print("Invalid args, use song id or share link.")
