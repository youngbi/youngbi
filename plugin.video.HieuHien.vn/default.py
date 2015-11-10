__author__ = 'hieuhien.vn'
#coding=utf-8
import xbmc,xbmcplugin,xbmcgui,xbmcaddon,urllib,urllib2,re,os,unicodedata,datetime,random,json
import base64

home = xbmc.translatePath(xbmcaddon.Addon().getAddonInfo('path')).decode("utf-8")
sys.path.append(os.path.join(home,'resources','lib'));from urlfetch import get,post;import xshare;import hdonline;import hdviet;import hayhaytv
from config import hayhaytv_vn,hdviet_com,dangcaphd_com,megabox_vn,phimgiaitri_vn,phimmoi_net, hdonlinevn,megaboxvn,vuahdtv,phimmoinet, csn,csn_logo, nct,nct_logo, home,logos,dataPath,www,color
from setting import myaddon, danhmucphim,hdonline_view,vuahd_view,hdviet_view,hayhaytv_view,dangcaphd_view,megabox_view,phimmoi_view,phimgiaitri_view
from xshare import myfolder,copyxml,subsfolder,tempfolder,rows

icon={}
for item in ['hdonline', 'vuahd', 'hdviet', 'hayhaytv', 'dangcaphd', 'megabox', 'phimmoi', 'phimgiaitri', 'next', 'icon']:
	icon.setdefault(item,os.path.join(logos,'%s.png'%item))
### -----------------
def setViewMode(view_mode = '2'):
	skin_used = xbmc.getSkinDir()
	if skin_used == 'skin.xeebo':
		xbmc.executebuiltin('Container.SetViewMode(52)')
	else:
		if view_mode == "1": # List
			xbmc.executebuiltin('Container.SetViewMode(502)')
		elif view_mode == "2": # Big List
			xbmc.executebuiltin('Container.SetViewMode(51)')
		elif view_mode == "3": # Thumbnails
			xbmc.executebuiltin('Container.SetViewMode(500)')
		elif view_mode == "4": # Poster Wrap
			xbmc.executebuiltin('Container.SetViewMode(501)')
		elif view_mode == "5": # Fanart
			xbmc.executebuiltin('Container.SetViewMode(508)')
		elif view_mode == "6":  # Media info
			xbmc.executebuiltin('Container.SetViewMode(504)')
		elif view_mode == "7": # Media info 2
			xbmc.executebuiltin('Container.SetViewMode(503)')
		elif view_mode == "8": # Media info 3
			xbmc.executebuiltin('Container.SetViewMode(515)')
		return
	
def strVnEn(str1, str2):
	try:                                                                   
		str = str1.lower()
		if str == '': return
		if type(str).__name__ == 'unicode': str = str.encode('utf-8')
		items = ["á","à","ả","ạ","ã","â","ấ","ầ","ẩ","ậ","ẫ","ă","ắ","ằ","ẳ","ặ","ẵ","đ","í","ì","ỉ","ị","ĩ","é","è","ẻ","ẹ","ẽ","ê","ế","ề","ể","ệ","ễ","ó","ò","ỏ","ọ","õ","ô","ố","ồ","ổ","ộ","ỗ","ơ","ớ","ờ","ở","ợ","ỡ","ú","ù","ủ","ụ","ũ","ư","ứ","ừ","ử","ự","ữ","ý","ỳ","ỷ","ỵ","ỹ"]
		for item in items:			
			if item in str :
				return str2, str1 + ' - ' + str2
		return str1, str2 + ' - ' + str1
	except: pass	
	
def fixString(string):
	string = string.replace('&amp;','&').replace("&#39;","'")
	return string
	
def fixSearch(string):
	string = string.replace('+','-').replace(' ','-')	
	string = string.replace('?','').replace('!','').replace('.','').replace(':','').replace('"','')
	string = string.replace('&amp;','and').replace('&','and').replace("&#39;","")
	i = 1
	while i < 10:
		string = string.replace('(Season '+str(i)+'','Season '+str(i))
		i += 1  # This is the same as i = i + 1	
	string = string.replace('- Season','Season')	# MegaBox	
	string = string.strip()
	return string

def fixSearchss(string):
	string = string.replace('+','-').replace(' ','-')	
	string = string.replace('?','').replace('!','').replace('.','').replace(':','')	
	string = string.replace('&amp;','and').replace('&','and').replace("&#39;","")
	string = string.upper()
	string = string.strip()
	return string
###-----------------	
def alert(message,title="Cantobu Media"):
  xbmcgui.Dialog().ok(title,"",message)

def notification(message, timeout=7000):
  xbmc.executebuiltin((u'XBMC.Notification("%s", "%s", %s)' % ('Cantobu Media', message, timeout)).encode("utf-8"))	
###-----------------
def Home():
	content = Get_Url(DecryptData(homeurl))
	match=re.compile("<title>([^<]*)<\/title>\s*<link>([^<]+)<\/link>\s*<thumbnail>(.+?)</thumbnail>").findall(content)
	for title,url,thumbnail in match:
		title = '[B]'+title+'[/B]'
		if 'MYPLAYLIST' in url or 'tvcatchup' in url:
			pass
		elif 'Setting' in url:			
			addLink(title,url,'menu_group',thumbnail)		
		else:
			addDir(title,url,'menu_group',thumbnail)		
		
def Menu_Group(url):
	if 'Setting' in url:
		xbmcaddon.Addon().openSettings()
		return
	elif 'MenuTivi' in url:
		content = Get_Url(url)
		match=re.compile("<title>([^<]*)<\/title>\s*<link>([^<]+)<\/link>\s*<thumbnail>(.+?)</thumbnail>").findall(content)
		for title,url,thumbnail in match:
			addDir(title,url,'indexgroup',thumbnail)
		setViewMode('3')
	elif 'MenuLiveShow' in url:
		content = Get_Url(url)
		match=re.compile("<title>([^<]*)<\/title>\s*<link>([^<]+)<\/link>\s*<thumbnail>(.+?)</thumbnail>").findall(content)
		for title,url,thumbnail in match:
			addDir(title,url,'indexgroup',thumbnail)
		setViewMode('3')
	elif 'MenuShows' in url:
		content = Get_Url(url)
		match=re.compile("<title>([^<]*)<\/title>\s*<link>([^<]+)<\/link>\s*<thumbnail>(.+?)</thumbnail>").findall(content)
		for title,url,thumbnail in match:
			if 'xml' in url:
				addDir(title,url,'get_xml',thumbnail)
			elif 'm3u' in url:
				addDir(title,url,'get_m3u',thumbnail)				
		setViewMode('3')
	elif 'MenuMusic' in url:
		content = Get_Url(url)
		match=re.compile("<title>([^<]*)<\/title>\s*<link>([^<]+)<\/link>\s*<thumbnail>(.+?)</thumbnail>").findall(content)
		for title,url,thumbnail in match:
			if 'LIVESHOWS' in url:
				addDir(title,url,'index_group',thumbnail)
			elif 'm3u' in url:
				addDir(title,url,'get_m3u',thumbnail)
			else:
				addDir(title,url,'category',thumbnail)
		setViewMode('2')
	elif 'MenuMovie' in url:
		categoryroot(url)
	elif 'MenuTube' in url:
		content = Get_Url(url)
		names = re.compile('<name>(.+?)</name>\s*<thumbnail>(.+?)</thumbnail>').findall(content)
		for name,thumb in names:
			addDir(name, url+"?n="+name, 'index', thumb)		
		setViewMode('3')
	elif 'SEARCH' in url:
		addDir('Tìm Video Chia Sẻ Nhạc','TimVideoCSN','search',csn_logo)
		addDir('Tìm Video Nhạc Của Tui','TimVideoNCT','search',nct_logo)
		servers = ['HDOnline', 'HDViet', 'PhimMoi']
		for server in servers:
			addDir('Tìm kiếm kho phim '+server,server,'search',icon[server.lower()])
		setViewMode('2')

