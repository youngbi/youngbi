# -*- coding: utf-8 -*-
import xbmc,xbmcplugin,xbmcgui,xbmcaddon,urllib,re,os,unicodedata,datetime,random,json

myaddon = xbmcaddon.Addon(); home = myaddon.getAddonInfo('path')
icon_path = xbmc.translatePath(os.path.join( home,'resources/media/'))
data_path = xbmc.translatePath(os.path.join( home,'resources/data/'))
datapath = xbmc.translatePath(os.path.join( xbmc.translatePath(myaddon.getAddonInfo('profile')),'data/'))
sys.path.append(xbmc.translatePath(os.path.join(home, 'resources', 'lib')));import urlfetch
thumucrieng = 'https://www.fshare.vn/folder/'+myaddon.getSetting('thumucrieng')
thumuccucbo =  myaddon.getSetting('thumuccucbo');copyxml = myaddon.getSetting('copyxml')
phim18 = myaddon.getSetting('phim18');search_file=datapath+"search.xml"
rows = int(myaddon.getSetting('sodonghienthi'))
googlesearch = myaddon.getSetting('googlesearch')

media_ext=['aif','iff','m3u','m4a','mid','mp3','mpa','ra','wav','wma','3g2','3gp','asf','asx','avi','flv','mov','mp4','mpg','mkv','m4v','rm','swf','vob','wmv','bin','cue','dmg','iso','mdf','toast','vcd','ts','flac']
hd = {'User-Agent' : 'Mozilla/5.0 Chrome/39.0.2171.71 Firefox/33.0'}
color={'fshare':'[COLOR gold]','vaphim':'[COLOR gold]','phimfshare':'[COLOR khaki]','4share':'[COLOR blue]','tenlua':'[COLOR fuchsia]','fptplay':'[COLOR orange]','trangtiep':'[COLOR lime]','search':'[COLOR lime]','ifile':'[COLOR blue]','hdvietnam':'[COLOR crimson]','xshare':'[COLOR blue]','subscene':'[COLOR green]','megabox':'[COLOR orangered]','dangcaphd':'[COLOR yellow]'}
icon={'icon':icon_path+'icon.png','fshare':icon_path+'fshare.png','vaphim':icon_path+'fshare.png','phimfshare':icon_path+'fshare.png','ifile':icon_path+'4share.png','4share':icon_path+'4share.png','tenlua':icon_path+'tenlua.png','hdvietnam':icon_path+'hdvietnam.png','khophim':icon_path+'khophim.png','xshare':icon_path+'icon.png','fptplay':icon_path+'fptplay.png','megabox':icon_path+'megabox.png','dangcaphd':icon_path+'dangcaphd.png'}

def mess(message, timeShown=5000):
	xbmc.executebuiltin((u'XBMC.Notification(%s,%s,%s,%s)'%('Xshare',message,timeShown,icon_path+'icon.png')).encode("utf-8"))





def mess_yesno(title='Xshare', mess='Are you ready ?'):
	dialog = xbmcgui.Dialog()#dialog.yesno(heading, line1[, line2, line3,nolabel,yeslabel])
	return dialog.yesno(title,mess)
	
def addir(name,link,img='',fanart='',mode=0,page=0,query='',isFolder=False):
	ok=True;name=re.sub(',|\|.*\||\||\<.*\>','',name)
	item = xbmcgui.ListItem(name,iconImage=img,thumbnailImage=img)
	query=menuContext(name,link,img,fanart,mode,query,item)
	item.setInfo(type="Video", infoLabels={"title":name})
	item.setProperty('Fanart_Image',fanart)
	u=sys.argv[0]+"?url="+urllib.quote_plus(link)+"&img="+urllib.quote_plus(img)+"&fanart="+urllib.quote_plus(fanart)+"&mode="+str(mode)+"&page="+str(page)+"&query="+query+"&name="+name
	if not isFolder:item.setProperty('IsPlayable', 'true')
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=item,isFolder=isFolder)
	return ok
	


