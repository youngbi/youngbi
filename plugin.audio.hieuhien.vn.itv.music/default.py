# -*- coding: utf-8 -*-

'''
Copyright (C) 2014                                                     

This program is free software: you can redistribute it and/or modify   
it under the terms of the GNU General Public License as published by   
the Free Software Foundation, either version 3 of the License, or      
(at your option) any later version.                                    

This program is distributed in the hope that it will be useful,        
but WITHOUT ANY WARRANTY; without even the implied warranty of         
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the          
GNU General Public License for more details.                           

You should have received a copy of the GNU General Public License      
along with this program. If not, see <http://www.gnu.org/licenses/>  
'''                                                                           

import urllib,urllib2,re,os
import xbmcplugin,xbmcgui,xbmcaddon
from BeautifulSoup import BeautifulSoup

addon = xbmcaddon.Addon(id='plugin.audio.hieuhien.vn.itv.music')
profile = addon.getAddonInfo('profile')
home = addon.getAddonInfo('path')
dataPatch = xbmc.translatePath(os.path.join(home, 'resources'))
logos = xbmc.translatePath(os.path.join(dataPatch, 'logos\\'))
fanart = xbmc.translatePath(os.path.join(home, 'fanart.jpg'))
icon = xbmc.translatePath(os.path.join(home, 'icon.png'))

reg = {
        'User-Agent' : 'Mozilla/5.0 (iPhone; CPU iPhone OS 5_0 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9A334 Safari/7534.48.3'
        }

dict = {'&#8211;':'-', '&#038;':'-', '&#8217':'-'}

def replace_all(text, dict):
	try:
		for a, b in dict.iteritems():
			text = text.replace(a, b)
		return text
	except:
		pass
		
def main():
    addDir(' Nhạc Việt Nam', 'http://conmatviet.com/nhac-chon-loc/nhac-viet-nam/', 3, icon, fanart, isFolder=True)  
    addDir(' Nhạc Vàng Trước 1975', 'http://conmatviet.com/nhac-vang-truoc-1975/', 3, icon, fanart, isFolder=True)
    addDir(' Hòa Tấu Việt Nam', 'http://conmatviet.com/nhac-chon-loc/nhac-hoa-tau/hoa-tau-viet-nam/', 3, icon, fanart, isFolder=True)
    addDir(' Nhạc Quốc Tế', 'http://conmatviet.com/nhac-chon-loc/nhac-quoc-te/', 3, icon, fanart, isFolder=True)
    addDir(' Nhạc Audiophile', 'http://conmatviet.com/tag/nhac-audiophile/', 3, icon, fanart, isFolder=True)
    addDir(' Hòa Tấu Quốc Tế', 'http://conmatviet.com/nhac-chon-loc/nhac-hoa-tau/hoa-tau-quoc-te/', 3, icon, fanart, isFolder=True)
    addDir(' Nhạc Demo', 'http://conmatviet.com/tag/test-demo-cd/', 3, icon, fanart, isFolder=True)
    xbmc.executebuiltin('Container.SetViewMode(515)')
	
def medialist(url):
    content = makeRequest( url, reg)	
    match = re.findall('<a title="(.+?)" href="(.+?)"><img src="(.+?)"></a>',content)
    for title, href, thumb in match:
        if 'mua-ban' in href:
            pass
        else:
	        addDir( replace_all(title, dict), href, 4, thumb +'.jpg', fanart, isFolder=True)
    if len(match) >= 21:
        match = re.findall('<a class="nextpostslink" rel="next" href="(.+?)">.+?</a>',content)
        for next_page in match:
            addDir( '[COLOR red]Next >>>[/COLOR]', next_page, 3, logos + 'NEXT.png', fanart, isFolder=True)
    xbmc.executebuiltin('Container.SetViewMode(502)')
		
def episodes(url,iconimage):
    content = makeRequest( url, reg)
    match = re.findall('{"title":"(.+?)","sources":.+?"file":"(http://conmatviet.com/.+?)"}',content)
    for name, link in match:
	    addDir( name.decode('unicode_escape').encode('utf-8'), link, 100, iconimage, fanart, isFolder=False)
    xbmc.executebuiltin('Container.SetViewMode(502)')		

def resolveUrl(url):
    mediaUrl = url    		
    item = xbmcgui.ListItem(path=mediaUrl)		
    xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)
    return
	
def makeRequest(url, headers=None):
    if headers is None:
        headers = {'User-agent' : 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
                 'Referer' : 'http://www.google.com'}
    try:
        req = urllib2.Request(url,headers=headers)
        f = urllib2.urlopen(req)
        body=f.read()
        return body
    except:
        pass 
  
def addDir(name,url,mode,iconimage,fanart,isFolder=False):
    u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&fanart="+urllib.quote_plus(fanart)
    ok=True
    liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
    liz.setInfo( type="Video", infoLabels={ "Title": name } )
    liz.setProperty('Fanart_Image',fanart)
    if not isFolder:
        liz.setProperty('IsPlayable', 'true')
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=isFolder)
    return ok 
	  	
def get_params():
    param=[]
    paramstring=sys.argv[2]
    if len(paramstring)>=2:
        params=sys.argv[2]
        cleanedparams=params.replace('?','')
        if (params[len(params)-1]=='/'):
            params=params[0:len(params)-2]
        pairsofparams=cleanedparams.split('&')
        param={}
        for i in range(len(pairsofparams)):
            splitparams={}
            splitparams=pairsofparams[i].split('=')
            if (len(splitparams))==2:
                param[splitparams[0]]=splitparams[1]
    return param

params=get_params()
url=None
name=None
mode=None
iconimage=None

try:url=urllib.unquote_plus(params["url"])
except:pass
try:name=urllib.unquote_plus(params["name"])
except:pass
try:mode=int(params["mode"])
except:pass
try:iconimage=urllib.unquote_plus(params["iconimage"])
except:pass
try:fanart=urllib.unquote_plus(params["fanart"])
except:pass

xbmcplugin.setContent(int(sys.argv[1]), 'movies')
sysarg=str(sys.argv[1])

if mode==None or url==None or len(url)<1:main()
#elif mode==1:search()
#elif mode==2:categories(url,name,page)
elif mode==3:medialist(url)
elif mode==4:episodes(url,iconimage)
elif mode==100:
    dialogWait = xbmcgui.DialogProgress()
    dialogWait.create('***ITV PLUS***', 'Đang tải. Vui lòng chờ trong giây lát...')
    resolveUrl(url)
    dialogWait.close()
    del dialogWait
  
xbmcplugin.endOfDirectory(int(sys.argv[1]))