def categoryroot(url):
	if danhmucphim == 'HDOnline' or 'HDOnline' in url:
		link = hdonline.GetContent("http://hdonline.vn/")
		link = ''.join(link.splitlines()).replace('\'','"')
		try:
			link =link.encode("UTF-8")
		except: pass
		vidcontent=re.compile('<nav class="tn-gnav">(.+?)</nav> ').findall(link)
		vidcontentlist=[]
		if(len(vidcontent)>0):
			addDir(color['search']+'Tìm kiếm kho phim HDOnline[/COLOR]','HDOnline','search',icon['hdonline'])
			vidcontentlist=re.compile('<li>(.+?)</div>\s*</div>\s*</li>').findall(vidcontent[0])
			for vidcontent in vidcontentlist:
				mainpart=re.compile('<a href="(.+?)"> <span class="tnico-(.+?)"></span>(.+?)</a>').findall(vidcontent)
				mainname=mainpart[0][2]
				href=mainpart[0][0]
				if 'hdonline.vn' not in href:href='http://hdonline.vn'+mainpart[0][0]
				vidlist=re.compile('<li><a [^>]*href=["\']?([^>^"^\']+)["\']?[^>]*>(.+?)</a></li>').findall(vidcontent)
				
				if 'TIN' in mainname : mainname = "MORE";href='http://hdonline.vn/danh-sach/phim-moi.html'
				xshare.addir('[B]'+mainname+'[/B]',href,img,'fanart',mode='category',page=0,query='Index',isFolder=True)	
				for vurl,vname in vidlist:
					#vname = vname.replace('Phim ','')
					if 'Mỹ' in vname : vname = 'Âu/	' + vname
					if mainname == "MORE" : vurl = 'http://hdonline.vn'+vurl
					if(vurl.find("javascript:") ==-1 and len(vurl) > 3):
						xshare.addir('- '+vname,vurl,img,'fanart',mode='category',page=0,query='Index',isFolder=True)	
			#vidcontent=re.compile('<nav class="tn-gnav">(.+?)</nav> ').findall(link)		
			#vidcontent=re.compile('<span class="tnico-news"></span> (.+?) </a>').findall(link)						
			#items2=re.findall('<a href="(.+?)" .?title=".+?">(.+?)</a>',vidcontent[0])	
			#for href,name in items2:
				#xshare.addir(name,href,img,'fanart',mode=10,page=0,query='Index',isFolder=True)					
	elif danhmucphim == 'HDViet' or 'HDViet' in url:
		home='http://movies.hdviet.com/';direct_link='https://api-v2.hdviet.com/movie/play?movieid=%s'
		addDir(color['search']+'Tìm kiếm kho phim HDViet[/COLOR]','HDViet','search',icon['hdviet'])
		
		xshare.addir('[B]PHIM LẺ[/B]',hdviet_com+'phim-le.html',img,fanart='',mode='category',page=1,query='',isFolder=True)
		body=xshare.make_request('http://movies.hdviet.com/phim-le.html')
		items=re.findall('<a href="(.+?)" .?menuid="(.+?)" .?title=".+?" >(.+?)</a>',body)
		for href,id,name in items:
			xshare.addir('- '+name,href,img,fanart='',mode='category',page=1,query=id,isFolder=True)		
		xshare.addir('[B]PHIM BỘ[/B]',hdviet_com+'phim-bo.html',img,fanart='',mode='category',page=1,query='',isFolder=True)
		body=xshare.make_request('http://movies.hdviet.com/phim-bo.html')
		items=re.findall('<a href="(.+?)" menuid="(.+?)" title=".+?">(.+?)</a>',body)
		items+=re.findall('<a class="childparentlib" menuid="(.+?)" href="(.+?)" title=".+?">(\s.*.+?)</a>',body)
		for href,id,name in items:
			if 'au-my' in href or 'tai-lieu' in href:name='Âu Mỹ %s'%name.strip()
			elif 'hong-kong' in href:name='Hồng Kông %s'%name.strip()
			elif 'trung-quoc' in href:name='Trung Quốc %s'%name.strip()
			else:name=name.strip()
			if href in '38-39-40':temp=href;href=id;id=temp
			xshare.addir('- '+name,href,img,fanart='',mode='category',page=1,query=id,isFolder=True)
		
		addLink('[B]THỂ LOẠI PHIM[/B]',"",0,img)
		for href,name in re.findall('<p><a href="(.+?)" title=".+?">(.+?)</a></p>',xshare.make_request(home)):
			xshare.addir('- '+name,href,img,fanart='',mode='category',page=1,query=id,isFolder=True)
			
		addLink('[B]THẾ GIỚI SAO[/B]',"",0,img)
		for href,name in re.findall('<li><a href="(.+?)" title=".+?">(.+?)</a></li>',xshare.make_request(home)):
			if 'Tất cả' not in name:
				xshare.addir('- '+name.replace('&nbsp;',''),href,img,fanart='',mode='category',page=1,query=id,isFolder=True)
		addDir('Đăng xuất tài khoản', '', 'logouthdviet', '')								
		setViewMode('2')
	elif danhmucphim == 'HayHayTV' or 'HayHayTV' in url:
		addDir(color['search']+'Tìm kiếm kho phim HayHayTV[/COLOR]','HayHayTV','search',icon['hayhaytv'])
		ajax=hayhaytv_vn+'ajax_hayhaytv.php'
		body=xshare.make_request(hayhaytv_vn)					
		for href,name in re.findall('menu_fa_text.+?" href="(.+?)".*>(.+?)</a>',body):
			url = href
			if name in 'PHIM LẺ-PHIM BỘ-SHOWS':
				name='[B]'+name+'[/B]'
				xshare.addir(name,href,img,fanart='',mode='category',page=1,query='M2',isFolder=True)
																			
				body=xshare.make_request(hayhaytv_vn+'/tim-kiem');pattern='http.+/\w{1,6}-'
				body=body[body.find(url):];body=body[:body.find('mar-r20')]
				for href,name in re.findall('href="(.+?)".*?>(.+?)</a></li>',body):
					xshare.addir('- '+name,href,img,fanart='',mode='category',page=1,query='M2',isFolder=True)
		addDir('Đăng xuất tài khoản', '', 'logouthayhaytv', '')								
		setViewMode(view_mode = '2')
	elif danhmucphim == 'DangCapHD' or 'DangCapHD' in url:
		addDir(color['search']+'Tìm kiếm kho phim DangCapHD[/COLOR]','DangCapHD','search',icon['dangcaphd'])
		body=xshare.make_request(dangcaphd_com)		
		for name in re.findall('</i>(.+?)<span class="caret">',body):
			name='[B]'+ name.strip() +'[/B]'
			xshare.addir(name,dangcaphd_com,icon['dangcaphd'],mode='category',query='DC1',isFolder=True)
			
			#body=xshare.make_request(dangcaphd_com)
			if 'the loai' in  xshare.no_accent(name).lower():
				for href,name in re.findall('<a href="(http://dangcaphd.com/cat.+?)" title="(.+?)">',body):
					#name='[B]'+name.strip()+'[/B]'
					xshare.addir('- '+name.strip(),href,icon['dangcaphd'],mode='category',query='DC2',isFolder=True)
			if 'quoc gia' in  xshare.no_accent(name).lower():
				for href,name in re.findall('<a href="(http://dangcaphd.com/country.+?)" title="(.+?)">',body):
					xshare.addir('- '+name.strip(),href,icon['dangcaphd'],mode='category',query='DC2',isFolder=True)
			
		for href,name in re.findall('<a href="(.+?)"><i class=".+?"></i>(.+?)</a>',body):
			if 'channel.html' not in href and 'product.html' not in href:
				name='[B]'+name.strip()+'[/B]'
				xshare.addir(name,href,icon['dangcaphd'],mode='category',query='DC2',isFolder=True)					
		setViewMode('2')
	elif danhmucphim == 'PhimMoi' or 'PhimMoi' in url:
		addDir(color['search']+'Tìm kiếm kho phim PhimMoi[/COLOR]','PhimMoi','search',icon['phimmoi'])
		body=xshare.make_request(phimmoi_net)
		content=xshare.xsearch('<ul id=".+?"(.+?)</ul></div>',body,1)
		for title in re.findall('<a>(.+?)</a>',content):
			addLink('[B]'+title+'[/B]',"",0,img)
			#xshare.addir('[B]'+title+'[/B]','',icon['phimmoi'],mode=mode,query='menubar',isFolder=True)

			content_=xshare.xsearch('<ul id=".+?"(.+?)</ul></div>',body,1)
			gen={'Thể loại':'the-loai','Quốc gia':'quoc-gia','Phim lẻ':'phim-le','Phim bộ':'phim-bo'}
			query=gen.get(re.sub('\[/?COLOR.*?\]|\(.+?\)','',title).strip())
			pattern='<a href="(%s/.*?)">(.+?)</a>'%query
			for href,title in re.findall(pattern,content_):
				xshare.addir('- '+title,phimmoi_net+href,icon['phimmoi'],mode='category',isFolder=True)
						
		for href,title in re.findall('<a href="([\w|-]+/|http://www.phimmoi.net/tags/.*?)">(.+?)</a>',content):
			if 'tags' not in href:href=phimmoi_net+href
			xshare.addir('[B]'+title+'[/B]',href,icon['phimmoi'],mode='category',isFolder=True)

			content_=xshare.xsearch('<ul id=".+?"(.+?)</ul></div>',body,1)
			gen={'Thể loại':'the-loai','Quốc gia':'quoc-gia','Phim lẻ':'phim-le','Phim bộ':'phim-bo'}
			query=gen.get(re.sub('\[/?COLOR.*?\]|\(.+?\)','',title).strip())
			pattern='<a href="(%s/.*?)">(.+?)</a>'%query
			for href,title in re.findall(pattern,content_):
				if len(href)>8:	#bỏ danh mục phim-le, phim-bo
					xshare.addir('- '+title,phimmoi_net+href,icon['phimmoi'],mode='category',isFolder=True)					
		setViewMode('2')		
	elif danhmucphim == 'Tất cả':
		#servers = ['HDOnline', 'VuaHD', 'HDViet', 'HayHayTV', 'DangCapHD', 'MegaBox', 'PhimMoi', 'PhimGiaiTri']
		servers = ['HDOnline', 'HDViet', 'PhimMoi']
		for server in servers:
			name='[B]'+'Kho phim '+server+'[/B]'				
			xshare.addir(name,'MenuMovie|'+server,icon[server.lower()],mode='menu_group',query='',isFolder=True)
		setViewMode('2')				
		