def searchContext(name,link,mode,query):
	context1='[COLOR blue]Sửa mục này[/COLOR]'
	context2='[COLOR orangered]Xóa mục này[/COLOR]'
	p=(myaddon.getAddonInfo('id'),name,link,query)
	cmd1='RunPlugin(plugin://%s/?mode=9&name=%s&url=%s&query=%s&page=2)'%(p)
	cmd2='RunPlugin(plugin://%s/?mode=9&name=%s&url=%s&query=%s&page=1)'%(p)
	command=[(context1,cmd1)]
	command.append((context2,cmd2))
	return command


def fileContext(link,mode):
	context1='[COLOR orangered]Xóa file này[/COLOR]'
	cmd1='RunPlugin(plugin://%s/?mode=96&url=%s)'%(myaddon.getAddonInfo('id'),urllib.quote_plus(link))
	command=[(context1,cmd1)]
	return command

def menuContext(name,link,img,fanart,mode,query,item):
	if query.split('?')[0]=='Search':
		query=query.split('?')[1]
		item.addContextMenuItems(searchContext(name,link,mode,query))
	elif query.split('?')[0]=='ID':
		query=query.split('?')[1]
		command=searchContext(name,link,15,query)
		for cmd in favouritesContext(name,link,img,fanart,mode,query):
			command.append((cmd))
		item.addContextMenuItems(command)
	elif mode in (3,38,90,95):
		item.addContextMenuItems(favouritesContext(name,link,img,fanart,mode,query))
	elif mode in (96,97):
		item.addContextMenuItems(fileContext(link,mode))
	return query


def make_request(url,headers={'User-Agent':'Mozilla/5.0 Chrome/39.0.2171.71 Firefox/33.0'}):
	try:
		response = urlfetch.get(url,headers=headers)
		body=response.body
		response.close()
	except: mess('Make Request Error: %s'%url);body=''
	return body#unicode:body=response.text

def no_accent(s):
	s = s.decode('utf-8')
	s = re.sub(u'Đ', 'D', s)
	s = re.sub(u'đ', 'd', s)
	return unicodedata.normalize('NFKD', unicode(s)).encode('ASCII', 'ignore')

def xshare_group(object,group):
	if object:temp=object.group(group)
	else:temp=''
	return temp

def download_subs(url):
	response=urlfetch.get(url)
	if int(response.getheaders()[0][1])<10485760:#size<10MB
		filename=no_accent(os.path.basename(url))
		filename=re.sub('\[.+?\]','',filename);f_fullpath=thumuccucbo+filename
		if os.path.isfile(f_fullpath):
			try:os.remove(f_fullpath)
			except:mess(u'File đã có trong Thư mục riêng trên máy: %s'%filename);return
		try:
			f=open(f_fullpath,"wb");f.write(response.body);f.close()
			mess(u'Đã tải file %s vào Thư mục riêng trên máy'%filename)
		except:pass
	return

def get_input(title=u"", default=u""):
	result = ''
	keyboard = xbmc.Keyboard(default, title)
	keyboard.doModal()
	if keyboard.isConfirmed():
		result = keyboard.getText()
	return result


	data='[{"a":"filemanager_builddownload_getinfo","n":"'+idf+'","r":'+str(random.random())+'}]'
	try:
		response = urlfetch.post('https://api2.tenlua.vn/',data=data,headers=h,follow_redirects = False)
		link=json.loads(response.body)[0]
	except:link={'type':'none'}
	return link




	
def trangtiep(query,items):
	if 'Trang' in query.split('?')[0]:
		trang=int(query.split('?')[0].split('Trang')[1])
		query=query.split('?')[1]
	else:trang=1
	del items[0:(trang-1)*rows]
	trang+=1
	return trang,query,items
	

	if url=='http://vaphim.com/':return temp
	elif '/tag/' in url:
		pattern='class="entry-title"><a href="(.+?)" rel="bookmark"'
		url=xshare_group(re.search(pattern,make_request(url)),1)
		if not url:return temp
	mess(url,100)
	for img,fanart,href,name in vp2fshare(url):
		if href not in temp:temp.append(href);addirs(name,href,img,fanart)
	return temp

