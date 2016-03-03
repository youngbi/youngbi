#!/usr/bin/python
# -*- coding: utf-8 -*-

import xbmc, xbmcaddon, xbmcgui
import json, os, re, requests, urllib, urllib2, uuid, zlib
from t0mm0.common.net import Net
from xbmcswift2 import Plugin

addonID = "plugin://plugin.video.hieuhien.vn.phim14.net"
plugin  = Plugin()
listMax = 32

@ plugin.route('/')
def Home():
	items = [
	{'label': 'Phim mới', 'path': '%s/latest/%s/%s' % (addonID, urllib.quote_plus('http://m.phim14.net/danh-sach/phim-moi/page-%s.html'), 1)},
	{'label': 'Phim lẻ', 'path': '%s/movies/%s/%s' % (addonID, urllib.quote_plus('http://m.phim14.net/danh-sach/phim-le/page-%s.html'), 1)},
	{'label': 'Phim bộ', 'path': '%s/series/%s/%s' % (addonID, urllib.quote_plus('http://m.phim14.net/danh-sach/phim-bo/page-%s.html'), 1)},
	{'label': 'Theo thể loại', 'path': '%s/genres' % addonID},
	{'label': 'Theo Quốc gia', 'path': '%s/nations' % addonID},
	{'label': '[ Tìm kiếm ]', 'path': '%s/search' % addonID}
	]
	return plugin.finish(items)

@ plugin.route('/latest/<murl>/<page>')
def Latest(murl, page):
	items = sortedItems(murl, page, 'latest')
	if plugin.get_setting('thumbview', bool):
		if xbmc.getSkinDir() in ('skin.confluence', 'skin.eminence'):
			return plugin.finish(items, view_mode = 500)
		elif xbmc.getSkinDir() == 'skin.heidi':
			return plugin.finish(items, view_mode = 52)
		else:
			return plugin.finish(items)
	else:
		return plugin.finish(items)

@ plugin.route('/movies/<murl>/<page>')
def Movies(murl, page):
	items = sortedItems(murl, page, 'movies')
	if plugin.get_setting('thumbview', bool):
		if xbmc.getSkinDir() in ('skin.confluence', 'skin.eminence'):
			return plugin.finish(items, view_mode = 500)
		elif xbmc.getSkinDir() == 'skin.heidi':
			return plugin.finish(items, view_mode = 52)
		else:
			return plugin.finish(items)
	else:
		return plugin.finish(items)

@ plugin.route('/series/<murl>/<page>')
def Series(murl, page):
	items = sortedItems(murl, page, 'series')
	if plugin.get_setting('thumbview', bool):
		if xbmc.getSkinDir() in ('skin.confluence', 'skin.eminence'):
			return plugin.finish(items, view_mode = 500)
		elif xbmc.getSkinDir() == 'skin.heidi':
			return plugin.finish(items, view_mode = 52)
		else:
			return plugin.finish(items)
	else:
		return plugin.finish(items)