def category(url, mode=''):
	if 'ott.thuynga' in url:
		match=menulist(dataPath+'/data/category.xml')
		for title,url,thumbnail in match:	  
			if 'ott.thuynga' in url:
				addDir(title,url,'episodes',thumbnail)
			else:pass				
	elif 'chiasenhac' in url:
		content=Get_Url(url)
		addDir(color['search']+'Tìm kiếm[/COLOR]','TimVideoCSN','search',csn_logo)	
		
		match=re.compile("<a href=\"hd(.+?)\" title=\"([^\"]*)\"").findall(content)[1:8]
		for url,name in match:
			addDir(name,csn+'hd'+url,'episodes',csn_logo)
	elif 'nhaccuatui' in url:
		content=Get_Url(url)
		addDir(color['search']+'Tìm kiếm[/COLOR]','TimVideoNCT','search',nct_logo)	
	
		match = re.compile("href=\"http:\/\/m.nhaccuatui.com\/mv\/(.+?)\" title=\"([^\"]*)\"").findall(content)
		for url, name in match:		
			if 'Phim' in name:
				pass
			else:
				addDir(name,nct + 'mv/' + url,'search_result',nct_logo)
		#match = re.compile("href=\"http:\/\/m.nhaccuatui.com\/mv\/(.+?)\" title=\"([^\"]*)\"").findall(content)
		#for url, name in match:
			#if 'Phim' in name:
				#add_dir('[COLOR orange]' + name + '[/COLOR]', nctm + 'mv/' + url, 3, logos + 'nhaccuatui.png', fanart)					
	else: Search_Result(url, query='', mode=mode)

def episodes(url, name=''):
	if 'hdonline.vn' in url :
		items=re.findall('<a href="(.+?)" .+?"><span>(.+?)</span></a>',xshare.make_request(url));
		for url, eps in items:
			name = name.replace('[COLOR tomato]', '').replace('[/COLOR]', '')						
			xshare.addir('Tập '+str(eps)+' - '+name,url,img,'fanart',mode='hdonlineplay',isFolder=False)
	elif 'vuahd.tv' in url :
		items=re.findall('<a href="#" class="btn-1 btnUpgrade">Xem (.+?)</a>',xshare.make_request(url));temp=[]
		for eps in items:	
			if eps not in temp:
				temp.append(eps);title=eps+'-'+name;tap=xshare.xshare_group(re.search('(\d{1,3})',eps),1)
				if tap:tap=format(int(tap),'02d')
				else:continue
				url = url.replace('tv-series/','')+'-%s'%tap
				url = url+'/watch'
				url = vuahdtv + url.replace('/', '%2F')			
				xshare.addir(title,url,img,'fanart',mode='16',isFolder=False)		
	elif 'hdviet.com' in url :
		url = query		
		href='http://movies.hdviet.com/lay-danh-sach-tap-phim.html?id=%s'%url
		response=xshare.make_request(href,resp='j')
		if not response:return
		for eps in range(1,int(response["Sequence"])+1):		
			name=re.sub(' \[COLOR tomato\]\(\d{1,4}\)\[/COLOR\]','',name)
			title='Tập %s/%s-%s'%(format(eps,'0%dd'%len(response['Episode'])),str(response['Episode']),re.sub('\[.?COLOR.{,12}\]','',name))
			xshare.addir(title,'%s_e%d'%(url,eps),img,fanart='',mode='22',page=1,query='hdvietplay')		
	elif 'hayhaytv.vn' in url :			
		if 'xem-show' in url:pattern='href="(.+?)".*src=".+?"\D*(\d{1,3})<'
		else:pattern='<a class=".*?" href="(.+?)"\D*(\d{1,3})<'
		resp=xshare.make_request(url,resp='o');body=resp.body if resp.status==200 else xshare.make_request(resp.headers['location'])
		items=re.findall(pattern,body)
		if not page:
			id=xshare.xshare_group(re.search('FILM_ID\D{3,7}(\d{3,6})',body),1)	
			url='https://www.fshare.vn/folder/5VNFUPO32P6F'
			hd=xshare.xshare_group(re.search('<title>.*xx(.+?)xx.*</title>',xshare.make_request(url)),1).split('-')
			#['Authorization', 'Basic', 'YXBpaGF5OmFzb2tzYXBySkRMSVVSbzJ1MDF1cndqcQ==']
			data='device=xshare&secure_token=1.0&request='+urllib.quote('{"movie_id":"%s"}'%id)
			response=xshare.make_post('http://api.hayhaytv.vn/movie/movie_detail',{hd[0]:'%s %s'%(hd[1],hd[2])},data)
			try:json=response.json['data']
			except:json={}						
			if json:page=json['total_episode'].encode('utf-8')
		for href,epi in items:
			xshare.addir('Tập %s/%s-%s'%(epi,page,re.sub('\[.?COLOR.{,12}\]','',name)),href,img,fanart='',mode=23,page=1,query='play')						
	elif 'phimmoi.net' in url :	
		body=xshare.make_request(url+'xem-phim.html');name=re.sub('\[/?COLOR.*?\]|\(.+?\)|\d{1,3} phút','',name).strip()
		for detail in re.findall('data-serverid="pcs"(.+?)</li></ul></div>',body,re.DOTALL):
			title=' '.join(s for s in xshare.xsearch('<h3 class="server-name">(.+?)</h3>',detail,1,re.DOTALL).split())
			if title and 'tập phim' not in title:xshare.addir('[COLOR lime]%s[/COLOR]'%'---'+title,'',img,'',mode,1,'no')
			label=name.replace('TM ','') if title and 'Thuyết minh' not in title else name
			for title,href in re.findall('title="(.+?)".+?href="(.+?)"',detail,re.DOTALL):
				try:
					xshare.addir(title+' '+label,phimmoi_net+href,img,'fanart',mode='24',query='pmplay',isFolder=False)
				except:
					xshare.addir(title+' '+label,href,img,'fanart',mode='16',query=phimmoi_net,isFolder=False)
	elif 'megabox.vn' in url :	
		content = Get_Url(url)
		match = re.compile("href='(.+?)' >(\d+)<").findall(content)
		for url, title in match:
			url = megaboxvn + url.replace('/', '%2F')
			xshare.addir('Tập ' + title,url,img,'fanart',mode='16',isFolder=False)
	elif 'phimgiaitri.vn' in url :
		add_Link('Tập 1', url, img)
		
		content = Get_Url(url)
		match = re.compile('<a href="(.+?)" page=(.+?)>').findall(content)
		for url,title in match:		
			add_Link('Tập ' + title, url, img)
	elif 'youtube' in url:
		add_Link(name, url, thumbnail)
	elif 'chiasenhac' in url:
		content = Get_Url(url)
		items=re.compile("<a href=\"([^\"]*)\" title=\"(.*?)\"><img src=\"([^\"]+)\"\s.+\s.+\s.+\s.+\s.+\s.+\s.+\s*<span style=\"color: .*?\">(.*?)</span>").findall(content)
		for url,name,thumbnail,cat in items:
			add_Link(name+color['cat']+' ['+cat+'][/COLOR]',csn+url,thumbnail)
		items=re.compile("<a href=\"hd\/video\/([a-z]-video\/new[0-9]+).html\" class=\"npage\">(\d+)<\/a>").findall(content)
		for url,name in items:
			addDir('[COLOR lime]Mới Chia Sẻ - Trang '+name+'[/COLOR]',csn+'hd/video/'+url+'.html','episodes',icon['next'])
		items=re.compile("<a href=\"hd\/video\/([a-z]-video\/down[0-9]+).html\" class=\"npage\">(\d+)<\/a>").findall(content)
		for url,name in items:
			addDir('[COLOR red]Download mới nhất - Trang '+name+'[/COLOR]',csn+'hd/video/'+url+'.html','episodes',icon['next'])			
						