def json_request(url):
	try:
		response=urlfetch.get(url,headers={'User-Agent':'Mozilla/5.0 Chrome/39.0.2171.71 Firefox/33.0'})
		body=response.json
		response.close()
	except:body=''
	return body

def google_search_api(url,start,string,items):#url:fshare.vn,4share.vn,tenlua.vn,hdvietnam.com
	string_search = urllib.quote_plus('"%s"'%string)
	href = 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&rsz=large&'
	href+='start=%s&q=site:%s+%s'%(start,url.lower(),string_search)
	print href
	json=json_request(href)
	if not json:mess(u'Lỗi get %s'%href);return items,'end'
	if json['responseStatus']==403:
		mess(u'Google: nghi ngờ lạm dụng Dịch vụ. Tự động chuyển sang web search')
		return google_search_web(url,query,page,mode,items)
	data=json['responseData']
	if not data or not data['results']:mess(u'Không tìm được tên phim phù hợp');return items,'end'
	currentPage=int(data['cursor']['currentPageIndex'])+1;nextPage=0
	for i in data['results']:
		if 'tenlua' in url and re.search('\w{16,20}/(.*)\Z',i['url'].encode('utf-8')):
			name=xshare_group(re.search('\w{16,20}/(.*)\Z',i['url'].encode('utf-8')),1)
		else: name=i['titleNoFormatting'].encode('utf-8')
		name=re.sub('\||<.+?>|\[.*\]|\(.*\)','',name.split(':')[0]).strip()
		if name and 'Forum' not in name and 'server-nuoc-ngoai' not in i['url']:
			items.append((name,i['url'].encode('utf-8')))
	start=str(int(start)+8)
	if start not in ' '.join(s['start'] for s in data['cursor']['pages']):start='end'
	return items,start

def google_search(url,query,mode,page,items=[]):
	srv=url.split('.')[0]
	if page==0:get_file_search(url,mode)
	elif page==1:
		query=get_string_search(url)
		if query:return google_search(url,query,mode,page=4)
		else:return 'no'
	else:
		query=no_accent(query);tempurl=[];templink=[]
		if '?' in query:
			start=query.split('?')[1];query=query.split('?')[0]
		else:start='0'
		if googlesearch=='Web':items,start=google_search_web(url,start,query,items)
		else:items,start=google_search_api(url,start,query,items)
		if not items:return 'no'
		for name,link in sorted(items,key=lambda l:l[0]):
			if link in templink:continue
			if url=='hdvietnam.com':tempurl=hdvn_get_link(link,temp=tempurl)
			elif url=='vaphim.com':tempurl=google_vaphim(link,temp=tempurl)
			elif url=='ifile.tv':tempurl=google_ifile(link,name,temp=tempurl)
			elif url=='4share.vn' and 'docs.4share' not in link:tempurl=DocTrang4share(link,temp=tempurl)
			else:addirs(name,link,icon[srv])
			templink.append(link)
		if start!='end':
			name=color['trangtiep']+'Trang tiep theo...trang %s[/COLOR]'%str(page-2)
			addir(name,url,icon[srv],mode=mode,query='%s?%s'%(query,start),page=page+1,isFolder=True)
	return ''
  
def google_search_web(url,start,query,items):
	num='20';google = 'https://www.google.com.vn/search?hl=vi&ie=utf-8&oe=utf-8&num=%s&'%num
	string_search = urllib.quote_plus('"%s"'%query);srv=url.split('.')[0]
	href=google+'start=%s&q=site:%s+%s'%(start,url.lower(),string_search)
	body=make_request(href)
	if '<TITLE>302 Moved</TITLE>' in body:
		mess(u'Google từ chối dịch vụ do bạn đã truy cập quá nhiều');return items,'end'
	links=re.findall('<a href="(.{,300})" onmousedown=".{,200}">(.{,200})</a></h3>',body)
	print href,url,len(links),len(body)
	for link,name in links:items.append((name,link))
	start=str(int(start)+int(num))
	if 'start=%s'%start not in body:start='end'
	return items,start

