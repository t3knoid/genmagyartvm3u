from django.http import HttpResponse
from lxml import html
import requests

mediaklikk_channels = {
    'Magyar M1':'https://player.mediaklikk.hu/playernew/player.php?video=mtv1live',
    'Magyar M2':'https://player.mediaklikk.hu/playernew/player.php?video=mtv2live',
    'Magyar M4':'https://player.mediaklikk.hu/playernew/player.php?video=mtv4live',
    'Magyar M5':'https://player.mediaklikk.hu/playernew/player.php?video=mtv5live',
    'Magyar Duna':'https://player.mediaklikk.hu/playernew/player.php?video=dunalive',
    'Magyar Duna World':'https://player.mediaklikk.hu/playernew/player.php?video=dunaworldlive',
}

# Create your views here.

################################################################################################
# This creates an index file that is an M3U file
# #EXTM3U
# #EXTINF: 1,Magyar M1
# https://c202-node62-cdn.connectmedia.hu/1100/a6f95540a87425cf2049d1c8bed6cf76/5a8b8932/02.m3u8
# #EXTINF: 2,Magyar M2
# https://c401-node62-cdn.connectmedia.hu/1101/ecb41b175801263d3b1a506eeca97e10/5a8b8932/02.m3u8
# #EXTINF: 3, Magyar M5
# https://c402-node61-cdn.connectmedia.hu/1105/890dca47f6a16c90087c81b9aa9bf1e0/5a8b8933/02.m3u8
# #EXTINF: 5, Magyar Duna World
# https://c402-node62-cdn.connectmedia.hu/1102/710c460ebb8bd77f3f3610c2358c9da2/5a8b8933/02.m3u8
# #EXTINF: 6, Magyar Duna Live (Danube)
# https://c401-node62-cdn.connectmedia.hu/1103/3b3611a3e1ae1f04e2593a8a06e15b59/5a8b8934/02.m3u8
# #EXTINF: 7, City TV
# https://citytv.hu/media/live/stream.m3u8
# #EXTINF: 8, BP Europe
# http://cloudfront44.lexanetwork.com:1730/HDE021/hls/livestream.sdp.m3u8
# #EXTINF: 9, Hatoscsatorna
# http://87.229.77.131:8081/Hatoscsatorna/livestream/playlist.m3u8
################################################################################################
def index(request):
    m1tvfeed = getm3u(get_vidsrc(mediaklikk_channels['Magyar M1'], '/html/body/script[3]/text()'))
    m2tvfeed = getm3u(get_vidsrc(mediaklikk_channels['Magyar M2'], '/html/body/script[3]/text()'))
    m4tvfeed = getm3u(get_vidsrc(mediaklikk_channels['Magyar M4'], '/html/body/script[3]/text()'))
    m5tvfeed = getm3u(get_vidsrc(mediaklikk_channels['Magyar M5'], '/html/body/script[3]/text()'))
    dunatvfeed = getm3u(get_vidsrc(mediaklikk_channels['Magyar Duna'], '/html/body/script[3]/text()'))    
    dunawtvfeed = getm3u(get_vidsrc(mediaklikk_channels['Magyar Duna World'], '/html/body/script[3]/text()'))
        
    message = f"""#EXTM3U
#EXTINF: -1,Magyar M1
{m1tvfeed}
#EXTINF: -1,Magyar M2
{m2tvfeed}
#EXTINF: -1, Magyar M4
{m4tvfeed}
#EXTINF: -1, Magyar M5
{m5tvfeed}
#EXTINF: -1, Magyar Duna World
{dunatvfeed}
#EXTINF: -1, Magyar Duna Live (Danube)
{dunawtvfeed}
"""
    
    return HttpResponse(message)
    
def getm3u(vidsrc):
    """ Gets the m3u8 file from an m3u8

    :param vidsrc:
    :return:
    """
    # Read index feed
    search_str = "/index.m3u8"    

    # Split the script into a list of individual lines
    lines = vidsrc.split('\n')

    # Get the line containing index.m3u8
    found_line = [s for s in lines if (search_str in s)][0]
    url_parts = found_line.split('"')
    m3u8_index = f'{url_parts[3].replace("\\", "")}'
    
    return m3u8_index

def get_vidsrc(index,xpath_str):
    """ Gets the video source from the given url and using the given xpath string.

    Arguments:
        index -- A URL containing the video source
        xpath_str -- The xpath string to find
    Returns:
        Returns the text that contains the video source.
    """
    headers = {
        "Referer": "https://mediaklikk.hu/",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/147.0.0.0 Safari/537.36"
    }

    pageContent = requests.get(
        index,
        headers=headers
    )

    tree = html.fromstring(pageContent.content)
    # Get the line containing the m3u source path
    vidsrc = tree.xpath(xpath_str)[0]

    # Split the script into a list of individual lines
    return vidsrc