def ServerList(name, url, mode, query):	
	search_string = fixSearch(query)
		
	name='['+danhmucphim+'] '+name
	if danhmucphim == 'HDOnline' and hdonline_view == 'true':
		if mode == '12' : mode='hdonlineplay';v_query='';isFolder=False
		else : mode='episodes';v_query='';isFolder=True;url='http://m.hdonline.vn'+url		
	elif danhmucphim == 'HDViet' and hdviet_view == 'true':
		if mode == '12' : mode='22';v_query='hdvietplay';isFolder=False
		else : mode='episodes';v_query=url;isFolder=True;url=hdviet_com
	elif danhmucphim == 'HayHayTV' and hayhaytv_view == 'true':
		if mode == '12' : mode='23';v_query='play';isFolder=False
		else : mode='episodes';v_query='';isFolder=True
	elif danhmucphim == 'DangCapHD' and dangcaphd_view == 'true':
		if mode == '12' : mode='18';v_query='DCP';isFolder=False
		else : mode='18';v_query='DC3';isFolder=True
	elif danhmucphim == 'PhimMoi' and phimmoi_view == 'true':
		if mode == '12' : mode='24';v_query='pmplay';isFolder=False
		else : mode='24';v_query='episodes';isFolder=True	
	xshare.addir(name,url,img,'fanart',mode=mode,page=1,query=v_query,isFolder=isFolder)
						
	if danhmucphim <> 'HDOnline' and hdonline_view == 'true':
		url = 'http://hdonline.vn/tim-kiem/'+search_string+'.html'      					
		Search_Result(url, query)			
	if danhmucphim <> 'VuaHD' and vuahd_view == 'true':
		url='http://vuahd.tv/movies/q/%s'%search_string
		Search_Result(url, query)
	if danhmucphim <> 'HDViet' and hdviet_view == 'true':
		url='http://movies.hdviet.com/tim-kiem.html?keyword=%s'%search_string
		Search_Result(url, query)
	if danhmucphim <> 'HayHayTV' and hayhaytv_view == 'true':
		url=hayhaytv_vn+'tim-kiem/%s/trang-1'%search_string
		Search_Result(url, query)
	if danhmucphim <> 'DangCapHD' and dangcaphd_view == 'true':
		url='http://dangcaphd.com/movie/search.html?key=%s&search_movie=1'%search_string
		Search_Result(url, query)	
	if danhmucphim <> 'Megabox' and megabox_view == 'true':
		url='http://phim.megabox.vn/search/index?keyword=' + search_string#+'/phim-le'
		Search_Result(url, query)	
	if danhmucphim <> 'PhimMoi' and phimmoi_view == 'true':
		url='http://www.phimmoi.net/tim-kiem/%s/'%search_string
		Search_Result(url, query)		
	if danhmucphim <> 'PhimGiaiTri' and phimgiaitri_view == 'true':
		url = phimgiaitri_vn+'result.php?type=search&keywords='+search_string      
		try:
			Search_Result(url, query)	
		except: pass
			
def Search(url): 	
	if '-' in url:query='-'
	else:query=''

	try:
		keyb=xbmc.Keyboard('', color['search']+'Nhập nội dung cần tìm kiếm[/COLOR]')
		keyb.doModal()
		if (keyb.isConfirmed()):
			searchText=urllib.quote_plus(keyb.getText())
		if 'TimVideoCSN' in url:  
			url=csn+'search.php?s='+searchText+'&cat=video'      
		elif 'TimVideoNCT' in url:
			url = nct + 'tim-kiem/mv?q=' + searchText     
		elif 'HDOnline' in url:
			url = 'http://hdonline.vn/tim-kiem/'+searchText.replace('+', '-')+'.html'      			
		elif 'VuaHD' in url:		
			url = 'http://vuahd.tv/movies/q/'+searchText.replace('+', '-')
		elif 'HDViet' in url:
			url = hdviet_com+'tim-kiem.html?keyword=%s'%searchText.replace('+', '-')
		elif 'HayHayTV' in url:
			url = hayhaytv_vn+'tim-kiem/%s/trang-1'%searchText.replace('+', '-')
		elif 'DangCapHD' in url:
			url = 'http://dangcaphd.com/movie/search.html?key=%s&search_movie=1'%searchText.replace('+', '-')
		elif 'MegaBox' in url:
			url = 'http://phim.megabox.vn/search/index?keyword='+searchText.replace('+', '-')
		elif 'PhimMoi' in url:
			url = 'http://www.phimmoi.net/tim-kiem/%s/'%searchText.replace('+', '-')     
		elif 'PhimGiaiTri' in url:  
			url = phimgiaitri_vn+'result.php?type=search&keywords='+searchText
   
		Search_Result(url, query)
	except:pass	