def open_category(query): #category.xml
	pattern='<a server="(...)" category="(.+?)" mode="(..)" color="(.*?)" icon="(.*?)">(.+?)</a>'
	items=re.findall(pattern,makerequest(data_path+'category.xml'))
	for server,category,mode,colo,icon,name in items:
		if (server!=query) or (("18" in category) and (phim18=="false")):continue
		if query=='VPH' and mode!='10':q='vaphim.xml'
		elif query=='IFI' and mode!='10':q='ifiletv.xml'
		else:q=category
		name='[COLOR '+colo+']'+name+'[/COLOR]';icon=icon_path+icon
		addir(name,category,icon,home+'/fanart.jpg',mode=int(mode),page=0,query=q,isFolder=(mode!='16'))

def main_menu(category,page,mode,query): #Doc list tu vaphim.xml hoac ifiletv.xml
	items = doc_xml(datapath+query,para=category);pages=len(items)/rows+1
	del items[0:page*rows];count=0;down=len(items)
	for id,img,fanart,href,name in items:
		down-=1;addirs(name,href,img,fanart);count+=1
		if count>rows and down>10:break
	if down>10:
		page+=1;name=color['trangtiep']+'Trang tiep theo...trang %d/%d[/COLOR]'%(page+1,pages)
		addir(name,category,icon['icon'],mode=mode,page=page,query=query,isFolder=True)

def clean_string(string):
	string=' '.join(s for s in re.sub('Fshare|-|4share|Tenlua|&.+ ','',string).split())
	return string

def menu_xml(url,filename='',page=0):
	if not page:items=doc_xml(url,filename=filename);f=open(data_path+'temp.txt','w');f.write(str(items));f.close()
	else:f=open(data_path+'temp.txt');items=eval(f.readlines()[0]);	f.close()
	pages=len(items)/rows+1
	del items[0:page*rows];count=0
	for id,href,img,fanart,name in items:
		if '47daklak.com' in href: addir(name,href,img,mode=47)
		else: addirs(name,href,img,fanart)
		count+=1
		if count>rows and len(items)>(rows+10):break
	if len(items)>(rows+10):
		page+=1;name=color['trangtiep']+'Trang tiep theo...trang %d/%d[/COLOR]'%(page+1,pages)
		addir(name,url,icon_path+'khophim.png',mode=97,page=page,isFolder=True)




def makerequest(file,string='',attr='r'):
	if attr=='r':
		try:f=open(file);body=f.read();f.close()
		except:mess('Loi mo file: %s'%os.path.basename(file));body=''
	else:
		if 'unicode' in str(type(string)):string=string.encode('utf-8')
		try:f=open(file,attr);f.write(string);f.close();body='ok'
		except:mess('Loi mo file: %s'%os.path.basename(file));body=''
	return body

def trangtiep_google_custom(url,results,string,mode,trang,start,apiary):
	if 'cursor' in results and 'pages' in results['cursor']:
		if str(int(start)+20) in ' '.join(s['start'] for s in results['cursor']['pages']):
			trang=str(int(trang)+1)
			name=color['trangtiep']+'Trang tiep theo...trang %s[/COLOR]'%trang
			addir(name,url,icon[url.split('.')[0]],mode=mode,page=4,query='%s?%s?%s'%(string,trang,apiary),isFolder=True)

def trang_search(string):
	if len(string.split('?'))==3:p=string.split('?')[2];trang=string.split('?')[1];string=string.split('?')[0]
	elif len(string.split('?'))==2:p=1;trang=string.split('?')[1];string=string.split('?')[0]
	else:p=trang='1'
	return string,trang,p