@ plugin.route('/genres')
def ListGenres():
	items = [
	{'label': 'Hành Động', 'path': '%s/genres/%s/%s' % (addonID, urllib.quote_plus('http://m.phim14.net/the-loai/phim-hanh-dong/page-%s.html'), 1)},
	{'label': 'Phiêu Lưu', 'path': '%s/genres/%s/%s' % (addonID, urllib.quote_plus('http://m.phim14.net/the-loai/phim-phieu-luu/page-%s.html'), 1)},
	{'label': 'Kinh Dị', 'path': '%s/genres/%s/%s' % (addonID, urllib.quote_plus('http://m.phim14.net/the-loai/phim-kinh-di/page-%s.html'), 1)},
	{'label': 'Tình Cảm', 'path': '%s/genres/%s/%s' % (addonID, urllib.quote_plus('http://m.phim14.net/the-loai/phim-tinh-cam/page-%s.html'), 1)},
	{'label': 'Hoạt Hình', 'path': '%s/genres/%s/%s' % (addonID, urllib.quote_plus('http://m.phim14.net/the-loai/phim-hoat-hinh/page-%s.html'), 1)},
	{'label': 'Võ Thuật', 'path': '%s/genres/%s/%s' % (addonID, urllib.quote_plus('http://m.phim14.net/the-loai/phim-vo-thuat/page-%s.html'), 1)},
	{'label': 'Hài Hước', 'path': '%s/genres/%s/%s' % (addonID, urllib.quote_plus('http://m.phim14.net/the-loai/phim-hai-huoc/page-%s.html'), 1)},
	{'label': 'Hình Sự', 'path': '%s/genres/%s/%s' % (addonID, urllib.quote_plus('http://m.phim14.net/the-loai/phim-hinh-su/page-%s.html'), 1)},
	{'label': 'Tâm Lý', 'path': '%s/genres/%s/%s' % (addonID, urllib.quote_plus('http://m.phim14.net/the-loai/phim-tam-ly/page-%s.html'), 1)},
	{'label': 'Viễn Tưởng', 'path': '%s/genres/%s/%s' % (addonID, urllib.quote_plus('http://m.phim14.net/the-loai/phim-vien-tuong/page-%s.html'), 1)},
	{'label': 'Thần Thoại', 'path': '%s/genres/%s/%s' % (addonID, urllib.quote_plus('http://m.phim14.net/the-loai/phim-than-thoai/page-%s.html'), 1)},
	{'label': 'Cổ trang', 'path': '%s/genres/%s/%s' % (addonID, urllib.quote_plus('http://m.phim14.net/the-loai/phim-co-trang/page-%s.html'), 1)},
	{'label': 'Chiến Tranh', 'path': '%s/genres/%s/%s' % (addonID, urllib.quote_plus('http://m.phim14.net/the-loai/phim-chien-tranh/page-%s.html'), 1)},
	{'label': 'Âm Nhạc', 'path': '%s/genres/%s/%s' % (addonID, urllib.quote_plus('http://m.phim14.net/the-loai/phim-am-nhac/page-%s.html'), 1)},
	{'label': 'TV Show', 'path': '%s/genres/%s/%s' % (addonID, urllib.quote_plus('http://m.phim14.net/the-loai/phim-tv-show/page-%s.html'), 1)}
]
	return plugin.finish(items)

@ plugin.route('/genres/<murl>/<page>')
def Genres(murl, page = 1):
	items = sortedItems(murl, page, 'genres')
	if plugin.get_setting('thumbview', bool):
		if xbmc.getSkinDir() in ('skin.confluence', 'skin.eminence'):
			return plugin.finish(items, view_mode = 500)
		elif xbmc.getSkinDir() == 'skin.heidi':
			return plugin.finish(items, view_mode = 52)
		else:
			return plugin.finish(items)
	else:
		return plugin.finish(items)

@ plugin.route('/nations')
def ListNations():
	items = [
	{'label': 'Hàn Quốc', 'path': '%s/nations/%s/%s' % (addonID, urllib.quote_plus('http://m.phim14.net/quoc-gia/phim-han-quoc/page-%s.html'), 1)},
	{'label': 'Trung Quốc', 'path': '%s/nations/%s/%s' % (addonID, urllib.quote_plus('http://m.phim14.net/quoc-gia/phim-trung-quoc/page-%s.html'), 1)},
	{'label': 'Đài Loan', 'path': '%s/nations/%s/%s' % (addonID, urllib.quote_plus('http://m.phim14.net/quoc-gia/phim-dai-loan/page-%s.html'), 1)},
	{'label': 'Việt Nam', 'path': '%s/nations/%s/%s' % (addonID, urllib.quote_plus('http://m.phim14.net/quoc-gia/phim-viet-nam/page-%s.html'), 1)},
	{'label': 'Mỹ', 'path': '%s/nations/%s/%s' % (addonID, urllib.quote_plus('http://m.phim14.net/quoc-gia/phim-my/page-%s.html'), 1)},
	{'label': 'Nhật Bản', 'path': '%s/nations/%s/%s' % (addonID, urllib.quote_plus('http://m.phim14.net/quoc-gia/phim-nhat-ban/page-%s.html'), 1)},
	{'label': 'Thái Lan', 'path': '%s/nations/%s/%s' % (addonID, urllib.quote_plus('http://m.phim14.net/quoc-gia/phim-thai-lan/page-%s.html'), 1)},
	{'label': 'Hồng Kông', 'path': '%s/nations/%s/%s' % (addonID, urllib.quote_plus('http://m.phim14.net/quoc-gia/phim-hong-kong/page-%s.html'), 1)},
	{'label': 'Philippines', 'path': '%s/nations/%s/%s' % (addonID, urllib.quote_plus('http://m.phim14.net/quoc-gia/phim-philippines/page-%s.html'), 1)},
	{'label': 'Châu Âu', 'path': '%s/nations/%s/%s' % (addonID, urllib.quote_plus('http://m.phim14.net/quoc-gia/phim-chau-au/page-%s.html'), 1)},
	{'label': 'Nước Khác', 'path': '%s/nations/%s/%s' % (addonID, urllib.quote_plus('http://m.phim14.net/quoc-gia/phim-nuoc-khac/page-%s.html'), 1)}
]
	return plugin.finish(items)

