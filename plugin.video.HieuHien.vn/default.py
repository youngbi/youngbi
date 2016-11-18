# -*- coding: utf-8 -*-
 
"""
Copyright (C) 2015 PodGod

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
"""

import urllib, urllib2, sys, re, os, unicodedata, cookielib, random, shutil
import xbmc, xbmcgui, xbmcplugin, xbmcaddon, base64, json
from operator import itemgetter, attrgetter

plugin_handle = int(sys.argv[1])
mysettings = xbmcaddon.Addon(id = 'plugin.video.HieuHien.vn')
profile = mysettings.getAddonInfo('profile')
home = mysettings.getAddonInfo('path')
getSetting = xbmcaddon.Addon().getSetting
enable_adult_section = mysettings.getSetting('enable_adult_section')
enable_tvguide = mysettings.getSetting('enable_tvguide')
enable_thongbao = mysettings.getSetting('enable_thongbao')
enable_youtube_channels = mysettings.getSetting('enable_youtube_channels')
enable_channel_tester = mysettings.getSetting('enable_channel_tester')
enable_local_tester = mysettings.getSetting('enable_local_tester')
server_notification = mysettings.getSetting('enable_server_notification')
enable_public_uploads = mysettings.getSetting('enable_public_uploads')
enable_links_to_tutorials = mysettings.getSetting('enable_links_to_tutorials')
local_path = mysettings.getSetting('local_path')
enable_online_tester = mysettings.getSetting('enable_online_tester')
online_path = mysettings.getSetting('online_path')
enable_iptvsimple_playlist = mysettings.getSetting('enable_iptvsimple_playlist')
choose_server_group = mysettings.getSetting('choose_server_group')
enable_server_selection = mysettings.getSetting('enable_server_selection')
select_a_server = mysettings.getSetting('select_a_server')
enable_other_sources = mysettings.getSetting('enable_other_sources')
enable_other_addons1 = mysettings.getSetting('enable_other_addons1')
enable_other_addons2 = mysettings.getSetting('enable_other_addons2')
enable_other_addons3 = mysettings.getSetting('enable_other_addons3')
enable_other_addons4 = mysettings.getSetting('enable_other_addons4')
enable_other_addons5 = mysettings.getSetting('enable_other_addons5')
enable_other_addons6 = mysettings.getSetting('enable_other_addons6')
viet_mode = mysettings.getSetting('viet_mode')
youtube_mode = mysettings.getSetting('youtube_mode')

local_thongbaomoi = xbmc.translatePath(os.path.join(home, 'thongbaomoi.txt'))
local_vietradio = xbmc.translatePath(os.path.join(home, 'vietradio.m3u'))
fanart = xbmc.translatePath(os.path.join(home, 'fanart.jpg'))
icon = xbmc.translatePath(os.path.join(home, 'icon.png'))

xml_regex = '<title>(.*?)</title>\s*<link>(.*?)</link>\s*<thumbnail>(.*?)</thumbnail>'
m3u_thumb_regex = 'tvg-logo=[\'"](.*?)[\'"]'
group_title_regex = 'group-title=[\'"](.*?)[\'"]'
m3u_regex = '#(.+?),(.+)\s*(.+)\s*'
adult_regex = '#(.+?)group-title="Adult",(.+)\s*(.+)\s*'
adult_regex2 = '#(.+?)group-title="Public-Adult",(.+)\s*(.+)\s*'
ondemand_regex = '[ON\'](.*?)[\'nd]'
server_regex = '<server>(.*?)</server>'
media_regex = '<medialink>(.*?)</medialink>'
yt = 'https://www.youtube.com/'
text = 'http://pastebin.com/raw.php?i=Zr0Hgrbw'
m3u = 'WVVoU01HTkViM1pNTTBKb1l6TlNiRmx0YkhWTWJVNTJZbE01ZVZsWVkzVmpSMmgzVURKck9WUlViRWxTYXpWNVZGUmpQUT09'.decode('base64')
dic = {';':'', '&amp;':'&', '&quot;':'"', '.':' ', '&#39;':'\'', '&#038;':'&', '&#039':'\'', '&#8211;':'-', '&#8220;':'"', '&#8221;':'"', '&#8230':'...', 'u0026quot':'"'}
iconpath = 'YUhSMGNITTZMeTl5WVhjdVoybDBhSFZpZFhObGNtTnZiblJsYm5RdVkyOXRMMk5zYjNWa2JHbHpkQzl5WlhCdmMybDBiM0o1TG5acGNHeHBjM1F2YldGemRHVnlMMDE1Um05c1pHVnlMM1pwWlhScFkyOXVjdz09'.decode('base64').decode('base64')
SRVlist = 'YUhSMGNITTZMeTl5WVhjdVoybDBhSFZpZFhObGNtTnZiblJsYm5RdVkyOXRMMk5zYjNWa2JHbHpkQzl5WlhCdmMybDBiM0o1TG5acGNHeHBjM1F2YldGemRHVnlMMDE1Um05c1pHVnlMM05sY25abGNuTXVkSGgw'.decode('base64').decode('base64')
medialink = 'YUhSMGNITTZMeTl5WVhjdVoybDBhSFZpZFhObGNtTnZiblJsYm5RdVkyOXRMMk5zYjNWa2JHbHpkQzl5WlhCdmMybDBiM0o1TG5acGNHeHBjM1F2YldGemRHVnlMMDE1Um05c1pHVnlMMjFsWkdsaGJHbHVheTUwZUhRPQ=='.decode('base64').decode('base64')
tubemenu = 'YUhSMGNITTZMeTluYjI4dVoyd3ZZVkZhU25KcA=='.decode('base64').decode('base64')
childrentube = 'YUhSMGNEb3ZMMmR2Ynk1bmJDOUZja3hNZGpjPQ=='.decode('base64').decode('base64')
ytsearchicon = 'YUhSMGNITTZMeTl5WVhjdVoybDBhSFZpZFhObGNtTnZiblJsYm5RdVkyOXRMMk5zYjNWa2JHbHpkQzl5WlhCdmMybDBiM0o1TG5acGNHeHBjM1F2YldGemRHVnlMMDE1Um05c1pHVnlMM2x2ZFhSMVltVXZhV052Ym5NdldWUlRaV0Z5WTJndWNHNW4='.decode('base64').decode('base64')
iptvsimple = xbmc.translatePath("special://home/userdata/addon_data/pvr.iptvsimple/iptv.m3u.cache")
public_uploads = 'plugin://plugin.program.chrome.launcher/?kiosk=no&mode=showSite&stopPlayback=no&url=https%3a%2f%2fscript.google.com%2fmacros%2fs%2fAKfycbxwkVU0o3lckrB5oCQBnQlZ-n8CMx5CZ_ajq6Y3o7YHSTFbcODk%2fexec'
otheraddons1 = 'YUhSMGNEb3ZMMmR2Ynk1bmJDOUNkMWh5ZDBrPQ=='.decode('base64').decode('base64')
List1 = 'YUhSMGNEb3ZMMnR2WkdrdVkyTnNaQzVwYnc9PQ=='.decode('base64').decode('base64')
otheraddons2 = 'YUhSMGNEb3ZMMmR2Ynk1bmJDOUliRWRQY1hBPQ=='.decode('base64').decode('base64')
List2 = 'YUhSMGNEb3ZMM2d1WTI4dlpHSmphREF4'.decode('base64').decode('base64')
otheraddons3 = 'YUhSMGNEb3ZMMmR2Ynk1bmJDOUxOR1IxVjFnPQ=='.decode('base64').decode('base64')
List3 = 'YUhSMGNEb3ZMMkZwYnk1alkyeHZkV1IwZGk1dmNtY3ZhMjlrYVE9PQ=='.decode('base64').decode('base64')
otheraddons4 = 'YUhSMGNEb3ZMMmR2Ynk1bmJDOXhhbkJFY1ZFPQ=='.decode('base64').decode('base64')
List4 = 'YUhSMGNEb3ZMMmR2TW13dWFXNXJMMnR2WkdrPQ=='.decode('base64').decode('base64')
otheraddons5 = 'YUhSMGNEb3ZMMmR2Ynk1bmJDOXVjMDVyVmtzPQ=='.decode('base64').decode('base64')
List5 = 'YUhSMGNEb3ZMMmR2Ynk1bmJDOVNNVUZHY0RBPQ=='.decode('base64').decode('base64')
otheraddons6 = 'YUhSMGNEb3ZMMmR2Ynk1bmJDOUpRV0ZKTkhnPQ=='.decode('base64').decode('base64')
othersources = 'YUhSMGNITTZMeTluYjI4dVoyd3ZVemQ1TlRCcw=='.decode('base64').decode('base64')
adultaddons = 'YUhSMGNITTZMeTl5WVhjdVoybDBhSFZpZFhObGNtTnZiblJsYm5RdVkyOXRMMk5zYjNWa2JHbHpkQzl5WlhCdmMybDBiM0o1TG5acGNHeHBjM1F2YldGemRHVnlMMDE1Um05c1pHVnlMMkZrZFd4MFlXUmtiMjV6TG5SNGRBPT0='.decode('base64').decode('base64')


def make_request(url):
	try:
		req = urllib2.Request(url)
		req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:19.0) Gecko/20100101 Firefox/19.0')
		response = urllib2.urlopen(req)
		link = response.read()
		response.close()
		return link
	except:
		pass

def read_file(file):
	try:
		f = open(file, 'r')
		content = f.read()
		f.close()
		return content
	except:
		pass

def srv_list():
	#match = re.compile(server_regex).findall(read_file(os.path.expanduser(r'~\Desktop\servers.txt')))
	match = re.compile(server_regex).findall(make_request(SRVlist))
	i=0
	while i < len(match):
		match[i] = match[i].decode('base64').decode('base64')
		i+=1 
	return match

List6 = srv_list()[-1]
if choose_server_group == '0':
	CCLOUDTV_SRV_URL = [List1, List2, List3, List4, List5, List6]
else:
	CCLOUDTV_SRV_URL = srv_list()