def get_file_search(url,mode):
	srv=url.split('.')[0]
	if mode==2:site='Google '
	else:site=''
	name=color['search']+'%sSearch[/COLOR] trên %s%s: [/COLOR]Nhập chuỗi tìm kiếm mới'%(site,color[srv],url)
	addir(name,url,icon[srv],mode=mode,page=1,query='INP',isFolder=True)
	if myaddon.getSetting('history')=='true':
		items = re.findall('<a>(.+?)</a>',makerequest(search_file))
		for string in items:
			addir(string,url,icon[srv],query='Search?'+string,page=4,mode=mode,isFolder=True)

def get_string_search(url):
	query = get_input('Nhập chuổi tên phim cần tìm trên %s'%url)
	if query:
		query = ' '.join(s for s in query.replace('"',"'").replace('?','').split() if s!='')
		makerequest(search_file,string='<a>%s</a>\n'%query,attr='a')
	return query

def edit_search_file(name,url,page,query):
	print name,url,page,query
	if page==1 and name==query:#delete string
		content=re.sub('<a>%s</a>\n'%query,'',makerequest(search_file))
		if makerequest(search_file,string=content,attr='w'):mess(u'Đã xóa mục: %s'%query.decode('utf-8'))
		else:mess(u'[COLOR orangered]Chưa xóa được mục: "%s"'%query.decode('utf-8'))
	elif page==1:#delete ID
		content=re.sub('<a href="%s">.+?</a>\n'%url,'',makerequest(search_file))
		if makerequest(search_file,string=content,attr='w'):mess(u'Đã xóa mục: %s'%name.decode('utf-8'))
		else:mess(u'[COLOR orangered]Chưa xóa được mục: "%s"'%name.decode('utf-8'))
	elif page==2 and name==query:#edit string
		string_new = get_input('Nhập chuổi search mới',query)
		if string_new and string_new!=query:
			string_new = ' '.join(s for s in string_new.replace('"',"'").replace('?','').split() if s!='')
			content=re.sub('<a>%s</a>\n'%query,'<a>%s</a>\n'%string_new,makerequest(search_file))
			if makerequest(search_file,string=content,attr='w'):mess(u'Đã sửa mục: %s'%query.decode('utf-8'))
			else:mess(u'[COLOR orangered]Chưa sửa được mục: "%s"'%query.decode('utf-8'))
	elif page==2:#edit ID
		temp=xshare_group(re.search('(\[COLOR.{,15}/COLOR]-)',name),1)
		name=re.sub('(\[COLOR.{,10}\]|\[/COLOR])','',re.sub('(\[COLOR.{,15}/COLOR]-)','',name))
		string_new = get_input('Nhập tên phim mới',name)
		if string_new==name.strip() or not string_new:return 'no'
		string_new=temp+string_new
		content=re.sub('<a href="%s">.+?</a>\n'%url,'<a href="%s">%s</a>\n'%(url,string_new),makerequest(search_file))
		if makerequest(search_file,string=content,attr='w'):mess(u'Đã sửa mục: %s'%name.decode('utf-8'))
		else:mess(u'[COLOR orangered]Chưa sửa được mục: "%s"'%name.decode('utf-8'))
	xbmc.executebuiltin("Container.Refresh")