@ plugin.route('/nations/<murl>/<page>')
def Nations(murl, page):
	items = sortedItems(murl, page, 'nations')
	if plugin.get_setting('thumbview', bool):
		if xbmc.getSkinDir() in ('skin.confluence', 'skin.eminence'):
			return plugin.finish(items, view_mode = 500)
		elif xbmc.getSkinDir() == 'skin.heidi':
			return plugin.finish(items, view_mode = 52)
		else:
			return plugin.finish(items)
	else:
		return plugin.finish(items)

@ plugin.route('/search/')
def Search():
	keyb = plugin.keyboard(heading = 'Tìm kiếm')
	if keyb:
		searchUrl = "http://m.phim14.net/search/keyword/page-%s.html".replace("keyword", keyb).replace(" ", "-")
		ListGenres = '%s/search/%s/%s' % (addonID, urllib.quote_plus(searchUrl), 1)
		plugin.redirect(ListGenres)

@ plugin.route('/search/<murl>/<page>')
def SearchResults(murl, page):
	items = sortedItems(murl, page, 'search')
	if plugin.get_setting('thumbview', bool):
		if xbmc.getSkinDir() in ('skin.confluence', 'skin.eminence'):
			return plugin.finish(items, view_mode = 500)
		elif xbmc.getSkinDir() == 'skin.heidi':
			return plugin.finish(items, view_mode = 52)
		else:
			return plugin.finish(items)
	else:
		return plugin.finish(items)

@ plugin.route('/mirrors/<murl>')
def Mirrors(murl):
	items = []
	for server in servers(murl):
		video = {}
		video["label"] = server["name"].strip()
		guid = str(uuid.uuid1())
		eps = plugin.get_storage(guid)
		eps["list"] = server["eps"]
		video["path"] = '%s/eps/%s' % (addonID, urllib.quote_plus(guid))
		items.append(video)
	return plugin.finish(items)

@ plugin.route('/eps/<eps_list>')
def Episodes(eps_list):
	items = []
	for episode in plugin.get_storage(eps_list)["list"]:
		video = {}
		video["label"] = episode["name"].strip()
		video["is_playable"] = True
		video["path"] = '%s/play/%s' % (addonID, urllib.quote_plus(episode["url"]))
		items.append(video)
	return plugin.finish(items)

@ plugin.route('/play/<url>')
def Play(url):
	dialogWait = xbmcgui.DialogProgress()
	dialogWait.create('phim14.net', 'Loading video. Please wait...')
	plugin.set_resolved_url(LoadVideos(url))
	dialogWait.close()
	del dialogWait

def LoadVideos(url):
	pageContent = getUrl(url)
	if "youtube" in pageContent:
		match = re.compile('(youtu\.be\/|youtube-nocookie\.com\/|youtube\.com\/(watch\?(.*&)?v=|(embed|v|user)\/))([^\?&"\'>]+)').findall(pageContent)
		youtubeID = match[0][len(match[0])-1].replace('v/', '')
		return 'plugin://plugin.video.youtube/?action=play_video&videoid=%s' % youtubeID
	if '{link:"' in pageContent:
		link = re.compile('\{link:"(.+?)"').findall(pageContent)[0]
		script = re.compile ( '<script type="text/javascript" src="(http://player\d+.phim14.net/.+?)"></script>').findall(pageContent)[0].replace("gkpluginsphp.js","gkpluginsphp.php")
		gkp = requests.post(script, data={'link': link, 'f': 'true'}).json()
		if "list" in gkp:
			source = gkp["list"][0]["link"][0]["link"]
			if plugin.get_setting('HQ', bool):
				source = gkp["list"][0]["link"][-1]["link"]
		else:
			source = gkp["link"][0]["link"]
			if plugin.get_setting('HQ', bool):
				source = gkp["link"][-1]["link"]
		return source
	if "www.dailymotion.com" in pageContent:
		match = re.compile('<div class="jp-player-video"><iframe src="(.+?)"[^>]*>').findall(pageContent)
		source = getDailyMotionUrl(match[0])
		return source

