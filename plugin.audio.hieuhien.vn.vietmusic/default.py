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
import urllib, urllib2, os, xbmcplugin, xbmcgui, xbmcaddon, urlfetch, re, random
from BeautifulSoup import BeautifulSoup

addon = xbmcaddon.Addon(id='plugin.audio.hieuhien.vn.vietmusic')
language = addon.getLocalizedString
home = addon.getAddonInfo('path')
icon = xbmc.translatePath( os.path.join( home, 'icon.png' ) )
logos = xbmc.translatePath( os.path.join( home, 'logos\\' ) )

def main(): # menu chính
  add_dir('[COLOR red]Tìm Kiếm[/COLOR]','timkiem', 9, logos+'Search.png', '', type, 0)  
  add_dir('Xếp Hạng', 'mp3/hot/', 1,  logos+'vietmusic.png', '', type, 0)
  add_dir('Video Clip','hd/video/', 1,  logos+'vietmusic.png', '', type, 0)
  add_dir('Playback','mp3/beat-playback/', 1,  logos+'vietmusic.png', '', type, 0)
  add_dir('Việt Nam','mp3/vietnam/', 1,  logos+'vietmusic.png', '', type, 0)
  add_dir('Âu, Mỹ','mp3/us-uk/', 1,  logos+'vietmusic.png', '', type, 0)
  add_dir('Nhạc Hoa','mp3/chinese/', 1,  logos+'vietmusic.png', '', type, 0)
  add_dir('Nhạc Hàn','mp3/korea/', 1,  logos+'vietmusic.png', '', type, 0)
  add_dir('Nước Khác','mp3/other/', 1,  logos+'vietmusic.png', '', type, 0)
  xbmc.executebuiltin('Container.SetViewMode(500)')
  
def categories(url, mode): #1 lấy danh sách thể loại
  content = make_request('http://chiasenhac.com')
  soup = BeautifulSoup(str(content), convertEntities=BeautifulSoup.HTML_ENTITIES)
  items = soup.find('div',{'id' : 'myslidemenu'}).find('ul').findAll('li')
  for item in items:
    href = item.a.get('href')
    if href is not None:
      try:
        if href.startswith(url) and len(href) > len(url):
          prefix = ''
          if url != 'mp3/hot/' and url !='hd/video/':
            prefix = '[COLOR gold]Songs[/COLOR]: '
          add_dir(prefix + item.a.text, 'http://chiasenhac.com/' + href, 2, logos+'vietmusic.png', query, type, 0)
      except:
        pass
  for item in items:
    href = item.a.get('href')
    if href is not None:
      try:
        if url != 'mp3/hot/' and url !='hd/video/' and href.startswith(url) and len(href) > len(url):
          add_dir('[COLOR blue]Albums[/COLOR]: ' + item.a.text, 'http://chiasenhac.com/' + href + 'album.html', 3, logos+'vietmusic.png', query, type, 0)
      except:
        pass		
  return
  