def media_link():
	#match = re.compile(media_regex).findall(read_file(os.path.expanduser(r'~\Desktop\medialink.txt')))
	match =  re.compile(media_regex).findall(make_request(medialink))
	i=0
	while i < len(match):
		match[i] = match[i].decode('base64').decode('base64')
		i+=1
	return match

def server_message(message, timeout = 5000):
	xbmc.executebuiltin((u'XBMC.Notification("%s", "%s", %s, %s)' % ('[B]cCloud.tv[/B]', message, timeout, icon)).encode("utf-8"))

def select_server():
	try:
		if (enable_iptvsimple_playlist == 'true') and (os.path.exists(iptvsimple)) and ('Welcome to cCloudTV' in (read_file(iptvsimple))):
			if server_notification == 'true':
				server_message('Using [COLOR chocolate]cCloudTV playlist[/COLOR] from [COLOR chocolate]IPTV Simple.[/COLOR]')
			#print ('Using cCloudTV playlist from IPTV Simple.')
			return (read_file(iptvsimple))
		elif enable_server_selection == 'true':
			if select_a_server == '0':
				server = List1
			elif select_a_server == '1':
				server = List2
			elif select_a_server == '2':
				server = List3
			elif select_a_server == '3':
				server = List4
			elif select_a_server == '4':
				server = List5
			elif select_a_server == '5':
				server = List6
			content = make_request(server)
			if server_notification == 'true':
				if content is None:
					#print ("Chosen server " + select_a_server + " is offline.")
					server_message("[COLOR red]Server " + select_a_server + " is offline. Choose another server.[/COLOR]")
				else:
					#print ("Currently using chosen server " + select_a_server)
					server_message("Currently using [COLOR brown]chosen server " + select_a_server + '[/COLOR]')
					return content
			else:
				if content is None:
					#print ("Chosen server " + select_a_server + " is offline.")
					return content
				else:
					#print ("Currently using [COLOR brown]chosen server " + select_a_server + '[/COLOR]')
					return content
		else:
			for server in (CCLOUDTV_SRV_URL):
				#print ("Checking server " + str(CCLOUDTV_SRV_URL.index(server)))
				content = make_request(server)
				if content is None:
					#print ("Server " + str(CCLOUDTV_SRV_URL.index(server)) + ": offline")
					server = CCLOUDTV_SRV_URL[CCLOUDTV_SRV_URL.index(server) + 1]
				else:
					#print ("Server " + str(CCLOUDTV_SRV_URL.index(server)) + ": online")
					#print ("Using server " + str(CCLOUDTV_SRV_URL.index(server)))
					if server_notification == 'true':
						if str(server) == str(CCLOUDTV_SRV_URL[-1]):
							server_message('[COLOR magenta] Backup server[/COLOR] is currently [COLOR magenta]online[/COLOR].')
						else:
							server_message('Server ' + str(CCLOUDTV_SRV_URL.index(server)) + ' is currently online.')
					return content
	except:
		server_message('[COLOR red]All cCloud TV servers seem to be down. Please try again in a few minutes.[/COLOR]')

def replace_all(text, dic):
	try:
		for a, b in dic.iteritems():
			text = text.replace(a, b)
		return text
	except:
		pass

def platform():
	if xbmc.getCondVisibility('system.platform.android'):
		return 'android'
	elif xbmc.getCondVisibility('system.platform.linux'):
		return 'linux'
	elif xbmc.getCondVisibility('system.platform.windows'):
		return 'windows'
	elif xbmc.getCondVisibility('system.platform.osx'):
		return 'osx'
	elif xbmc.getCondVisibility('system.platform.atv2'):
		return 'atv2'
	elif xbmc.getCondVisibility('system.platform.ios'):
		return 'ios'

def main():
	
	
	if enable_other_addons1 == 'true':
		addDir('PHIM TRUYỆN', 'NoLinkRequired', 100, 'http://goo.gl/tOBhgd', fanart)
		
	if enable_other_addons2 == 'true':
		addDir('TRUYỀN HÌNH', 'NoLinkRequired', 102, 'http://goo.gl/M0NCZA', fanart)	
	
	if enable_other_addons3 == 'true':
		addDir('ÂM NHẠC', 'NoLinkRequired', 103, 'http://goo.gl/PBy2cd', fanart)	
	
	if enable_other_addons4 == 'true':
		addDir('THỂ THAO', 'NoLinkRequired', 104, 'http://goo.gl/zn28G2', fanart)	
	
	if enable_other_addons5 == 'true':
		addDir('PHIM NƯỚC NGOÀI', 'NoLinkRequired', 105, 'http://goo.gl/ok0VNC', fanart)	
					
	if enable_youtube_channels == 'true':
		addDir('KÊNH GIẢI TRÍ', tubemenu, 18, 'http://goo.gl/D9nS4f', fanart)
		
	if enable_youtube_channels == 'true':
		addDir('KÊNH THIẾU NHI', childrentube, 18, 'http://goo.gl/vikREi', fanart)
	
	if enable_other_addons6 == 'true':
		addDir('TỔNG HỢP', 'NoLinkRequired', 106, 'http://goo.gl/j4sDm7', fanart)	
	
	if enable_other_sources == 'true':
		addDir('LINK IPTV', 'NoLinkRequired', 110, 'http://goo.gl/RhGeAq', fanart)
	
	addDir('Dọn rác', 'clearcache', 109, 'http://goo.gl/R2ceCh', fanart)	
	
	addDir('***Giới thiệu***', yt, 3, 'http://goo.gl/MZuYDV', fanart)
	
	
"""
	addDir('[COLOR red][B]Search[/B][/COLOR]', 'searchlink', 99, '%s/search.png'% iconpath, fanart)
	if len(CCLOUDTV_SRV_URL) > 0:
		addDir('[COLOR yellow][B]All Channels[/B][/COLOR]', yt, 2, '%s/allchannels.png'% iconpath, fanart)
	if (len(CCLOUDTV_SRV_URL) < 1 ):
		mysettings.openSettings()
		xbmc.executebuiltin("Container.Refresh")
	if enable_tvguide == 'true':
		addDir('[COLOR yellow][B]TV Guide[/B][/COLOR]', 'guide', 97, '%s/guide.png'% iconpath, fanart)
	if enable_channel_tester == 'true':
		addDir('[COLOR lime][B]Channel Tester[/B][/COLOR]', 'channeltester', 40, '%s/channeltester.png'% iconpath, fanart)
	if enable_local_tester == 'true':
		addDir('[COLOR lime][B]Local M3U Playlist Tester[/B][/COLOR]', 'localtester', 41, '%s/localtester.png'% iconpath, fanart)
	if enable_online_tester == 'true':
		addDir('[COLOR lime][B]Online M3U Playlist Tester[/B][/COLOR]', 'onlinetester', 42, '%s/onlinetester.png'% iconpath, fanart)
	if platform() == 'windows' or platform() == 'osx':
		if enable_public_uploads == 'true':
			addDir('[COLOR brown][B]Public Uploads[/B][/COLOR]', public_uploads, None, '%s/ChromeLauncher.png'% iconpath, fanart)
		if enable_links_to_tutorials == 'true':
			addDir('[COLOR green][B]Links to Tutorials[/B][/COLOR]', media_link()[1], 27, '%s/tutlinks.png'% iconpath, fanart)
	if viet_mode == 'group':
		addDir('[COLOR royalblue][B]Vietnam[/B][/COLOR]', 'vietnam_group', 30, '%s/vietnam.png'% iconpath, fanart)
	if viet_mode == 'abc order':
		addDir('[COLOR royalblue][B]Vietnam[/B][/COLOR]', 'vietnam_abc_order', 48, '%s/vietnam.png'% iconpath, fanart)
	if viet_mode == 'category':
		addDir('[COLOR royalblue][B]Vietnam[/B][/COLOR]', 'vietnam_category', 70, '%s/vietnam.png'% iconpath, fanart)
	addDir('[COLOR royalblue][B]English[/B][/COLOR]', 'english', 62, '%s/english.png'% iconpath, fanart)
	addDir('[COLOR royalblue][B]Top 10[/B][/COLOR]', 'top10', 51, '%s/top10.png'% iconpath, fanart)
	addDir('[COLOR royalblue][B]Sports[/B][/COLOR]', 'sports', 52, '%s/sports.png'% iconpath, fanart)
	addDir('[COLOR royalblue][B]News[/B][/COLOR]', 'news', 53, '%s/news.png'% iconpath, fanart)
	addDir('[COLOR royalblue][B]Documentary[/B][/COLOR]', 'documentary', 54, '%s/documentary.png'% iconpath, fanart)
	addDir('[COLOR royalblue][B]Entertainment[/B][/COLOR]', 'entertainment', 55, '%s/entertainment.png'% iconpath, fanart)
	addDir('[COLOR royalblue][B]Family[/B][/COLOR]', 'family', 56, '%s/family.png'% iconpath, fanart)
	addDir('[COLOR royalblue][B]Lifestyle[/B][/COLOR]', 'lifestyle', 63, '%s/lifestyle.png'% iconpath, fanart)
	addDir('[COLOR royalblue][B]Movies[/B][/COLOR]', 'movie', 57, '%s/movies.png'% iconpath, fanart)
	addDir('[COLOR royalblue][B]Music[/B][/COLOR]', 'music', 58, '%s/music.png'% iconpath, fanart)
	addDir('[COLOR royalblue][B]On Demand Movies[/B][/COLOR]', 'ondemandmovies', 59, '%s/ondemandmovies.png'% iconpath, fanart)
	addDir('[COLOR royalblue][B]On Demand Shows[/B][/COLOR]', 'ondemandshows', 65, '%s/ondemandshows.png'% iconpath, fanart)
	addDir('[COLOR royalblue][B]24/7 Channels[/B][/COLOR]', '24', 60, '%s/twentyfourseven.png'% iconpath, fanart)
	addDir('[COLOR royalblue][B]Radio[/B][/COLOR]', 'radio', 61, '%s/radio.png'% iconpath, fanart)
	addDir('[COLOR royalblue][B]Non-English/International (Z-A)[/B][/COLOR]', 'international', 64,'%s/international.png'% iconpath, fanart)
	if getSetting("enable_adult_section") == 'true':
		addDir('[COLOR magenta][B]Adult(18+)[/B][/COLOR]', 'adult', 98, '%s/adult.png'% iconpath, fanart)
"""

