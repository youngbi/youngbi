import sys
import urllib
import urlparse
import xbmcgui
import xbmcplugin
import xbmcaddon
import xbmc
import urllib, json


base_url = sys.argv[0]
addon_handle = int(sys.argv[1])


addon       = xbmcaddon.Addon()
addonname   = addon.getAddonInfo('name')
#xbmcgui.Dialog().ok(addonname, sys.argv[0], sys.argv[1], sys.argv[2])

args = urlparse.parse_qs(sys.argv[2][1:])


xbmcplugin.setContent(addon_handle, 'movies')

def build_url(query):
    return base_url + '?' + urllib.urlencode(query)

mode = args.get('mode', None)


url = "http://pastebin.com/raw.php?i=D1JJE060" 
response = urllib.urlopen(url);
data = json.loads(response.read())
xbmc.log(str(data["catalogues"]))


if mode is None:
    for cat in data["catalogues"]:
        foldername=cat["name"].encode('utf-8')
        xbmc.log(cat["name"].encode('utf-8'))
        url = build_url({'mode': 'folder', 'foldername': foldername, "id":str(cat["id"])})
        li = xbmcgui.ListItem(foldername, iconImage='DefaultFolder.png')
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)

    #url = build_url({'mode': 'folder', 'foldername': 'Folder Two'})
    #li = xbmcgui.ListItem(url, iconImage='DefaultFolder.png')
    #xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
    #                           listitem=li, isFolder=True)

    xbmcplugin.endOfDirectory(addon_handle)

elif mode[0] == 'folder':
    id=int(args.get('id', None)[0])
    for chan in data["catalogues"][id]["channels"]:
        xbmc.log("chan:"+str(chan))
        xbmc.log("chan ID:"+chan["id"])
        url = "plugin://plugin.video.youtube/"+chan["id"].encode('utf-8')
        li = xbmcgui.ListItem(chan["name"].encode('utf-8'))
        li.setProperty('isplayable', 'true')
        xbmcplugin.addDirectoryItem(handle=addon_handle , url=url, listitem=li, isFolder=True)



	#playlist = xbmc.PlayList( xbmc.PLAYLIST_VIDEO )
    #playlist.clear()
    #playlist.add('plugin://plugin.video.youtube/play/?video_id=B3fgR_6KIDw')
    #xbmc.Player().play('plugin://plugin.video.youtube/play/?video_id=B3fgR_6KIDw')

    #foldername = args['foldername'][0]
    #url = build_url({'mode': 'folder', 'foldername': 'Folder'+sys.argv[1]})
    #url = 'plugin://plugin.video.youtube/play/?video_id=B3fgR_6KIDw'
    #url='plugin://plugin.video.youtube/play/?video_id=B3fgR_6KIDw'
    #li = xbmcgui.ListItem(url, iconImage='DefaultVideo.png')
    #li.setInfo( type="Video", infoLabels={ "Title": 'Hiii' })
    #li.setProperty('mimetype', 'video/x-msvideo')    
    #xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)
    #xbmc.executebuiltin("XBMC.PlayMedia(plugin://plugin.video.youtube/play/?video_id=kgf55eYb26")
    #foldername = args['foldername'][0]
    url = "plugin://plugin.video.youtube/user/tinhtevideo/"
    #li = xbmcgui.ListItem(foldername + ' Videos', iconImage='DefaultVideo.png')
    #li.setProperty('IsPlayable', 'true')
    #xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)
    #playlist = xbmc.PlayList( xbmc.PLAYLIST_VIDEO )
    #playlist.clear()
    #playlist.load(url)
    #xbmc.Player().play(url, xbmcgui.ListItem('Hiii'))
    #xbmcplugin.endOfDirectory(addon_handle)
    ##li = xbmcgui.ListItem('21 March 2010 - "Introduction" video')
    ##li.setProperty('isplayable', 'true')
    #li.setProperty('Video', 'true')
    ##ytplugin_link = 'plugin://plugin.video.youtube/play/?playlist_id=PL7DBFFA1831EA52D3'    
    ##xbmcplugin.addDirectoryItem(handle=addon_handle , url=url, listitem=li, isFolder=True)
    xbmcplugin.endOfDirectory(addon_handle)