def subscene(name,url,query):#,img='',fanart='',query=''
	if query=='subscene.com':
		href = get_input('Hãy nhập link của sub trên subscene.com','http://subscene.com/subtitles/')
		if href is None or href=='' or href=='http://subscene.com/subtitles/':return 'no'
	else:href=url
	if not re.search('\d{5,10}',href):
		if not os.path.basename(href):href=os.path.dirname(href)
		pattern='<a href="(/subtitles/.+?)">\s+<span class=".+?">\s*(.+?)\s+</span>\s+<span>\s+(.+?)\s+</span>'
		subs=re.findall(pattern,urlfetch.get(url=href,headers={'Cookie':'LanguageFilter=13,45'}).body)
		for url,lang,name in subs:
			if '/english/' in url:name='Eng '+name
			else:name='[COLOR red]Vie[/COLOR]-'+name
			print url
			addirs(name,'http://subscene.com'+url,query='download')
		return ''
	pattern='<a href="(.+?)" rel="nofollow" onclick="DownloadSubtitle.+">'
	downloadlink='http://subscene.com' + xshare_group(re.search(pattern,make_request(href)),1)
	if len(downloadlink)<20:mess(u'Không tìm được maxspeed link sub');return
	print 'downloadlink %s'%downloadlink
		
	typeid="srt"
	body=make_request(downloadlink)
	tempfile = os.path.join(thumuccucbo, "subtitle.sub")
	f = open(tempfile, "wb");f.write(body);f.close()
	f = open(tempfile, "rb");f.seek(0);fread=f.read(1);f.close()
	if fread == 'R':	typeid = "rar"
	elif fread == 'P':typeid = "zip"

	tempfile = os.path.join(thumuccucbo, "subtitle." + typeid)
	if os.path.exists(tempfile):
		try:os.remove(tempfile)
		except:return
	os.rename(os.path.join(thumuccucbo, "subtitle.sub"), tempfile)
	if os.path.exists(tempfile):mess(u'Đã tải sub vào Thư mục riêng trên máy: %s'%name.decode('utf-8'))
	if typeid in "rar-zip":
		tempath=thumuccucbo
		if 'Eng' in name and myaddon.getSetting('trans_sub')=='true':
			tempath = xbmc.translatePath(os.path.join(thumuccucbo,'temp/'));import shutil
			if os.path.exists(tempath):
				shutil.rmtree(tempath)
			try:os.mkdir(tempath)
			except:
				xbmc.sleep(1000)
				try:os.mkdir(tempath)
				except:mess(u'Không tạo được thư mục sub');return 'no'
		xbmc.sleep(500)
		try:xbmc.executebuiltin(('XBMC.Extract("%s","%s")'%(tempfile,tempath)).encode('utf-8'), True)
		except:pass
		if tempath!=thumuccucbo:
			exts = [".srt", ".sub", ".txt", ".smi", ".ssa", ".ass"];sub_list=[]
			for root, dirs, files in os.walk(tempath):
				for f in files:
					f=re.sub(',|"|\'','',f)
					file = os.path.join(root, f)
					filesub=os.path.join(thumuccucbo, f)
					if os.path.splitext(file)[1] in exts:
						sub_list.append(file)
						mess(u'Google đang dịch sub từ tiếng Anh sang tiếng Việt', timeShown=20000)
						try:
							tempfile=xshare_trans(file,tempath)
							os.remove(file)
							if os.path.exists(filesub):os.remove(filesub)
							os.rename(tempfile,filesub)
							mess(u'Đã dịch xong sub từ tiếng Anh sang tiếng Việt') 
						except:mess(u'Không dịch được sub từ tiếng Anh sang tiếng Việt') 

	return 'ok'


    