def clear_cache():  #### plugin.video.xbmchubmaintenance ####
	xbmc_cache_path = os.path.join(xbmc.translatePath('special://temp'))
	if os.path.exists(xbmc_cache_path) == True:
		for root, dirs, files in os.walk(xbmc_cache_path):
			file_count = 0
			file_count += len(files)
			if file_count > 0:
				dialog = xbmcgui.Dialog()
				if dialog.yesno("Xóa file rác trong KODI", "Đã tìm thấy " + str(file_count) + " files rác của KODI trong bộ nhớ Cache.", "Bạn có muốn xóa " + str(file_count) +" files rác này không?"):
					for f in files:
						try:
							os.unlink(os.path.join(root, f))
						except:
							pass
					for d in dirs:
						if any(x in d for x in ['subs', 'temp', 'xshare']):
							pass
						else:
							try:
								shutil.rmtree(os.path.join(root, d))
							except:
								pass
					dialog = xbmcgui.Dialog()
					dialog.ok("Hieuhien.vn Media Center", "", "Đã xóa " + str(file_count) + " file rác thành công!")
			else:
				pass
	sys.exit()


def other_sources():
	#content = read_file(os.path.expanduser(r'~\Desktop\othersources.txt'))
	content = make_request(othersources)
	match = re.compile(m3u_regex).findall(content)
	for thumb, name, url in match:
		if 'tvg-logo' in thumb:
			thumb = re.compile(m3u_thumb_regex).findall(str(thumb))[0].replace(' ', '%20')
			if thumb.startswith('http'):
				addDir(name, url, 111, thumb, thumb)
			else:
				thumb = '%s/%s' % (iconpath, thumb)
				addDir(name, url, 111, thumb, thumb)
		else:
			addDir(name, url, 111, icon, fanart)

def other_sources_list(url):
	content = make_request(url)
	match = re.compile(m3u_regex).findall(content)
	for thumb, name, url in match:
		try:
			m3u_playlist(name, url, thumb)
		except:
			pass

def other_addons1():
#	reposinstaller = xbmc.translatePath(os.path.join(home, 'repos.zip'))
#	if os.path.exists(reposinstaller):
#		d = xbmcgui.Dialog().yesno('Repos Installer', 'Do you want to install necessary repositories for "Other Addons" section?', '[COLOR magenta]Quí vị có muốn cài đặt những repositories cần thiết cho mục "Other Addons" không?[/COLOR]', '', '')
#		if d:
#			import time, extract
#			dp = xbmcgui.DialogProgress()
#			dp.create("Repos Installer", "Working...", "", "")
#			addonfolder = xbmc.translatePath(os.path.join('special://', 'home'))
#			time.sleep(2)
#			dp.update(0,"", "Extracting zip files. Please wait...")
#			extract.all(reposinstaller,addonfolder,dp)
#			time.sleep(2)
#			os.remove(reposinstaller)
#			xbmcgui.Dialog().ok("Installation Completed.", "Please restart Kodi.", "", "[COLOR magenta]Vui lòng khởi động lại kodi.[/COLOR]")
#			sys.exit()
#		else:
#			sys.exit()
#	else:
		#content = read_file(os.path.expanduser(r'~\Desktop\otheraddons.txt'))
		content = make_request(otheraddons1)
		match = re.compile(m3u_regex).findall(content)
		for thumb, name, url in match:
			if 'tvg-logo' in thumb:
				thumb = re.compile(m3u_thumb_regex).findall(str(thumb))[0].replace(' ', '%20')
				if thumb.startswith('http'):
					addDir(name, url, None, thumb, thumb)
				else:
					thumb = '%s/%s' % (iconpath, thumb)
					addDir(name, url, None, thumb, thumb)
			else:
				addDir(name, url, None, icon, fanart)


def other_addons2():
		content = make_request(otheraddons2)
		match = re.compile(m3u_regex).findall(content)
		for thumb, name, url in match:
			if 'tvg-logo' in thumb:
				thumb = re.compile(m3u_thumb_regex).findall(str(thumb))[0].replace(' ', '%20')
				if thumb.startswith('http'):
					addDir(name, url, None, thumb, thumb)
				else:
					thumb = '%s/%s' % (iconpath, thumb)
					addDir(name, url, None, thumb, thumb)
			else:
				addDir(name, url, None, icon, fanart)
				

def other_addons3():
		content = make_request(otheraddons3)
		match = re.compile(m3u_regex).findall(content)
		for thumb, name, url in match:
			if 'tvg-logo' in thumb:
				thumb = re.compile(m3u_thumb_regex).findall(str(thumb))[0].replace(' ', '%20')
				if thumb.startswith('http'):
					addDir(name, url, None, thumb, thumb)
				else:
					thumb = '%s/%s' % (iconpath, thumb)
					addDir(name, url, None, thumb, thumb)
			else:
				addDir(name, url, None, icon, fanart)

def other_addons4():
		content = make_request(otheraddons4)
		match = re.compile(m3u_regex).findall(content)
		for thumb, name, url in match:
			if 'tvg-logo' in thumb:
				thumb = re.compile(m3u_thumb_regex).findall(str(thumb))[0].replace(' ', '%20')
				if thumb.startswith('http'):
					addDir(name, url, None, thumb, thumb)
				else:
					thumb = '%s/%s' % (iconpath, thumb)
					addDir(name, url, None, thumb, thumb)
			else:
				addDir(name, url, None, icon, fanart)

def other_addons5():
		content = make_request(otheraddons5)
		match = re.compile(m3u_regex).findall(content)
		for thumb, name, url in match:
			if 'tvg-logo' in thumb:
				thumb = re.compile(m3u_thumb_regex).findall(str(thumb))[0].replace(' ', '%20')
				if thumb.startswith('http'):
					addDir(name, url, None, thumb, thumb)
				else:
					thumb = '%s/%s' % (iconpath, thumb)
					addDir(name, url, None, thumb, thumb)
			else:
				addDir(name, url, None, icon, fanart)
				
def other_addons6():
		content = make_request(otheraddons6)
		match = re.compile(m3u_regex).findall(content)
		for thumb, name, url in match:
			if 'tvg-logo' in thumb:
				thumb = re.compile(m3u_thumb_regex).findall(str(thumb))[0].replace(' ', '%20')
				if thumb.startswith('http'):
					addDir(name, url, None, thumb, thumb)
				else:
					thumb = '%s/%s' % (iconpath, thumb)
					addDir(name, url, None, thumb, thumb)
			else:
				addDir(name, url, None, icon, fanart)
				
def removeAccents(s):
	return ''.join((c for c in unicodedata.normalize('NFD', s.decode('utf-8')) if unicodedata.category(c) != 'Mn'))

def search(): 
	try:
		keyb = xbmc.Keyboard('', 'Enter Channel Name')
		keyb.doModal()
		if (keyb.isConfirmed()):
			searchText = urllib.quote_plus(keyb.getText(), safe="%/:=&?~#+!$,;'@()*[]").replace('+', ' ')
		if len(CCLOUDTV_SRV_URL) > 0:
			content = select_server()
			match = re.compile(m3u_regex).findall(content)
			for thumb, name, url in sorted(match, key = itemgetter(1)):
				if re.search(searchText, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE):
					m3u_playlist(name, url, thumb)
	except:
		pass

def tutorial_links(url):
	content = make_request(url)
	if url.endswith('m3u'):
		match = re.compile(m3u_regex).findall(content)
		for thumb, name, url in match:
			if 'plugin.program.chrome.launcher' in url:
				if 'tvg-logo' in thumb:
					thumb = re.compile(m3u_thumb_regex).findall(str(thumb))[0].replace(' ', '%20')
					if thumb.startswith('http'):
						addDir(name, url, None, thumb, thumb)
					else:
						thumb = '%s/%s' % (iconpath, thumb)
						addDir(name, url, None, thumb, thumb)
				else:
					addDir(name, url, None, icon, fanart)
			else:
				if 'tvg-logo' in thumb:
					thumb = re.compile(m3u_thumb_regex).findall(str(thumb))[0].replace(' ', '%20')
					if thumb.startswith('http'):
						addLink(name, url, 1, thumb, thumb)
					else:
						thumb = '%s/%s' % (iconpath, thumb)
						addLink(name, url, 1, thumb, thumb)
				else:
					addLink(name, url, 1, icon, fanart)
	elif url.endswith('xml'):
		match = re.compile(xml_regex).findall(content)
		for name, url, thumb in match:
			if 'plugin.program.chrome.launcher' in url:
				addDir(name, url, None, thumb, thumb)
			else:
				addLink(name, url, 1, thumb, thumb)

def search_youtube(): 
	try:
		keyb = xbmc.Keyboard('', 'Enter Channel Name')
		keyb.doModal()
		if (keyb.isConfirmed()):
			searchText = urllib.quote_plus(keyb.getText()) 
		url = 'https://www.youtube.com/results?search_query=' + searchText
		youtube_search(url)
	except:
		pass

def youtube_search(url):
	content = make_request(url)
	match = re.compile('href="/watch\?v=(.+?)" class=".+?" data-sessionlink=".+?" title="(.+?)".+?Duration: (.+?).</span>').findall(content)
	for url, name, duration in match:
		name = replace_all(name, dic)
		thumb = 'https://i.ytimg.com/vi/' + url + '/mqdefault.jpg'
		url = 'plugin://plugin.video.youtube/play/?video_id=' + url
		addLink(name + ' (' + duration + ')', url, 1, thumb, fanart)
	match = re.compile('href="/results\?search_query=(.+?)".+?aria-label="Go to (.+?)"').findall(content)
	for url, name in match:
		url = 'https://www.youtube.com/results?search_query=' + url
		addDir('[COLOR cyan]' + name + '[/COLOR]', url, 26, ytsearchicon, ytsearchicon)

