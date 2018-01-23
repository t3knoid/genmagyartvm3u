# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from lxml import html
import requests
import urlparse

search_str = "\/index.m3u8"
m1index = 'https://player.mediaklikk.hu/playernew/player.php?video=mtv1live'
m2index = 'https://player.mediaklikk.hu/playernew/player.php?video=mtv2live'
m4index = 'https://player.mediaklikk.hu/playernew/player.php?video=mtv4live'
m5index = 'https://player.mediaklikk.hu/playernew/player.php?video=mtv5live'
dunaindex = 'https://player.mediaklikk.hu/playernew/player.php?video=dunalive'
dunawindex = 'https://player.mediaklikk.hu/playernew/player.php?video=dunaworldlive'
bpeuropeindex = 'http://wdsonline.gdsinfo.com/itplayer/bptv_inc.php'
sixthchindex = 'http://www.hatoscsatorna.hu/livetv.php'

high_res_m3u = "02.m3u8"


# Create your views here.

def index(request):
    m1tvfeed = getm3u(m1index)
    m2tvfeed = getm3u(m2index)
    m4tvfeed = getm3u(m4index)
    m5tvfeed = getm3u(m5index)
    dunatvfeed = getm3u(dunaindex)
    dunawtvfeed = getm3u(dunawindex)
    citytvfeed = "https://citytv.hu/media/live/stream.m3u8"

    message = """#EXTM3U\n#EXTINF: 1,Magyar M1\n%s\n#EXTINF: 2,Magyar M2\n%s\n#EXTINF: 3, Magyar M4\n%s\n#EXTINF: 4, Magyar M5\n%s\n#EXTINF: 5, Magyar Duna World\n%s\n#EXTINF: 6, Magyar Duna Live (Danube)\n%s\n,#EXTINF: 7, CityTV\n%s\n"""
    return HttpResponse(message % (m1tvfeed, m2tvfeed, m4tvfeed, m5tvfeed, dunatvfeed, dunawtvfeed, citytvfeed))

def getm3u(index):
    # Read index feed
    pageContent = requests.get(
        index
    )
    tree = html.fromstring(pageContent.content)

    # Get the script text containing the m3u8 index URL
    script = tree.xpath('/html/body/script[3]/text()')[0]

    # Split the script into a list of individual lines
    lines = script.split('\n')

    # Get the line containing index.m3u8
    found_line = [s for s in lines if (search_str in s)][0]

    url_parts = found_line.split('"')
    m3u8_index = 'https:%s' % url_parts[3].replace('\\', '')

    high_res_video = urlparse.urljoin(m3u8_index, high_res_m3u)
    return high_res_video
