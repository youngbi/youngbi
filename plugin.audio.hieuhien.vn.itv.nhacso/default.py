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

import CommonFunctions as common
import urllib
import urllib2
import os
import xbmc
import xbmcplugin
import xbmcgui
import xbmcaddon
import re, string, json

addon = xbmcaddon.Addon(id='plugin.audio.hieuhien.vn.itv.nhacso')
home = addon.getAddonInfo('path')
icon = xbmc.translatePath( os.path.join( home, 'icon.png' ) )
logos = xbmc.translatePath( os.path.join( home, 'logos\\' ) )
homeUrl = 'http://nhacso.net/'
albumUrl = 'http://nhacso.net/albums/ajax-list-album?category_id=12&'
list_view = addon.getSetting('view_list')
mode_view = addon.getSetting('view_mode')

def view():
    if mode_view == 'List':
      try:  
        xbmc.executebuiltin('Container.SetViewMode(502)')
      except:
	    pass
    elif mode_view == 'Thumbnails':  
      try:  
        xbmc.executebuiltin('Container.SetViewMode(500)')
      except:
	    pass

def album_categories():
    addDir('[COLOR red]Tìm Album[/COLOR]','homeUrl', 1, logos+'Search.png')
    addDir( 'Mới Cập Nhật', albumUrl+'&view_type=latest&limit='+list_view, 102, icon, page=1)
    addDir( 'Nhạc Trẻ', albumUrl+'category_children_id=1&view_type=latest&limit='+list_view, 102, icon, page=1)
    addDir( 'Nhạc Trữ Tình', albumUrl+'category_children_id=2&view_type=latest&limit='+list_view, 102, icon, page=1)
    addDir( 'Nhạc Cách Mạng', albumUrl+'category_children_id=3&view_type=latest&limit='+list_view, 102, icon, page=1)
    addDir( 'Nhạc Trịnh', albumUrl+'category_children_id=4&view_type=latest&limit='+list_view, 102, icon, page=1)
    addDir( 'Nhạc Tiền Chiến', albumUrl+'category_children_id=5&view_type=latest&limit='+list_view, 102, icon, page=1)
    addDir( 'Nhạc Dân Tộc', albumUrl+'category_children_id=6&view_type=latest&limit='+list_view, 102, icon, page=1)
    addDir( 'Nhạc Thiếu Nhi', albumUrl+'category_children_id=7&view_type=latest&limit='+list_view, 102, icon, page=1)
    addDir( 'Nhạc Hải Ngoại', albumUrl+'category_children_id=10&view_type=latest&limit='+list_view, 102, icon, page=1)
    addDir( 'Nhạc Quê Hương', albumUrl+'category_children_id=11&view_type=latest&limit='+list_view, 102, icon, page=1)
    addDir( 'Rock Việt', albumUrl+'category_children_id=9&view_type=latest&limit='+list_view, 102, icon, page=1)
    addDir( 'Rap Việt - Hiphop', albumUrl+'category_children_id=14&view_type=latest&limit='+list_view, 102, icon, page=1)
    view()
	
def search():#1 
    try:
        keyb = xbmc.Keyboard('', '[COLOR lime]Nhập tên [COLOR red]Album[/COLOR] cần tìm kiếm...[/COLOR]')
        keyb.doModal()
        if (keyb.isConfirmed()):
            searchText=urllib.quote_plus(keyb.getText()) 
        url = 'http://nhacso.net/tim-kiem-tat-ca.html?keyName=' + urllib.quote_plus(searchText.replace(' ','+'))
        print "Searching URL: "+url
        #search_result(url)
    except:
        pass
    content = make_request(url)  
    match = re.compile('class="is-load-ajax is-push-url is-top is-detail" data-id-content=".wrap-page" href="/nghe-album/(.*?)">\s*<img  class="video-thumb" src="(.*?)" alt="(.*?)"',re.DOTALL).findall(content)  
    for (href, thumb, title) in match:
        addDir( '['+ '[COLOR gold]Album[/COLOR]' + '] ' + title.strip(), homeUrl+'nghe-album/'+href, 103, thumb)
    view()
		
def album_medialist(url,page=1): #102
    content = make_request(url)
    match = re.compile('<a class=".*?global-image" data-id-content=".wrap-page" href="(.*?)" title="(.*?)" data-id=".*?">\s*<span  style="background-image: url\((.*?)\).*?"></span>',re.DOTALL).findall(content)
    for (link,title,thumb) in match:
        addDir('['+ '[COLOR gold]Album[/COLOR]' + '] ' + title.strip(), link, 103, thumb)
    page = page+1
    next_page = url + '&page=' + str(page)
    addDir('[COLOR blue]Xem thêm[/COLOR]', next_page, 102, '',page=page) 		
    view()
	
def album_episodes(url): #103
    parts = url.split('.')
    url = 'http://nhacso.net/albums/ajax-get-detail-album?dataId=' + parts[len(parts)-2]
    content = make_request(url)
    data = json.loads(content)
    if len(data['songs']) == 0:
        url = 'http://nhacso.net/albums/ajax-get-detail-album?dataId=' + parts[len(parts)-2]
        content = make_request(url)
        data = json.loads(content)
    
    for song in data['songs']:
        thumb = song['link_image']
        title = song['name']
        songid = song['id']
        link = song['link_mp3']
        artist = song['singer'][0]['alias']
        data_url = 'http://nhacso.net/songs/ajax-get-detail-song?dataId=' + songid
        addDir(color_artist(title.strip(),artist.strip()), data_url, 100, thumb, playable=True)	

def album_resolveUrl(url): #100
    content = make_request(url)
    data = json.loads(content)
    mediaUrl = data['first_song']['link_mp3']
    listitem = xbmcgui.ListItem(path = mediaUrl)
    xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, listitem)

def make_request(url, headers=None):
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

def color_artist(title, artist):
    if title is not None:
        title = title.strip()
    if artist is not None:
        artist = artist.strip()
    if artist is not None and len(artist) > 0:
        return title + ' - [COLOR red]' + artist + '[/COLOR]'
    return title	  
	  
def addDir(name,url,mode,iconimage,query='',type='f',page=0,playable=False):
    u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&query="+str(query)+"&type="+str(type)+"&page="+str(page)
    ok=True
    liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
    if playable:
        liz.setProperty('IsPlayable', 'true')
    liz.setInfo( type="Video", infoLabels={ "Title": name } )
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=(not playable))
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

xbmcplugin.setContent(int(sys.argv[1]), 'movies')
params=get_params()

url=''
name=None
mode=None
query=''
type='f'
page=0

try:
    type=urllib.unquote_plus(params["type"])
except:
    pass
try:
    page=int(urllib.unquote_plus(params["page"]))
except:
    pass
try:
    query=urllib.unquote_plus(params["query"])
except:
    pass
try:
    url=urllib.unquote_plus(params["url"])
except:
    pass
try:
    name=urllib.unquote_plus(params["name"])
except:
    pass
try:
    mode=int(params["mode"])
except:
    pass

if mode==None:
  album_categories()
  
elif mode==1:
  search()
elif mode==100:
  album_resolveUrl(url)
elif mode==102:
  album_medialist(url,page)  
elif mode==103:
  album_episodes(url)

xbmcplugin.endOfDirectory(int(sys.argv[1]))