def youtube_menu(url):
	#if url == tubemenu:
	#	addDir('[COLOR yellow][B]YouTube - Search[/B][/COLOR]', 'ytsearch', 25, ytsearchicon, ytsearchicon)
	content = make_request(url)
	match = re.compile(xml_regex+'\s*<mode>(.*?)</mode>').findall(content)
	for name, url, thumb, mode in match:
		if youtube_mode == 'direct':
			if 'plugin://plugin.video.youtube' in url:
				addLink(name, url, mode, thumb, thumb)
			else:
				addDir(name, url, mode, thumb, thumb) 
		elif youtube_mode == 'tubelink':
			if mode == '20':
				getDir(name, url, None, thumb, thumb)
			else:
				if 'plugin://plugin.video.youtube' in url:
					addLink(name, url, mode, thumb, thumb)
				else:
					addDir(name, url, mode, thumb, thumb) 

def youtube_channels(url):
	content = make_request(url)
	match = re.compile(xml_regex).findall(content)
	for name, url, thumb in match:
		if youtube_mode == 'direct':
			addDir(name, url, 20, thumb, thumb)
		elif youtube_mode == 'tubelink':
			getDir(name, url, None, thumb, thumb)

def youtube_list(url):
	addDir('[COLOR magenta][B]Playlists[/B][/COLOR]', (url + '/playlists?sort=dd&view=1'), 21, '%s/YTPlaylist.png'% iconpath, fanart)
	link = make_request(url + '/videos')
	link = ''.join(link.splitlines()).replace('\t','')
	match = re.compile('src="//i.ytimg.com/vi/(.+?)".+?aria-label.+?>(.+?)</span>.+?href="/watch\?v=(.+?)">(.+?)</a>').findall(link)
	for thumb, duration, url, name in match:
		name = replace_all(name, dic)
		thumb = 'https://i.ytimg.com/vi/' + thumb
		addLink(name, 'plugin://plugin.video.youtube/play/?video_id=' + url, 1, thumb, thumb)
	try:
		match = re.compile('data-uix-load-more-href="(.+?)"').findall(link)
		addDir('[COLOR yellow][B]Next page [/B][/COLOR][COLOR lime][B]>>[/B][/COLOR]', 'https://www.youtube.com' + match[0].replace('&amp;','&'), 23, '%s/nextpage.png'% iconpath, fanart)
	except:
		pass

def youtube_playlist(url):
	link = make_request(url)
	link = ''.join(link.splitlines()).replace('\t','')
	match = re.compile('[src|data-thumb]="//i.ytimg.com/vi/(.+?)".+?href="/playlist(.+?)">(.+?)<').findall(link)    # Either src or data-thumb [src|data-thumb]
	for thumb, url, name in match:
		name = replace_all(name, dic)
		thumb = 'https://i.ytimg.com/vi/' + thumb
		if 'Liked videos' in name or 'Favorites' in name:
			pass
		else:
			addDir(name, url, 22, thumb, thumb)

def youtube_playlist_index(url):
	link = make_request('https://www.youtube.com/playlist' + url)
	link = ''.join(link.splitlines()).replace('\t','')
	newmatch = re.compile('data-title="(.+?)".+?href="\/watch\?v=(.+?)\&amp\;.+?data-thumb="(.+?)".+?aria-label.+?>(.+?)<\/span><\/div>').findall(link)
	for name, url, thumb, duration in newmatch:
		name = replace_all(name, dic)
		thumb = 'https:' + thumb
		if '[Deleted Video]' in name:
			pass
		else:
			addLink(name, 'plugin://plugin.video.youtube/play/?video_id=' + url, 1, thumb, thumb)
	try:
		match = re.compile('data-uix-load-more-href="(.+?)"').findall(link)
		addDir('[COLOR magenta]Next page >>[/COLOR]', 'https://www.youtube.com' + match[0].replace('&amp;','&'), 24, '%s/nextpage.png'% iconpath, fanart)
	except:
		pass

def next_page(url):
	req = urllib2.Request(url)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:19.0) Gecko/20100101 Firefox/19.0')
	response = urllib2.urlopen(req) 
	link = response.read()
	response.close()
	newlink = ''.join(link.splitlines()).replace('\\', '').replace('\t','')
	match = re.compile('src="//i.ytimg.com/vi/(.+?)".+?aria-label="(.+?)".+?dir="ltr" title="(.+?)".+?href="/watch\?v=(.+?)"').findall(newlink)
	for thumb, duration, name, url in match:
		name = replace_all(name, dic)
		thumb = 'https://i.ytimg.com/vi/' + thumb
		addLink(name, 'plugin://plugin.video.youtube/play/?video_id=' + url, 1, thumb, thumb)
	try:
		match = re.compile('data-uix-load-more-href="(.+?)"').findall(newlink)
		addDir('[COLOR yellow][B]Next page [/B][/COLOR][COLOR lime][B]>>[/B][/COLOR]', 'https://www.youtube.com' + match[0].replace('&amp;','&'), 23, '%s/nextpage.png'% iconpath, fanart)
	except:
		pass

def next_page_playlist(url):
	req = urllib2.Request(url)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:19.0) Gecko/20100101 Firefox/19.0')
	response = urllib2.urlopen(req) 
	link = response.read()
	response.close()
	newlink = ''.join(link.splitlines()).replace('\\', '').replace('\t','')
	match = re.compile('data-video-id="(.+?)".+?data-title="(.+?)".+?data-thumb="//i.ytimg.com/vi/(.+?)".+?aria-label="(.+?)"').findall(newlink)
	for url, name, thumb, duration in match:
		name = replace_all(name, dic)
		thumb = 'https://i.ytimg.com/vi/' + thumb
		addLink(name, 'plugin://plugin.video.youtube/play/?video_id=' + url, 1, thumb, thumb)
	try:
		match = re.compile('data-uix-load-more-href="(.+?)"').findall(newlink)
		addDir('[COLOR magenta]Next page >>[/COLOR]', 'https://www.youtube.com' + match[0].replace('&amp;','&'), 24, '%s/nextpage.png'% iconpath, fanart)
	except:
		pass

def vietmedia_tutorials():
	thumb = 'https://yt3.ggpht.com/-Y4hzMs0ItTw/AAAAAAAAAAI/AAAAAAAAAAA/OquSyoI-Y2s/s100-c-k-no/photo.jpg'
	addLink('[COLOR orange][B]VietMedia - YouTube - Hướng Dẫn[/B][/COLOR]', 'NoLinkRequired', 1, thumb, thumb)
	content = make_request(yt + 'playlist?list=PLCFeyxaD_7E30Ibjhm8D5qn7KUVDE7os2')
	newcontent = ''.join(content.splitlines()).replace('\t','')
	newmatch = re.compile('data-title="(.+?)".+?href="\/watch\?v=(.+?)\&amp\;.+?data-thumb="(.+?)".+?aria-label.+?>(.+?)<\/span><\/div>').findall(newcontent)
	for name, url, thumb, duration in newmatch:
		thumb = 'https:' + thumb
		if '[Deleted Video]' in name:
			pass
		else:
			name = replace_all(name, dic)
			addLink(name, 'plugin://plugin.video.youtube/play/?video_id=' + url, 1, thumb, thumb)
	content = make_request(yt + 'playlist?list=PLCFeyxaD_7E3LLqjhIwkboAePgDT--8YF')
	newcontent = ''.join(content.splitlines()).replace('\t','')
	newmatch = re.compile('data-title="(.+?)".+?href="\/watch\?v=(.+?)\&amp\;.+?data-thumb="(.+?)".+?aria-label.+?>(.+?)<\/span><\/div>').findall(newcontent)
	for name, url, thumb, duration in newmatch:
		thumb = 'https:' + thumb
		if '[Deleted Video]' in name:
			pass
		else:
			name = replace_all(name, dic)
			addLink(name, 'plugin://plugin.video.youtube/play/?video_id=' + url, 1, thumb, thumb)
	thumb1 = '%s/utube.png'% iconpath
	addLink('[COLOR magenta][B]Other Tutorials on YouTube - Những Hướng Dẫn Khác[/B][/COLOR]', 'NoLinkRequired', 1, thumb1, thumb1)
	content = make_request(media_link()[1])
	match = re.compile(m3u_regex).findall(content)
	for thumb, name, url in match:
		if 'plugin.video.youtube' in url:
			if 'tvg-logo' in thumb:
				thumb = re.compile(m3u_thumb_regex).findall(str(thumb))[0].replace(' ', '%20')
				if thumb.startswith('http'):
					addLink(name, url, 1, thumb, thumb)
				else:
					thumb = '%s/%s' % (iconpath, thumb)
					addLink(name, url, 1, thumb, thumb)
			else:
				addLink(name, url, 1, icon, fanart)
		else:
			pass

def vietnam_abc_order():
	try:
		searchText = '\(VN\)|(Vietnamese)'
		if len(CCLOUDTV_SRV_URL) > 0:
			content = select_server()
			match = re.compile(m3u_regex).findall(content)
			for thumb, name, url in sorted(match, key = itemgetter(1)):
				if (re.search(searchText, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE)):
					if ('\(Adult\)' in name) or ('\(Public-Adult\)' in name):
						pass
					else:
						m3u_playlist(name, url, thumb)
	except:
		pass
	try:
		content = make_request(media_link()[3])
		match = re.compile(m3u_regex).findall(content)
		for thumb, name, url in match:
			if 'tvg-logo' in thumb:
				thumb = re.compile(m3u_thumb_regex).findall(str(thumb))[0].replace(' ', '%20')
				addLink(name, url, 1, thumb, thumb)
			else:
				addLink(name, url, 1, icon, fanart)
		content = make_request(media_link()[2])
		match = re.compile(m3u_regex).findall(content)
		for thumb, name, url in match:
			if 'tvg-logo' in thumb:
				thumb = re.compile(m3u_thumb_regex).findall(str(thumb))[0].replace(' ', '%20')
				addLink(name, url, 1, thumb, thumb)
			else:
				addLink(name, url, 1, icon, fanart)
		vietmedia_tutorials()
	except:
		pass

