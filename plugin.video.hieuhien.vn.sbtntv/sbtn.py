# -*- coding: utf-8 -*-
import urllib,urllib2,re,xbmc,xbmcplugin,xbmcgui,xbmcaddon
myaddonsettings = xbmcaddon.Addon(id = 'plugin.video.hieuhien.vn.sbtntv')
addonpath=xbmc.translatePath("special://home/addons/plugin.video.hieuhien.vn.sbtntv")
sbtn_live_tv='https://raw.githubusercontent.com/bac-ha/repository.bacha/master/playlist/sbtnlivetv.m3u'
sbtn_youtube='https://raw.githubusercontent.com/bac-ha/repository.bacha/master/playlist/sbtn.xml'
youtube_mode = myaddonsettings.getSetting('youtube_mode')
dic = {';':'', '&amp;':'&', '&quot;':'"', '.':' ', '&#39;':'\'', '&#038;':'&', '&#039':'\'', '&#8211;':'-', '&#8220;':'"', '&#8221;':'"', '&#8230':'...', 'u0026quot':'"'}
def replace_all(text,dic):
 try:
  for a,b in dic.iteritems():
   text=text.replace(a, b)
  return text
 except:
  pass
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
def mainMenu():
 link=makeRequest(sbtn_live_tv)
 match=re.compile('#(.+?),(.+)\s*(.+)\s*').findall(link)
 for thumb,name,url in match:
  addLink(name,url,3,'%s/sbtn.png' % addonpath)
 addDir("Tin Tức - Bình Luận","http://www.sbtn.tv/vi/chương-trình-sbtn/tin-tức-bình-luận.html",1,'%s/icon.png' % addonpath)
 addDir( "Giải Trí - Đời Sống","http://www.sbtn.tv/vi/chương-trình-sbtn/giải-trí-đời-sống.html",1,'%s/icon.png' % addonpath)  
 addDir("Phóng Sự","http://www.sbtn.tv/vi/phóng-sự.html",2,'%s/icon.png' % addonpath)
 addDir( "SBTN Special","http://www.sbtn.tv/vi/sbtn-special.html",2,'%s/icon.png' % addonpath)
 #f=open('%s/sbtn.xml' % addonpath, "r")
 #link=f.read()
 #f.close()
 link=makeRequest(sbtn_youtube)
 match=re.compile('<title>(.*?)</title>\s*<link>(.*?)</link>\s*<thumbnail>(.*?)</thumbnail>').findall(link)
 for name,url,thumb in match:
  if youtube_mode == "tubelink" or youtube_mode == "0":             # type="select" or type="enum"
   getDir(name,url,None,'%s/youtube.png' % addonpath)
  elif youtube_mode == "direct" or youtube_mode == "1":
   addDir(name,url,4,'%s/youtube.png' % addonpath)
def sbtn_video_list(url):
 addDir('[COLOR magenta][B]Playlists[/B][/COLOR]',url+'/playlists?sort=dd&view=1',5,'%s/playlist.png' % addonpath)
 link=makeRequest(url+'/videos')
 link=''.join(link.splitlines()).replace('\t','')
 match=re.compile('src="//i.ytimg.com/vi/(.+?)".+?aria-label.+?>(.+?)</span>.+?href="/watch\?v=(.+?)">(.+?)</a>').findall(link)
 for thumb,duration,url,name in match:
  name=replace_all(name,dic)
  thumb='https://i.ytimg.com/vi/'+thumb
  addLink(name,'plugin://plugin.video.youtube/play/?video_id='+url,3,thumb)
 try:
  match=re.compile('data-uix-load-more-href="(.+?)"').findall(link)
  addDir('[COLOR yellow][B]Next page [/B][/COLOR][COLOR lime][B]>>[/B][/COLOR]','https://www.youtube.com'+match[0].replace('&amp;','&'),7,'%s/next.png' % addonpath)
 except:
  pass