def categories_group(url = None, page = 0): #3 lấy danh sách nhóm thể loại
  if url == '':
    content = make_request('http://chiasenhac.com')
    soup = BeautifulSoup(str(content), convertEntities=BeautifulSoup.HTML_ENTITIES)
    items = soup.find('div',{'id' : 'myslidemenu'}).find('ul').findAll('li')
    for item in items:
      if item.a is not None:
        href = item.a.get('href')
        if href is not None:
          try:
            add_dir(item.a.text, 'http://chiasenhac.com/' + href, 2, logos+'vietmusic.png', query, type, 0)
          except:
            pass			
    return
  # bảng xếp hạng
  if '/mp3/hot/' in url:  
    content = make_request(url)
    soup = BeautifulSoup(str(content), convertEntities=BeautifulSoup.HTML_ENTITIES)
    tables = soup.findAll('tr',{'class' : '2'})
    for table in tables:
      item = table.find('a', {'class':'musictitle'})
      if item is not None:
        href = item.get('href')
        text = item.get('title')
        if text is not None:
          if 'chiasenhac.com' not in href:
            href = 'http://chiasenhac.com/' + href
          quality = table.find('span', {'style':['color: red','color: orange','color: darkblue','color: darkgreen']})
          if quality is not None:
            quality = '[' + quality.text + '] '
          else:
            quality = '';
          try:
            t1 = table.find('div', {'class':'gensmall'}).text
            t2 = t1 + item.text
            t3 = table.find('div', {'class':'musicinfo'}).text
          except:
            t3 = ''
            t2 = ''
            pass

          text = text + ' - [COLOR firebrick]' + t3.replace(t2,'') + '[/COLOR]'
          
          add_link('', quality + text, 0, href, 100, logos+'file.png', '')		  
    return   
  # video clip
  if '/hd/video/' in url:
    content = make_request(url)
    soup = BeautifulSoup(str(content), convertEntities=BeautifulSoup.HTML_ENTITIES)
    tables = soup.findAll('div',{'class' : 'list-l list-1'})
    for table in tables:
      item = table.find('div', {'class':'info'}).find('a')
      href = item.get('href')
      text = item.text
      text_casi = table.find('div', {'class':'info'}).find('p').text

      text = text + ' - [COLOR firebrick]' + text_casi + '[/COLOR]'

      if 'playlist.chiasenhac.com' not in href:
        href = 'http://playlist.chiasenhac.com/' + href
      img = table.find('div', {'class':'gensmall'}).find('a').find('img')
      quality = table.find('span', {'style':['color: red','color: orange','color: darkblue','color: darkgreen']})
      if quality is not None:
        quality = '[' + quality.text + '] '
      else:
        quality = '';
      add_link('', quality + text, 0, href, 100, img.get('src'), '')

    url_parts = url.split('/')
    if page == 0:
      page = 2
    url_parts[len(url_parts) -1] = 'new' + str(page) + '.html'
    add_dir(u'Trang tiếp >>', '/'.join(url_parts) , 2, logos+'next.png', query, type, page + 1)	
    return
	
  # playback + thể loại
  if '/mp3/beat-playback/' in url or '/mp3/vietnam/' in url or '/mp3/thuy-nga/' in url or '/mp3/us-uk/' in url or '/mp3/chinese/' in url or '/mp3/korea/' in url or '/mp3/other/' in url:
    content = make_request(url)
    soup = BeautifulSoup(str(content), convertEntities=BeautifulSoup.HTML_ENTITIES)
    if page == 0:
      tables = soup.findAll('div',{'class' : 'list-r list-1'})
      for table in tables:
        item = table.find('div', {'class':'text2'}).find('a')
        href = item.get('href')
        text = item.text
        text_casi = table.find('div', {'class':'text2'}).find('p').text

        text = text + ' - [COLOR firebrick]' + text_casi + '[/COLOR]'

        if 'playlist.chiasenhac.com' not in href:
          href = 'http://playlist.chiasenhac.com/' + href
        quality = table.find('div',{'class':'texte2'}).find('span', {'style':['color: red','color: orange','color: darkblue','color: darkgreen']})
        if quality is not None:
          quality = '[' + quality.text + '] '
        else:
          quality = '';
        add_link('', quality + text, 0, href, 100, logos+'file.png', '')
    else:
      tables = soup.findAll('tr',{'class' : '2'})
      for table in tables:
        item = table.find('a', {'class':'musictitle'})
        if item is not None:
          href = item.get('href')
          text = item.parent.text.replace(item.text, item.text + ' - ')
          if 'chiasenhac.com' not in href:
            href = 'http://chiasenhac.com/' + href
          quality = table.find('span', {'style':['color: red','color: orange','color: darkblue','color: darkgreen']})
          if quality is not None:
            quality = '[' + quality.text + '] '
          else:
            quality = '';
          tt =text.split('-')
          if len(tt) == 2:
            text = tt[0] + ' - [COLOR firebrick]' + tt[1] + '[/COLOR]'
          add_link('', quality + text, 0, href, 100, logos+'file.png', '')
    
    url_parts = url.split('/')
    if page == 0:
      page = 1
    url_parts[len(url_parts) -1] = 'new' + str(page) + '.html'
    add_dir(u'Trang tiếp >>', '/'.join(url_parts) , 2, logos+'next.png', query, type, page + 1)	
    return	
  return

def get_chiasenhac_album(url = None, page = 0): # lấy danh sách album
  album_url = url

  content = make_request(album_url)
  soup = BeautifulSoup(str(content), convertEntities=BeautifulSoup.HTML_ENTITIES)

  albums_thumbs = {}
  albums = soup.findAll('span',{'class' : 'genmed'})
  for album in albums:
    a = album.find('a').get('href')
    b = album.find('img').get('src')
    albums_thumbs[a] = b

  albums = soup.findAll('span',{'class' : 'gen'})
  for album in albums:
    href = album.find('a', {'class' : 'musictitle'})
    title = href.get('title')
    link = href.get('href')
    thumb = None
    if link in albums_thumbs:
      thumb = albums_thumbs[link]
    
    quality = href.parent.find('span', {'style':['color: red','color: orange','color: darkblue','color: darkgreen']})
    if quality is not None:
      quality = '[' + quality.text + '] '
    else:
      quality = '';
    add_dir(quality + title, link, 4, thumb, query, type, 0)
  
  url_parts = url.split('/')
  if page == 0:
    page = 2
  if page < 3:
    url_parts[len(url_parts) -1] = 'album' + str(page) + '.html'
    add_dir(u'Trang tiếp >>', '/'.join(url_parts) , 3, logos+'next.png', query, type, page + 1)
  return   