def vietnam_group():
	addDir('Movies', 'vietnam_group', 77, '%s/group.png'% iconpath, fanart)
	addDir('Music', 'vietnam_group', 75, '%s/group.png'% iconpath, fanart)
	addDir('Radio', 'vietnam_group', 79, '%s/group.png'% iconpath, fanart)
	addDir('Sports', 'vietnam_group', 82, '%s/group.png'% iconpath, fanart)
	addDir('Tutorials', 'vietnam_group', 83, '%s/group.png'% iconpath, fanart)
	addDir('TV', 'vietnam_group', 31, '%s/group.png'% iconpath, fanart)

def viet_tv_group():
	try:
		searchText = '\(VN\)|(Vietnamese)'
		if len(CCLOUDTV_SRV_URL) > 0:
			content = select_server()
			match = re.compile(m3u_regex).findall(content)
			for thumb, name, url in sorted(match, key = itemgetter(1)):
				if (re.search(searchText, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE)): 
					if ('\(Adult\)' in name) or ('\(Public-Adult\)' in name) or ('OnDemandMovies' in name) or ('Music' in name) or ('Radio' in name) or ('Sports' in name) or ('Tutorials' in name):
						pass
					else:
						m3u_playlist(name, url, thumb)
	except:
		pass
	try:
		content = make_request(media_link()[3])
		match = re.compile(m3u_regex).findall(content)
		for thumb, name, url in match:
			if 'tvg-logo' in thumb:
				thumb = re.compile(m3u_thumb_regex).findall(str(thumb))[0].replace(' ', '%20')
				addLink(name, url, 1, thumb, thumb)
			else:
				addLink(name, url, 1, icon, fanart)
	except:
		pass

def vietnam_category(): 
	addDir('Documentary', 'vietnam_category', 71, '%s/category.png'% iconpath, fanart)
	addDir('Entertainment', 'vietnam_category', 72, '%s/category.png'% iconpath, fanart)
	addDir('Family', 'vietnam_category', 73, '%s/category.png'% iconpath, fanart)
	addDir('Movie Channels', 'vietnam_category', 74, '%s/category.png'% iconpath, fanart)
	addDir('Music', 'vietnam_category', 75, '%s/category.png'% iconpath, fanart)
	addDir('News', 'vietnam_category', 76, '%s/category.png'% iconpath, fanart)
	addDir('On Demand Movies', 'vietnam_category', 77, '%s/category.png'% iconpath, fanart)
	addDir('On Demand Shows', 'vietnam_category', 78, '%s/category.png'% iconpath, fanart)
	addDir('Radio', 'vietnam_category', 79, '%s/category.png'% iconpath, fanart)
	addDir('Random Air Time 24/7', 'vietnam_category', 80, '%s/category.png'% iconpath, fanart)
	addDir('Special Events', 'vietnam_category', 81, '%s/category.png'% iconpath, fanart)
	addDir('Sports', 'vietnam_category', 82, '%s/category.png'% iconpath, fanart)
	addDir('Tutorials', 'vietnam_category', 83, '%s/category.png'% iconpath, fanart)

def viet_Documentary():
	try:
		searchText = '\(VN\)|(Vietnamese)'
		if len(CCLOUDTV_SRV_URL) > 0:
			content = select_server()
			match = re.compile(m3u_regex).findall(content)
			for thumb, name, url in sorted(match, key = itemgetter(1)):
				if (re.search(searchText, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE)):
					if ('\(Adult\)' in name) or ('\(Public-Adult\)' in name):
						pass
					if 'Documentary' in name:
						m3u_playlist(name, url, thumb)
	except:
		pass

def viet_Entertainment():
	try:
		searchText = '\(VN\)|(Vietnamese)'
		if len(CCLOUDTV_SRV_URL) > 0:
			content = select_server()
			match = re.compile(m3u_regex).findall(content)
			for thumb, name, url in sorted(match, key = itemgetter(1)):
				if (re.search(searchText, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE)):
					if ('\(Adult\)' in name) or ('\(Public-Adult\)' in name):
						pass
					if 'Entertainment' in name:
						m3u_playlist(name, url, thumb)
	except:
		pass

def viet_Family():
	try:
		searchText = '\(VN\)|(Vietnamese)'
		if len(CCLOUDTV_SRV_URL) > 0:
			content = select_server()
			match = re.compile(m3u_regex).findall(content)
			for thumb, name, url in sorted(match, key = itemgetter(1)):
				if (re.search(searchText, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE)):
					if ('\(Adult\)' in name) or ('\(Public-Adult\)' in name):
						pass
					if 'Family' in name:
						m3u_playlist(name, url, thumb)
	except:
		pass
	try:
		content = make_request(media_link()[3])
		match = re.compile(m3u_regex).findall(content)
		for thumb, name, url in match:
			if 'tvg-logo' in thumb:
				thumb = re.compile(m3u_thumb_regex).findall(str(thumb))[0].replace(' ', '%20')
				addLink(name, url, 1, thumb, thumb)
			else:
				addLink(name, url, 1, icon, fanart)
	except:
		pass

def viet_Movie_Channels():
	try:
		searchText = '\(VN\)|(Vietnamese)'
		if len(CCLOUDTV_SRV_URL) > 0:
			content = select_server()
			match = re.compile(m3u_regex).findall(content)
			for thumb, name, url in sorted(match, key = itemgetter(1)):
				if (re.search(searchText, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE)):
					if ('\(Adult\)' in name) or ('\(Public-Adult\)' in name):
						pass
					if 'Movie Channels' in name:
						m3u_playlist(name, url, thumb)
	except:
		pass

def viet_Music():
	try:
		searchText = '\(VN\)|(Vietnamese)'
		if len(CCLOUDTV_SRV_URL) > 0:
			content = select_server()
			match = re.compile(m3u_regex).findall(content)
			for thumb, name, url in sorted(match, key = itemgetter(1)):
				if (re.search(searchText, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE)):
					if ('\(Adult\)' in name) or ('\(Public-Adult\)' in name):
						pass
					if 'Music' in name:
						m3u_playlist(name, url, thumb)
	except:
		pass

def viet_News():
	try:
		searchText = '\(VN\)|(Vietnamese)'
		if len(CCLOUDTV_SRV_URL) > 0:
			content = select_server()
			match = re.compile(m3u_regex).findall(content)
			for thumb, name, url in sorted(match, key = itemgetter(1)):
				if (re.search(searchText, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE)):
					if ('\(Adult\)' in name) or ('\(Public-Adult\)' in name):
						pass
					if 'News' in name:
						m3u_playlist(name, url, thumb)
	except:
		pass

def viet_OnDemandMovies():
	try:
		searchText = '\(VN\)|(Vietnamese)'
		if len(CCLOUDTV_SRV_URL) > 0:
			content = select_server()
			match = re.compile(m3u_regex).findall(content)
			for thumb, name, url in sorted(match, key = itemgetter(1)):
				if (re.search(searchText, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE)):
					if ('\(Adult\)' in name) or ('\(Public-Adult\)' in name):
						pass
					if 'OnDemandMovies' in name:
						m3u_playlist(name, url, thumb)
	except:
		pass

def viet_OnDemandShows():
	try:
		searchText = '\(VN\)|(Vietnamese)'
		if len(CCLOUDTV_SRV_URL) > 0:
			content = select_server()
			match = re.compile(m3u_regex).findall(content)
			for thumb, name, url in sorted(match, key = itemgetter(1)):
				if (re.search(searchText, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE)):
					if ('\(Adult\)' in name) or ('\(Public-Adult\)' in name):
						pass
					if 'OnDemandShows' in name:
						m3u_playlist(name, url, thumb)
	except:
		pass

def viet_Radio():
	try:
		searchText = '\(VN\)|(Vietnamese)'
		if len(CCLOUDTV_SRV_URL) > 0:
			content = select_server()
			match = re.compile(m3u_regex).findall(content)
			for thumb, name, url in sorted(match, key = itemgetter(1)):
				if (re.search(searchText, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE)):
					if ('\(Adult\)' in name) or ('\(Public-Adult\)' in name):
						pass
					if 'Radio' in name:
						m3u_playlist(name, url, thumb)
	except:
		pass
	try:
		content = make_request(media_link()[2])
		match = re.compile(m3u_regex).findall(content)
		for thumb, name, url in match:
			if 'tvg-logo' in thumb:
				thumb = re.compile(m3u_thumb_regex).findall(str(thumb))[0].replace(' ', '%20')
				addLink(name, url, 1, thumb, thumb)
			else:
				addLink(name, url, 1, icon, fanart)
	except:
		pass

def viet_RandomAirTime():
	try:
		searchText = '\(VN\)|(Vietnamese)'
		if len(CCLOUDTV_SRV_URL) > 0:
			content = select_server()
			match = re.compile(m3u_regex).findall(content)
			for thumb, name, url in sorted(match, key = itemgetter(1)):
				if (re.search(searchText, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE)):
					if ('\(Adult\)' in name) or ('\(Public-Adult\)' in name):
						pass
					if 'RandomAirTime 24/7' in name:
						m3u_playlist(name, url, thumb)
	except:
		pass

def viet_Special_Events():
	try:
		searchText = '\(VN\)|(Vietnamese)'
		if len(CCLOUDTV_SRV_URL) > 0:
			content = select_server()
			match = re.compile(m3u_regex).findall(content)
			for thumb, name, url in sorted(match, key = itemgetter(1)):
				if (re.search(searchText, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE)):
					if ('\(Adult\)' in name) or ('\(Public-Adult\)' in name):
						pass
					if 'Special Events' in name:
						m3u_playlist(name, url, thumb)
	except:
		pass