def Search_Result(url, query='', mode=''):
	search_string = fixSearch(query)
	if search_string=='-':search_string=''	
	if 'hdonline.vn' in url:
		content = hdonline.GetContent(url)
		content = ''.join(content.splitlines()).replace('\'','"')
		try:
			content =content.encode("UTF-8")
		except: pass
		#movielist=re.compile('<li>\s*<div class="tn-bxitem">(.+?)<div class="clearfix">').findall(content)
		movielist=re.compile('<li>\s*<div class="tn-bxitem">(.+?)</li>').findall(content)
		for idx in range(len(movielist)):
			vcontent = movielist[idx]				
			items=re.compile('<a href="(.+?)"(.+?)<img src="(.+?)".+?<p class="name-vi">(.+?)</p>\s*<p class="name-en">(.+?)</p>').findall(vcontent)										
			for url, episodes, img, nameen, namevn in items :
				name = namevn + ' - ' + nameen							
				if fixSearchss(search_string) in fixSearchss(name) or search_string == '' : # xu ly tim kiem cho nhieu ket qua																
					isFolder=True;v_query=nameen
					if 'episodes' in episodes :														
						v_mode='120'
						name = '[HDOnline] ' + name if query!='' else color['phimbo'] + name + '[/COLOR]'
					else :						
						v_mode='12'
						if query!='':name = '[HDOnline] ' + name
						
					if danhmucphim != 'Tất cả': pass
					else:
						if v_mode == '12' :
							v_mode='hdonlineplay';isFolder=False						
						else :
							v_mode='episodes';url = 'http://m.hdonline.vn' + url													
					xshare.addir(name,url,img,fanart='fanart',mode=v_mode,page=1,query=v_query,isFolder=isFolder)
			setViewMode('3')
		if query=='':
			pagecontent=re.compile('<ul class="pagination">(.+?)</ul>').findall(content)
			if(len(pagecontent)>0):
				pagelist=re.compile('<li><a [^>]*href=["\']?([^>^"^\']+)["\']?[^>]*>(.+?)</a></li>').findall(pagecontent[0])
				for vurl,vname in pagelist:
					if 'Trang' not in vname : vname = 'Trang ' + vname
					if mode!='category':vurl='http://hdonline.vn'+vurl
					addDir(vname,vurl,mode if mode=='category' else 'search_result',"")		
	elif 'hdviet' in url:
		#category
		#body=xshare.make_request(url)
		#body=xshare.sub_body(body,'class="homesection"','class="h2-ttl cf"')
		#xshare.additemshdviet(body, danhmucphim)

		body=xshare.make_request(url);body=body[body.find('box-movie-list'):body.find('h2-ttl cf')];		
		pattern='<a href="(.{,200})"><img src="(.+?)"(.+?)"h2-ttl3">(.+?)<span>(.+?)</span>(.*?)<a'
		links=re.findall(pattern,body)
		for link,img,temp,ttl3,title,cap in links:
			strNameEn, name = strVnEn(title, ttl3.replace('&nbsp;',''))
			if fixSearchss(search_string) in fixSearchss(name) or search_string == '' : # xu ly tim kiem cho nhieu ket qua																					
				isFolder=True;v_query=strNameEn
				caps=''
				if 'icon-SD' in cap:caps+='[COLOR gold]SD[/COLOR]'
				if 'icon-720' in cap:caps+='[COLOR gold]HD[/COLOR]720'
				if 'icon-1080' in cap:caps+='[COLOR gold]HD[/COLOR]1080'
				if 'icon-TM' in cap:caps+='[COLOR green]TM[/COLOR]'
				if '>18+<' in cap:caps+='[COLOR red]18+[/COLOR]'
				isFolder=xshare.xshare_group(re.search('"labelchap2">(\d{1,3})</span>',temp),1)
				link=xshare.xshare_group(re.search('id="tooltip(\d{,10})"',temp),1).strip()

				if not isFolder:
					v_mode='12'
					if query!='':name = '[HDViet] ' + name
				#elif isFolder=='1':hdviet(title,link,img,mode='22',page=1,query='folder',isFolder=True)
				else:
					v_mode='120'
					name = '[HDViet] ' + name if query!='' else color['phimbo'] + name + '[/COLOR]'

				if danhmucphim != 'Tất cả': pass
				else:
					if v_mode == '12' :
						v_mode='22';isFolder=False
						v_query='hdvietplay'
					else :
						v_mode='episodes';link = hdviet_com													
						v_query=link
				xshare.addir(name,link,img,fanart='fanart',mode=v_mode,page=1,query=v_query,isFolder=isFolder)					
		if query=='':					
			pages=re.findall('<li class=""><a href="(.+?)">(.+?)</a></li>',body[body.find('class="active"'):])
			if pages:
				pagenext=pages[0][1];pageend=pages[len(pages)-1][1]
				name='%sTrang tiếp theo: trang %s/%s[/COLOR]'%(color['trangtiep'],pagenext,pageend)
				addDir(name,pages[0][0],mode if mode=='category' else 'search_result',"")
				#xshare.addir(name,pages[0][0],img,fanart='fanart',mode='search_result',page=1,query='hdvietplay',isFolder=True)			
		setViewMode('3')
	elif 'hayhaytv' in url:					
		if '/shows' in url or mode=='search_result':
			body=xshare.make_request(url);#body=body[body.find('slide_child_div_dt'):];body=body[:body.find('class="paging"')]
			content=body[body.find('slide_child_div_dt'):];content=content[:content.find('class="paging"')]
			pattern='tooltip="(.+?)" href="(.+?)">\s.*"(http://img.+?)".*\s.*color">(.*?)<.*\s.*>(.*?)</span>'
			#pattern='href="(.+?)".*\s.*alt="poster phim (.+?)" src="(.+?)"'
			ids=dict((re.findall('id="(sticky\d{1,3})".{,250}Số tập[\D]{,30}(\d{1,4})',body,re.DOTALL)))		
			items=re.findall(pattern,content)		
		else:
			#body=xshare.make_request(url)		
			body=xshare.make_post(re.sub('page=\d{1,3}','page=%d'%page,url)).body
			pattern='tooltip="(.+?)" href="(.+?)">\s.*"(http://img.+?)".*\s.*color">(.*?)<.*\s.*>(.*?)</span>'
			items=re.findall(pattern,body)
			ids=dict((re.findall('id="(sticky\d{1,3})".{,250}Số tập[\D]{,30}(\d{1,4})',body,re.DOTALL)))
								
		for stic,href,img,name_e,name_v in items:		
			isFolder=True
			name=name_v+' - '+name_e if name_v else name_e			
			if fixSearchss(search_string) in fixSearchss(name) or search_string == '' : # xu ly tim kiem cho nhieu ket qua					
				v_query = name_e[:-7]
				if re.search('Tap-\d{1,3}',href):													
					v_mode='120'
					name = '[HayHayTV] ' + name if query!='' else color['phimbo'] + name + '[/COLOR]'
				else :						
					v_mode='12'
					if query!='':name = '[HayHayTV] ' + name							
					
				if danhmucphim != 'Tất cả' and 'xem-show' not in href: pass
				else:
					if v_mode == '12' :
						v_mode='23';isFolder=False
						v_query = 'play'						
					else :
						v_mode='episodes';isFolder=True				
				xshare.addir(name,href,img,fanart='fanart',mode=v_mode,page=1,query=v_query,isFolder=isFolder)								
		if '/shows' in url or mode=='search_result':
			if query=='':
				if len(items)>14 or (len(items)>7 and 'su-kien' in url):
					temp='trang-' if 'trang-' in url else 'page=';url=re.sub('%s\d{1,3}'%temp,'%s%d'%(temp,page+1),url)
					name='%sTrang tiếp theo: trang %s[/COLOR]'%(color['trangtiep'],page+1)
					addDir(name,url,'search_result&page=%d'%(page+1),"")		
		else:
			body=body[body.find('javascript:slideTogglePage1()'):body.find('data-tooltip="sticky')]						
			items=re.findall('<a href=\'(.+?)\' onclick=.*?>(.+?)</a>',body)
			for href, name in items:				
				name = color['trangtiep'] + 'Trang ' + name + '[/COLOR]'
				addDir(name,href,'category',"")		
				
		setViewMode('3')
	elif 'vuahd' in url:
		body=xshare.make_request(url)
		items=re.findall('img src="(.+?)".{,500}<a href="(.+?)" title="(.+?)"',body,re.DOTALL)
		home='http://vuahd.tv'
		for img,href,name in items:			
			names=re.findall('<h2>(.+?)<br />\s*(.+?)\s*</h2>',xshare.make_request(home+href),re.DOTALL)
			for nameen, namevn in names:
				name = namevn.replace('( ', '').replace(')', '') + ' - ' + nameen.strip()				

			if fixSearchss(search_string) in fixSearchss(name) or search_string == '' : # xu ly tim kiem cho nhieu ket qua			
				isFolder=True
				if 'tv-series' in href:	#Phim bộ
					if query=='':
						name = color['phimbo'] + name + '[/COLOR]'
						v_mode='episodes'	
					elif query=='-':
						name = color['phimbo'] + name + '[/COLOR]'
						v_mode='120'
					else:
						name = '[VuaHD] ' + name
						v_mode='120'
					v_mode='episodes'
					href = home+href
				elif 'actors' not in href:
					isFolder=False
					href = vuahdtv + 'http%3A%2F%2Fvuahd.tv' + href.replace('/', '%2F')					
					if query=='':
						name = '[Phim lẻ] ' + name
						v_mode='16'						
					elif query=='-':
						name = '[Phim lẻ] ' + name
						v_mode='12'
					else:
						name = '[VuaHD] ' + name
						v_mode='12'
					v_mode='16'	
				xshare.addir(fixString(name),href,img,fanart='fanart',mode=v_mode,page=1,query=nameen.strip(),isFolder=isFolder)
		if query=='':pass			
			#if items and len(items)>25:
				#name=color['trangtiep']+'Trang tiếp theo: trang %s[/COLOR]'%str(page+1)
				#xshare.addir(name,url,icon['vuahd'],fanart,v_mode,page=page+1,query='trangtiep',isFolder=True)		
	elif 'dangcaphd' in url:			
		body=re.sub('\t|\n|\r|\f|\v','',xshare.make_request(url))
		items=re.findall('<a class="product.+?" href="(.+?)" title="(.+?)">.+?<img src="(.+?)" (.+?)</li>',body)		
		for href,name,img,other in items:			
			if ' - ' in name:
				arrName = name.split(' - ')
				str1=str2=strYear=''
				str1 = arrName[0]#.strip()
				if len(arrName) > 1: str2 = arrName[1]#.strip()		
				strNameEn, name = strVnEn(str2, str1)
				if len(arrName) > 2:
					strYear = arrName[2]#.strip()
					name = name + ' (' + strYear + ')'
			if fixSearchss(search_string) in fixSearchss(name) or search_string == '' : # xu ly tim kiem cho nhieu ket qua			
				isFolder=True;v_query=strNameEn
				if re.search('<div class="sale">.+?</div>',other):
					name=name+' - ('+xshare.xshare_group(re.search('<div class="sale">(.+?)</div>',other),1)+')'
					if query!='' and query!='-':name = '[DangCapHD] ' + name
					else:name = color['phimbo'] + name + '[/COLOR]'
					if query=='' or (query!='' and danhmucphim <> 'DangCapHD'):
						#v_mode='episodes'#episodes
						v_mode='18'
						v_query = 'DC3'
					else:v_mode='120'#list_server
				else:
					if query!='' and query!='-':name = '[DangCapHD] ' + name
					if query=='' or (query!='' and danhmucphim <> 'DangCapHD'):
						v_mode='18';isFolder=False
						v_query = 'DCP'
					else:v_mode='12'#list_server
				xshare.addir(name,href,img,fanart='fanart',mode=v_mode,page=1,query=v_query,isFolder=isFolder)
		if query=='':
			pattern='<a class="current">\d{1,5}</a><a href="(.+?)">(\d{1,5})</a>.*<a href=".+?page=(\d{1,5})">.+?</a></div>'
			page_control=re.search(pattern,body)
			if page_control:
				href=re.sub('&amp;','&',page_control.group(1));pagenext=page_control.group(2)
				pages=int(page_control.group(3))/rows+1
				name=color['trangtiep']+'Trang tiếp theo: trang %s/%d[/COLOR]'%(pagenext,pages)
				xshare.addir(name,href,mode if mode=='category' else 'search_result',isFolder=True)
		setViewMode('3')
	elif 'megabox.vn' in url:
		content = Get_Url(url)	
		items = re.compile('src="(.+?)">\s*<span class="features">\s*</span>\s*</a>\s*<div class="meta">\s*<h3 class="H3title">\s*<a href="(.+?)">(.+?)</a></h3>\s*<div class="explain">(.+?)</div>').findall(content)
		for img, href, titleVn, titleEn in items:
			name = titleVn + ' - ' + titleEn	
			if fixSearchss(search_string) in fixSearchss(name) or search_string == '' : # xu ly tim kiem cho nhieu ket qua			
				if query=='':
					#name = '[Phim lẻ] ' + name
					v_mode='16'						
					isFolder=False
				elif query=='-':
					#name = '[Phim lẻ] ' + name
					v_mode='12'
				else:
					name = '[MegaBox] ' + name
					v_mode='12'				
			
				href = megaboxvn + href.replace('/', '%2F').replace(':', '%3A')			
				xshare.addir(name,href,img,'fanart',mode='16',page=1,query='play',isFolder=False)
		items = re.compile('src="(.+?)">\s*<span class=\'esp\'>.+?<span class="features">\s*</span>\s*</a>\s*<div class="meta">\s*<h3 class="H3title">\s*<a href="(.+?)">(.+?)</a></h3>\s*<div class="explain">(.+?)</div>').findall(content)
		for img, href, titleVn, titleEn in items:
			name = titleVn + ' - ' + titleEn
			if fixSearchss(search_string) in fixSearchss(name) or search_string == '' : # xu ly tim kiem cho nhieu ket qua
				if query=='':
					name = color['phimbo'] + name + '[/COLOR]'
					v_mode='episodes'	
				elif query=='-':
					name = color['phimbo'] + name + '[/COLOR]'
					v_mode='120'
				else:
					name = '[MegaBox] ' + name
					v_mode='120'											
				xshare.addir(name,href,img,'fanart',mode='episodes',page=1,query='eps',isFolder=True)
				
		#items = re.compile('class="next"><a href="(.+?)">').findall(content)
		#addDir('[COLOR red]Trang Tiếp Theo[/COLOR]', megabox_vn + items[0],'episodes',icon['next'])	
			
	elif 'phimmoi' in url:
		body=xshare.make_request(url);menu1='Add to Tủ phim'
		for content in re.findall('<li class="movie-item">(.+?)</li>',body,re.DOTALL):		
			title=xshare.xsearch('title="(.+?)"',content,1);href=xshare.xsearch('href="(.+?)"',content,1)
			arr = title.split(' - ')
			titleEn=arr[1] if len(arr)>1 else ''			
						
			img=xshare.xsearch('\((http.+?)\)',content,1);detail=' '.join(re.findall('<span(.+?)</span>',content))
			title,href,img,v_query,isFolder=xshare.get_info(title,href,img,detail)
			menu=[(menu1,{'name':menu1,'url':href,'query':'tuphim'})]

			if fixSearchss(search_string) in fixSearchss(title) or search_string == '' : # xu ly tim kiem cho nhieu ket qua			
				isFolder=True
				if v_query == 'pmfolder' :														
					if query!='':v_mode='120'
					if query!='' and query!='-':title = '[PhimMoi] ' + title
					else:title = color['phimbo'] + title + '[/COLOR]'
					if query=='' or (query!='' and danhmucphim <> 'PhimMoi'):
						v_mode='episodes'
				else :						
					if query!='':v_mode='12'
					if query!='' and query!='-':title = '[PhimMoi] ' + title
					if query=='' or (query!='' and danhmucphim <> 'PhimMoi'):
						v_mode='24';isFolder=False
				xshare.pm_addir2(title,href,img,fanart='',mode=v_mode,page=1,query=titleEn,isFolder=isFolder)#,menu=menu)
		if query=='':
			urlnext=xshare.xshare_group(re.search('<li><a href="(.+?)">Trang kế.+?</a></li>',body),1)
			if urlnext:
				pagenext=xshare.xshare_group(re.search('/page-(\d{1,3})\.html',urlnext),1)
				name='%sTrang tiếp theo: trang %s[/COLOR]'%(color['trangtiep'],pagenext)
				xshare.addir(name,phimmoi_net+urlnext,img,fanart='',mode=mode if mode=='category' else 'search_result',page=1,query='readpage',isFolder=True)
	elif 'phimgiaitri' in url:
		content = xshare.make_request(url)			
		#try:
		#items = re.compile('<a style=\'text-decoration:none\' href=\'([^\']*).html\'>\s*<img style=.+?src=(.+?) ><table style.+?:0px\'>(.+?)\s*<\/font>').findall(content)
		items = re.compile('<a style=\'text-decoration:none\' href=\'([^\']*).html\'>\s*<img style=.+?src=(.+?) ><table style.+?:0px\'>(.+?)\s*</font>.+?\'> (.+?)</font>').findall(content)
		for href,img,namevn,nameen in items:		
			strNameEn, name =  strVnEn(namevn, nameen)
			if fixSearchss(search_string) in fixSearchss(name) or search_string == '' : # xu ly tim kiem cho nhieu ket qua			
				if query=='':
					v_mode='16'						
					isFolder=False
				elif query=='-':
					v_mode='12'
				else:
					name = '[PhimGiaiTri] ' + name
					v_mode='12'			
			href = phimgiaitri_vn+href+'/Tap-1.html'
			add_Link(name,href,phimgiaitri_vn+img)
			#xshare.addir(href,href,phimgiaitri_vn+img,'fanart',mode='stream',page=1,query='play',isFolder=False)
			
			#href = phimgiaitri_vn  + 'http:%2F%2Fphimgiaitri.vn%2F' + href.replace('/', '%2F')
			#xshare.addir(href,href,phimgiaitri_vn+img,'fanart',mode='16',page=1,query='play',isFolder=False)

		items = re.compile('<a style=\'text-decoration:none\' href=\'([^\']*).html\'>\s*<img style=.+?src=(.+?) ><div class=\'text\'>\s*(.+?)\s*</div><table style.+?:0px\'>(.+?)\s*</font>.+?\'> (.+?)</font>').findall(content)
		for href,img,eps,namevn,nameen in items:		
			name =  namevn + ' - ' + nameen
			if fixSearchss(search_string) in fixSearchss(name) or search_string == '' : # xu ly tim kiem cho nhieu ket qua					
				if '01/01' in eps : #truong hop phim le o trang chu co hien thi (Tập 01/01)
					if query=='':
						v_mode='16'						
						isFolder=False
					elif query=='-':
						v_mode='12'
					else:
						name = '[PhimGiaiTri] ' + name
						v_mode='12'		
					href = phimgiaitri_vn+href+'/Tap-1.html'
					add_Link(name,href,phimgiaitri_vn+img)					
					#xshare.addir(name,url,phimgiaitri_vn+img,'fanart',v_mode='play',page=1,isFolder=False)	
				else : 
					if query=='':
						name = color['phimbo'] + name + '[/COLOR]'
						v_mode='episodes'	
					elif query=='-':
						name = color['phimbo'] + name + '[/COLOR]'
						v_mode='120'
					else:
						name = '[PhimGiaiTri] ' + name
						v_mode='120'	
					href = phimgiaitri_vn+href+'/Tap-1.html'
					xshare.addir(name,href,phimgiaitri_vn+img,'fanart',mode='episodes',page=1,isFolder=True)	
								
		#items = re.compile("<a  href='(.+?)'>(\d+)  <\/a>").findall(content) 		
		#for url,name in items:
		  #addDir('[COLOR lime]Trang tiếp theo '+name+'[/COLOR]',phimgiaitri_vn+href.replace(' ','%20'),'search_result',icon['next'])
		#except:pass
										
	elif 'chiasenhac' in url:
		content = Get_Url(url)
		items=re.compile("<a href=\"([^\"]*)\" title=\"(.*?)\"><img src=\"([^\"]+)\"").findall(content)
		#items=re.compile("<a href=\"([^\"]*)\" title=\"(.*?)\"><img src=\"([^\"]+)\"\s.+\s.+\s.+\s.+\s.+\s.+\s.+\s.+\s.+\s.+\s.+\s.+\s.+\s.+\s.+\s.+\s.+\s.+\s.+\s*<span class=\"gen\">.*?<br /><span style=\"color: .*?\">(.*?)</span>").findall(content)
		cat = '...'
		if 'page=' not in url:url=url+"&page=1"
		for href,name,thumbnail in items:
			name=name.replace(';',' +')
			add_Link(name+color['cat']+' ['+cat+'][/COLOR]',csn+href,thumbnail)
		items=re.compile("href=\"(.+?)\" class=\"npage\">(\d+)<").findall(content)
		for href,name in items:
			if 'page='+name not in url:
				addDir(color['trangtiep']+'Trang '+name+'[/COLOR]',href.replace('&amp;','&'),'search_result',icon['next'])
	elif 'nhaccuatui' in url:
		content = Get_Url(url)
		match = re.compile("href=\"http:\/\/m.nhaccuatui.com\/video\/([^\"]*)\" title=\"([^\"]+)\"><img alt=\".+?\" src=\"(.*?)\"").findall(content)		
		for url, name, thumb in match:			
			add_Link(name,nct + 'video/' + url,thumb)
		match = re.compile("href=\"([^\"]*)\" class=\"next\" titlle=\"([^\"]+)\"").findall(content)
		for url, name in match:	
			addDir(color['trangtiep']+name+'[/COLOR]',url,mode if mode=='episodes' else 'search_result',icon['next'])					

