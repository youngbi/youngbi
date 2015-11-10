__author__ = 'Anphunl'
# -*- coding: utf-8 -*-
import urllib, urllib2, json, re, urlparse, sys, time, os, hashlib
import xbmc, xbmcgui, xbmcaddon, xbmcplugin
from BeautifulSoup import BeautifulSoup

base_url = sys.argv[0]
addon_handle = int(sys.argv[1])
#args = urlparse.parse_qs(sys.argv[2][1:])

#xbmcplugin.setContent(addon_handle, 'movies')

my_addon = xbmcaddon.Addon()
subtitle_lang = 'VIE'
npp = str(my_addon.getSetting('npp')) == '25'
video_quality = 'Full HD'
use_api = my_addon.getSetting('info_method') == 'API'
use_vi_audio = 'true'
use_dolby_audio = 'true'
try_fullhd = 'true'
apitoken = my_addon.getSetting('tokenhdviet')
if apitoken == 'none': apitoken = '22bb07a59d184383a3c0cd5e3db671fc'
#reload(sys);

fixed_quality = (video_quality != 'Chọn khi xem')

min_width = {'SD' : 0, 'HD' : 1024, 'Full HD' : 1366}
max_width = {'SD' : 1024, 'HD' : 1366, 'Full HD' : 10000}

header_web = {'User-agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:15.0) Gecko/20100101 Firefox/15.0.1'}
header_api = {'User-Agent' : 'Mozilla/5.0 (Linux; U; Android 4.2.2; en-us; AndyWin Build/JDQ39E) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Safari/534.30',
			'Access-Token' : apitoken}
header_app = {'User-agent' : 'com.hdviet.app.ios.HDViet/2.0.1 (unknown, iPhone OS 8.2, iPad, Scale/2.000000)'}

def make_request(url, params=None, headers=None):
	if headers is None:
		headers = header_web
	try:
		if params is not None:
			params = urllib.urlencode(params)
			req = urllib2.Request(url,params,headers)
		else:req = urllib2.Request(url,headers=headers)
		f = urllib2.urlopen(req)
		body=f.read()
		f.close()
		return body
	except:
		pass
def make_request(url, params=None, headers=None):
	if headers is None:
		headers = header_web
	try:
		if params is not None:
			params = urllib.urlencode(params)
			req = urllib2.Request(url,params,headers)
		else:req = urllib2.Request(url,headers=headers)
		f = urllib2.urlopen(req)
		body=f.read()
		f.close()
		return body
	except:
		pass
def login():
	username = my_addon.getSetting('userhdviet')
	password = my_addon.getSetting('passhdviet')
	if len(username) < 5 or len(password) < 1:
		my_addon.setSetting("tokenhdviet", "none")
		xbmc.executebuiltin((u'XBMC.Notification(%s,%s,%s)'%('HDViet','[COLOR red]Chưa nhập user/password HDViet[/COLOR]',3000)).encode("utf-8"))
		return "fail"
	h = hashlib.md5()
	h.update(password)
	passwordhash = h.hexdigest()
	result = make_request('https://api-v2.hdviet.com/user/login?email=%s&password=%s' % (username,passwordhash), None, header_app)
	if "AccessTokenKey" in result:
		res = json.loads(result)["r"]
		my_addon.setSetting("tokenhdviet", res["AccessTokenKey"])
		xbmc.executebuiltin((u'XBMC.Notification(%s,%s,%s)'%('HDViet','[COLOR green]Logged in ![/COLOR]',2000)).encode("utf-8"))
		return res["AccessTokenKey"];
	else:
		#xbmcgui.Dialog().ok("HDViet", passwordhash)
		my_addon.setSetting("tokenhdviet", "none")
		xbmc.executebuiltin((u'XBMC.Notification(%s,%s,%s)'%('HDViet','[COLOR red]Log in Failed ![/COLOR]',2000)).encode("utf-8"))
		return "fail"
def logout():
	my_addon.setSetting("tokenhdviet", "none")
	xbmc.executebuiltin((u'XBMC.Notification(%s,%s,%s)'%('HDViet','[COLOR red]Logged out ![/COLOR]',2000)).encode("utf-8"))
	