def viet_Sports():
	try:
		searchText = '\(VN\)|(Vietnamese)'
		if len(CCLOUDTV_SRV_URL) > 0:
			content = select_server()
			match = re.compile(m3u_regex).findall(content)
			for thumb, name, url in sorted(match, key = itemgetter(1)):
				if (re.search(searchText, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE)):
					if ('\(Adult\)' in name) or ('\(Public-Adult\)' in name):
						pass
					if 'Sports' in name:
						m3u_playlist(name, url, thumb)
	except:
		pass

def viet_Tutorials():
	try:
		searchText = '\(VN\)|(Vietnamese)'
		if len(CCLOUDTV_SRV_URL) > 0:
			content = select_server()
			match = re.compile(m3u_regex).findall(content)
			for thumb, name, url in sorted(match, key = itemgetter(1)):
				if (re.search(searchText, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE)):
					if ('\(Adult\)' in name) or ('\(Public-Adult\)' in name):
						pass
					if 'Tutorials' in name:
						m3u_playlist(name, url, thumb)
	except:
		pass
	try:
		vietmedia_tutorials()
	except:
		pass

def top10():
	try:
		searchText = '(Top10)'
		if len(CCLOUDTV_SRV_URL) > 0:
			content = select_server()
			match = re.compile(m3u_regex).findall(content)
			for thumb, name, url in sorted(match, key = itemgetter(1)):
				if re.search(searchText, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE):
					m3u_playlist(name, url, thumb)
	except:
		pass

def sports():
	try:
		searchText = '(Sports)'
		if len(CCLOUDTV_SRV_URL) > 0:
			content = select_server()
			match = re.compile(m3u_regex).findall(content)
			for thumb, name, url in sorted(match, key = itemgetter(1)):
				if re.search(searchText, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE):
					m3u_playlist(name, url, thumb)
	except:
		pass

def news():
	try:
		searchText = '(News)'
		if len(CCLOUDTV_SRV_URL) > 0:
			content = select_server()
			match = re.compile(m3u_regex).findall(content)
			for thumb, name, url in sorted(match, key = itemgetter(1)):
				if re.search(searchText, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE):
					m3u_playlist(name, url, thumb)
	except:
		pass

def documentary():
	try:
		searchText = '(Document)'
		if len(CCLOUDTV_SRV_URL) > 0:
			content = select_server()
			match = re.compile(m3u_regex).findall(content)
			for thumb, name, url in sorted(match, key = itemgetter(1)):
				if re.search(searchText, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE):
					m3u_playlist(name, url, thumb)
	except:
		pass

def entertainment():
	try:
		searchText = '(Entertainment)'
		if len(CCLOUDTV_SRV_URL) > 0:
			content = select_server()
			match = re.compile(m3u_regex).findall(content)
			for thumb, name, url in sorted(match, key = itemgetter(1)):
				if re.search(searchText, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE):
					m3u_playlist(name, url, thumb)
	except:
		pass

def family():
	try:
		searchText = '(Family)'
		if len(CCLOUDTV_SRV_URL) > 0:
			content = select_server()
			match = re.compile(m3u_regex).findall(content)
			for thumb, name, url in sorted(match, key = itemgetter(1)):
				if re.search(searchText, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE):
					m3u_playlist(name, url, thumb)
	except:
		pass

def lifestyle():
	try:
		searchText = '(Lifestyle)'
		if len(CCLOUDTV_SRV_URL) > 0:
			content = select_server()
			match = re.compile(m3u_regex).findall(content)
			for thumb, name, url in sorted(match, key = itemgetter(1)):
				if re.search(searchText, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE):
					m3u_playlist(name, url, thumb)
	except:
		pass

def movie():
	try:
		searchText = '(Movie Channels)'
		if len(CCLOUDTV_SRV_URL) > 0:
			content = select_server()
			match = re.compile(m3u_regex).findall(content)
			for thumb, name, url in sorted(match, key = itemgetter(1)):
				if re.search(searchText, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE):
					m3u_playlist(name, url, thumb)
	except:
		pass

def music():
	try:
		searchText = '(Music)'
		if len(CCLOUDTV_SRV_URL) > 0:
			content = select_server()
			match = re.compile(m3u_regex).findall(content)
			for thumb, name, url in sorted(match, key = itemgetter(1)):
				if re.search(searchText, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE):
					m3u_playlist(name, url, thumb)
	except:
		pass

def ondemandmovies():
	try:
		searchText = '(OnDemandMovies)'
		if len(CCLOUDTV_SRV_URL) > 0:
			content = select_server()
			match = re.compile(m3u_regex).findall(content)
			for thumb, name, url in sorted(match, key = itemgetter(1)):
				if re.search(searchText, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE):
					m3u_playlist(name, url, thumb)
	except:
		pass

def ondemandshows():
	try:
		searchText = '(OnDemandShows)'
		if len(CCLOUDTV_SRV_URL) > 0:
			content = select_server()
			match = re.compile(m3u_regex).findall(content)
			for thumb, name, url in sorted(match, key = itemgetter(1)):
				if re.search(searchText, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE):
					m3u_playlist(name, url, thumb)
	except:
		pass

def twentyfour7():
	try:
		searchText = '(RandomAirTime 24/7)'
		if len(CCLOUDTV_SRV_URL) > 0:
			content = select_server()
			match = re.compile(m3u_regex).findall(content)
			for thumb, name, url in sorted(match, key = itemgetter(1)):
				if re.search(searchText, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE):
					m3u_playlist(name, url, thumb)
	except:
		pass

def radio():
	try:
		searchText = '(Radio)'
		if len(CCLOUDTV_SRV_URL) > 0:
			content = select_server()
			match = re.compile(m3u_regex).findall(content)
			for thumb, name, url in sorted(match, key = itemgetter(1)):
				if re.search(searchText, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE):
					m3u_playlist(name, url, thumb)
	except:
		pass

def adult():
	addDir('[COLOR red][B]Adult Addons[/B][/COLOR]', 'adult_addons', 120, '%s/xxx.png'% iconpath, fanart)
	try:
		content = make_request(media_link()[4])
		match = re.compile(m3u_regex).findall(content)
		for thumb, name, url in match:
			if 'plugin://plugin' in url:
				if 'tvg-logo' in thumb:
					thumb = re.compile(m3u_thumb_regex).findall(str(thumb))[0].replace(' ', '%20')
					if thumb.startswith('http'):
						addDir(name, url, 111, thumb, thumb)
					else:
						thumb = '%s/%s' % (iconpath, thumb)
						addDir(name, url, 111, thumb, thumb)
				else:
					addDir(name, url, 111, icon, fanart)
			else:
				if 'tvg-logo' in thumb:
					thumb = re.compile(m3u_thumb_regex).findall(str(thumb))[0].replace(' ', '%20')
					if thumb.startswith('http'):
						addLink(name, url, 1, thumb, thumb)
					else:
						thumb = '%s/%s' % (iconpath, thumb)
						addLink(name, url, 1, thumb, thumb)
				else:
					addLink(name, url, 1, icon, fanart)
	except:
		pass
	try:
		content = make_request('http://www.giniko.com/watch.php?id=95')
		match = re.compile('image: "([^"]*)",\s*file: "([^"]+)"').findall(content)
		for thumb, url in match:
			addLink('[COLOR magenta][B]Miami TV (Adult 18+)[/B][/COLOR]', url, 1, thumb, thumb)
	except:
		pass
	try:
		searchText = ('(Adult)') or ('(Public-Adult)')
		if len(CCLOUDTV_SRV_URL) > 0:
			content = select_server()
			match = re.compile(adult_regex).findall(content)
			for thumb, name, url in sorted(match, key = itemgetter(1)):
				if re.search(searchText, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE):
					adult_playlist(name, url, thumb)
		if len(CCLOUDTV_SRV_URL) > 0:
			content = select_server()
			match = re.compile(adult_regex2).findall(content)
			for thumb, name, url in sorted(match, key = itemgetter(1)):
				if re.search(searchText, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE):
					adult_playlist(name, url, thumb)
	except:
		pass

def adult_addons():
	adultreposinstaller = xbmc.translatePath(os.path.join(home, 'adult_repos.zip'))
	if os.path.exists(adultreposinstaller):
		d = xbmcgui.Dialog().yesno('Adult Repos Installer', 'Do you want to install necessary repositories for "Adult Addons" section?', '[COLOR magenta]Quí vị có muốn cài đặt những repositories cần thiết cho mục "Adult Addons" không?[/COLOR]', '', '')
		if d:
			import time, extract
			dp = xbmcgui.DialogProgress()
			dp.create("Adult Repos Installer", "Working...", "", "")
			addonfolder = xbmc.translatePath(os.path.join('special://', 'home'))
			time.sleep(2)
			dp.update(0,"", "Extracting zip files. Please wait...")
			extract.all(adultreposinstaller,addonfolder,dp)
			time.sleep(2)
			os.remove(adultreposinstaller)
			xbmcgui.Dialog().ok("Installation Completed.", "Please restart Kodi.", "", "[COLOR magenta]Vui lòng khởi động lại kodi.[/COLOR]")
			sys.exit()
		else:
			sys.exit()
	else:
		content = make_request(adultaddons)
		match = re.compile(m3u_regex).findall(content)
		for thumb, name, url in match:
			if 'tvg-logo' in thumb:
				thumb = re.compile(m3u_thumb_regex).findall(str(thumb))[0].replace(' ', '%20')
				if thumb.startswith('http'):
					addDir(name, url, None, thumb, thumb)
				else:
					thumb = '%s/%s' % (iconpath, thumb)
					addDir(name, url, None, thumb, thumb)
			else:
				addDir(name, url, None, icon, fanart)

def english():
	try:
		searchText = '(English)'
		if len(CCLOUDTV_SRV_URL) > 0:
			content = select_server()
			match = re.compile(m3u_regex).findall(content)
			for thumb, name, url in sorted(match, key = itemgetter(1)):
				if re.search(searchText, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE):
					m3u_playlist(name, url, thumb)
	except:
		pass