def sbtn_playlist(url):
 link=makeRequest(url)
 link=''.join(link.splitlines()).replace('\t','')
 match=re.compile('[src|data-thumb]="//i.ytimg.com/vi/(.+?)".+?href="/playlist(.+?)">(.+?)<').findall(link)
 for thumb,url,name in match[:-1]:
  name=replace_all(name,dic)
  thumb='https://i.ytimg.com/vi/'+thumb
  addDir(name,url,6,thumb)
def sbtn_playlist_index(url):
 link=makeRequest('https://www.youtube.com/playlist'+url)
 link=''.join(link.splitlines()).replace('\t','')
 match=re.compile('data-title="(.+?)".+?href="\/watch\?v=(.+?)\&amp\;.+?data-thumb="(.+?)".+?aria-label.+?>(.+?)<\/span><\/div>').findall(link)
 for name,url,thumb,duration in match:
  name=replace_all(name,dic)
  thumb='https:'+thumb
  if '[Deleted Video]' in name:
   pass
  else:
   addLink(name,'plugin://plugin.video.youtube/play/?video_id='+url,3,thumb)
 try:
  match=re.compile('data-uix-load-more-href="(.+?)"').findall(link)
  addDir('[COLOR magenta]Next page >>[/COLOR]','https://www.youtube.com'+match[0].replace('&amp;','&'),8,'%s/next.png' % addonpath)
 except:
  pass
def next_page(url):
 req=urllib2.Request(url)
 req.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64; rv:19.0) Gecko/20100101 Firefox/19.0')
 response=urllib2.urlopen(req) 
 link=response.read()
 response.close()
 link=''.join(link.splitlines()).replace('\\','').replace('\t','')
 match=re.compile('src="//i.ytimg.com/vi/(.+?)".+?aria-label="(.+?)".+?dir="ltr" title="(.+?)".+?href="/watch\?v=(.+?)"').findall(link)
 for thumb,duration,name,url in match:
  name=replace_all(name,dic)
  thumb='https://i.ytimg.com/vi/'+thumb
  addLink(name,'plugin://plugin.video.youtube/play/?video_id='+url,3,thumb)
 try:
  match=re.compile('data-uix-load-more-href="(.+?)"').findall(link)
  addDir('[COLOR yellow][B]Next page [/B][/COLOR][COLOR lime][B]>>[/B][/COLOR]','https://www.youtube.com'+match[0].replace('&amp;','&'),7,'%s/next.png' % addonpath)
 except:
  pass
def next_page_playlist(url):
 req=urllib2.Request(url)
 req.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64; rv:19.0) Gecko/20100101 Firefox/19.0')
 response=urllib2.urlopen(req) 
 link=response.read()
 response.close()
 link=''.join(link.splitlines()).replace('\\','').replace('\t','')
 match=re.compile('data-video-id="(.+?)".+?data-title="(.+?)".+?data-thumb="//i.ytimg.com/vi/(.+?)".+?aria-label="(.+?)"').findall(link)
 for url,name,thumb,duration in match:
  name=replace_all(name,dic)
  thumb='https://i.ytimg.com/vi/'+thumb
  addLink(name,'plugin://plugin.video.youtube/play/?video_id='+url,3,thumb)
 try:
  match=re.compile('data-uix-load-more-href="(.+?)"').findall(link)
  addDir('[COLOR magenta]Next page >>[/COLOR]','https://www.youtube.com'+match[0].replace('&amp;','&'),8,'%s/next.png' % addonpath)
 except:
  pass 
def addDir(name,url,mode,iconimage):
 u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
 ok=True
 liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
 liz.setInfo( type="Video", infoLabels={ "Title": name } )
 ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
 return ok
def getDir(name,url,mode,iconimage):
 u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
 ok=True
 liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
 liz.setInfo( type="Video", infoLabels={ "Title": name } )
 if ('www.youtube.com/user/' in url) or ('www.youtube.com/channel/' in url):
  u = 'plugin://plugin.video.youtube/%s/%s/' % (url.split( '/' )[-2], url.split( '/' )[-1])
 ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
 return ok