def Get_M3U(url,iconimage):
	m3ucontent = Get_Url(url)
	items = re.compile('#EXTINF:-?\d,(.+?)\n(.+)').findall(m3ucontent)
	for name,url in items:	
		#if 'youtube' in url:
			#addLink('' + name + '', url, 'play', iconimage)
		#else:
		add_Link(name.replace('TVSHOW - ','').replace('MUSIC - ',''),url,iconimage)

def Get_XML(url,iconimage):
	xmlcontent = GetUrl(url)
	match=re.compile("<title>([^<]*)<\/title>\s*<link>([^<]+)<\/link>\s*<thumbnail>(.+?)</thumbnail>").findall(xmlcontent)
	for title,url,thumbnail in match:
		add_Link(title, url, thumbnail)
		#addLink('' + title + '', url, 'play', thumbnail)
		
def Index(url,iconimage):
    byname = url.split("?n=")[1]
    url = url.split("?")[0]
    xmlcontent = GetUrl(url)
    channels = re.compile('<channel>(.+?)</channel>').findall(xmlcontent)
    for channel in channels:
        if byname in channel:
            items = re.compile('<item>(.+?)</item>').findall(channel)
            for item in items:
                thumb=""
                title=""
                link=""
                if "/title" in item:
                    title = re.compile('<title>(.+?)</title>').findall(item)[0]
                if "/link" in item:
                    link = re.compile('<link>(.+?)</link>').findall(item)[0]
                if "/thumbnail" in item:
                    thumb = re.compile('<thumbnail>(.+?)</thumbnail>').findall(item)[0]
                if "youtube" in link:					                    
					if 'MenuTube' in url:
						addDir(title, link, 'episodes', thumb)
					else:
						add_Link(title, link, thumb)
                else:					
                    addLink('' + title + '', link, 'play', thumb)
    skin_used = xbmc.getSkinDir()
    if skin_used == 'skin.xeebo':
        xbmc.executebuiltin('Container.SetViewMode(50)')
		