def play(movie_id, ep = 0):
	token = my_addon.getSetting('tokenhdviet')
	# get link to play and subtitle
	if token == 'none': token = login()
	if token == 'fail': return
	res = make_request('https://api-v2.hdviet.com/movie/play?movieid=%s&accesstokenkey=%s&ep=%s' % (movie_id, token, ep), None, header_app)
	if "0000000000" in res:
		token = login()
		if token != 'fail': res = make_request('https://api-v2.hdviet.com/movie/play?movieid=%s&accesstokenkey=%s&ep=%s' % (movie_id, token, ep), None, header_app)
		
	movie = json.loads(res)["r"]	
	if movie:
		subtitle_url = ''
		try:
			subtitle_url = movie['Subtitle'][subtitle_lang]['Source']
			if subtitle_url == '':
				subtitle_url = movie['SubtitleExt'][subtitle_lang]['Source']
			if subtitle_url == '':
				subtitle_url = movie['SubtitleExtSe'][subtitle_lang]['Source']
		except:
			pass

		# get link and resolution
		got = False
		if try_fullhd:
			link_to_play = re.sub(r'_\d+_\d+_', '_320_4096_', movie['LinkPlay'])
			result = make_request(link_to_play, None, header_app)
			if 'RESOLUTION=' in result: got = True
		if not got:
			link_to_play = movie['LinkPlay']
			result = make_request(link_to_play, None, header_app)

		# audioindex
		audio_index = 0
		if (use_vi_audio and movie['Audio'] > 0) or (movie['Audio'] == 0 and use_dolby_audio):
			audio_index = 1
		
		playable_items = []
		lines = result.splitlines()

		i = 0
		# find the first meaning line
		while (i < len(lines)):
			if 'RESOLUTION=' in lines[i]:
				break
			i += 1
		while (i < len(lines)):
			playable_item = {}
			playable_item['res'] = lines[i][lines[i].index('RESOLUTION=') + 11:]

			if lines[i + 1].startswith('http'):
				playable_item['url'] = lines[i + 1]
			else:
				playable_item['url'] = movie['LinkPlay'].replace('playlist.m3u8', lines[i + 1])

			playable_items.append(playable_item)
			i += 2

		if not fixed_quality:
			for item in playable_items:
				addMovie(item['res'], {'mode':'play_url', 'stream_url' : '%s?audioindex=%d' % (item['url'], audio_index), 'subtitle_url' : subtitle_url}, '', '')
		else:
			i = len(playable_items) - 1
			while (i >= 0):
				current_width = int(playable_items[i]['res'].split('x')[0])
				if (min_width[video_quality] <= current_width and max_width[video_quality] > current_width) or current_width < min_width[video_quality]:
					break
				i -= 1

			if i >= 0:
				set_resolved_url('%s?audioindex=%d' % (playable_items[i]['url'], audio_index), subtitle_url)

	
def set_resolved_url(stream_url, subtitle_url):
	print subtitle_url
	h1 = '|User-Agent=' + urllib.quote_plus('HDViet/2.0.1 CFNetwork/711.2.23 Darwin/14.0.0')
	h2 = '&Accept=' + urllib.quote_plus('*/*')
	h3 = '&Accept-Language=' + urllib.quote_plus('en-us')
	h4 = '&Connection=' + urllib.quote_plus('Keep-Alive')
	h5 = '&Accept-Encoding=' + urllib.quote_plus('gzip, deflate')
	xbmcplugin.setResolvedUrl(addon_handle, succeeded=True, listitem=xbmcgui.ListItem(label = '', path = stream_url + h1 + h2 + h3 + h5))
	player = xbmc.Player()
	
	subtitlePath = xbmc.translatePath(xbmcaddon.Addon().getAddonInfo('path')).decode("utf-8")
	subfile = xbmc.translatePath(os.path.join(subtitlePath, "temp.sub"))
	try:
		if os.path.exists(subfile):
			os.remove(subfile)
		f = urllib2.urlopen(subtitle_url)
		with open(subfile, "wb") as code:
			code.write(f.read())
		xbmc.sleep(3000)
		xbmc.Player().setSubtitles(subfile)
	except:
		pass
	
	for _ in xrange(30):
		if player.isPlaying():
			break
		time.sleep(1)
	else:
		raise Exception('No video playing. Aborted after 30 seconds.')