def international():
	if len(CCLOUDTV_SRV_URL) > 0:
		content = select_server()
		match = sorted(re.compile(m3u_regex).findall(content), key = itemgetter(1))
		try:
			searchVietnamese = '\(VN\)|(Vietnamese)'
			for thumb, name, url in match:
				if (re.search(searchVietnamese, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE)):
					if ('\(Adult\)' in name) or ('\(Public-Adult\)' in name):
						pass
					else:
						m3u_playlist(name, url, thumb)
		except:
			pass
		try:
			searchUrdu = '(Urdu)'
			for thumb, name, url in match:
				if re.search(searchUrdu, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE):
					m3u_playlist(name, url, thumb)
		except:
			pass
		try:
			searchUkrainian = '(Ukrainian)'
			for thumb, name, url in match:
				if re.search(searchUkrainian, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE):
					m3u_playlist(name, url, thumb)
		except:
			pass
		try:
			searchTamil = '(Tamil)'
			for thumb, name, url in match:
				if re.search(searchTamil, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE):
					m3u_playlist(name, url, thumb)
		except:
			pass
		try:
			searchSpanish = '(Spanish)'
			for thumb, name, url in match:
				if re.search(searchSpanish, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE):
					m3u_playlist(name, url, thumb)
		except:
			pass
		try:
			searchSomali = '(Somali)'
			for thumb, name, url in match:
				if re.search(searchSomali, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE):
					m3u_playlist(name, url, thumb)
		except:
			pass
		try:
			searchSlovenian = '(Slovenian)'
			for thumb, name, url in match:
				if re.search(searchSlovenian, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE):
					m3u_playlist(name, url, thumb)
		except:
			pass
		try:
			searchRussian = '(Russian)'
			for thumb, name, url in match:
				if re.search(searchRussian, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE):
					m3u_playlist(name, url, thumb)
		except:
			pass
		try:
			searchRomanian = '(Romanian)'
			for thumb, name, url in match:
				if re.search(searchRomanian, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE):
					m3u_playlist(name, url, thumb)
		except:
			pass
		try:
			searchPortuguese = '(Portuguese)'
			for thumb, name, url in match:
				if re.search(searchPortuguese, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE):
					m3u_playlist(name, url, thumb)
		except:
			pass
		try:
			searchPolish = '(Polish)'
			for thumb, name, url in match:
				if re.search(searchPolish, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE):
					m3u_playlist(name, url, thumb)
		except:
			pass
		try:
			searchMandarin = '(Mandarin)'
			for thumb, name, url in match:
				if re.search(searchFilipino, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE):
					m3u_playlist(name, url, thumb)
		except:
			pass
		try:
			searchMaltese = '(Maltese)'
			for thumb, name, url in match:
				if re.search(searchMaltese, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE):
					m3u_playlist(name, url, thumb)
		except:
			pass
		try:
			searchMacedonian = '(Macedonian)'
			for thumb, name, url in match:
				if re.search(searchMacedonian, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE):
					m3u_playlist(name, url, thumb)
		except:
			pass
		try:
			searchLithuanian = '(Lithuanian)'
			for thumb, name, url in match:
				if re.search(searchLithuanian, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE):
					m3u_playlist(name, url, thumb)
		except:
			pass
		try:
			searchKurdish = '(Kurdish)'
			for thumb, name, url in match:
				if re.search(searchKurdish, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE):
					m3u_playlist(name, url, thumb)
		except:
			pass
		try:
			searchJamaica = '(Jamaica)'
			for thumb, name, url in match:
				if re.search(searchJamaica, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE):
					m3u_playlist(name, url, thumb)
		except:
			pass
		try:
			searchItalian = '(Italian)'
			for thumb, name, url in match:
				if re.search(searchItalian, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE):
					m3u_playlist(name, url, thumb)
		except:
			pass
		try:
			searchIsraeli = '(Israeli)'
			for thumb, name, url in match:
				if re.search(searchIsraeli, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE):
					m3u_playlist(name, url, thumb)
		except:
			pass
		try:
			searchIndian = '(Indian)'
			for thumb, name, url in match:
				if re.search(searchIndian, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE):
					m3u_playlist(name, url, thumb)
		except:
			pass
		try:
			searchhungarian = '(Hungarian)'
			for thumb, name, url in match:
				if re.search(searchHungarian, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE):
					m3u_playlist(name, url, thumb)
		except:
			pass
		try:
			searchHindi = '(Hindi)'
			for thumb, name, url in match:
				if re.search(searchHindi, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE):
					m3u_playlist(name, url, thumb)
		except:
			pass
		try:
			searchGreek = '(Greek)'
			for thumb, name, url in match:
				if re.search(searchGreek, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE):
					m3u_playlist(name, url, thumb)
		except:
			pass
		try:
			searchGerman = '(German)'
			for thumb, name, url in match:
				if re.search(searchGerman, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE):
					m3u_playlist(name, url, thumb)
		except:
			pass
		try:
			searchFrench = '(French)'
			for thumb, name, url in match:
				if re.search(searchFrench, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE):
					m3u_playlist(name, url, thumb)
		except:
			pass
		try:
			searchFilipino = '(Filipino)'
			for thumb, name, url in match:
				if re.search(searchFilipino, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE):
					m3u_playlist(name, url, thumb)
		except:
			pass
		try:
			searchFarsi = '(Farsi)'
			for thumb, name, url in match:
				if re.search(searchFarsi, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE):
					m3u_playlist(name, url, thumb)
		except:
			pass
		try:
			searchDutch = '(Dutch)'
			for thumb, name, url in match:
				if re.search(searchDutch, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE):
					m3u_playlist(name, url, thumb)
		except:
			pass
		try:
			searchDeutsch = '(Deutsch)'
			for thumb, name, url in match:
				if re.search(searchDeutsch, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE):
					m3u_playlist(name, url, thumb)
		except:
			pass
		try:
			searchChinese = '(Chinese)'
			for thumb, name, url in match:
				if re.search(searchChinese, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE):
					m3u_playlist(name, url, thumb)
		except:
			pass
		try:
			searchCatalan = '(Catalan)'
			for thumb, name, url in match:
				if re.search(searchCatalan, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE):
					m3u_playlist(name, url, thumb)
		except:
			pass
		try:
			searchArabic = '(Arabic)'
			for thumb, name, url in match:
				if re.search(searchArabic, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE):
					m3u_playlist(name, url, thumb)
		except:
			pass
		try:
			searchAfrikaans = '(Afrikaans)'
			for thumb, name, url in match:
				if re.search(searchAfrikaans, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE):
					m3u_playlist(name, url, thumb)
		except:
			pass

def thongbao():
	try:
		text = '[COLOR royalblue][B]***Thông Báo Mới***[/B][/COLOR]'
		if urllib.urlopen(media_link()[0]).getcode() == 200:
			link = make_request(media_link()[0])
		else:
			link = read_file(local_thongbaomoi)
		match=re.compile("<START>(.+?)<END>",re.DOTALL).findall(link)
		for status in match:
			try:
					status = status.decode('ascii')
			except:
					status = status.decode('utf-8')
			status = status.replace('&amp;','')
			text = status
		showText('[COLOR royalblue][B]***Thông Báo Mới***[/B][/COLOR]', text)
	except:
		pass

def text_online():
	xbmc_cache_path = os.path.join(xbmc.translatePath('special://temp'))
	dialog = xbmcgui.Dialog()
	dialog.ok("Giới thiệu về Addon [COLOR lime]Hieuhien.vn Media Center[/COLOR]", "", "Đây là addon được chỉnh sửa từ addon [COLOR lime]Ccloud.tv[/COLOR] của bác [COLOR blue]Tony Nguyễn[/COLOR]. Sử dụng 1 số tính năng để [COLOR red]Hieuhien.vn[/COLOR] có thể dễ dàng cập nhật các addon mới nhất dành cho người dùng KODI Việt Nam. Xin chân thành cảm ơn tác giả [COLOR blue]Tony Nguyễn![/COLOR]")
	sys.exit()

def showText(heading, text):
	id = 10147
	xbmc.executebuiltin('ActivateWindow(%d)' % id)
	xbmc.sleep(100)
	win = xbmcgui.Window(id)
	retry = 50
	while (retry > 0):
		try:
			xbmc.sleep(10)
			retry -= 1
			win.getControl(1).setLabel(heading)
			win.getControl(5).setText(text)
			return
		except:
			pass

def guide():
	dialog = xbmcgui.Dialog()
	ret = dialog.yesno('cCloud TV Guide', '[COLOR yellow]cCloud TV[/COLOR] is now integrated with your favourite TV Guides.','This is currently in beta and not all channels are supported.','[COLOR yellow]>>>>>>>>>>>>>  Choose Your Guide Below  <<<<<<<<<<<<<[/COLOR]','iVue TV Guide','Renegades TV Guide')
	if ret == 1:
		xbmc.executebuiltin("RunAddon(script.renegadestv)")
		sys.exit()
	if ret == 0:
		xbmc.executebuiltin("RunAddon(script.ivueguide)")
		sys.exit()
	else:
		sys.exit()

def channelTester():
	try:
		keyb = xbmc.Keyboard('', 'Enter Channel Name [COLOR lime]- Tiếng Việt Không Dấu[/COLOR]')
		keyb.doModal()
		if (keyb.isConfirmed()):
			name = urllib.quote_plus(keyb.getText(), safe="%/:=&?~#+!$,;'@()*[]").replace('+', ' ')
		keyb = xbmc.Keyboard('', 'Enter Channel URL [COLOR lime](m3u8, rtmp, mp4)[/COLOR]')
		keyb.doModal()
		if (keyb.isConfirmed()):
			url = urllib.quote_plus(keyb.getText(), safe="%/:=&?~#+!$,;'@()*[]").replace('+', ' ')
		keyb = xbmc.Keyboard('', 'Enter Logo URL [COLOR lime]- Không Bắt Buộc[/COLOR]')
		keyb.doModal()
		if (keyb.isConfirmed()):
			thumb = urllib.quote_plus(keyb.getText(), safe="%/:=&?~#+!$,;'@()*[]").replace('+', ' ')
		if len(name) > 0 and len(url) > 0:
			if len(thumb) < 1:
				thumb = icon
			addLink(name, url, 1, thumb, fanart)
	except:
		pass