def IndexGroup(url):
    xmlcontent = GetUrl(url)
    names = re.compile('<name>(.+?)</name>').findall(xmlcontent)
    if len(names) == 1:
        items = re.compile('<item>(.+?)</item>').findall(xmlcontent)
        for item in items:
            thumb=""
            title=""
            link=""
            if "/title" in item:
                title = re.compile('<title>(.+?)</title>').findall(item)[0]
            if "/link" in item:
                link = re.compile('<link>(.+?)</link>').findall(item)[0]
            if "/thumbnail" in item:
                thumb = re.compile('<thumbnail>(.+?)</thumbnail>').findall(item)[0]
            add_Link(title, link, thumb)
        skin_used = xbmc.getSkinDir()
        if skin_used == 'skin.xeebo':
            xbmc.executebuiltin('Container.SetViewMode(52)')
        else:
            xbmc.executebuiltin('Container.SetViewMode(%d)' % 500)			
    else:
        for name in names:
            addDir('' + name + '', url+"?n="+name, 'index', '')

def Index_Group(url):
	xmlcontent = GetUrl(url)
	names = re.compile('<name>(.+?)</name>\s*<thumbnail>(.+?)</thumbnail>').findall(xmlcontent)
	if len(names) == 1:
		items = re.compile('<item>(.+?)</item>').findall(xmlcontent)
		for item in items:
			thumb=""
			title=""
			link=""
			if "/title" in item:
				title = re.compile('<title>(.+?)</title>').findall(item)[0]
			if "/link" in item:
				link = re.compile('<link>(.+?)</link>').findall(item)[0]
			if "/thumbnail" in item:
				thumb = re.compile('<thumbnail>(.+?)</thumbnail>').findall(item)[0]
			addLink(title, link, 'play', thumb)
		skin_used = xbmc.getSkinDir()
		if skin_used == 'skin.xeebo':
				xbmc.executebuiltin('Container.SetViewMode(50)')
	else:
		for name,thumb in names:
			addDir(name, url+"?n="+name, 'index', thumb)

def menulist(homepath):
	try:
		mainmenu=open(homepath, 'r')  
		link=mainmenu.read()
		mainmenu.close()
		match=re.compile("<title>([^<]*)<\/title>\s*<link>([^<]+)<\/link>\s*<thumbnail>(.+?)</thumbnail>").findall(link)
		return match
	except:
		pass
	
def resolve_url(url):
	if 'xemphimso' in url:
		content = Get_Url(url)	
		url = urllib.unquote_plus(re.compile("file=(.+?)&").findall(content)[0])
	elif 'vtvplay' in url:
		content = Get_Url(url)
		url = content.replace("\"", "")
		url = url[:-5]
	elif 'vtvplus' in url:
		content = Get_Url(url)
		url = re.compile('var responseText = "(.+?)";').findall(content)[0]		
	elif 'htvonline' in url:
		content = Get_Url(url)	
		url = re.compile('data\-source=\"([^\"]*)\"').findall(content)[0]
	elif 'hplus' in url:
		content = Get_Url(url)	
		url = re.compile('iosUrl = "(.+?)";').findall(content)[0]
	elif 'megabox' in url:
		content = Get_Url(url)	
		url = re.compile('var iosUrl = "(.+?)"').findall(content)[0]+'|User-Agent=Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36 VietMedia/1.0'		
	elif 'chiasenhac' in url:
		content = Get_Url(url)
		try:
		  url = re.compile("\"hd-2\".+?\"([^\"]+)\"").findall(content)[0].replace('%3A',':').replace('%2F','/').replace('%2520','%20')
		except:
		  url = re.compile("\"file\".*?\"([^\"]*)\"").findall(content)[-1].replace('%3A', ':').replace('%2F', '/').replace('%2520', '%20')		
		  #url = re.compile("\"hd-2\".+?\"([^\"]+)\"").findall(content)[-1].replace('%3A',':').replace('%2F','/').replace('%2520','%20')
	elif 'nhaccuatui' in url:
		content = Get_Url(url)
		url = re.compile("title=\".+?\" href=\"([^\"]*)\"").findall(content)[0] 
		
	elif 'f.vp9.tv' in url:
		content = Get_Url(url)
		try:
		  try:
		    url = url+re.compile('<a href="(.*?)HV.mp4"').findall(content)[0]+'HV.mp4'
		  except:
		    url = url+re.compile('<a href="(.*?)mvhd.mp4"').findall(content)[0]+'mvhd.mp4'
		except:
		  url = url+re.compile('<a href="(.*?)mv.mp4"').findall(content)[0]+'mv.mp4'
	elif 'ott.thuynga' in url:
		content = Get_Url(url)	
		url=re.compile("var iosUrl = '(.+?)'").findall(content)[0]
	elif 'phim7' in url:
		content = Get_Url(url)
		try:
		  url = 'https://redirector' + re.compile('file: "https://redirector(.+?)", label:".+?", type: "video/mp4"').findall(content)[-1]
		except:
		  url = 'plugin://plugin.video.youtube/play/?video_id=' + re.compile('file : "http://www.youtube.com/watch\?v=(.+?)&amp').findall(content)[0]		
	elif 'phimgiaitri' in url:
		xbmc.log(url)	
		arr = url.split('/')
		phimid = arr[len(arr) - 3]
		tap = arr[len(arr) - 1]
		tap2 = tap.split('-')
		tap3 = tap2[1].split('.')
		tap = tap3[0]
		url2 = 'http://120.72.85.195/phimgiaitri/mobile/service/getep3.php?phimid=' + phimid
		content = Get_Url(url2)
		content = content[3:]
		infoJson = json.loads(content)
		tapindex = int(tap) -1
		link = infoJson['ep_info'][tapindex]['link']
		link = link.replace('#','*')
		url3 ='http://120.72.85.195/phimgiaitri/mobile/service/getdireclink.php?linkpicasa=' + link
		content = Get_Url(url3)
		content = content[3:]
		linkJson = json.loads(content)
		url = linkJson['linkpi'][0]['link720'] or linkJson['linkpi'][0]['link360']		
	else:
		url = url
	item=xbmcgui.ListItem(path=url)
	xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)	  
	return

def PlayVideo(url,title):
    if(url.find("youtube") > 0):
        vidmatch=re.compile('(youtu\.be\/|youtube-nocookie\.com\/|youtube\.com\/(watch\?(.*&)?v=|(embed|v|user)\/))([^\?&"\'>]+)').findall(url)
        vidlink=vidmatch[0][len(vidmatch[0])-1].replace('v/','')
        url = 'plugin://plugin.video.youtube?path=/root/video&action=play_video&videoid=' + vidlink.replace('?','')
        xbmc.executebuiltin("xbmc.PlayMedia("+url+")")	
    else:
        title = urllib.unquote_plus(title)
        playlist = xbmc.PlayList(1)
        playlist.clear()
        listitem = xbmcgui.ListItem(title)
        listitem.setInfo('video', {'Title': title})
        xbmcPlayer = xbmc.Player()
        playlist.add(url, listitem)
        xbmcPlayer.play(playlist)
	
def Get_Url(url):
    try:
		req=urllib2.Request(url)
		req.add_header('User-Agent', 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; WOW64; Trident/6.0)')
		response=urllib2.urlopen(req)
		link=response.read()
		response.close()  
		return link
    except:
		pass
    
def GetUrl(url):
    link = ""
    if os.path.exists(url)==True:
        link = open(url).read()
    else:
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; WOW64; Trident/6.0)')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
    link = ''.join(link.splitlines()).replace('\'','"')
    link = link.replace('\n','')
    link = link.replace('\t','')
    link = re.sub('  +',' ',link)
    link = link.replace('> <','><')
    return link
	