def fptplay(name,url,img,mode,page,query):
	if query=="FPP":
		body=make_request('http://fptplay.net')
		name=color['search']+"Search trên fptplay.net[/COLOR]"
		addir(name,"fptplay.net/tim-kiem",icon['fptplay'],mode=mode,query="FPS",isFolder=True)
		name=color['fptplay']+'Trang chủ fptplay.net[/COLOR]'
		addir(name,"http://fptplay.net",icon['fptplay'],mode=mode,query='FP0',isFolder=True)
		start='top_menu reponsive';end='top_listitem';body=body[body.find(start):body.find(end)]
		for href,title in re.findall('<li ><a href="(http://fptplay.net/danh-muc/.+?)">(.+?)</a></li>',body):
			title=color['fptplay']+fptplay_2s(title)+'[/COLOR]'
			addir(title,href,icon['fptplay'],mode=mode,query='FP2',isFolder=True)
	elif query=="FPS":get_file_search(url,mode)
	elif query=="INP":
		query=get_string_search(url)
		if query:return fptplay(name,url,img,mode,page,query)
		else:return 'no'
	elif url=="fptplay.net/tim-kiem":
		search_string = urllib.quote(query)
		url='http://fptplay.net/show/more?type=search&stucture_id=key&page=1&keyword=%s'%search_string
		return fptplay(name,url,img,mode,page,query='FP3')
	elif query=="FP0":
		body=make_request('http://fptplay.net')
		name=color['fptplay']+'Phổ biến hiện nay[/COLOR]'
		addir(name,'phim_popular',icon['fptplay'],mode=mode,query='FP1',isFolder=True)
		name=color['fptplay']+'Đặc sắc[/COLOR]'
		addir(name,'phim_trending',icon['fptplay'],mode=mode,query='FP1',isFolder=True)
		pattern='<a href="(.+?)" title="(.+?)" class="pull-left btn_arrow_right"></a>'
		items=re.findall(pattern,body)
		for href,title in items:
			title=color['fptplay']+fptplay_2s(title)+'[/COLOR]'
			addir(title,href,icon['fptplay'],mode=mode,query='FP1',isFolder=True)
	elif query=="FP1":
		body=make_request('http://fptplay.net')
		if 'phim_popular' in url:start='data-tooltip="phim_popular';end='data-tooltip="phim_trending'
		elif 'phim_trending' in url:start='data-tooltip="phim_trending';end='id="selTab_5284685d169a585a2449c489"'
		elif 'phim' in url:start='id="selTab_5284685d169a585a2449c489"';end='id="selTab_52847232169a585a2449c48c'
		elif 'tv-show' in url:start='id="selTab_52847232169a585a2449c48c';end='id="selTab_54fd271917dc136162a0c'
		elif 'thieu-nhi' in url:	start='id="selTab_54fd271917dc136162a0cf2d';end='id="selTab_52842df7169a580a79169'
		elif 'the-thao' in url:start='id="selTab_52842df7169a580a79169efd"';	end='id="selTab_5283310e169a585a05b920d'
		elif 'ca-nhac' in url:start='id="selTab_5283310e169a585a05b920de"';end='id="selTab_52842dd3169a580a79169efc'
		elif 'tong-hop' in url:start='id="selTab_52842dd3169a580a79169efc"';end='</body>'
		body=body[body.find(start):body.find(end)]
		pattern='<a href=".+?-(\w+)\.html".*alt="(.+?)"'
		items=re.findall(pattern,body);temp=[]
		for id,title in items:
			if id not in temp:temp.append(id);fptplay_getlink(id,fptplay_2s(title),mode)
	elif query=="FP2":
		pattern='<a href="(http://fptplay.net/the-loai/.+?)" title="(.+?)"'
		items=re.findall(pattern,make_request(url))
		for href,name in items:
			name=color['fptplay']+fptplay_2s(name)+"[/COLOR]";id=xshare_group(re.search('(\w{22,26})',href),1)
			data='type=new&keyword=undefined&page=1&stucture_id=%s'%id;url='http://fptplay.net/show/more?%s'%data
			addir(name,url,icon["fptplay"],mode=mode,query="FP3",isFolder=True)
	elif query=="FP3":
		try:body=urlfetch.post(url).body
		except:mess(u'Lỗi get data từ fptplay.net');return 'no'
		items=re.findall('<a href=".+-(\w+)\.html".+class="title">(.+?)</a>',body)
		for id,title in items:fptplay_getlink(id,fptplay_2s(title),mode)
		if len(items)>35:
			page=xshare_group(re.search('page=(\d{1,3})',url),1);page=str(int(page)+1);
			url=re.sub('page=\d{1,3}','page='+page,url)
			name=color['trangtiep']+"Trang tiếp theo - Trang %s[/COLOR]"%page
			addir(name,url,icon["fptplay"],mode=mode,query="FP3",isFolder=True)
		elif not items:mess(u'Không tìm thấy dữ liệu');return 'no'
	elif query=="FP4":fptplay_getlink(url,name,mode,dir=False)
	elif query=='play':
		item = xbmcgui.ListItem(path=url)
		xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)
	return ''
	