def get_chiasenhac_album_songs(url = None): # lấy danh sách nhạc trong album
  content = make_request(url)
  soup = BeautifulSoup(str(content), convertEntities=BeautifulSoup.HTML_ENTITIES)

  albums = soup.find('div',{'id':'playlist'}).findAll('span',{'class' : 'gen'})
  for album in albums:
    a = album.findAll('a')
    if (len(a) == 3):
      href = 'http://chiasenhac.com/' + a[1].get('href')
      text = album.text
      tt =text.split('-')
      if len(tt) == 2:
        text = tt[0] + ' - [COLOR firebrick]' + tt[1] + '[/COLOR]'

      add_link('', text, 0, href, 100, logos+'file.png', '')      
  return 

def search_group(): # menu search
  add_dir('Tìm theo tên bài hát','', 10, logos+'Search.png', '', type, 0)#210
  add_dir('Tìm theo tên album','', 11, logos+'Search.png', '', type, 0) #211  
  add_dir('Tìm theo tên ca sỹ/ban nhạc','', 13, logos+'Search.png', '', type, 0) #213
  add_dir('Tìm video','', 12, logos+'Search.png', '', type, 0) #212
  
'''  
def show_search_recent(mode): 
  add_dir('Tìm kiếm','', mode - 200, icon, '', type, 0)
  saved_search = addon.getSetting('saved_search_' + str(mode - 200))
  if saved_search is not None:
    items=saved_search.split('~')
    for i in range(len(items)):
      if len(items[i]) > 0:
        add_dir(items[i],'', mode - 200, icon, items[i], type, 0)
'''

def search(query = '', page = 0, mode = 10, cat = 'music'): # tìm kiếm theo tên bài hát, ca sĩ, video clip
  if len(query)==0:
    query = common.getUserInput('Search', '')
    if query is None:
      return
    saved = addon.getSetting('saved_search_' + str(mode))
    if saved is None:
      saved = query + '~'
      addon.setSetting('saved_search_' + str(mode),saved)
    else:
      if query + '~' in saved:
        saved = saved.replace(query + '~','')
      saved = query + '~' + saved
      addon.setSetting('saved_search_' + str(mode),saved)

  if page == 0:
    page = 1

  url = 'http://search.chiasenhac.com/search.php?s=' + urllib.quote(query) + '&page=' + str(page) + '&cat=' + cat
  if 'artist' in cat:
    url = 'http://search.chiasenhac.com/search.php?s=' + urllib.quote(query) + '&page=' + str(page) + '&cat=music&mode=' + cat
  
  content = make_request(url)
  soup = BeautifulSoup(str(content), convertEntities=BeautifulSoup.HTML_ENTITIES)
  items = soup.find('table',{'class':'tbtable'}).findAll('tr')
  for ii in items:
    item = ii.find('div',{'class':'tenbh'})
    if item is not None:
      a = item.find('a')
      p = item.findAll('p')[1]
      if a is not None:
        href = a.get('href')
        if 'chiasenhac.com' not in href:
          href = 'http://chiasenhac.com/' + href   
        quality = ii.find('span',{'class':'gen'}).find('span', {'style':['color: red','color: orange','color: darkblue','color: darkgreen']})
        if quality is not None:
          quality = '[' + quality.text + '] '
        else:
          quality = '';
        add_link('', quality + a.text + ' - [COLOR firebrick]' + p.text + '[/COLOR]', 0, href, 100, logos+'file.png', '')

  add_dir(u'Trang tiếp >>', '', mode, logos+'next.png', query, type, page + 1)  
  return