def localTester():
	if len(local_path) < 1:
		mysettings.openSettings()
		sys.exit()
	else:
		content = read_file(local_path)
		match = re.compile(m3u_regex).findall(content)
		for thumb, name, url in match:
			try:
				m3u_playlist(name, url, thumb)
			except:
				pass

def onlineTester():
	if len(online_path) < 1:
		mysettings.openSettings()
		sys.exit()
	else:
		content = make_request(online_path)
		match = re.compile(m3u_regex).findall(content)
		for thumb, name, url in match:
			try:
				m3u_playlist(name, url, thumb)
			except:
				pass

def m3u_online():
	content = select_server() 
	match = re.compile(m3u_regex).findall(content)
	for thumb, name, url in match[0:1]:
		m3u_playlist('[COLOR yellow][B]' + name + '[/B][/COLOR]', url, thumb)
	for thumb, name, url in sorted(match, key = itemgetter(1)):
		try:
			if 'Welcome to cCloudTV' in name:
				pass
			else:
				m3u_playlist(name, url, thumb)
		except:
			pass

def m3u_playlist(name, url, thumb):
	name = re.sub('\s+', ' ', name).strip()
	url = url.replace('"', ' ').replace('&amp;', '&').strip()
	if ('youtube.com/user/' in url) or ('youtube.com/channel/' in url) or ('youtube/user/' in url) or ('youtube/channel/' in url):
		if 'tvg-logo' in thumb:
			thumb = re.compile(m3u_thumb_regex).findall(str(thumb))[0].replace(' ', '%20')
			addDir(name, url, '', thumb, thumb)
		else:
			addDir(name, url, '', icon, fanart)
	else:
		if ('(Adult)' in name) or ('(Public-Adult)' in name):
			name = 'ADULTS ONLY'.url = 'http://ignoreme.com'
		if 'youtube.com/watch?v=' in url:
			url = 'plugin://plugin.video.youtube/play/?video_id=%s' % (url.split('=')[-1])
		elif 'dailymotion.com/video/' in url:
			url = url.split('/')[-1].split('_')[0]
			url = 'plugin://plugin.video.dailymotion_com/?mode=playVideo&url=%s' % url
		else:
			url = url
		if 'tvg-logo' in thumb:
			thumb = re.compile(m3u_thumb_regex).findall(str(thumb))[0].replace(' ', '%20')
			addLink(name, url, 1, thumb, thumb)
		else:
			addLink(name, url, 1, icon, fanart)

def adult_playlist(name, url, thumb):
	name = re.sub('\s+', ' ', name).strip()
	url = url.replace('"', ' ').replace('&amp;', '&').strip()
	if ('youtube.com/user/' in url) or ('youtube.com/channel/' in url) or ('youtube/user/' in url) or ('youtube/channel/' in url):
		if 'tvg-logo' in thumb:
			thumb = re.compile(m3u_thumb_regex).findall(str(thumb))[0].replace(' ', '%20')
			addDir(name, url, '', thumb, thumb)
		else:
			addDir(name, url, '', icon, fanart)
	else:
		if 'youtube.com/watch?v=' in url:
			url = 'plugin://plugin.video.youtube/play/?video_id=%s' % (url.split('=')[-1])
		elif 'dailymotion.com/video/' in url:
			url = url.split('/')[-1].split('_')[0]
			url = 'plugin://plugin.video.dailymotion_com/?mode=playVideo&url=%s' % url
		else:
			url = url
		if 'tvg-logo' in thumb:
			thumb = re.compile(m3u_thumb_regex).findall(str(thumb))[0].replace(' ', '%20')
			addLink(name, url, 1, thumb, thumb)
		else:
			addLink(name, url, 1, icon, fanart)

def play_video(url):
	media_url = url
	item = xbmcgui.ListItem(name, path = media_url)
	xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)
	return

def get_params():
	param = []
	paramstring = sys.argv[2]
	if len(paramstring)>= 2:
		params = sys.argv[2]
		cleanedparams = params.replace('?', '')
		if (params[len(params)-1] == '/'):
			params = params[0:len(params)-2]
		pairsofparams = cleanedparams.split('&')
		param = {}
		for i in range(len(pairsofparams)):
			splitparams = {}
			splitparams = pairsofparams[i].split('=')
			if (len(splitparams)) == 2:
				param[splitparams[0]] = splitparams[1]
	return param

def getDir(name, url, mode, iconimage, fanart):
	u = sys.argv[0] + "?url=" + urllib.quote_plus(url) + "&mode=" + str(mode) + "&name=" + urllib.quote_plus(name) + "&iconimage=" + urllib.quote_plus(iconimage)
	ok = True
	liz = xbmcgui.ListItem(name, iconImage = "DefaultFolder.png", thumbnailImage = iconimage)
	liz.setInfo( type = "Video", infoLabels = { "Title": name } )
	liz.setProperty('fanart_image', fanart)
	if ('www.youtube.com/user/' in url) or ('www.youtube.com/channel/' in url):
		u = 'plugin://plugin.video.youtube/%s/%s/' % (url.split( '/' )[-2], url.split( '/' )[-1])
	ok = xbmcplugin.addDirectoryItem(handle = int(sys.argv[1]), url = u, listitem = liz, isFolder = True)
	return ok

def addDir(name, url, mode, iconimage, fanart):
	u = sys.argv[0] + "?url=" + urllib.quote_plus(url) + "&mode=" + str(mode) + "&name=" + urllib.quote_plus(name) + "&iconimage=" + urllib.quote_plus(iconimage)
	ok = True
	liz = xbmcgui.ListItem(name, iconImage = "DefaultFolder.png", thumbnailImage = iconimage)
	liz.setInfo( type = "Video", infoLabels = { "Title": name } )
	liz.setProperty('fanart_image', fanart)
	if 'plugin://plugin' in url or 'script://script' in url:
		u = url
	ok = xbmcplugin.addDirectoryItem(handle = int(sys.argv[1]), url = u, listitem = liz, isFolder = True)
	return ok

def addLink(name, url, mode, iconimage, fanart):
	u = sys.argv[0] + "?url=" + urllib.quote_plus(url) + "&mode=" + str(mode) + "&name=" + urllib.quote_plus(name) + "&iconimage=" + urllib.quote_plus(iconimage)
	liz = xbmcgui.ListItem(name, iconImage = "DefaultVideo.png", thumbnailImage = iconimage)
	liz.setInfo( type = "Video", infoLabels = { "Title": name } )
	liz.setProperty('fanart_image', fanart)
	liz.setProperty('IsPlayable', 'true')
	ok = xbmcplugin.addDirectoryItem(handle = int(sys.argv[1]), url = u, listitem = liz)

params = get_params()
url = None
name = None
mode = None
iconimage = None

try:
	url = urllib.unquote_plus(params["url"])
except:
	pass
try:
	name = urllib.unquote_plus(params["name"])
except:
	pass
try:
	mode = int(params["mode"])
except:
	pass
try:
	iconimage = urllib.unquote_plus(params["iconimage"])
except:
	pass

print "Mode: " + str(mode)
print "URL: " + str(url)
print "Name: " + str(name)
print "iconimage: " + str(iconimage)

if mode == None or url == None or len(url) < 1:
	main()

elif mode == 1:
	play_video(url)

elif mode == 2:
	m3u_online()

elif mode == 3:
	text_online()

elif mode == 4:
	thongbao()

elif mode == 18:
	youtube_menu(url)

elif mode == 19:
	youtube_channels(url)

elif mode == 20:
	youtube_list(url)

elif mode == 21:
	youtube_playlist(url)

elif mode == 22:
	youtube_playlist_index(url)

elif mode == 23:
	next_page(url)

elif mode == 24:
	next_page_playlist(url)

elif mode == 25:
	search_youtube()

elif mode == 26:
	youtube_search(url)

elif mode == 27:
	tutorial_links(url)

elif mode == 30:
	vietnam_group()

elif mode == 31:
	viet_tv_group()

elif mode == 40:
	channelTester()

elif mode == 41:
	localTester()

elif mode == 42:
	onlineTester()

elif mode == 48:
	vietnam_abc_order()

elif mode == 50:
	vietnam(name)

elif mode == 51:
	top10()

elif mode == 52:
	sports()

elif mode == 53:
	news()

elif mode == 54:
	documentary()

elif mode == 55:
	entertainment()

elif mode == 56:
	family()

elif mode == 57:
	movie()

elif mode == 58:
	music()

elif mode == 59:
	ondemandmovies()

elif mode == 65:
	ondemandshows()

elif mode == 60:
	twentyfour7()

elif mode == 61:
	radio()

elif mode == 62:
	english()

elif mode == 63:
	lifestyle()

elif mode == 64:
	international()

elif mode == 70:
	vietnam_category()

elif mode == 71:
	viet_Documentary()

elif mode == 72:
	viet_Entertainment()

elif mode == 73:
	viet_Family()

elif mode == 74:
	viet_Movie_Channels()

elif mode == 75:
	viet_Music()

elif mode == 76:
	viet_News()

elif mode == 77:
	viet_OnDemandMovies()

elif mode == 78:
	viet_OnDemandShows()

elif mode == 79:
	viet_Radio()

elif mode == 80:
	viet_RandomAirTime()

elif mode == 81:
	viet_Special_Events()

elif mode == 82:
	viet_Sports()

elif mode == 83:
	viet_Tutorials()

elif mode == 97:
	guide()

elif mode == 98:
	adult()

elif mode == 99:
	search()

elif mode == 100:
	other_addons1()

elif mode == 102:
	other_addons2()	
	
elif mode == 103:
	other_addons3()

elif mode == 104:
	other_addons4()

elif mode == 105:
	other_addons5()

elif mode == 106:
	other_addons6()
	
elif mode == 109:
	clear_cache()	
elif mode == 110:
	other_sources()

elif mode == 111:
	other_sources_list(url)

elif mode == 120:
	adult_addons()
     
xbmcplugin.endOfDirectory(plugin_handle)