def add_Link(name,url,iconimage):
    u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode=stream"+"&img="+urllib.quote_plus(iconimage)
    liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
    liz.setInfo( type="Video", infoLabels={ "Title": name } )
    liz.setProperty('IsPlayable', 'true')  
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz)  

def addLink(name,url,mode,iconimage):
    u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
    ok=True
    liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
    liz.setInfo( type="Video", infoLabels={ "Title": name } )
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz)
    return ok
	
def addDir(name,url,mode,iconimage):
    u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&img="+urllib.quote_plus(iconimage)
    ok=True
    liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
    liz.setInfo( type="Video", infoLabels={ "Title": name } )
    if ('www.youtube.com/user/' in url) or ('www.youtube.com/channel/' in url):
		u = 'plugin://plugin.video.youtube/%s/%s/' % (url.split( '/' )[-2], url.split( '/' )[-1])
		ok = xbmcplugin.addDirectoryItem(handle = int(sys.argv[1]), url = u, listitem = liz, isFolder = True)
		return ok	
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
    return ok	
	
DecryptData = base64.b64decode	
homeurl = 'aHR0cDovL3d3dy5oaWV1aGllbi52bi9YQk1DL0hpZXVoaWVuTWVkaWEvTWVudS54bWw='
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
### ------------
xbmcplugin.setContent(int(sys.argv[1]), 'movies');params=get_params();mode=0;page=1;temp=[]
homnay=datetime.date.today().strftime("%d/%m/%Y");url=name=fanart=img=date=query=end=''

try:url=urllib.unquote_plus(params["url"])
except:pass
try:name=urllib.unquote_plus(params["name"])
except:pass
try:img=urllib.unquote_plus(params["img"])
except:pass
try:fanart=urllib.unquote_plus(params["fanart"])
except:pass
try:mode=str(params["mode"])
except:pass
try:page=int(params["page"])
except:pass
try:query=urllib.unquote_plus(params["query"])
except:pass#urllib.unquote

### ------------
print "Main---------- Mode: "+str(mode),"URL: "+str(url),"Name: "+str(name),"query: "+str(query),"page: "+str(page)
if not mode:Home();xshare.init_file(),setViewMode('3')
elif mode == 'index':Index(url,img)
elif mode == 'indexgroup':IndexGroup(url)	
elif mode == 'index_group':Index_Group(url)	
elif mode == 'menu_group':Menu_Group(url)
elif mode == 'category':category(url, mode),setViewMode('3')
elif mode == 'episodes':episodes(url, name)
elif mode == 'get_m3u':Get_M3U(url,img)
elif mode == 'get_xml':Get_XML(url,img)
elif mode == 'search_result':Search_Result(url)
elif mode == 'search':Search(url)	
elif mode=='stream':
    dialogWait = xbmcgui.DialogProgress()
    dialogWait.create('Hieuhien.vn Media Center', 'Đang tải. Vui lòng chờ trong giây lát...')
    resolve_url(url)
    dialogWait.close()
    del dialogWait	
elif mode=='play':
    dialogWait = xbmcgui.DialogProgress()
    dialogWait.create('Hieuhien.vn Media Center', 'Đang tải. Vui lòng chờ trong giây lát...')
    PlayVideo(url,name)
    dialogWait.close()
    del dialogWait

elif mode=='logouthdviet':hdviet.logout()
elif mode=='logouthayhaytv':hayhaytv.logout()
elif mode=='12' or mode=='120':#serverlist	
	ServerList(name, url, mode, query)
	
elif mode=='hdonlineplay':
	fid = xshare.xshare_group(re.search('-(\d{1,5}).html',url),1)
	url = 'http://hdonline.vn/frontend/episode/loadxmlconfigorder?ep=1&fid='+str(fid)
	content = hdonline.GetContent(url)
	
	vurl=re.compile('<jwplayer:file>(.+?)</jwplayer:file>').findall(content)[0]
	if(vurl.find("http") == -1):
		vurl=hdonline.decodevplug(vurl)		
		#vurl='https://drive.google.com/file/d/0BxgS9RbZFNQkb1FuTXByN1NFTzQ/view'
	vsubtitle=re.compile('<jwplayer:vplugin.subfile>(.+?)</jwplayer:vplugin.subfile>').findall(content)
	suburl=""
	if(len(vsubtitle)>0 and vsubtitle[0].find("http")>-1):
		suburl=vsubtitle[0]
	elif(len(vsubtitle)>0):
		suburl=decodevplug(vsubtitle[0])
	for item in suburl.split(','):
		if 'VIE' in item:suburl=item				

	link=vurl
	subtitle=suburl
	
	listitem = xbmcgui.ListItem(path=link)
	xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, listitem)
	if len(subtitle) > 0:
	  subtitlePath = xbmc.translatePath(xbmcaddon.Addon().getAddonInfo('path')).decode("utf-8")
	  subfile = xbmc.translatePath(os.path.join(subtitlePath, "temp.sub"))
	  try:
		if os.path.exists(subfile):
		  os.remove(subfile)
		f = urllib2.urlopen(subtitle)
		with open(subfile, "wb") as code:
		  code.write(f.read())
		xbmc.sleep(3000)
		xbmc.Player().setSubtitles(subfile)
	  except:
		notification(u'Không tải được phụ đề phim.');
	  #urllib.urlretrieve (subtitle,subfile )
	elif 'TM' not in vurl:
	  notification('Video này không có phụ đề rời.');
elif mode=='16':
	_version = '1.0.11'
	_user = 'vietmedia'
	def fetch_data(url, headers=None):
	  #visitor = get_visitor()
	  #visitor = '175f2580-3a59-11e5-a8f2-701a0439657d'
	  if headers is None:
		headers = { 'User-agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36 VietMedia/1.0',
					'Referers':'http://www..google.com',
					#'X-Visitor':visitor,
					'X-Version':_version,
					'X-User':_user
				  }
	  try:
		req = urllib2.Request(url,headers=headers)
		f = urllib2.urlopen(req)
		body=f.read()
		return body
	  except:
		pass			

	if 'hdonline.vn' in query:
		url = hdonlinevn + 'http:%2F%2Fhdonline.vn' + url.replace('/', '%2F').replace('?', '%3f').replace('=', '%3D')
	elif 'phimmoi.net' in query:
		url = phimmoinet + 'http:%2F%2Fphimmoi.net%2F' + url.replace('/', '%2F')		

	content = fetch_data(url)	
	jsonObject = json.loads(content)

	if jsonObject.get('url'):		
		link = jsonObject['url']		
		if 'phimhd3s.com' in link or 'vn-hd.com' in link:
		  client_id = hdonline.client_id_2()
		  if client_id is not None:
			link = link.replace('dc469e7a3c7f76e5bfcc0e104526fb85',client_id)		

		subtitle = ''
		if jsonObject.get('subtitle'):
		  subtitle = jsonObject['subtitle']

		listitem = xbmcgui.ListItem(path=link)
		xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, listitem)
		if len(subtitle) > 0:
		  subtitlePath = xbmc.translatePath(xbmcaddon.Addon().getAddonInfo('path')).decode("utf-8")
		  subfile = xbmc.translatePath(os.path.join(subtitlePath, "temp.sub"))
		  try:
			if os.path.exists(subfile):
			  os.remove(subfile)
			f = urllib2.urlopen(subtitle)
			with open(subfile, "wb") as code:
			  code.write(f.read())
			xbmc.sleep(3000)
			xbmc.Player().setSubtitles(subfile)
		  except:
			notification(u'Không tải được phụ đề phim.');
		  #urllib.urlretrieve (subtitle,subfile )
		elif jsonObject.get('subtitle'):
		  notification('Video này không có phụ đề rời.');
	elif jsonObject.get('error') is not None:	
		alert(jsonObject['error'])

elif mode=='17':end=xshare.megabox(name,url,mode,page,query)
elif mode=='18':xshare.dangcaphd(name,url,img,mode,page,query)
elif mode==19:xshare.pubvn(name,url,img,mode,page,query)
elif mode=='21':xshare.vuahd(name,url,img,mode,page,query)
elif mode=='22':	
	hdviet.play(url, ep = 1)
	#xshare.hdviet(name,url,img,mode,page,query)
elif mode=='23':
	try:
		hd = {'User-Agent' : 'Mozilla/5.0 Chrome/39.0.2171.71 Firefox/33.0'}
		body=xshare.make_request(url,headers=hd,maxr=3)	
		movie_id=xshare.xshare_group(re.search('FILM_ID\D{3,7}(\d{3,6})',body),1)
		hayhaytv.play(movie_id, 1, subtitle='')
	except:
		xshare.hayhaytv(name,url,img,'fanart',mode,page,query)
elif mode=='24':xshare.phimmoi(name,url,img,mode,page,query)	

xbmcplugin.endOfDirectory(int(sys.argv[1]))