def search_albums(start, query, page): # tìm kiếm theo album
  mode = 11
  if len(query) == 0:
    query = common.getUserInput('Search', '')
    if query is None:
      return
    saved = addon.getSetting('saved_search_' + str(mode))
    if saved is None:
      saved = query + '~'
      addon.setSetting('saved_search_' + str(mode),saved)
    else:
      if query + '~' in saved:
        saved = saved.replace(query + '~','')
      saved = query + '~' + saved
      addon.setSetting('saved_search_' + str(mode),saved)
  if page == 0:
    page = 1
  url = 'http://search.chiasenhac.com/search.php?mode=album&s=' + urllib.quote_plus(query) + '&page=' + str(page) + '&start=' + start
  content = make_request(url)
  soup = BeautifulSoup(str(content), convertEntities=BeautifulSoup.HTML_ENTITIES)
  thumbs = soup.find('table',{'class' : 'tbtable'}).findAll('span',{'class' : 'genmed'})
  albums_thumbs = {}
  for thumb in thumbs:
    img = thumb.find('img')
    href = thumb.find('a')
    if (img is not None) and (href is not None):
      a = img.get('src');
      b = href.get('href')
      albums_thumbs[b] = a

  albums = soup.find('table',{'class' : 'tbtable'}).findAll('span',{'class' : 'gen'})
  for album in albums:
    href = album.find('a')
    if href is not None:
      link = href.get('href')
      title = album.text.replace(u'(Xem chi tiết...)','').replace('Lossless',' - Lossless').replace('320kbps',' - 320kbps').replace('192kbps',' - 192kbps').replace('128kbps',' - 128kbps')
      thumb = None
      if link in albums_thumbs:
        thumb = albums_thumbs[link]
      
      add_dir(title, link, 4, thumb, query, type, 0)
  xt = soup.find('a',{'class' : 'xt'})
  if xt is not None:
    href = xt.get('href')
    parts = href.split('=')
    start = parts[len(parts) - 1]
    add_dir(u'Trang tiếp >>', start, mode, logos+'next.png', query, type, page + 1)	
  return

def resolve_url(url):#100
    content = make_request(url)
    vid = re.compile('decodeURIComponent\("(.+stream.+?)"\)').findall(content)[-1]
    if 'http://' not in vid:
	    mediaUrl = urllib.unquote(vid).replace('/m4a/','/flac/').replace('.m4a.','.flac.')
    if '/m4a/' in vid and '.m4a.' in vid:
	    mediaUrl = vid.replace('/m4a/','/flac/').replace('.m4a.','.flac.')
    item = xbmcgui.ListItem(path = mediaUrl)		
    xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)
    return
	
def _makeCookieHeader(cookie):
      cookieHeader = ""
      for value in cookie.values():
          cookieHeader += "%s=%s; " % (value.key, value.value)
      return cookieHeader

def make_request(url, headers=None):
        if headers is None:
            headers = {'User-agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:15.0) Gecko/20100101 Firefox/15.0.1',
                       'Cookie':'vq=i%3A1080%3B; mq=i%3A500%3B', 'Referer' : 'http://www.google.com'}
        try:
            req = urllib2.Request(url,headers=headers)
            f = urllib2.urlopen(req)
            body=f.read()
            return body
        except urllib2.URLError, e:
            print 'We failed to open "%s".' % url
            if hasattr(e, 'reason'):
                print 'We failed to reach a server.'
                print 'Reason: ', e.reason
            if hasattr(e, 'code'):
                print 'We failed with error code - %s.' % e.code
  
def add_link(date, name, duration, href, mode, thumb, desc):
    description = date+'\n\n'+desc
    u=sys.argv[0]+"?url="+urllib.quote_plus(href)+"&mode="+str(mode)
    liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=thumb)
    liz.setInfo(type="Video", infoLabels={ "Title": name, "Plot": description, "Duration": duration})
    liz.setProperty('IsPlayable', 'true')
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz)

def add_dir(name,url,mode,iconimage,query='',type='f',page=0):
    u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&query="+str(query)+"&type="+str(type)+"&page="+str(page)
    ok=True
    liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
    liz.setInfo( type="Video", infoLabels={ "Title": name } )
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
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

try:type=urllib.unquote_plus(params["type"])
except:pass
try:page=int(urllib.unquote_plus(params["page"]))
except:pass
try:query=urllib.unquote_plus(params["query"])
except:pass
try:url=urllib.unquote_plus(params["url"])
except:pass
try:name=urllib.unquote_plus(params["name"])
except:pass
try:mode=int(params["mode"])
except:pass

if mode==None:
  try:main()
  except:pass
elif mode==1:
  try:categories(url,mode)
  except:pass
elif mode==2:
  try:categories_group(url,page)
  except:pass
elif mode==3:
  try:get_chiasenhac_album(url, page)
  except:pass
elif mode==4:
  try:get_chiasenhac_album_songs(url)
  except:pass
elif mode==9:
  try:search_group()
  except:pass   
elif mode==100:
  try:resolve_url(url)
  except:pass
elif mode==210:
  try:show_search_recent(mode)
  except:pass
elif mode==10:
  try:search(query,page,mode,'music')
  except:pass
elif mode==211:
  try:show_search_recent(mode)
  except:pass
elif mode==11:
  try:search_albums(url,query,page)
  except:pass  
elif mode==213:
  try:show_search_recent(mode)
  except:pass
elif mode==13:
  try:search(query,page,mode,'artist')
  except:pass
elif mode==212:
  try:show_search_recent(mode)
  except:pass
elif mode==12:
  try:search(query,page,mode,'video')
  except:pass

xbmcplugin.endOfDirectory(int(sys.argv[1]))