def sortedItems(url, page, route_name):
	pageNumber = int(page)+1
	pageContent = getUrl(url % page)
	match = re.compile('<a href="(http://m.phim14.net/phim/.+?)" class="content-items"><img src="(.+?)" alt="(.+?)"[^>]*><h3>.+?</h3><h4>.+?</h4><ul[^>]*><li>Năm phát hành:(.+?)</li><li>Thể loại:.+?</li></ul><p[^>]*>Trạng thái:(.*?)</p></a>').findall(pageContent)
	items = []
	for path, thumbnail, label, year, label2 in match:
		video = {}
		video["label"] = "%s(%s)" % (label, label2)
		video["thumbnail"] = thumbnail
		video["info"] = {"year": year}
		video["path"] = '%s/%s/%s' % (addonID, "mirrors", urllib.quote_plus(path.replace("/phim/", "/xem-phim/")))
		items.append(video)
	if len(items) == listMax:
		items.append({'label': 'Next >>', 'path': '%s/%s/%s/%s' % (addonID, route_name, urllib.quote_plus(url), pageNumber), 'thumbnail': 'http://icons.iconarchive.com/icons/rafiqul-hassan/blogger/128/Arrow-Next-icon.png'})
	return items

def servers(murl):
	pageContent = getUrl(murl)
	match = re.compile('<span class="svname">(.+?)</span><span class="svep">(.+?)</span>').findall(pageContent)
	name = re.compile('<title>(.+?)</title>').findall(pageContent)[0]
	serverList = []
	for serverName, episodeList in match:
		serverEps = []
		for url, part in re.compile('<a[^>]*href="(.+?)"[^>]*>(.+?)</a>').findall(episodeList):
			episode = {}
			episode["url"] = url
			episode["name"] = "Part %s - %s" % (part, name.split(" | ")[0])
			serverEps.append(episode)
		server = {}
		server["name"] = serverName
		server["eps"] = serverEps
		serverList.append(server)
	return serverList

@ plugin.cached(TTL = 60)
def getUrl(url):
	r = urllib2.Request(url)
	r.add_header('User-Agent', 'Mozilla/5.0(iPhone; U; CPU iPhone OS 5_1_1 like Mac OS X; da-dk)AppleWebKit/534.46.0(KHTML, like Gecko)CriOS/19.0.1084.60 Mobile/9B206 Safari/7534.48.3')
	r.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8')
	r.add_header('Accept-Encoding', 'gzip, deflate, sdch')
	r.add_header('Cookie', 'location.href=1')
	response = urllib2.urlopen(r)
	content = response.read()
	response.close()
	if "gzip" in response.info().getheader('Content-Encoding'):
		content = zlib.decompress(content, 16 + zlib.MAX_WBITS)
	content = ''.join(content.splitlines()).replace('\'', '"')
	content = content.replace('\n', '')
	content = content.replace('\t', '')
	content = re.sub('  +', ' ', content)
	content = content.replace('> <', '><')
	return content

def GetContent(link):
	try:
		net = Net()
		second_response = net.http_GET(link)
		return second_response.content
	except BaseException as e:
		d = xbmcgui.Dialog()
		d.ok(link,str(e))

def getDailyMotionUrl(link):
	content = GetContent(link)
	if content.find('"statusCode":410') > 0 or content.find('"statusCode":403') > 0:
		xbmc.executebuiltin('XBMC.Notification(Info:,'+translation(30022)+' (DailyMotion)!,5000)')
		return ""
	else:
		get_json_code = re.compile(r'dmp\.create\(document\.getElementById\(\'player\'\),\s*(.+?)}}\)').findall(content)[0]
		#print len(get_json_code)
		print get_json_code
		cc= json.loads(get_json_code+"}}")['metadata']['qualities'] #['380'][0]['url']
		#print cc
		if '1080' in cc.keys():
			#print 'found hd'
			return cc['1080'][0]['url']
		elif '720' in cc.keys():
			return cc['720'][0]['url']
		elif '480' in cc.keys():
			return cc['480'][0]['url']
		elif '380' in cc.keys():
			return cc['380'][0]['url']
		elif '240' in cc.keys():
			return cc['240'][0]['url']
		elif 'auto' in cc.keys():
			return cc['auto'][0]['url']
		else:
			xbmc.executebuiltin('XBMC.Notification(Info:, No playable Link found (DailyMotion)!,5000)')

if __name__ == '__main__':
	plugin.run()