def fptplay_2s(string):
	return ' '.join(re.sub('&.+;',xshare_group(re.search('&(\w).+;',s),1),s) for s in string.split())

def fptplay_getlink(id,name,mode,dir=True):
	try:
		json=urlfetch.post('http://fptplay.net/show/getlink?id=%s&episode=1&mobile=web'%id).json
		if dir:
			url = json['quality'][0]['url'][0]['url']
			img = json['quality'][0]['thumb']
			title = json['quality'][0]['title']
			if len(json['quality'])==1:addir(name.strip(),url,img,img,mode=mode,query='play')
			else:addir(color['fptplay']+name.strip()+"[/COLOR]",id,img,img,mode=mode,query='FP4',isFolder=True)
		else:
			for i in json['quality']:
				url = i['url'][0]['url']
				img = i['thumb']
				title = re.sub('\[.{,20}\]','',name.strip())+' - '+i['title'].encode('utf-8')
				addir(title,url,img,img,mode=mode,query='play')
	except:pass

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
homnay=datetime.date.today().strftime("%d/%m/%Y")
url=name=fanart=img=date=query=end=''
mode=page=0;temp=[]

try:url=urllib.unquote_plus(params["url"])
except:pass
try:name=urllib.unquote_plus(params["name"])
except:pass
try:img=urllib.unquote_plus(params["img"])
except:pass
try:fanart=urllib.unquote_plus(params["fanart"])
except:pass
#try:date=urllib.unquote_plus(params["date"])
#except:pass
try:mode=int(params["mode"])
except:pass
try:page=int(params["page"])
except:pass
try:query=urllib.unquote_plus(params["query"])
except:pass#urllib.unquote

print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)
print "query: "+str(query)
print "page: "+str(page)

if mode==0 or mode=='':
	open_category("FRE")
	xbmcplugin.endOfDirectory(int(sys.argv[1]))
	
elif mode==2:end=google_search(url,query,mode,page)
elif mode==3:end=resolve_url(url)
elif mode==4:phimchon('http://vaphim.com','vaphim.xml','data="(.+?)" title')
elif mode==5:vp_xemnhieu()
elif mode==6:end=phimFshare(name,url,mode,page,query)
elif mode==7:end=fptplay(name,url,img,mode,page,query)
elif mode==8:hdvietnam(query,mode)
elif mode==9:edit_search_file(name,url,page,query)
elif mode==10:open_category(query)
elif mode==13:end=xshare_search(url,query,mode,page)
elif mode==15:end=mo_id_file(url,name,mode,page,query)
elif mode==16:end=Mo_maxspeed_link()
elif mode==17:end=megabox(name,url,mode,page,query)
elif mode==18:dangcaphd(name,url,img,mode,page,query)
elif mode==20:end=vp_update()
elif mode==31:end=ifile_update()
elif mode==34:phimchon("http://ifile.tv/phim","ifiletv.xml",'href=".+(\d{5}).+" class="mosaic-backdrop"')
elif mode==35:phimchon("http://ifile.tv/phim/index","ifiletv.xml",'href=".+(\d{5}).+" class="mosaic-backdrop"')
elif mode==38:DocTrang4share(url)#38
elif mode==39:DocTrangifiletv(url)
elif mode==47:daklak47(name,url,img)
elif mode==90:end=DocTrangFshare(url,img,fanart)
elif mode==91:main_menu(url,page,mode,query)
elif mode==94:end=subscene(name,url,query)
elif mode==95:lay_link_tenlua(url)
elif mode==96:doc_thumuccucbo(url)
elif mode==97:menu_xml(url,name,page)
elif mode==98:xshare_favourites(name,url,img,fanart,query)
elif mode==99:myaddon.openSettings();end='ok'
#xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_DATE)
if end not in 'no-ok' or end=='':xbmcplugin.endOfDirectory(int(sys.argv[1]))
#https://urlfetch.readthedocs.org/en/v0.5.3/examples.html
#http://hdonline.vn/
#addir(name,url,img,fanart,mode,page,query,isFolder)