def categories(url):
 link=makeRequest(url)
 if "tin-tức-bình-luận" in url:
  match=re.compile('<li class=".*?leaf"><a href="http://www.sbtn.tv/vi/tin-tức-bình-luận/(.+?)" title="">(.+?)</a></li>').findall(link)
  for url,name in match:
   addDir(name.replace("&amp;", "và"),"http://www.sbtn.tv/vi/tin-tức-bình-luận/"+url,2,'%s/icon.png' % addonpath)
  match=re.compile('<li class=".*?leaf"><a href="http://www.sbtn.tv/vi/tin-tuc-binh-luan/(.+?)" title="">(.+?)</a></li>').findall(link)
  for url,name in match:
   addDir(name.replace("&amp;", "và"),"http://www.sbtn.tv/vi/tin-tuc-binh-luan/"+url,2,'%s/icon.png' % addonpath)                
 else:
  match=re.compile('<li class=".*?leaf"><a href="http://www.sbtn.tv/vi/giải-trí-đời-sống/(.+?)" title="">(.+?)</a></li>').findall(link)
  for url,name in match:
   addDir(name.replace("&amp;", "và"),"http://www.sbtn.tv/vi/giải-trí-đời-sống/"+url,2,'%s/icon.png' % addonpath) 
  match=re.compile('<li class=".*?leaf"><a href="http://www.sbtn.tv/vi/giai-tri-doi-song/(.+?)" title="">(.+?)</a></li>').findall(link)
  for url,name in match:
   addDir(name.replace("&amp;", "và"),"http://www.sbtn.tv/vi/giai-tri-doi-song/"+url,2,'%s/icon.png' % addonpath)                 
def index(url):
 link=makeRequest(url)
 match=re.compile('<a href="(.+?)" rel="tag" title="(.+?)">').findall(link)
 for url,name in match:
  name=replace_all(name,dic)
  addLink(name.replace("&amp;", "và"),"http://www.sbtn.tv"+url,3,'') 
 match=re.compile('<li class="pager-next"><a title="Đến (.+?)" href="(.+?)">').findall(link)               
 for name,url in match:
  url="http://www.sbtn.tv"+url.replace("&amp;", "&")
  #addDir(name.replace("t", "T"),url,2,next)
  addDir(name.replace("trang sau", "Next page >>"),url,2,'%s/next.png' % addonpath)  
def makeRequest(url):
 req=urllib2.Request(url)
 req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:19.0) Gecko/20100101 Firefox/19.0')
 response=urllib2.urlopen(req)
 link=response.read()
 response.close()  
 return link        
def videoLink(url):
 if "http://www.sbtn.tv" in url:
  link=makeRequest(url)
  videoUrl=re.compile('<source src="(.+?)" type="video/mp4" />').findall(link)[0]
 else:
  videoUrl=url
 item=xbmcgui.ListItem(name, path=videoUrl)
 xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)  
 return
def addLink(name,url,mode,iconimage):
 u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
 ok=True
 liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
 liz.setInfo( type="Video", infoLabels={ "Title": name } )
 liz.setProperty('IsPlayable', 'true')
 ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz)
 return ok
params=get_params()
url=None
name=None
mode=None
try:url=urllib.unquote_plus(params["url"])
except:pass
try:name=urllib.unquote_plus(params["name"])
except:pass
try:mode=int(params["mode"])
except:pass
if mode==1:categories(url)
elif mode==2:index(url)  
elif mode==3:videoLink(url)
elif mode==4:sbtn_video_list(url)
elif mode==5:sbtn_playlist(url)
elif mode==6:sbtn_playlist_index(url)
elif mode==7:next_page(url)
elif mode==8:next_page_playlist(url)
else:mainMenu()   
xbmcplugin.endOfDirectory(int(sys.argv[1]))