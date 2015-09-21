# -*- coding: utf-8 -*-
import xbmc,xbmcplugin,xbmcgui,xbmcaddon,urllib,re,os,unicodedata,datetime,random,json

myaddon=xbmcaddon.Addon()
home=xbmc.translatePath(myaddon.getAddonInfo('path'));datapath=xbmc.translatePath(myaddon.getAddonInfo('profile'))
iconpath=os.path.join(datapath,'icon');datapath=os.path.join(datapath,'data')
iconpath=xbmc.translatePath(os.path.join(home,"logos\\"))
iconpath=xbmc.translatePath(os.path.join(home,"logos"))
datapath=os.path.join(datapath,'data')
sys.path.append(os.path.join(home,'resources','lib'));from urlfetch import get,post
search_file=os.path.join(datapath,"search.xml");data_path=os.path.join(home,'resources','data')
rows=int(myaddon.getSetting('sodonghienthi'));googlesearch=myaddon.getSetting('googlesearch')

media_ext=['aif','iff','m3u','m4a','mid','mp3','mpa','ra','wav','wma','3g2','3gp','asf','asx','avi','flv','mov','mp4','mpg','mkv','m4v','rm','swf','vob','wmv','bin','cue','dmg','iso','mdf','toast','vcd','ts','flac','m2ts']
color={'fshare':'[COLOR gold]','vaphim':'[COLOR gold]','phimfshare':'[COLOR khaki]','4share':'[COLOR blue]','tenlua':'[COLOR fuchsia]','fptplay':'[COLOR orange]','trangtiep':'[COLOR lime]','search':'[COLOR lime]','ifile':'[COLOR blue]','hdvietnam':'[COLOR red]','xshare':'[COLOR blue]','subscene':'[COLOR green]','megabox':'[COLOR orangered]','dangcaphd':'[COLOR yellow]'};icon={}
for hd in ['xshare','4share', 'dangcaphd', 'downsub', 'favorite', 'fptplay', 'fshare', 'gsearch', 'hdvietnam', 'icon', 'id', 'ifiletv', 'isearch', 'khophim', 'maxspeed', 'megabox', 'movie', 'msearch', 'myfolder', 'myfshare', 'phimfshare', 'serverphimkhac', 'setting', 'tenlua', 'vaphim']:
	icon.setdefault(hd,os.path.join(iconpath,'%s.png'%hd))
hd = {'User-Agent' : 'Mozilla/5.0 Chrome/39.0.2171.71 Firefox/33.0'}

def mess(message, timeShown=10000,title=''):
	xbmc.executebuiltin((u'XBMC.Notification(%s,%s,%s,%s)'%('Kho phim Xshare Free [COLOR green]%s[/COLOR]'%title,message,timeShown,icon['icon'])).encode("utf-8"))

def mess_yesno(title='[COLOR green]Xshare[/COLOR]', line1='', line2=''):
	dialog=xbmcgui.Dialog()#dialog.yesno(heading, line1[, line2, line3,nolabel,yeslabel])
	return dialog.yesno(title,line1,line2)

def no_accent(s):
	s=re.sub(u'Đ','D',str2u(s));s=re.sub(u'đ','d',s)
	return unicodedata.normalize('NFKD', unicode(s)).encode('ASCII', 'ignore')

def str2u(s):
	if type(s)==str:
		try:s=s.decode('utf-8','ignore')
		except:pass
	return s

def s2u(s):
    if isinstance(s,str):s=s.decode('utf-8')
    return s
	
def unescape(string):
	return ' '.join(re.sub('&.+;',xsearch('&(\w).+;',s,1),s) for s in string.split())

def u2s(s):
	if isinstance(s,unicode):s=s.encode('utf-8')
	return s

def clean_string(string):
	return ' '.join(s for s in re.sub('Fshare|4share|Tenlua','',string).split())

def joinpath(p1,p2):
	try:p=os.path.join(p1,p2)
	except:p=os.path.join(p1,str2u(p2))
	return p

def init_file():
	datafolder=xbmc.translatePath(myaddon.getAddonInfo('profile'))
	for folder in (datafolder,datapath,iconpath,myfolder,subsfolder,tempfolder):
		if not os.path.exists(folder):os.mkdir(folder)
	xmlheader='<?xml version="1.0" encoding="utf-8">\n';p=datapath;q=myfolder
	for i in [(p,'search.xml'),(p,'hdvietnam.xml'),(p,'favourites.xml'),(p,'phimmoi.xml'),(p,'fpt.xml'),(q,'mylist.xml')]:
		file=joinpath(i[0],i[1])
		if not os.path.isfile(file):makerequest(file,xmlheader,'w')

def xshare_group(object,group):
	return object.group(group) if object else ''

def sub_body(content,s1,s2):
	if not isinstance(content,str):content=str(content)
	if s1 and s2:result=content[content.find(s1):content.find(s2)]
	elif s1:result=content[content.find(s1):]
	elif s2:result=content[:content.find(s2)]
	else:result=content
	return result

def json_rw(file,dicts={},key=''):
	if dicts:makerequest(joinpath(datapath,file),json.dumps(dicts),'w')
	else:
		try:dicts=json.loads(makerequest(joinpath(datapath,file)))
		except:dicts={}
		if key:dicts=dicts.get(key,())
	return dicts

def delete_files(folder,mark='',temp='ok'):
	for file in os.listdir(folder):
		if os.path.isfile(joinpath(folder,file)) and (not mark or mark in file):
			try:os.remove(joinpath(folder,file))
			except:temp='';pass
	return temp

def endxbmc():
	xbmcplugin.endOfDirectory(int(sys.argv[1]))

def xbmcsetResolvedUrl(url,name=''):
	item=xbmcgui.ListItem(path=url)
	if 'Maxlink' in name:
		if name!='Maxlink':name=name.replace('Maxlink','');item.setInfo('video', {'Title':name})
		else:item.setInfo('video', {'Title':os.path.basename(url)})
		name=''
	xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item);endxbmc()
	if myaddon.getSetting('autoload_sub')=='true' and name!='xshare':
		if name:url=name
		urltitle=urllib.unquote(os.path.splitext(os.path.basename(url))[0]).lower()
		urltitle='.'+'.'.join(s for s in re.sub('_|\W+',' ',re.split('\d\d\d\d',urltitle)[0]).split())+'.'
		subfile='';items=[]
		for file in os.listdir(subsfolder):
			filefullpath=joinpath(subsfolder,file).encode('utf-8')
			filename=re.sub('vie\.|eng\.','',os.path.splitext(file)[0].lower().encode('utf-8'))
			filename=re.split('\d\d\d\d',filename)[0];count=0
			for word in re.sub('_|\W+',' ',filename).split():
				if '.%s.'%word in urltitle:count+=1
			if count:items.append((count,filefullpath))
		for item in items:
			if item[0]>=count:count=item[0];subfile=item[1]
		if subfile:
			xbmc.sleep(1000);xbmc.Player().setSubtitles(subfile)
			#mess(u'[B][COLOR green]%s[/B][/COLOR]'%str2u(os.path.basename(subfile)),20000,'Auto load sub')

def addir(name,link,img='',fanart='',mode=0,page=0,query='',isFolder=False):
	def xquote(href):return urllib.quote_plus(href)
	if '18+' in name and myaddon.getSetting('phim18')=="false":return
	name=unescape(re.sub(',|\|.*\||\||\<.*\>','',u2s(name)))
	item=xbmcgui.ListItem(name,iconImage=img,thumbnailImage=img)
	query=menuContext(name,link,img,fanart,mode,query,item)
	item.setInfo(type="Video", infoLabels={"title":name})
	if not fanart:fanart=joinpath(home,'fanart.jpg')
	item.setProperty('Fanart_Image',fanart)
	li='%s?name=%s&url=%s&img=%s&fanart=%s&mode=%d&page=%d&query=%s'
	li=li%(sys.argv[0],urllib.quote(name),xquote(link),xquote(img),xquote(fanart),mode,page,query)
	if not isFolder:item.setProperty('IsPlayable', 'true')
	xbmcplugin.addDirectoryItem(int(sys.argv[1]),li,item,isFolder)

def addirs(name,href,img='',fanart='',query=''):
	name=clean_string(name)
	if not fanart and iconpath not in img:fanart=img
	if 'xml' in query:
		if name=='mylist.xml':name=color['subscene']+name+'[/COLOR]'
		query=query.replace('xml','');name='%sList xml[/COLOR]-%s'%(color['fptplay'],name)
		addir(name,href,img,fanart,mode=97,query=query,isFolder=True)
	elif query=='file':addir(name,href,img=icon['icon'],mode=96,query=query,isFolder=True)
	elif 'www.fshare.vn/file' in href:
		if str2u('phụ đề việt') in str2u(name).lower():
			name=color['fshare']+'Phụ đề Việt[/COLOR]-%s'%name
			addir(name,href,img,fanart,mode=3,query=query,isFolder=True)
		else:addir(color['fshare']+'Fshare[/COLOR]-%s'%name,href,img,fanart,mode=3,query=query)
	elif 'www.fshare.vn/folder' in href:
		if str2u('chia sẻ') in str2u(name):name=color['trangtiep']+name+'[/COLOR]'
		else:name=color['fshare']+name+'[/COLOR]'
		addir(name,href,img,fanart,mode=90,query=query,isFolder=True)
	elif '4share.vn/d/' in href:
		addir(color['4share']+name+'[/COLOR]',href,img,fanart,mode=38,query=query,isFolder=True)
	elif '4share.vn' in href:
		addir(color['4share']+'4share[/COLOR]-%s'%name,href,img,fanart,mode=3,query=query)
	elif 'tenlua.vn/fm/folder/' in href or '#download' in href:
		addir(color['tenlua']+name+'[/COLOR]',href,img,fanart,mode=95,query=query,isFolder=True)
	elif 'tenlua.vn' in href:
		addir(color['tenlua']+'TenLua[/COLOR]-%s'%name,href,img,fanart,mode=3,query=query)
	elif 'subscene.com' in href:
		addir(color['subscene']+'Subscene[/COLOR]-%s'%name,href,img,fanart,mode=94,query='download',isFolder=True)
	elif 'http://pubvn.' in href:
		addir(color['4share']+name+'[/COLOR]',href,img,fanart,mode=38,query=query,isFolder=True)
	elif 'http://vuahd.tv' in href:
		addir(color['vuahd']+name+'[/COLOR]',href,img,fanart,mode=38,query=query,isFolder=True)

def menuContext(name,link,img,fanart,mode,query,item):
	if query.split('?')[0]=='Search':
		query=query.split('?')[1]
		item.addContextMenuItems(searchContext(name,link,img,fanart,mode))
	elif query.split('?')[0]=='ID':
		query=query.split('?')[1]
		command=searchContext(name,link,img,fanart,15)
		command+=favouritesContext(name,link,img,fanart,mode)
		item.addContextMenuItems(command)
	elif 'fshare.vn' in link or '4share.vn' in link or 'tenlua.vn' in link:#mode in (3,38,90,95):
		item.addContextMenuItems(favouritesContext(name,link,img,fanart,mode))
	elif myfolder in str2u(link):
		item.addContextMenuItems(make_myFile(name,link,img,fanart,mode,query))
	elif query in 'hdvietfolder-hdvietplay':
		item.addContextMenuItems(hdvietContext(name,link,img,fanart,mode))
	return query

def makeContext(name,link,img,fanart,mode,query):
	if query=='Add to MyFshare favorite':make='AddFavorite'
	elif query=='Remove from MyFshare favorite':make='RemoveFavorite'
	else:make=query.split()[0]
	if 'Rename' in make:colo=color['fshare']
	elif 'Remove' in make:colo=color['hdvietnam']
	else:colo=color['trangtiep']
	context=colo+query+'[/COLOR]'
	p=(myaddon.getAddonInfo('id'),mode,name,link,img,fanart,make)
	cmd='RunPlugin(plugin://%s/?mode=%d&name=%s&url=%s&img=%s&fanart=%s&query=%s)'%(p)
	return context,cmd

def hdvietContext(name,link,img,fanart,mode):
	context=color['trangtiep']+'Thêm vào phim yêu thích[/COLOR]'
	p=(myaddon.getAddonInfo('id'),mode,name,link.split('_')[0],img,fanart,'Themmucyeuthich')
	cmd='RunPlugin(plugin://%s/?mode=%d&name=%s&url=%s&img=%s&fanart=%s&query=%s)'%(p)
	command=[(context,cmd)]
	return command

def searchContext(name,link,img,fanart,mode):
	command=[(makeContext(name,link,img,fanart,9,'Rename item'))]
	command.append((makeContext(name,link,img,fanart,9,'Remove item')))
	return command

def favouritesContext(name,link,img,fanart,mode):
	def makecmd(mode,title):command.append((makeContext(name,link,img,fanart,mode,title)))
	command=[]
	if type(link)==unicode:link=link.encode('utf-8')
	if link in makerequest(joinpath(datapath,"favourites.xml")):	
		makecmd(98,'Rename in MyFavourites');makecmd(98,'Remove from MyFavourites')
	else:makecmd(98,'Add to MyFavourites')
	if 'www.fshare.vn' in link:
		if query=='MyFshare':makecmd(11,'Remove from MyFshare');makecmd(11,'Rename from MyFshare')
		else:makecmd(11,'Add to MyFshare')
		if query=='favorite':makecmd(11,'Remove from MyFshare favorite')
		else:makecmd(11,'Add to MyFshare favorite')
	if link in makerequest(joinpath(myfolder,'mylist.xml')):
		makecmd(12,'Rename in Mylist.xml');makecmd(12,'Remove from Mylist.xml')
	else:makecmd(12,'Add to Mylist.xml')
	command.append((makeContext(name,'addstring.xshare.vn',img,fanart,13,'Add item name to string search')))
	return command

def make_myFile(name,link,img,fanart,mode,query):
	name=re.sub('\[COLOR.{,12}\]|\[/COLOR\]|Fshare|4share|TenLua|List xml|-|:|"','',name).strip();command=[]
	if os.path.isfile(str2u(link)):
		command.append((makeContext(name,link,img,fanart,11,'Upload to MyFshare')));temp='file'
	else:temp='folder'
	command.append((makeContext(name,link,img,fanart,96,'Rename this %s'%temp)))
	command.append((makeContext(name,link,img,fanart,96,'Remove this %s'%temp)))
	return command

def make_mySearch(name,url,img,fanart,mode,query):
	attr='w';body=makerequest(search_file);r='<a href="%s">.+?</a>\n'%url
	if query=='Rename':
		string=get_input('Nhập chuổi mới',re.sub('\[.*\]-','',name)).strip()
		if not string or string==re.sub('\[.*\]-','',name):return
		string=' '.join(s for s in re.split(' |\.|\'|"\?',string));r1='<a href="%s">%s</a>\n'%(url,string)
		body=re.sub(r,r1,body) if re.search('http.?://',url) else body.replace(name,string)
	elif query=='Remove':
		body=re.sub(r,'',body) if re.search('http.?://',url) else re.sub('<a>%s</a>\n'%name,'',body)
	elif query=='Add':
		if not re.search(url,body):body='<a href="%s">%s</a>\n'%(url,name);attr='a'
		else:return
	elif query=='Input':
		query = get_input('Nhập chuổi tên phim cần tìm trên %s'%url);attr='a'
		if query:
			query = ' '.join(s for s in query.replace('"',"'").replace('?','').split() if s!='')
			if not re.search(query,body):body='<a>%s</a>\n'%query
			else:return query
		else:return ''
	elif query=='get':
		srv=url.split('.')[0];site='Google ' if mode==2 else ''
		name=color['search']+'%sSearch[/COLOR] trên %s%s: [/COLOR]Nhập chuỗi tìm kiếm mới'%(site,color[srv],url)
		addir(name,url,icon[srv],mode=mode,page=1,query='INP',isFolder=True)
		if myaddon.getSetting('history')=='true':
			for string in re.findall('<a>(.+?)</a>',makerequest(search_file)):
				addir(string,url,icon[srv],query='Search?'+string,page=4,mode=mode,isFolder=True)
		return
	if makerequest(search_file,string=body,attr=attr):
		if attr=='w':mess(u'%s chuổi thành công'%str2u(query));xbmc.executebuiltin("Container.Refresh")
	elif attr=='w':mess(u'%s chuổi thất bại'%str2u(query))
	return query


def make_request(url,headers={'User-Agent':'Mozilla/5.0 Chrome/39.0.2171.71 Firefox/33.0'},resp='b',maxr=0):
	try:
		if maxr==0:response=get(url,headers=headers)
		else:response=get(url,headers=headers,max_redirects=maxr)
		if resp=='o':resp=response
		else:
			if resp=='j':resp=response.json
			elif resp=='s':resp=response.status
			elif resp=='u':resp=response.text
			elif resp=='c':resp=response.cookiestring
			else:resp=response.body
			response.close()
	except: 
		mess(u'[COLOR red]Lỗi kết nối tới: %s[/COLOR]'%xshare_group(re.search('//(.+?)/',str2u(url)),1))
		resp='';print 'Make Request Error: %s'%url
	return resp#unicode:body=response.text

def make_post(url,headers={'User-Agent':'Mozilla/5.0 Chrome/39.0.2171.71 Firefox/33.0'},data='',resp='o'):
	try:
		if data:response=post(url=url,headers=headers,data=data)
		else:response=post(url=url,headers=headers)
		if resp=='b':response=response.body
		elif resp=='j':response=response.json
	except:
		mess(u'Post link error: %s'%str2u(url));print 'Post link error: %s'%str2u(url)
		response={} if resp=='j' else ''
	return response

def makerequest(file,string='',attr='r'):
	file=str2u(file)
	if attr=='r':
		try:f=open(file);body=f.read();f.close()
		except:body=''
	else:
		try:f=open(file,attr);f.write(string);f.close();body=string
		except:mess(u'Lỗi ghi file: %s'%str2u(os.path.basename(file)));body=''
	return body

def rename_file(sf,df,kq='ok'):
	try:
		if os.path.isfile(df):os.remove(df)
		os.rename(sf,df)
	except:kq='';pass
	return kq

def download_subs(url):
	response=make_request(url,resp='o');downloaded=''
	if not response or response.status!=200:return
	try:filelength=int(dict(response.getheaders()).get('content-length'))
	except:filelength=10485760
	if filelength<10485760:#size<10MB
		if myaddon.getSetting('autodel_sub')=='true':delete_files(subsfolder)
		filename=urllib.unquote(os.path.basename(url));delete_files(tempfolder)
		subfile=joinpath(tempfolder,re.sub('\[.+?\]','',filename))
		if makerequest(subfile,string=response.body,attr="wb"):
			if 	response.body[0] in 'R-P':
				xbmc.sleep(500);f1=subfile.encode('utf-8');f2=tempfolder.encode('utf-8')
				xbmc.executebuiltin('XBMC.Extract("%s","%s")'%(f1,f2),True);os.remove(subfile)
				exts = [".srt", ".sub", ".txt", ".smi", ".ssa", ".ass"];sub_list=[]
				for file in os.listdir(tempfolder):
					tempfile=joinpath(tempfolder,file)
					if os.path.isfile(tempfile) and os.path.splitext(tempfile)[1] in exts:
						if re.search('vietname|vie',filename):
							if rename_file(tempfile,joinpath(subsfolder,'Vie.%s'%re.sub(',|"|\'','',file))):
								downloaded='ok'
						elif rename_file(tempfile,joinpath(subsfolder,re.sub(',|"|\'','',file))):downloaded='ok'
			elif rename_file(subfile,joinpath(subsfolder,'Vie.%s'%re.sub('\[.+?\]','',filename))):downloaded='ok'
		else:mess(u'Lỗi download sub')
		#if downloaded:mess(u'Đã download sub vào Subsfolder')
	else:mess(u'Oh! Sorry. [COLOR red]Không chơi được file rar[/COLOR]')
	return downloaded

def get_input(title=u"", default=u""):
	result = ''
	keyboard = xbmc.Keyboard(default, title)
	keyboard.doModal()
	if keyboard.isConfirmed():
		result = keyboard.getText()
	return result


def check_media_ext(direct_link,srv):
	check=True;message='sorry! this is not a media file'
	sub_ext=['rar','zip','srt','sub','txt','smi','ssa','ass','nfo']
	file_ext=os.path.splitext(direct_link)[1][1:].lower()
	if 'fshare.vn' in direct_link and file_ext not in media_ext:
		if file_ext in sub_ext:download_subs(direct_link)
		else:mess(message)
		check=False
	elif '4share.vn' in direct_link and os.path.splitext(srv)[1][1:].lower() not in media_ext:
		if os.path.splitext(srv)[1][1:].lower() in sub_ext:
			download_subs(direct_link)
		else:mess(message)
		check=False
	return check


def trangtiep(query,items):
	if 'Trang' in query.split('?')[0]:
		trang=int(query.split('?')[0].split('Trang')[1])
		query=query.split('?')[1]
	else:trang=1
	del items[0:(trang-1)*rows]
	trang+=1
	return trang,query,items


def google_search_api(url,start,string,items):#url:fshare.vn,4share.vn,tenlua.vn,hdvietnam.com
	string_search = urllib.quote_plus('"%s"'%string)
	href = 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&rsz=large&'
	href+='start=%s&q=site:%s+%s'%(start,url.lower(),string_search)
	json=make_request(href,resp='j')
	if not json:mess(u'Lỗi get %s'%str2u(href));return items,'end'
	if json['responseStatus']!=200:
		mess(u'Google: nghi ngờ lạm dụng Dịch vụ. Tự động chuyển sang web search',2000)
		return google_search_web(url,start+'xshare',string,items)
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
	if page==0:make_mySearch('',url,'','',mode,'get')
	elif page==1:
		query=make_mySearch('',url,'','','','Input')
		return google_search(url,query,mode,page=4) if query else 'no'
	else:
		query=no_accent(query);tempurl=[];templink=[]
		if '?' in query:
			start=query.split('?')[1];query=query.split('?')[0]
		else:start='0'
		if googlesearch=='Web' or 'xshare' in start:items,start=google_search_web(url,start,query,items)
		else:items,start=google_search_api(url,start,query,items)
		if not items:return 'no'
		for name,link in sorted(items,key=lambda l:l[0]):
			if link in templink:continue
			if url=='hdvietnam.com':tempurl=hdvn_get_link(link,temp=tempurl)
			elif url=='vaphim.com':tempurl=google_vaphim(link,temp=tempurl)
			elif url=='ifile.tv':tempurl=google_ifile(link,name,temp=tempurl)
			elif url=='4share.vn' and 'docs.4share' not in link:tempurl=doc_Trang4share(link,temp=tempurl)
			else:addirs(name,link,icon[srv])
			templink.append(link)
		if start!='end':
			name=color['trangtiep']+'Trang tiep theo...trang %s[/COLOR]'%str(page-2)
			addir(name,url,icon[srv],mode=mode,query='%s?%s'%(query,start),page=page+1,isFolder=True)
	return ''

def google_search_web(url,start,query,items):
	num='20';google = 'https://www.google.com.vn/search?hl=vi&ie=utf-8&oe=utf-8&num=%s&'%num
	string_search = urllib.quote_plus('"%s"'%query);srv=url.split('.')[0]
	if 'xshare' in start:start=start.replace('xshare','');xshare='yes'
	else:xshare=''
	href=google+'start=%s&q=site:%s+%s'%(start,url.lower(),string_search)
	body=make_request(href)
	if '<TITLE>302 Moved</TITLE>' in body:
		mess(u'Google từ chối dịch vụ do bạn đã truy cập quá nhiều');return items,'end'
	links=re.findall('<a href="(.{,300})" onmousedown=".{,200}">(.{,200})</a></h3>',body)
	for link,name in links:items.append((name,link))
	start=str(int(start)+int(num))
	if 'start=%s'%start not in body:start='end'
	elif 'xshare':start=start+'xshare'
	return items,start

def open_category(query): #category.xml
	pattern='<a server="(.+?)" category="(.+?)" mode="(\d\d)" color="(.*?)" icon="(.*?)">(.+?)</a>'
	items=re.findall(pattern,makerequest(joinpath(data_path,'category.xml')));q='';fanart=home+'/fanart.jpg'
	for server,category,mode,colo,icon,name in items:
		if (server!=query) or (("18" in category) and (myaddon.getSetting('phim18')=="false")):continue
		if query=='VPH' and mode!='10':q='vaphim.xml'
		elif query=='IFI' and mode!='10':q='ifiletv.xml'
		else:q=category
		name='[COLOR '+colo+']'+name+'[/COLOR]';icon=joinpath(iconpath,icon)
		addir(name,category,icon,fanart,mode=int(mode),page=0,query=q,isFolder=(mode!='16'))
	if q=='vaphim.xml':
		body=makerequest(joinpath(datapath,"vp_menu.txt"));icon=joinpath(iconpath,'vaphim.png')
		if not body:mess(u'[COLOR red]Đang update menu...[/COLOR]');vp_make_datanew();return
		for query,name in eval(body):
			if "18" in name and myaddon.getSetting('phim18')=="false":continue
			addir('%s%s[/COLOR]'%(color['vaphim'],name),'vaphim.xml',icon,fanart,92,1,query,True)

def main_menu(category,page,mode,query): #Doc list tu vaphim.xml hoac ifiletv.xml
	items = doc_xml(joinpath(datapath,query),para=category);pages=len(items)/rows+1
	del items[0:page*rows];count=0;down=len(items)
	for id,img,fanart,href,name in items:
		down-=1;addirs(name,href,img,fanart);count+=1
		if count>rows and down>10:break
	if down>10:
		page+=1;name=color['trangtiep']+'Trang tiep theo...trang %d/%d[/COLOR]'%(page+1,pages)
		addir(name,category,icon['icon'],mode=mode,page=page,query=query,isFolder=True)

def update_xml(items_new,items_old,filename): #update vaphim,ifiletv xml
	try:items = sorted(items_new+items_old,key=lambda l:int(l[1]),reverse=True)
	except:items = items_new+items_old
	contents='<?xml version="1.0" encoding="utf-8">\n'
	for id_tip,id_htm,category,img,fanart,href,fullname in items:
		content='<a id_tip="%s" id="%s" category="%s" img="%s" fanart="%s" href="%s">%s</a>\n'
		content=content%(id_tip,id_htm,category,img,fanart,href,fullname);contents+=content
	if makerequest(joinpath(datapath,filename),string=contents,attr='w'):
		mess(u'Đã cập nhật được %d phim'%len(items_new),2000,'[COLOR blue]%s auto update[/COLOR]'%filename)
	else: mess(u'Đã xảy ra lỗi cập nhật')
	return
		
def doc_list_xml(url,filename='',page=0):
	if not page:
		items=doc_xml(url,filename=filename)
		makerequest(joinpath(data_path,'temp.txt'),string=str(items),attr='w')
	else:f=open(joinpath(data_path,'temp.txt'));items=eval(f.readlines()[0]);f.close()
	pages=len(items)/rows+1
	del items[0:page*rows];count=0
	for id,href,img,fanart,name in items:
		if '47daklak.com' in href: addir(name,href,img,mode=47)
		else: addirs(name,href,img,fanart)
		count+=1
		if count>rows and len(items)>(rows+10):break
	if len(items)>(rows+10):
		page+=1;name=color['trangtiep']+'Trang tiep theo...trang %d/%d[/COLOR]'%(page+1,pages)
		addir(name,url,iconpath+'khophim.png',mode=97,page=page,isFolder=True)

def doc_xml(url,filename='',para=''): 
	if (datapath in url) or (myfolder in str2u(url)):body=makerequest(url)
	else:body=make_request(resolve_url(url,xml=True))

	if ('vaphim' in url) or ('ifiletv' in url) or ('phimfshare' in url) or ('hdvietnam' in url):
		if para and para[:6]=='search':
			string=para[7:].replace('(','.').replace(')','.')
			if ('phimfshare' in url) or ('hdvietnam' in url):
				r='href="(.+?)" img="(.+?)">(.*%s.*)</a>'%string
				items=[(s[1],s[1],s[0],s[2]) for s in re.findall(r,no_accent(body),re.IGNORECASE)]
			else:
				r='img="(.*?)" fanart="(.*?)" href="(.+?)">(.*%s.*)</a>'%string
				items=re.compile(r, re.I).findall(no_accent(body))
		else:
			if not para:r='<a id_tip="(.*?)" id="(.+?)" category="(.*?)" img="(.*?)" fanart="(.*?)" href="(.+?)">(.+?)</a>'
			else: #Doc theo category
				r='<a.*id="(.+?)" category=".*%s.*" img="(.*?)" fanart="(.*?)" href="(.+?)">(.+?)</a>'%para
			items = sorted(re.findall(r,body),key=lambda l:l[0], reverse=True)
	else:#Doc cac list xml khac
		r='<a.+id="(.*?)".+href="(.+?)".+img="(.*?)".+fanart="(.*?)".*>(.+?)</a>'
		items = re.compile(r).findall(body)
		if len(items)<1:items = re.findall('.+()href="(.+?)".+img="(.*?)".*()>(.+?)</a>',body)
		if len(items)<1:items = re.findall('.+()href="(.+?)".*()()>(.+?)</a>',body)
		if (myaddon.getSetting('copyxml')=="true") and ('http' in url) and (len(items)>0) :
			filename=re.sub('\.xml.*','.xml',filename.replace('[COLOR orange]List xml[/COLOR]-',''))
			filename=re.sub('\[.{1,10}\]','',filename);f_fullpath=joinpath(myfolder,filename)
			if not os.path.isfile(f_fullpath):
				string='<?xml version="1.0" encoding="utf-8">\n'
				for id,href,img,fanart,name in items:
					string+='<a id="%s" href="%s" img="%s" fanart="%s">%s</a>\n'%(id,href,img,fanart,name)
				if makerequest(f_fullpath,string=string,attr='w'):
					mess(u'Đã tải file %s vào MyFolder'%str2u(filename))
	return items

def play_maxspeed_link(url):
	if not url or url=='Maxlink':
		query=get_input('Hãy nhập max speed link của Fshare, 4share hoặc tênlửa')
		if query is None or query=='':return 'no'
		url=query.replace(' ','');print url
	elif len(url)<13:
		fsend=getFsend(url)
		if fsend:url=fsend[0][1]
		else:mess(u'[COLOR red]Lỗi get Fsend[/COLOR]');return
	if check_media_ext(url,'fshare.vn'):xbmcsetResolvedUrl(url,'Maxlink')
	return ''

def read_all_filexml(fn="vaphim.xml",string_search='',lists=[],index=[]):
	if string_search:lists=lists+doc_xml(joinpath(datapath,fn),para='search:'+string_search)
	else:lists=lists+doc_xml(joinpath(datapath,fn))
	if not string_search:
		for id_tip,id_htm,category,img,fanart,url,name in lists:index.append((id_htm))
	return lists,index

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


def subtitle_of_year(title):
	string=xshare_group(re.search('(.+?20\d\d|.+?19\d\d)',title),1)
	string=re.sub(xshare_group(re.search('multi ',string,re.IGNORECASE),0),'',string)
	return string if string else title

def data_download():
	delete_files(tempfolder);init_file();download=downloadresult=''
	if os.path.isfile(joinpath(data_path,'htvonline.png')):
		rename_file(joinpath(data_path,'htvonline.png'),joinpath(iconpath,'htvonline.png'))
	#Kiểm tra database
	files=['hdvietnam.xml','ifiletv.xml','phimfshare.xml','vaphim.xml']
	file_now=os.listdir(datapath)
	for file in files:
		if file not in file_now:download='download';break
	if not download:
		for file in file_now:
			size=os.path.getsize(joinpath(datapath,file))
			if file.lower()=='vaphim.xml' and size<4218000:download='download';break
			if file.lower()=='ifiletv.xml' and size<2611000:download='download';break
			if file.lower()=='hdvietnam.xml' and size<630000:download='download';break
			if file.lower()=='phimfshare.xml' and size<629000:download='download';break
	if download=='download':
		mess(u'Đang download database cho xshare')
		if data_download_fromFshare('data.zip','data-hot.zip'):downloadresult='yes'
	if 'fpt.xml' not in file_now or os.path.getsize(joinpath(datapath,'fpt.xml'))<22345000:
		if data_download_fromFshare('fpt.zip','fpt-hot.zip'):downloadresult='yes'
	#Kiểm tra file fanart
	file=joinpath(home,'fanart.jpg')
	if (os.path.isfile(file) and os.path.getsize(file)<613860) or not os.path.isfile(file):
		if data_download_fromFshare('fanart.jpg','fanart-hot.jpg'):downloadresult='yes'
	#Kiểm tra bộ icon
	files=['4share.png','dangcaphd.png','downsub.png','favorite.png','fptplay.png','fshare.png','gsearch.png','hdvietnam.png','icon.png','id.png','ifiletv.png','isearch.png','khophim.png','maxspeed.png','megabox.png','movie.png','msearch.png','myfolder.png','myfshare.png','phimfs.png','serverphimkhac.png','setting.png','tenlua.png','vaphim.png','xshare.png']
	file_now=os.listdir(iconpath);download=''
	for file in files:
		if file not in file_now:download='download';break
	if download=='download':
		mess(u'Đang download bộ icon của LUC QUYET CHIEN cho xshare')
		if data_download_fromFshare('icon.zip','icon-hot.zip'):downloadresult='yes'
	
	kq='ok'
	if downloadresult:
		mess(u'Đang unzip......')
		for f in os.listdir(tempfolder):
			file=joinpath(tempfolder,f);ext=os.path.splitext(file)[1][1:].lower()
			if ext=='xml':dest_path=datapath
			elif ext=='png':dest_path=iconpath
			elif ext=='jpg':dest_path=home
			else:continue
			size=os.path.getsize(file);dest_file=joinpath(dest_path,f)
			if not os.path.isfile(dest_file) or os.path.getsize(dest_file)<size:
				if not rename_file(file,dest_file):kq=''
	if downloadresult and kq:mess(u'Download database cho xshare thành công!',10000)
	elif downloadresult:mess(u'Download database cho xshare thất bại!',10000)
	else:mess(u'Đã kiểm tra database cho xshare thành công!',10000)
	if kq:
		myaddon.setSetting('thank2xshare','true');myaddon.setSetting('checkdatabase','false')
		if os.path.isfile(joinpath(data_path,'checkdatabase.txt')):os.remove(joinpath(data_path,'checkdatabase.txt'))
		delete_files(tempfolder)
	return

def data_update():
	ngay=datetime.date.today().strftime("%Y%m%d");gio=datetime.datetime.now().strftime("%H")
	file=joinpath(datapath,"last_update.dat")
	last_update=datetime.datetime.fromtimestamp(os.path.getmtime(file) if os.path.isfile(file) else 0)
	if ngay>last_update.strftime("%Y%m%d"):
		makerequest(joinpath(datapath,"last_update.dat"),'','w');delete_files(tempfolder)
		try:vp_update();ifile_update();vp_make_datanew()
		except:pass
	if abs(int(gio)-int(last_update.strftime("%H")))>2:
		makerequest(joinpath(datapath,"last_update.dat"),'','w')
		try:hdvn_update();pfs_update()#;vp_update_rss()
		except:pass

def subscene(name,url,query):#,img='',fanart='',query=''
	if query=='subscene.com':
		href = get_input('Hãy nhập link của sub trên subscene.com','http://subscene.com/subtitles/')
		if href is None or href=='' or href=='http://subscene.com/subtitles/':return 'no'
	else:href=url
	if not re.search('\d{5,10}',href):
		if not os.path.basename(href):href=os.path.dirname(href)
		pattern='<a href="(/subtitles/.+?)">\s+<span class=".+?">\s*(.+?)\s+</span>\s+<span>\s+(.+?)\s+</span>'
		subs=re.findall(pattern,make_request(href,headers={'Cookie':'LanguageFilter=13,45'}))
		mess(u'Tên phim: %s'%str2u(name).replace('[COLOR green]Subscene[/COLOR]-',''),30000)
		for url,lang,name in sorted(subs,key=lambda l:l[1], reverse=True):
			name='Eng '+name if '/english/' in url else '[COLOR red]Vie[/COLOR]-'+name
			addirs(name,'http://subscene.com'+url,query='download')
		return ''
	pattern='<a href="(.+?)" rel="nofollow" onclick="DownloadSubtitle.+">'
	downloadlink='http://subscene.com' + xshare_group(re.search(pattern,make_request(href)),1)
	if len(downloadlink)<20:mess(u'Không tìm được maxspeed link sub');return
		
	if myaddon.getSetting('autodel_sub')=='true':delete_files(subsfolder)
	body=make_request(downloadlink);tempfile=joinpath(tempfolder,"subtitle.sub");delete_files(tempfolder)
	body=makerequest(tempfile,string=body,attr='wb')
	if body[0]=='R':typeid="rar"
	elif body[0]=='P':typeid="zip"
	else:typeid="srt"
	
	folder=tempfolder if typeid in "rar-zip" else subsfolder
	subfile=joinpath(folder,"subtitle."+typeid);rename_file(tempfile,subfile)
	
	if typeid in "rar-zip":
		f1=subfile.encode('utf-8');f2=tempfolder.encode('utf-8')
		xbmc.sleep(500)
		xbmc.executebuiltin('XBMC.Extract("%s","%s")'%(f1,f2),True);os.remove(subfile)
		exts = [".srt", ".sub", ".txt", ".smi", ".ssa", ".ass"];sub_list=[]
		for file in os.listdir(tempfolder):
			tempfile=joinpath(tempfolder,file)
			if os.path.isfile(tempfile) and os.path.splitext(tempfile)[1] in exts:
				if 'Eng' in name and myaddon.getSetting('autotrans_sub')=='true':
					mess(u'Google đang dịch sub từ tiếng Anh sang tiếng Việt', timeShown=20000)
					subfile=xshare_trans(tempfile)
					if rename_file(subfile,joinpath(subsfolder,'Vie.%s'%re.sub(',|"|\'','',file))):
						mess(u'Đã dịch xong sub từ tiếng Anh sang tiếng Việt');os.remove(tempfile)
					elif rename_file(tempfile,joinpath(subsfolder,'Eng.%s'%re.sub(',|"|\'','',file))):
						mess(u'Không dịch được sub, giữ nguyên bản tiếng Anh') 
				elif 'Eng' in name and rename_file(tempfile,joinpath(subsfolder,'Eng.%s'%re.sub(',|"|\'','',file))):
					mess(u'Đã download sub vào Subsfolder') 
				elif rename_file(tempfile,joinpath(subsfolder,'Vie.%s'%re.sub(',|"|\'','',file))):
					mess(u'Đã download sub vào Subsfolder') 
	return 'ok'

def xshare_trans(sourcefile):
	tempfile = joinpath(tempfolder,"temp"+os.path.splitext(sourcefile)[1])
	fs=open(sourcefile);ft=open(tempfile,'w');lineslist=[];substring=''
	for line in fs:
		if re.search('[a-zA-Z]',line):
			substring+='+'.join(''.join(re.split('<.+?>',line.replace('"',''))).strip().split())+'+xshare+'
			lineslist.append('xshare')
		else:
			lineslist.append(line.strip()+'\n')
			if len(substring)>1500:
				write_trans(ft,substring,lineslist)
				substring='';lineslist=[]
	if len(substring)>0:write_trans(ft,substring,lineslist)
	fs.close();ft.close()
	return tempfile

def write_trans(fo,string,m):
	translist=google_trans(string);j=0
	for i in m:
		if i=='xshare':
			try:fo.write(translist[j].strip()+'\n');j+=1
			except:pass
		else:fo.write(i)

def google_trans(s):
	hd={'User-Agent':'Mozilla/5.0','Accept-Language':'en-US,en;q=0.8,vi;q=0.6','Cookie':''}
	url='https://translate.google.com.vn/translate_a/single?oe=UTF-8&tl=vi&client=t&hl=vi&sl=en&dt=t&ie=UTF-8&q=%s'%s
	body= make_request(url,headers=hd)
	body=body.replace(',,"en"','').replace('[[[','').replace(']]]','')
	result=''
	for i in body.split('],['):
		research=xshare_group(re.search('"(.+?)","(.+?)"',i),1)
		if research:result+=research+' '
		else:print '%s :not research'%i
	return result.replace('Xshare','xshare').split('xshare')

def fptplay(name,url,img,mode,page,query):
	def fpt2s(string):
		return ' '.join(re.sub('&.+;',xsearch('&(\w).+;',s,1),s) for s in string.split())
	def login():
		email=myaddon.getSetting('mail_fptplay');password=myaddon.getSetting('pass_fptplay')
		response=make_request('http://fptplay.net/user/login',headers=hd,resp='o',maxr=3)
		body=response.body;pattern='<input.+?value="(.+?)"><input.+?value="(.+?)">'
		csrf_token=xsearch(pattern,body,1);next=xsearch(pattern,body,2)
		data={'csrf_token':csrf_token,'next':next,'email':email,'password':password,'submit':'Đăng nhập'}
		hd['Cookie']=response.cookiestring
		response=make_post('https://moid.fptplay.net/',headers=hd,data=urllib.urlencode(data))
		hd['Cookie']=response.cookiestring;url='https://moid.fptplay.net/oauth2/authorize'
		if response.status==302:
			client_id=xsearch('client_id=(.+?)&',response.headers['location'],1)
			data={'client_id':client_id,'scope':'email','response_type':'code','confirm':'yes'}
			response=make_post(url,headers=hd,data=urllib.urlencode(data))
			if response.status==302:response=make_request(response.headers['location'],headers=hd,resp='o')
		if 'laravel_value' in response.cookiestring:
			#mess(u'[COLOR green]Login fptplay.net thành công[/COLOR]');f=response.cookiestring
			makerequest(joinpath(datapath,'fptplay.cookie'),f,'w')
		else:f=''
		#get('https://fptplay.net/user/logout',headers=hd) status=302
		return f
	def colors(name,title):
		name=name.strip()+' '+title.strip()
		if 'Thuyết Minh' in name:name='[COLOR gold]TM[/COLOR] '+name
		elif 'Phụ Đề' in name:name='[COLOR green]PĐ[/COLOR] '+name
		elif 'Trailer' in name:name=name+' [COLOR red](Trailer)[/COLOR]'
		return name
	def getlinklivetv(id,headers='',href=''):
		headers['X-Requested-With']='XMLHttpRequest';headers['Referer']='http://fptplay.net/livetv'
		for quality in [3,2,1]:
			url='http://fptplay.net/show/getlinklivetv/?id=%s&quality=%d&mobile=web'%(id,quality)
			response=make_post(url,headers=headers)
			try:href=response.json['stream'];break
			except:
				try:
					if response.json['msg_code']=='login':href='login';break
				except:pass
		if not href:
			try:href=response.json['msg_code']
			except:href='Getting error'
		return href
	def getlink(id,name,url=''):
		hd['X-Requested-With']='XMLHttpRequest';hd['Referer']=url
		json=make_post('http://fptplay.net/show/getlink?id=%s&episode=1&mobile=web'%id,headers=hd,resp='j')
		if not json:return list()
		id=json.get('_id').encode('utf-8');items=list()
		for i in json.get('quality'):
			title=i['title'].encode('utf-8');img=i['thumb'].encode('utf-8')
			href=i['url'][0]['url'].encode('utf-8')
			items.append((id,href,img,title,name))
		return items
	def getdir(items,name,url=''):#id,img,title   name
		ids=[s[0] for s in items]
		if not items:mess(u'[COLOR red]Không get được data từ fptplay.net[/COLOR]');return 'no'
		pattern='<div id="(.+?)" name="(.+?)">(.+?)</div>'
		hrefs=[s for s in re.findall(pattern,makerequest(joinpath(datapath,'fpt.xml')),re.DOTALL) if s[0] in ids]
		ids=list(set([s[0] for s in hrefs]));string='';list_update=[]
		if any(s for s in items if s[0] not in ids):
			mess(u'%s [COLOR green]Updating ...[/COLOR]'%str2u(name),5000,'[COLOR orange]FPTPlay database Update[/COLOR]')
		for iD,img,name in items:
			name=fpt2s(name)
			if iD not in ids:
				lists=getlink(iD,name,url);string+='<div id="%s" name="%s">\n'%(iD,name)
				for id,href,thumb,title,name in lists:string+='<a href="%s" img="%s">%s</a>\n'%(href,thumb,title)
				string+='</div>\n'
			else:
				content=''.join(s[2] for s in hrefs if s[0]==iD);lists=[]
				for href,thumb,title in re.findall('<a href="(.+?)" img="(.*?)">(.*?)</a>',content):
					lists.append((iD,href,thumb,title,name))
			if len(lists)>2:
				addir(color['fptplay']+name+'[/COLOR]',iD,img,lists[0][2],mode,page,'folder',True)
			elif len(lists)>0:
				for id,href,thumb,title,name in lists:
					addir(colors(name,title),href,img,thumb,mode,page,'play')
					if re.search('Tập \d{1,2}',title):list_update.append((id,href,name))
		if string:
			makerequest(joinpath(datapath,'fpt.xml'),string,'a')
			mess(u'[COLOR green]FPTPlay database Updated[/COLOR]',1000,'[COLOR orange]FPTPlay database Update[/COLOR]')
		return list_update
	def update_list(items):
		direct_links=[s[1] for s in items];ids=[];string='';lists=[]
		for id,href,name in items:
			if id in ids:continue
			ids.append(id)
			lists=[s for s in getlink(id,name) if s[1] not in direct_links]#id,href,img,title,name
			if lists:
				string+='<div id="%s" name="%s">\n'%(id,name)
				for id,href,thumb,title,name in lists:
					string+='<a href="%s" img="%s">%s</a>\n'%(href,thumb,title)
				string+='</div>\n'
		if string:makerequest(joinpath(datapath,'fpt.xml'),string,'a')
		return True if string else False
	if not os.path.isfile(joinpath(datapath,'fptplay.cookie')):hd['Cookie']=login()
	else:hd['Cookie']=makerequest(joinpath(datapath,'fptplay.cookie'))
	if query=="fptplay.net":
		body=make_request('http://fptplay.net',hd);href='http://fptplay.net/livetv'
		name=color['search']+"Search trên fptplay.net[/COLOR]"
		addir(name,"fptplay.net",icon['fptplay'],mode=mode,query="FPS",isFolder=True)
		addir(color['fptplay']+'Live TV[/COLOR]',href,icon['fptplay'],mode=mode,query='FTV',isFolder=True)
		if not body:return ''
		content=xsearch('"top_menu reponsive"(.+?)"top_listitem"',body,1,re.DOTALL)
		for href,title in re.findall('<li ><a href="(http://fptplay.net/danh-muc/.+?)">(.+?)</a></li>',content):
			title=color['fptplay']+fpt2s(title)+'[/COLOR]'
			addir(title,href,icon['fptplay'],mode=mode,query='FP2',isFolder=True)
		content=xsearch('<ul class="slide_banner">.+?<li>(.+?)</ul>',body,1,re.DOTALL)
		#iD,img,name
		pattern='<li>.+?src="(.+?)\?.+?title="(.+?)".+?-(\w+)\.html'
		items=[(s[2],s[0],s[1]) for s in re.findall(pattern,content,re.DOTALL) if len(s[2])>20]
		ids=[s[0] for s in items]
		content=xsearch('Phổ biến hiện nay</span>(.+?)title="Thể Thao"',body,1,re.DOTALL)
		pattern='<a href=".+?-(\w+)\.html".+?title="(.+?)".+?data-original="(.+?)\?'
		items+=[(s[0],s[2],s[1]) for s in re.findall(pattern,content) if s[0] not in ids]#id,img,title
		list_update=getdir(list(set(items)),'Home page')
		if list_update:endxbmc();update_list(list_update)
	elif query=="FTV":
		body=make_request(url,hd);i=1
		content=xsearch('Begin kenh truyen hinh(.+?)END Tong Hop',body,1,re.DOTALL)
		pattern='<a class=".+?" title="(.+?)".+?href="http://fptplay.net/livetv/(.+?)"(.+?)original="(.+?)\?.+?"'
		for name,href,lock,img in re.findall(pattern,content,re.DOTALL):
			j='00%d '%i if i<10 else '0%d '%i if i<100 else '%d '%i;name=j+fpt2s(name);i+=1
			if '"lock"' in lock:name=name+' ([COLOR red]Có phí[/COLOR])'
			addir(name,href,img,mode=mode,query="PTV")
	elif query=="PTV":
		href=getlinklivetv(url,hd)
		if 'm3u8' in href:xbmcsetResolvedUrl(href)
		elif href=='login':
			href=getlinklivetv(url,hd)
			if 'm3u8' in href:xbmcsetResolvedUrl(href)
			else:hd['Cookie']=login();href=getlinklivetv(url,hd)
			if 'm3u8' in href:xbmcsetResolvedUrl(href)
			else:mess(u'[COLOR red]%s[/COLOR]'%href,title='Fptplay LiveTV')
		else:mess(u'[COLOR red]%s[/COLOR]'%href,title='Fptplay LiveTV')
	elif query=="FPS":make_mySearch('',url,'','',mode,'get')
	elif query=="INP":
		query=make_mySearch('',url,'','','','Input')
		if query:return fptplay(name,url,img,mode,page,query)
		else:return 'no'
	elif url=="fptplay.net":
		search_string = urllib.quote(query)
		url='http://fptplay.net/show/more?type=search&stucture_id=key&page=1&keyword=%s'%search_string
		print url
		return fptplay(name,url,img,mode,page,query='FP3')
	elif query=="FP2":
		body=make_request(url,hd);pattern='<a href="(http://fptplay.net/the-loai/.+?)" title="(.+?)"';temp=[]
		for href,title in re.findall(pattern,body):
			if href in temp:continue
			temp.append(href)
			title=color['fptplay']+fpt2s(title)+"[/COLOR]";id=xsearch('(\w{22,26})',href,1)
			data='type=new&keyword=undefined&page=1&stucture_id=%s'%id;url='http://fptplay.net/show/more?%s'%data
			addir(title,url,icon["fptplay"],mode=mode,query="FP3",isFolder=True)
		content=xsearch('<ul class="slide_banner">.+?<li>(.+?)</ul>',body,1,re.DOTALL)
		#iD,img,name
		items=[(s[2],s[0],s[1]) for s in re.findall('src="(.+?)\?.+?title="(.+?)".+?-(\w+)\.html',content,re.DOTALL)]
		list_update=getdir(list(set(items)),name)
		if list_update:endxbmc();update_list(list_update)
	elif query=="FP3":
		body=make_post(url,resp='b')
		if not body:mess(u'[COLOR red]Error get data/not found from fptplay.net[/COLOR]');return 'no'
		items=re.findall('<a href=".+-(\w+)\.html".+?src="(.+?)\?.+?alt="(.+?)"',body)
		list_update=getdir(items,name,url)
		if len(items)>35:
			try:pagenext=str(int(xsearch('page=(\d{1,3})',url,1))+1)
			except:pagenext=''
			url=re.sub('page=\d{1,3}','page=%s'%pagenext,url)
			name=color['trangtiep']+"Trang tiếp theo - Trang %s[/COLOR]"%pagenext
			addir(name,url,icon["fptplay"],mode=mode,query="FP3",isFolder=True)
		if list_update:endxbmc();update_list(list_update)
	elif query=="folder":
		pattern='<div id="%s" name="(.+?)">(.+?)</div>'%url
		hrefs=re.findall(pattern,makerequest(joinpath(datapath,'fpt.xml')),re.DOTALL)
		content=''.join(s[1] for s in hrefs);items=re.findall('<a href="(.+?)" img="(.*?)">(.*?)</a>',content)
		for href,thumb,title in items:
			addir(colors(title,hrefs[0][0]),href,img,thumb,mode,page,'play')
		endxbmc()# Update 1 folder
		if update_list([(url,s[0],hrefs[0][0]) for s in items]):xbmc.executebuiltin("Container.Refresh")
	elif query=='play':xbmcsetResolvedUrl(url)
	return ''

def xsearch(pattern,string,group,flags=0):
	research=re.search(pattern,string,flags)
	if research:
		try:result=research.group(group)
		except:result=''
	else:result=''
	return result

def checkupdate(filename,folder=datapath):
	filecheck=joinpath(folder,filename)
	filetime=os.path.getmtime(filecheck) if os.path.isfile(filecheck) else 0
	last_update=datetime.datetime.fromtimestamp(filetime);timeformat='%Y%m%d%H'
	return int(datetime.datetime.now().strftime(timeformat))-int(last_update.strftime(timeformat))

def megabox(name,url,img,fanart,mode,page,query):
	home='http://phim.megabox.vn/'
	cat={1:'Phim lẻ',2:'Phim bộ',3:'Show',4:'Clip'}
	gen={1:'Hành động',2:'Phiêu lưu',3:'Ma kinh dị',4:'Tình cảm',5:'Hoạt hình',6:'Võ thuật',7:'Hài',8:'Tâm lý',9:'Kiếm hiệp',10:'Sử thi',11:'',12:'',13:'Hình sự',14:'',15:'Âm nhạc',16:'Khoa học',17:'Tài liệu',18:'Gia đình',21:'Chiến tranh',22:'Thể thao',25:'Độc-Lạ',27:'Khoa học viễn tưởng',28:'Ẩm thực',29:'Thời trang',30:'Điện ảnh',31:'Thiếu nhi',32:'Giáo dục',33:'TV-Show',34:'Live Show',36:'Công nghệ',37:'Khám phá thế giới',38:'Động vật',39:'Shock'}
	country={1:'Âu-Mỹ',2:'Hàn Quốc',3:'Hồng Kông',4:'Trung Quốc',5:'Nhật Bản',6:'Thái Lan',7:'Quốc Gia khác',8:'Mỹ',9:'Pháp',11:'Việt Nam',12:'Ấn Độ',13:'Philippines'}#get(url,headers=hd,maxr=2)
	def mes(string):mess(string,title=namecolor('megabox.vn'))
	def namecolor(name):return color['megabox']+name+'[/COLOR]'
	def get_id(url):return xsearch('-(\d{1,6})\.html',url,1)
	def duration(string):return xsearch('Thời lượng:<.+?> (.+?)</li>',string,1)
	def countview(string,tag='span'):return xsearch('class=.count-view.><%s></%s> (.+?)</span>'%(tag,tag),string,1)
	def thuyetminh(string):return color['subscene']+'TM[/COLOR] ' if xsearch('class=.ico-sub.',string,0) or string=='TM' else ''
	def phim18(string):return '[COLOR red][B]M+[/B][/COLOR] ' if xsearch('class=.ico-rating.',string,0) or string=='M+' else ''
	def episode(string):return xsearch('class=.esp.><i>(.+?)</span>',string,1).replace('</i>','')
	def update_dict(dict):
		body=make_request(home,headers=hd)
		#(phim-le,Phim lẻ),(phim-bo,Phim bộ),(show,Show),(clip,Clip)
		dict['MGB1']=re.findall('<li><a href="(.+?)" title="">(.+?)</a></li>',body)
		#(Lẻ Bộ Show Clip Mới Nhất, Chiếu Rạp) (Megabox giới thiệu, Top 10, sắp chiếu, lẻ-bộ-show-clip xem nhiều)
		dict['MGB2']=re.findall('"H2title">(.+?)</h2>',body)
		content=sub_body(body,'id="phimle"','id="phimbo"')
		dict['phim-letl']=re.findall("title='(.+?)'.{1,3}href='(.+?)'",content[:content.find('Quốc gia')])
		dict['phim-leqg']=re.findall("title='(.+?)'.{1,3}href='(.+?)'",content[content.find('Quốc gia'):])
		content=sub_body(body,'id="phimbo"','id="tvshow"')
		dict['phim-boqg']=re.findall("title='(.+?)'.{1,3}href='(.+?)'",content[:content.find('Thể Loại')])
		dict['phim-botl']=re.findall("title='(.+?)'.{1,3}href='(.+?)'",content[content.find('Thể Loại'):])
		content=sub_body(body,'id="tvshow"','id="clip"')
		dict['showtl']=re.findall("title='(.+?)'.{1,3}href='(.+?)'",content[:content.find('Quốc gia')])
		dict['showqg']=re.findall("title='(.+?)'.{1,3}href='(.+?)'",content[content.find('Quốc gia'):])
		content=sub_body(body,'id="clip"','class="search-toogle"')
		dict['cliptl']=re.findall("title='(.+?)'.{1,3}href='(.+?)'",content)
		dict['gioithieu']=re.findall("<li><a href='(.+?)'",sub_body(body,'class="hotFilmSlider"','id="bx-pager"'))
		dict['top10']=re.findall('href="(.+?)"',sub_body(body,'begin topFilm','end topFilm'))
		dict['sapchieu']=re.findall("<a href='(.+?)'>",sub_body(body,'Phim sắp chiếu','end primary'))
		for i in range(1,5):
			s1='id="subCate-%d"'%i;s2='id="ul-%d"'%i
			dict['subCate%d'%i]=re.findall('data=.(.+?). data1=.(.+?).>(.+?)</a>',sub_body(body,s1,s2))
		return json_rw(dict)
	def get_detail(urls,dict):
		#mes('[COLOR green]Xshare database updating ...[/COLOR]')
		for url in urls:
			id=get_id(url);body=sub_body(make_request(url,maxr=3),'begin primary','end primary');tm='TM' if thuyetminh(body) else ''
			views=countview(body);esp=xsearch('Số tập <i>(.+?)</i>',body,1);p18='M+' if phim18(body) else ''
			items=re.findall('alt=\'(.+?)\' src="(.+?)"',body)
			if not items:continue
			elif len(items)==1:title=items[0][0];fanart=img=items[0][1]
			else:title=items[0][0];fanart=items[0][1];img=items[1][1]
			if esp:series='y'
			else:series='n';esp=duration(body)
			dict[id]=(series,title,img,fanart,views,esp,tm,p18)
		return dict
	def json_rw(dicts={}):
		if dicts:makerequest(joinpath(datapath,'megabox.json'),json.dumps(dicts),'w')
		else:
			try:dicts=json.loads(makerequest(joinpath(datapath,'megabox.json')))
			except:dicts={}
		return dicts
	def load_urls(urls):
		dict=json_rw();urls_old=[];urls_new=[];ids=[];update=False
		for url in urls:
			id=get_id(url)
			if not id:continue
			elif dict.has_key(id) and dict[id]:urls_old.append(url)
			else:urls_new.append(url)
			ids.append((id,url))
		if urls_new:dict=get_detail(urls_new,dict)
		for id,url in ids:
			try:tm=thuyetminh(dict[id][6])+phim18(dict[id][7])
			except:tm=''
			img=dict[id][2];fanart=dict[id][3]
			if dict[id][0]=='y':
				epi=xsearch('(.+?)\W(.*?)\Z',dict[id][5],1);eps=xsearch('(.+?)\W(.*?)\Z',dict[id][5],2)
				title=namecolor(dict[id][1])+color['subscene'];query='1episode'+eps;isFolder=True
				title=title+' - %s views:%s[/COLOR]'%(dict[id][5],dict[id][4])
			else:
				title=dict[id][1]+color['subscene']+' - (%s - views:%s)[/COLOR]'%(dict[id][5],dict[id][4].strip())
				query='mgbplay';isFolder=False
			addir(tm+title,url,img,fanart,mode,1,query,isFolder=isFolder)
		if urls_new:endxbmc();json_rw(get_detail(urls_old,dict));#mes('[COLOR lime]Xshare database updated[/COLOR]')
	def put_items(items,tag='span'):#class='count-view'><span></span> 551</span>
		dict=json_rw();cl=color['subscene']
		href_old=[s[0] for s in items if get_id(s[0]) in dict]
		href_new=[s[0] for s in items if s[0] not in href_old]
		for href,name,dura,img,esp,view in items:
			id=get_id(href);views=countview(view,tag);dura=duration(dura)
			tm=thuyetminh(esp)+phim18(esp);esp=episode(esp);eps=xsearch('\W(.*)\Z',esp,1)
			if esp:title,query,series,isFolder=namecolor(name),'1episode'+eps,'y',True
			else:title,esp,query,series,isFolder=name,dura,'mgbplay','n',False
			title=tm+title+' %s%s views: %s[/COLOR]'%(cl,esp,views)
			try:fanart=dict[id][3] if href in href_old else img
			except:fanart=img
			p18='M+' if 'M+' in tm else '';tm='TM' if 'TM' in tm else ''
			dict[id]=(series,name,img,fanart,views,esp,tm,p18)
			addir(title,href,img,fanart,mode,1,query,isFolder)
		return href_new,dict
	def update_href_new(hrefs,dict):
		#mes('[COLOR green]Xshare database updating ...[/COLOR]')
		for href in href_new:
			id=get_id(href);body=sub_body(make_request(href,maxr=3),'begin primary','end primary')
			items=re.findall('alt=\'(.+?)\' src="(.+?)"',body)
			if len(items)<2:continue
			series,name,img,fanart,views,esp,tm,p18=dict[id];fanart=items[0][1];img=items[1][1]
			dict[id]=(series,name,img,fanart,views,esp,tm,p18)
		json_rw(dict);#mes('[COLOR lime]Xshare database updated[/COLOR]')
	
	if query=='megabox.vn':make_mySearch('',url,'','',mode,'get')
	elif query=="INP":
		query=make_mySearch('',url,'','','','Input')
		if query:return megabox(query,url,img,fanart,mode,page,query)
		else:return 'no'
	elif query==name:#Search in megabox.vn
		search_string = urllib.quote_plus(query)
		body=make_post('http://phim.megabox.vn/tim-kiem?keyword=%s'%search_string).body
		body=sub_body(body,'class="item"','id="footer"')
		patt='<a class.+?href="(.+?)".+?title.>(.+?)</h3>(.+?)<img.+?src="(.+?)"(.+?)</a>.+?<a.+?a>(.+?)</div></div>'
		put_items(re.findall(patt,body,re.DOTALL))
	elif query=='MGB':
		dict=json_rw()
		if not dict.get('MGB1'):dict=update_dict(dict)
		name=color['search']+"Search trên megabox.vn[/COLOR]"
		addir(name,'megabox.vn',icon['megabox'],'',mode,1,'megabox.vn',True)
		for href,name in dict['MGB1']:#(phim-le,Phim lẻ),(phim-bo,Phim bộ),(show,Show),(clip,Clip)
			addir(color['megabox']+name+'[/COLOR]',href,icon['megabox'],'',mode,1,'mainmenu',True)
		for name in dict['MGB2']:
			if isinstance(name,unicode):name=name.encode('utf-8')
			result=re.search('href="(.+?)">(.+?)</a>',name)
			if result:#Lẻ Bộ Show Clip Mới Nhất, Chiếu Rạp
				title=namecolor(result.group(2));href=result.group(1)
				addir(title,href,icon['megabox'],'',mode,1,'subCate',True)
			else:#Megabox giới thiệu, Top 10, sắp chiếu, lẻ-bộ-show-clip xem nhiều
				title=namecolor(re.sub('<.+?>','',name+' trong ngày' if 'xem' in name else name))
				addir(title,home,icon['megabox'],'',mode,1,'xemnhieu',True)
		if checkupdate('megabox.json')>8:dict=update_dict(dict)
	elif query=='mainmenu' and url in ('phim-letl','phim-leqg','phim-botl','phim-boqg','showtl','showqg','cliptl'):
		dict=json_rw()
		for title,href in dict[url]:
			title=color['megabox']+title.replace('Phim ','')+'[/COLOR]'
			addir(title,href,icon['megabox'],'',mode,1,'mainmenu',True)
	elif query=='mainmenu':#url:(phim-le,phim-bo,show,clip)
		submenu={'phim-le':'Phim lẻ','phim-bo':'Phim bộ','show':'Show','clip':'Clip'}
		if url=='clip':
			title=color['xshare']+submenu[url]+' theo thể loại[/COLOR]'
			addir(title,url+'tl',icon['megabox'],'',mode,1,query,True)
		elif url in ('phim-le','phim-bo','show'):
			title=color['xshare']+submenu[url]+' theo thể loại[/COLOR]'
			addir(title,url+'tl',icon['megabox'],'',mode,1,query,True)
			title=color['xshare']+submenu[url]+' theo quốc gia[/COLOR]'
			addir(title,url+'qg',icon['megabox'],'',mode,1,query,True)
		pattern='<a class.+?href="(.+?)".+?title.>(.+?)</h3>(.+?)<img.+?src="(.+?)">(.+?)</a>.+?<a.+?a>(.+?)</div><'
		body=sub_body(make_request(home+url,maxr=3),'begin primary','end primary')
		href_new,dict=put_items(re.findall(pattern,body,re.DOTALL),'i')
		url_next=xsearch('<li class="next"><a href="(.+?)">',body,1)
		if url_next:
			page_end=xsearch('<span></span>Trang.{1,10}/(\d{1,3})</div>',body,1)
			page_next=xsearch('trang-(.+)\Z',url_next,1)
			name=color['trangtiep']+'Trang tiếp theo: trang %s/%s[/COLOR]'%(page_next,page_end)
			addir(name,url_next,icon['megabox'],'',mode,1,query,True)
		if href_new:endxbmc();update_href_new(href_new,dict)
	elif query=='mgbplay':
		url='/'.join((os.path.dirname(url),urllib.quote(os.path.basename(url))))
		body=make_request(url,resp='o',maxr=5);link=xsearch("changeStreamUrl\('(.+?)'\)",body.body,1)
		if not link:play_youtube(xsearch("\'(https://www.youtube.com/watch\?v=.+?)\'",body.body,1));return
		hd['Cookie']=body.cookiestring
		maxspeedlink=make_post('http://phim.megabox.vn/content/get_link_video_lab',data={"link":"%s"%link},resp='j')
		if maxspeedlink.get('link'):
			name=re.sub(' \[COLOR.+?/COLOR\]','',name)
			xbmcsetResolvedUrl(maxspeedlink.get('link')+'|'+urllib.urlencode(hd),name+'Maxlink')
		else:mes('[COLOR red]Get maxspeed link thất bại[/COLOR]')
	elif 'episode' in query:
		art=fanart.split('/banner/')[0] if fanart!=fanart.split('/banner/')[0] else ''
		href=os.path.dirname(url);id=get_id(url)
		start=query.split('episode')[0];eps=query.split('episode')[1]
		try: eps=int(eps)
		except:eps=int(xsearch('(\d{1,4})/\?',name,1) if xsearch('(\d{1,4})/\?',name,1) else '1')
		for epi in make_request('http://phim.megabox.vn/content/ajax_episode?id=%s&start=%s'%(id,start),resp='j'):
			name=epi['name'];href='%s/%s-%s.html'%(href,epi['cat_id'],epi['content_id'])
			if not art:fanart='http://img.phim.megabox.vn/300x168'+epi['image_banner']
			else:fanart=art+epi['image_banner']
			addir(name,href,img,fanart,mode,1,'mgbplay')
		if int(start)+30<eps:
			name=color['trangtiep']+u'Các tập tiếp theo: %d-%d[/COLOR]'%(int(start)+30,eps)
			addir(name,url,img,fanart,mode,1,'%depisode%d'%(int(start)+30,eps),True)
	elif 'Megabox giới thiệu' in name:dict=json_rw();load_urls(dict['gioithieu'])
	elif 'Top 10 phim trong ngày' in name:dict=json_rw();load_urls(dict['top10'])
	elif 'Phim sắp chiếu' in name:dict=json_rw();load_urls(dict['sapchieu'])
	elif query=='xemnhieu':#lẻ-bộ-show-clip xem nhiều
		cats={'lẻ':1,'bộ':2,'show':3,'clip':4};cat=[cats[s] for s in cats if s in name][0]
		href='http://phim.megabox.vn/mostviewed/ajax/?cat=%d&period=%d'
		period=[('ngày',1),('tuần',2),('tháng',3)];per=[s[0] for s in period if s[0] in name][0]
		for pe in period:
			if pe[0]==per:href=href%(cat,pe[1]);continue
			title=color['xshare']+re.sub('\[.?COLOR.*?\]','',name).replace(per,pe[0])+'[/COLOR]'
			addir(title,url,icon['megabox'],'',mode,1,query,True)
		load_urls(re.findall('<a href="(.+?)">',make_request(href,hd)))
	elif 'Phim Chiếu Rạp' in name or query=='phim-chieu-rap':
		href='http://phim.megabox.vn/t/phim-chieu-rap-29/phim-le/trang-%d'
		body=sub_body(make_request(href%page,maxr=3),'begin main','end main')
		pattern='<a class.+?href="(.+?)".+?title.>(.+?)</h3>(.+?)<img.+?src="(.+?)">(.+?)</a>.+?<a.+?a>(.+?)</div><'
		href_new,dict=put_items(re.findall(pattern,body,re.DOTALL))
		page_end=xsearch('<li class="last"><a href="t/phim-chieu-rap-29/phim-le/trang-(.+?)">',body,1)
		name=color['trangtiep']+'Trang tiếp theo: trang %d/%s[/COLOR]'%(page+1,page_end)
		addir(name,href,icon['megabox'],'',mode,page+1,'phim-chieu-rap',True)
		if href_new:endxbmc();update_href_new(href_new,dict)
	elif query=='subCate':#url=phim-le,phim-bo,t/phim-chieu-rap-29,show,clip
		if '/' in url:gen=url.split('/')[1];url=url.split('/')[0]
		else:gen='ALL'
		cat={'phim-le':('Lẻ',1),'phim-bo':('Bộ',2),'show':('Show',3),'clip':('Clip',4)}
		href='http://phim.megabox.vn/home/getcontent/?cat=%s&genre=%s&country=%s';dict=json_rw()
		for genre,country,gen_name in dict['subCate%d'%cat[url][1]]:
			gen_name=gen_name.encode('utf-8') if type(gen_name)==unicode else str2u(gen_name)
			if gen_name==gen:href=href%(cat[url][1],genre,country);continue
			title=color['xshare']+re.sub('\[.?COLOR.*?\]','',name);
			title=re.sub('%s.+\Z'%cat[url][0],cat[url][0]+' %s Mới Nhất[/COLOR]'%gen_name,title)
			addir(title,url+'/'+gen_name,icon['megabox'],'',mode,1,query,True)
		patt="<a class.+?href='(.+?)'.+?title.>(.+?)</h3>(.+?)<img.+?src='(.+?)'(.+?)</a>.+?<a.+?a>(.+?)</div></div>"
		put_items(re.findall(patt,make_request(href,hd),re.DOTALL),'i')
		cat={'phim-le':'Phim lẻ','phim-bo':'Phim bộ','show':'Show','clip':'Clip'}
		name=color['trangtiep']+'%s Xem Thêm...[/COLOR]'%cat[url]
		addir(name,url,icon['megabox'],'',mode,1,'mainmenu',True)
	return ''


def hdviet(name,url,img,mode,page,query):
	color['hdviet']='[COLOR darkorange]';icon['hdviet']=os.path.join(iconpath,'hdviet.png')
	home='http://movies.hdviet.com/'
	direct_link='https://api-v2.hdviet.com/movie/play?accesstokenkey=%s&movieid=%s'
	def namecolor(name):return '%s%s[/COLOR]'%(color['hdviet'],name)
	def getcookie():
		u=myaddon.getSetting('userhdviet');p=myaddon.getSetting('passhdviet')
		import hashlib;data=urllib.urlencode({'email':u,'password':hashlib.md5(p).hexdigest()})
		response=make_post('http://movies.hdviet.com/dang-nhap.html',hd,data)
		return response.cookiestring
	def login_hdviet():
		u=myaddon.getSetting('userhdviet');p=myaddon.getSetting('passhdviet')
		url='https://id.hdviet.com/authentication/login'
		response=make_post(url,data='email=%s&password=%s'%(u,p),resp='j')
		if response and response.get('error')==0:
			response=response.get('data')
			#mess(u'[COLOR green]Login hdviet.com Success[/COLOR]',title='%sHDViet.com[/COLOR]'%color['hdviet'])
			json_rw('hdviet.cookie',response)
		elif response and response.get('error')==27:
			mess(u'[COLOR red]Acc bị khóa tạm thời. Vào web để login nhé!!![/COLOR]',title='%sHDViet.com[/COLOR]'%color['hdviet']);response=dict()
		elif response and response.get('error') in (25,22):
			#mess(u'[COLOR red]%s[/COLOR]'%response.get('message'),title='%sHDViet.com[/COLOR]'%color['hdviet'])
			response=dict()
		else:
			import hashlib;data=urllib.urlencode({'email':u,'password':hashlib.md5(p).hexdigest()})
			response=make_post('http://movies.hdviet.com/dang-nhap.html',hd,data)
			try:resp=response.json
			except:resp={u'r': u'Lỗi đăng nhập hdviet.com', u'e': 3}
			if resp.get('e')==0:
				mess(u'[COLOR green]%s[/COLOR]'%resp['r'],title='%sHDViet.com[/COLOR]'%color['hdviet'])
				hd['Cookie']=response.cookiestring
				response=make_request('http://movies.hdviet.com/dieu-khoan-su-dung.html',headers=hd)
				import base64
				token=base64.b64decode(xsearch('<a class="userinfo".+?token=(.+?)"',response,1))
				response={'Cookie':hd['Cookie'],'access_token':token};json_rw('hdviet.cookie',response)
			else:response=dict();mess(u'[COLOR red]%s[/COLOR]'%resp['r'],title='%shdviet.com[/COLOR]'%color['hdviet'])
		url='http://movies.hdviet.com/dang-xuat.html?accesstokenkey=%s'
		make_post(url%response.get('access_token')).body
		return response
	def getResolvedUrl(id_film,loop=0):#Phim le/phim chieu/ke doi dau thien ac
		def getlinkhdviet(token,id_film):
			id_film=id_film.replace('_e','&ep=')
			response=make_request(direct_link%(token,id_film),resp='j')
			try:links=response['r'];link=response['r']['LinkPlay']
			except:links=dict()
			return links
		data=json_rw('hdviet.cookie')
		links=getlinkhdviet(data.get('access_token'),id_film)
		if not links:return links
		link=links.get('LinkPlay')
		if '0000000000000000000000' in link:
			data=login_hdviet();links=getlinkhdviet(data.get('access_token'),id_film);link=links.get('LinkPlay')
		if links:
			max_resolution='_1920_' if myaddon.getSetting('hdvietresolution')=='1080' else '_1280_'
			resolutions=['_1920_','_1885_','_1876_','_1866_','_1792_','_1280_','_1024_','_800_','_640_','_480_']
			if '_e' in id_film:link=re.sub('%s_e\d{1,3}_'%id_film.split('_')[0],'%s_'%id_film,link)
			href=link
			for resolution in resolutions:
				if resolution in link:link=link.replace(resolution,max_resolution);break
			extm3u=make_request(link);link=''
			if not extm3u:extm3u=make_request(href)
			for resolution in resolutions:
				if resolution in extm3u:link=xsearch('(http://.+%s.+m3u8)'%resolution,extm3u,1)
				if link:break
		if link and loop==0:
			response=make_request(link,resp='o')
			if response and 'filename' not in response.headers.get('content-disposition',''):
				data=login_hdviet();return getResolvedUrl(id_film,1)
		if link:
			audioindex=-1
			try:
				for audio in links.get('AudioExt'):
					if audio.get('Label')==u'Thuyết Minh':
						audioindex=int(audio.get('Index'))-1
				linksub='xshare' if audioindex>-1 else ''
			except:linksub=''
			if not linksub:
				for source in ['Subtitle','SubtitleExt','SubtitleExtSe']:
					try:
						linksub=links['%s'%source]['VIE']['Source']
						if linksub:
							if download_subs(linksub):break
					except:pass
			if audioindex>-1:link=link+'?audioindex=%d'%audioindex
		else:linksub=''
		return link,linksub
	def additems(body):
		pattern='<li class="mov-item".+?href="(.+?)".+?src="(.+?)".+?title="Phim (.+?)".+?<span(.+?) data-id="(.+?)">'
		data=re.findall(pattern,body,re.DOTALL);listitems=list()
		for href,img,title,detail,id_film in data:
			epi=xsearch('"labelchap2">(\d{1,3})</span>',detail,1);title=unescape(title)
			res=xsearch('id="fillprofile" class="icon-(.+?)11">',detail,1)
			res='[COLOR gold]SD[/COLOR]' if 'SD' in res else '[COLOR gold]HD[/COLOR]%s'%res
			phim18=xsearch('class="children11".+?>(.+?)</label></span>',detail,1)
			TM=xsearch('id="fillaudio" class="icon-(.+?)">',detail,1)
			TM='%s[COLOR green]%s[/COLOR][COLOR red]%s[/COLOR]'%(res,TM,phim18)
			plot=xsearch('<span class="cot1">(.+?)</span>',detail,1)
			year=xsearch('<span class="chil-date".+?>(.*?)</label></span>',detail,1)
			act=', '.join(s for s in re.findall('<a href="http://movies.hdviet.com/dien-vien/.+?">(.+?)</a>',detail))
			drt=', '.join(s for s in re.findall('<a href="http://movies.hdviet.com/dao-dien/.+?">(.+?)</a>',detail))
			rat=xsearch('<span class="fl-left">.+?<span>(.+?)</span>',detail,1)
			upl=xsearch('<span class="fl-right">.+?<span>(.+?)</span>',detail,1)
			if not epi:title=TM+' '+title;query='hdvietplay'
			elif epi=='1':query='hdvietfolder'
			else:title=TM+' '+namecolor(title)+' [COLOR green](%s)[/COLOR]'%epi;query='hdvietfolder'
			listItem = xbmcgui.ListItem(label=title,iconImage=img,thumbnailImage=img)
			if rat:rat='[COLOR tomato]IMDb:[/COLOR] %s, '%rat
			if upl:upl='[COLOR tomato]Uploader:[/COLOR] %s, '%upl
			if act:act='[COLOR tomato]Diễnviên:[/COLOR] %s, '%act
			if drt:drt='[COLOR tomato]Đạodiễn:[/COLOR] %s, '%drt
			plot=rat+upl+act+drt+'\n'+plot
			info={'title':title,'year':year,'rating':xsearch('(\d\.\d{1,2})',rat,1),'plot':plot,'episode':epi,'director':drt,'writer':act}
			listItem.setInfo(type="Video", infoLabels=info)
			listItem.setArt({"thumb":img,"poster":img,"fanart":img})
			if query=='hdvietplay':listItem.setProperty('IsPlayable', 'true')
			u=sys.argv[0]+"?url="+id_film+"&img="+urllib.quote_plus(img)+"&fanart="+urllib.quote_plus(img)+"&mode="+str(mode)+"&page="+str(page)+"&query="+query+"&name="+title
			listitems.append((u,listItem,False if query=='hdvietplay' else True))
		xbmcplugin.addDirectoryItems(int(sys.argv[1]),listitems,totalItems=len(listitems))
	def hdviet_search(string):
		url='http://movies.hdviet.com/tim-kiem.html?keyword=%s'%urllib.quote_plus(string)
		hdviet(name,url,img,mode,page,query='timkiem')
	if query=='hdviet.com':
		name=color['search']+"Search trên hdviet.com[/COLOR]"
		addir(name,'http://movies.hdviet.com/tim-kiem.html',icon['icon'],fanart,mode,1,'search',True)
		if checkupdate('hdviet.html')>8:body=makerequest(joinpath(datapath,'hdviet.html'),make_request(home),'w')
		else:body=makerequest(joinpath(datapath,'hdviet.html'))
		items=re.findall('"mainitem" menuid="(.+?)" href="(.+?)" title=".+?">(.+?)</a>',body)
		for id,href,name in items:
			addir(namecolor(name),home,icon['hdviet'],fanart,mode,1,id,True)
		addir(namecolor('Thể loại phim'),'the-loai',icon['icon'],fanart,mode,1,'the-loai-phim',True)
		url='http://movies.hdviet.com/phim-yeu-thich.html'
		addir(namecolor('Phim yêu thích'),url,icon['icon'],fanart,mode,1,'yeu-thich',True)
		items=re.findall('<div class="h2-ttl cf">.+?<a href="(.+?)" title=".+?" >(.+?)</a>.+?</div>(.+?)</ul>',body,re.DOTALL)
		for href,name,subbody in items:
			addir('%s%s[/COLOR]'%(color['search'],name),href,icon['hdviet'],fanart,mode,page,'1',True)
			additems(subbody)
	elif query=='search':make_mySearch('','hdviet.com','','',mode,'get')
	elif query=="INP":hdviet_search(make_mySearch('',url,'','','','Input'))
	elif url=='hdviet.com':page=1 if 'Trang tiếp theo' not in name else page;hdviet_search(query)
	elif query=='the-loai-phim':
		for href,name in re.findall('<p><a href="(.+?)" title=".+?">(.+?)</a></p>',makerequest(joinpath(datapath,'hdviet.html'))):
			addir(namecolor(name),href,icon['hdviet'],fanart,mode,page,'theloai',True)
	elif query=='3' and url==home:#Phim lẻ
		items=re.findall('<a href="(.+?)" .?menuid="(.+?)" .?title=".+?" >(.+?)</a>',makerequest(joinpath(datapath,'hdviet.html')))
		for href,id,name in items:
			addir(namecolor(name),href,icon['hdviet'],fanart,mode,page,id,True)
	elif query=='10' and url==home:#Phim bộ
		body=makerequest(joinpath(datapath,'hdviet.html'))
		items=re.findall('<a href="(.+?)" menuid="(.+?)" title=".+?">(.+?)</a>',body)
		items+=re.findall('<a class="childparentlib" menuid="(.+?)" href="(.+?)" title=".+?">(\s.*.+?)</a>',body)
		for href,id,name in items:
			if 'au-my' in href:name='Phim bộ Âu Mỹ %s'%name.strip()
			elif 'hong-kong' in href:name='Phim bộ Hồng Kông %s'%name.strip()
			elif 'trung-quoc' in href:name='Phim bộ Trung Quốc %s'%name.strip()
			else:name='Phim bộ %s'%name.strip()
			if href in '38-39-40':temp=href;href=id;id=temp
			addir(namecolor(name),href,icon['hdviet'],fanart,mode,page,id,True)
	elif query=='hdvietfolder':
		href='http://movies.hdviet.com/lay-danh-sach-tap-phim.html?id=%s'%url
		response=make_request(href,resp='j')
		if not response:return
		for eps in range(1,int(response["Sequence"])+1):
			name=re.sub(' \[COLOR green\]\(\d{1,4}\)\[/COLOR\]','',name)
			title='Tập %s/%s-%s'%(format(eps,'0%dd'%len(response['Episode'])),str(response['Episode']),re.sub('\[.?COLOR.{,12}\]','',name))
			addir(title,'%s_e%d'%(url,eps),img,fanart,mode,page,'hdvietplay',False)
	elif query=='hdvietplay':
		link,sub=getResolvedUrl(url)
		if not link:mess(u'[COLOR red]Get link thất bại[/COLOR]',title='%sHDViet.com[/COLOR]'%color['hdviet'])
		else:
			if sub:
				#mess(u'[COLOR green]Phụ đề của HDViet.com[/COLOR]',title='%sHDViet.com[/COLOR]'%color['hdviet'])
				sub=urllib.unquote(os.path.splitext(os.path.basename(sub))[0])
			xbmcsetResolvedUrl(link+'|'+urllib.urlencode(hd),sub)
	elif query=='Themmucyeuthich':
		hd['Cookie']=getcookie()
		body=make_post('http://movies.hdviet.com/them-phim-yeu-thich.html',hd,urllib.urlencode({"MovieID":"%s"%url}))
		try:mess(u'[COLOR green]%s[/COLOR]'%body.json['r'],title='%sHDViet.com[/COLOR]'%color['hdviet'])
		except:mess(u'[COLOR red]Lỗi thêm phim yêu thích[/COLOR]',title='%sHDViet.com[/COLOR]'%color['hdviet'])
	else:
		if query=='yeu-thich':hd['Cookie']=getcookie();body=make_request(url,hd)
		else:body=make_request(url)
		body=sub_body(body,'class="homesection"','class="h2-ttl cf"')
		additems(body)
		pages=re.findall('<li class=""><a href="(.+?)">(.+?)</a></li>',sub_body(body,'class="active"',''))
		if pages:
			pagenext=pages[0][1];pageend=pages[len(pages)-1][1]
			name='%sTrang tiếp theo: trang %s/%s[/COLOR]'%(color['trangtiep'],pagenext,pageend)
			addir(name,pages[0][0],img,fanart,mode,page,query,True)
		xbmc.executebuiltin('Container.SetViewMode(504)')

def play_youtube(url):#https://www.youtube.com/get_video_info?video_id=xhNy0jnAgzI
	def choice_solution(items,label_quality):#label_quality in ('quality','quality_label')
		url=''
		for solution in ('1080','720','medium','small'):
			for item in items:
				x,y=item.get(label_quality),item.get('type')
				if x and y and solution in x and 'video' in y and 'mp4' in y:
					url=urllib.unquote(item.get('url'));break
			if url:break
		return url
	url='https://www.youtube.com/watch?v=%s&spf=navigate-back'%xsearch('(\w{10,20})',url,1)
	data=make_request(url,resp='j',maxr=3);fmts=''
	if not data:return
	for i in range(0,len(data)):#'adaptive_fmts','url_encoded_fmt_stream_map'
		try:fmts=data[i]['data']['swfcfg']['args']['url_encoded_fmt_stream_map'];break
		except:pass
	data=[];link=''
	for items in fmts.split(','):
		dict={}
		for item in items.split('&'):
			try:dict[item.split('=')[0]]=item.split('=')[1]
			except:pass
		data.append(dict)
	link=choice_solution(data,'quality')
	if link:xbmcsetResolvedUrl(link,re.sub(' \[COLOR.+?/COLOR\]','',name)+'Maxlink')
	else:mess(u'[COLOR red]Get maxspeed link fail[/COLOR]',title='[COLOR green]youtube.com[/COLOR]')

def hayhaytv(name,url,img,fanart,mode,page,query):
	home='http://www.hayhaytv.vn/';ajax=home+'ajax_hayhaytv.php';api='http://api.hayhaytv.vn/'
	color['hayhaytv']='[COLOR tomato]';icon['hayhaytv']=os.path.join(iconpath,'hayhaytv.png')
	def login():
		u=myaddon.getSetting('userhayhay');p=myaddon.getSetting('passhayhay')
		data=urllib.urlencode({'email':u,'password':p,'remember_account':0})
		response=make_post('%sajax_jsonp.php?p=jsonp_login'%home,data=data)
		try:
			if response.json['success']=='success':
				f=response.cookiestring
				makerequest(joinpath(datapath,'hayhaytv.cookie'),f,'w')
			else:f=''
		except:f=''
		return f
	def mes(string):mess(string,title=namecolor('hayhaytv.vn'))
	def namecolor(name):return '%s%s[/COLOR]'%(color['hayhaytv'],name)
	def get_date(string):
		s=xsearch('/(\d{8})/',string,1)
		return '%s/%s/%s'%(s[:2],s[2:4],s[4:8]) if s else None
	def get_year(string):return xsearch('(20\d\d|19\d\d)',string,1)
	def get_idw(url):return xsearch('-(\w{6,20})\.html',url,1)
	def get_id(content):return xshare_group(re.search('FILM_ID\D{3,7}(\d{3,6})',content),1)
	def get_i(content,tag):return xsearch('<.+%s:.+>(.+?)?</li>'%tag,content,1).strip()
	def setskin():
		if xbmc.getSkinDir()=='skin.confluence':xbmc.executebuiltin('Container.SetViewMode(504)')
	def hayhaytv_search(string):
		url='http://www.hayhaytv.vn/tim-kiem/%s/trang-1'%'-'.join(s for s in string.split())
		hayhaytv(name,url,img,fanart,mode,page=1,query='submenu')
	def getinfo(body,sticky=dict()):
		for stic,info,plot in re.findall('id="(sticky.+?)" class="atip">(.+?)<p>(.*?)</p>',body,re.DOTALL):
			gen=get_i(info,'Thể loại');ctry=get_i(info,'Quốc Gia');rat=get_i(info,'IMDB')
			dur=xsearch('(\d{1,4})',get_i(info,'Thời lượng'),1)
			eps=xsearch('<span>Số tập:</span>(.+?)</li>',info,1,re.DOTALL).strip()
			sticky[stic]=(eps,gen,ctry,dur,rat,plot)
		#pattern='<a.+?tooltip="(.+?)" href="(.+?)">.*?"(http://img.*?)".*?color">(.*?)</span>.*?<span>(.*?)</span>(.*?)</a>'
		pattern='tooltip="(.+?)".+?href="(.+?)">.+?"(http://img.+?)".+?color">(.*?)</span>.*?<span>(.*?)</span>(.*?)</a>'
		items=list()#vie,eng,href,img,epi,eps,gen,ctry,dur,rat,plot
		for stic,href,img,eng,vie,tap in re.findall(pattern,body,re.DOTALL):
			if sticky.get(stic):items.append(((vie,eng,href,img,xsearch('<p>(.+?)</p>',tap,1))+sticky[stic]))
		return items
	def update_home(adict):
		mes(u'[COLOR green] Database updating...[/COLOR]')
		body=make_request(home,headers=hd)
		if not body:return adict
		content=sub_body(body,'class="menu_header"','class="box_login"')
		adict['mar-r20']=[s for s in re.findall('menu_fa_text.+?" href="(.+?)".*>(.+?)</a>',body) if os.path.basename(s[0])]
		for href,item in re.findall('href="(.+?)".+?<a (.+?)</ul>',content,re.DOTALL):
			for link,name in adict['mar-r20']:
				if href==link and 'trailer' not in link:
					name=os.path.basename(href)
					adict['m-%s'%name]=re.findall('href="(.+?)".*?>(.+?)</a>',item)
		pattern='href="(.+?)".*?>(.+\s.+|.+?)</a>.*\s?.*</h2>'
		adict['main']=[(s[0],' '.join(s for s in s[1].split())) for s in re.findall(pattern,body)]
		content=sub_body(body,'class="banner_slider"','class="main"')
		adict['banner_slider']=re.findall('<h3><a href=".+-(\w{5,20})\.html"',content)
		for p in ('phimbo','phimle','tvshow','clip'):
			mes(u'[COLOR green] Database updating...%s[/COLOR]'%p)
			for page in range(1,100):
				url='http://www.hayhaytv.vn/ajax_hayhaytv.php?p=%s&page=%d'%(p,page)
				items=getinfo(make_post(url,resp='b'));items_new=[s for s in items if get_idw(s[2]) not in adict]
				for s in items:adict[get_idw(s[2])]=s
				if len(items_new)==0:break
		xbmc.executebuiltin("Dialog.Close(all, true)")
		return json_rw('hayhaytv.json',dicts=adict)
	def addDirs(items,page='1'):
		listitems=list()
		for item in items:
			vie,eng,href,img,epi,eps,gen,ctry,dur,rat,plot=item
			#vie,eng,href,img,fan,thumb,date,year,gen,ctry,dur,rat,rev,views,epi,eps,drt,act,upl,sea,plot=item
			href='%s/%s'%(os.path.dirname(href),urllib.quote(u2s(os.path.basename(href))))
			title=vie+' - '+eng if vie and eng else vie if vie else eng;dur=xsearch('(\d{1,4})',dur,1)
			if eps and eps!='1':query='readfolder';title=namecolor(title)+' %s/%s'%(epi if epi else '?',eps)
			else:query='play'
			fan=img.replace('/crop/','/');thumb=img.replace('/crop/','/thumb/')
			date=get_date(img);year=get_year(eng);sea=xsearch('Season (\d{1,2})',eng,1)
			listItem = xbmcgui.ListItem(label=title,iconImage=img,thumbnailImage=thumb)
			if rat:plot='[COLOR tomato]IMDB:[/COLOR] %s\n'%rat+plot
			info={'title':title,'date':date,'year':year,'duration':dur,'rating':rat,'country':ctry,'genre':gen+' [COLOR green]%s[/COLOR]'%ctry,'plot':plot,'Episode':epi,'Season':sea}
			listItem.setInfo(type="Video", infoLabels=info)
			listItem.setArt({"thumb":thumb,"poster":img,"fanart":fan})
			if query=='play':listItem.setProperty('IsPlayable', 'true')
			u=sys.argv[0]+"?url="+urllib.quote_plus(href)+"&img="+urllib.quote_plus(img)+"&fanart="+urllib.quote_plus(fan)+"&mode="+str(mode)+"&page="+str(page)+"&query="+query+"&name="+title
			listitems.append((u,listItem,False if query=='play' else True))
		xbmcplugin.addDirectoryItems(int(sys.argv[1]),listitems,totalItems=len(listitems))
		return len(listitems)
	def getlink(body):
		movie_id=get_id(body);pattern='<title>.*xx(.+?)xx.*</title>';print 'movie_id %s'%movie_id
		href=xsearch('<link rel="canonical" href="(.+?)"',body,1)
		list_episodes=dict(re.findall('class=.*?href="(.+?)".*?>\D*([\d-]+)</',body))
		tap=list_episodes.get(href);print 'Tap: %s'%tap
		s=xsearch(pattern,make_request('https://www.fshare.vn/folder/5VNFUPO32P6F'),1).split('-')
		hd={s[0]:'%s %s'%(s[1],s[2])};data={"secure_token":"1.0","request":'{"movie_id":"%s"}'%movie_id}
		response=make_post('%smovie/movie_detail'%api,hd,data,'j');print 'Tap %s'%tap
		if response.get('data') and response['data'].get('list_episode') and len(response['data']['list_episode'])>0:
			eps=response['data']['list_episode']
			ids=[(s.get('id'),s.get('vn_subtitle')) for s in eps if s.get('name')==tap or s.get('name')==u'Tập '+tap]
			if ids:movie_id,sub=ids[0];href='%sgetlink/movie_episode'%api
			else:href=sub=''
		else:
			href='%sgetlink/movie'%api
			try:sub=response['data']['vn_subtitle'];print 'movie_id %s'%movie_id
			except:sub=''
		if href:
			data["request"]='{"data":[{"type":"facebook","email":"%s"}]}'%myaddon.getSetting('userhayhay')
			response=make_post('%suser/signup_social_network'%api,hd,data,'j')
			if response:
				token=response['data']['token_app'];user_id=response['data']['user_id']
				data['request']='{"token":"%s","user_id":"%s","movie_id":"%s"}'%(token,user_id,movie_id)
				print data
				response=make_post(href,hd,data,'j')
				try:href=response['data']['link_play'][0]['mp3u8_link']
				except:href=''
		return href,sub

	if checkupdate('hayhaytv.cookie')>24:hd['Cookie']=login()
	else:hd['Cookie']=makerequest(joinpath(datapath,'hayhaytv.cookie'))
	if query=='hayhaytv.vn':
		name=color['search']+"Search trên hayhaytv.vn[/COLOR]"
		addir(name,'http://www.hayhaytv.vn/tim-kiem/',icon['hayhaytv'],fanart,mode,1,'search',True)
		addir(namecolor("HayhayTV giới thiệu"),'gioithieu',icon['hayhaytv'],fanart,mode,1,'gioithieu',True)
		adict=json_rw('hayhaytv.json')
		if not adict.get('mar-r20') or not adict.get('main'):adict=update_home(adict)
		for href,name in adict['mar-r20']:
			addir(namecolor(name),href,icon['hayhaytv'],fanart,mode,1,'mainmenu',True)
		for href,name in adict['main']:
			addir(namecolor(name),href,icon['hayhaytv'],fanart,mode,1,'submenu',True)
		if checkupdate('hayhaytv.json')>8 and not os.path.isfile(joinpath(datapath,'hayhaytv.tmp')):
			endxbmc();makerequest(joinpath(datapath,'hayhaytv.tmp'),'','w')
			adict=update_home(adict);delete_files(datapath,mark='hayhaytv.tmp')
	elif query=='search':make_mySearch('','hayhaytv.vn','','',mode,'get')
	elif query=="INP":hayhaytv_search(make_mySearch('',url,'','','','Input'))
	elif url=='hayhaytv.vn':page=1 if 'Trang tiếp theo' not in name else page;hayhaytv_search(query)
	if query=='gioithieu':
		adict=json_rw('hayhaytv.json')
		addDirs([adict.get(s) for s in adict.get('banner_slider')]);setskin()
	elif query=='mainmenu':
		theloai=os.path.basename(url).replace('-','');q='filter'
		if theloai=='shows':theloai='tvshow'
		elif theloai=='cliphay':theloai='clip';q='theloai'
		elif url=='http://www.hayhaytv.vn/trailer':
			href='http://www.hayhaytv.vn/ajax_hayhaytv.php?p=trailer&page=1'
			return hayhaytv(name,href,img,fanart,mode,1,'submenu')
		for href,name in json_rw('hayhaytv.json',key='m-%s'%os.path.basename(url)):
			addir(namecolor(name),href,img,fanart,mode,1,'submenu',True)
	elif query=='submenu':
		body=make_request(url,maxr=3);adict=json_rw('hayhaytv.json')
		if 'http://www.hayhaytv.vn/su-kien/' in url or 'q=su-kien' in url:
			ids=re.findall('<a title=".+?" href=".+-(\w{10,20})\.html"',body)
			if not ids:mes(u'[COLOR red]Hiện tại không có nội dung mục này.[/COLOR]');return 'no'
			addDirs([adict.get(s) for s in ids])
			urlnext=home+xsearch('class=.active.+?onclick=.+?"(ajax_ht.php.+?)"',body,1)
			pagenext=xsearch('page=(\d{1,4})',urlnext,1);pagelast=xsearch('trang-(\d{1,4})-.{,50}Cuối',body,1)
		else:
			items=getinfo(body)
			if not items:mes(u'[COLOR red]Hiện tại không có nội dung mục này.[/COLOR]');return 'no'
			addDirs(items);urlnext=home+xsearch('class=.active.+?"(ajax_hayhaytv.php.+?)"',body,1)
			pagenext=xsearch('page=(\d{1,4})',urlnext,1);pagelast=xsearch('Trang \d{1,4}/(\d{1,4})',body,1)
		if pagenext:
			name=re.sub('\[.+?\]','',name.split('-')[0].strip())
			name='%s%s - Trang tiếp theo: trang %s/%s[/COLOR]'%(color['trangtiep'],name,pagenext,pagelast)
			addir(name,urlnext,img,fanart,mode,page+1,'submenu',True)
		setskin()
	elif query=='readfolder':#Phim bo moi: Truy Tìm Kho Báu
		pages=0;adict=json_rw('hayhaytv.json')
		if page==1:
			body=sub_body(make_request(url,headers=hd,maxr=3),'<div id="new_player">','class="content_div"')
			list_episodes=re.findall('class=.*?href="(.+?)".*?>\D*([\d-]+)</',body);items=list()
			item=adict.get(get_idw(url))
			if item:vie,eng,href,img,epi,eps,gen,ctry,dur,rat,plot=item
			else:vie=re.sub('\[.+?\]','',s2u(name));eps=xsearch('\w{0,3}/(\d{1,4})',name,1);eng=epi=gen=ctry=dur=rat=plot=''
			for href,tap in list_episodes:
				vi=u'Tập %s/%s%s'%(tap,eps,'-'+vie if vie else '')
				items.append((vi,eng,href,img,epi,'',gen,ctry,dur,rat,plot))
			if 'http://www.hayhaytv.vn/xem-show' in url:
				pages=xsearch("onclick='paging\((\d{1,3})\)'> &raquo",body,1)
				pages=int(pages) if pages else 0;id=xsearch('episode_(.+?)_unactive',body,1)
				url='http://www.hayhaytv.vn/tvshow/paging?page=2&q=episode&id=%s&pages=%d'%(id,pages)
			if pages or len(items)>rows:makerequest(joinpath(datapath,"temp.txt"),str(items),'w')
		else:
			try:items=eval(makerequest(joinpath(datapath,"temp.txt")))
			except:items=[]
			if 'http://www.hayhaytv.vn/tvshow/paging' in url and items:
				vie,eng,href,img,epi,eps,gen,ctry,dur,rat,plot=items[0]
				body=make_post(url.split('?')[0],data=url.split('?')[1],resp='b');items=list()
				for href,tap in re.findall('class=.*?href="(.+?)".*?>\D*([\d-]+)</',body):
					vi=re.sub(u'Tập \d{1,4}/',u'Tập %s/'%tap,vie)
					items.append((vi,eng,href,img,epi,'',gen,ctry,dur,rat,plot))
				pages=xsearch('pages=(\d{1,4})\Z',url.split('?')[1],1)
				if pages and int(pages)>page:
					url=re.sub('page=\d{1,4}&','page=%s&'%str(page+1),url);pages=int(pages)
				else:pages=0
		if 'http://www.hayhaytv.vn/tvshow' not in url:
			pages=len(items)/(rows+1)+1;del items[:rows*(page-1)];del items[rows:]
		addDirs(items)
		if pages>page:
			name=color['trangtiep']+'Trang tiếp theo...trang %d/%d[/COLOR]'%(page+1,pages)
			addir(namecolor(name),url,img,fanart,mode,page+1,'readfolder',True)
		setskin()
	elif query=='play':
		print url
		body=make_request(url,headers=hd,maxr=3);trailer=xsearch("initTrailerUrl = '(.+?)'",body,1)
		if trailer:xbmcsetResolvedUrl(trailer)
		elif '/xem-clip/' not in url:
			if '/xem-show/' in url:mes(u'[COLOR red]Chưa code phần này !!![/COLOR]');return
			href,sub=getlink(body)
			if href:
				if sub and download_subs(sub):mes(u'[COLOR green]Phụ đề của hayhaytv.vn[/COLOR]')
				xbmcsetResolvedUrl(href,urllib.unquote(os.path.splitext(os.path.basename(sub))[0]))
			else:mes(u'[COLOR red]Get max link thất bại...[/COLOR]')
		else:
			href=xsearch('src="(http://www.youtube.com.+?)"',body,1)
			if href:play_youtube(href)
			else:mes('[COLOR red]Link youtube.com find not found ![/COLOR]')

def phimmoi(name,url,img,mode,page,query):
	color['phimmoi']='[COLOR ghostwhite]';icon['phimmoi']=os.path.join(iconpath,'phimmoi.png')
	home='http://www.phimmoi.net/';refresh=False;phimmoixml=joinpath(datapath,'phimmoi.xml')
	tempfolder=xbmc.translatePath('special://temp')
	def namecolor(name):return '%s%s[/COLOR]'%(color['phimmoi'],name)
	def mes(string):mess(string,title=namecolor('phimmoi.net'))
	def login_pm():
		u=myaddon.getSetting('userphimmoi');p=myaddon.getSetting('passphimmoi')
		import hashlib;p=hashlib.md5(p).hexdigest()
		response=make_post('http://www.phimmoi.net/login/',data=urllib.urlencode({'username':u,'password_md5':p}))
		if response.status==302 and makerequest(joinpath(datapath,'phimmoi.cookie'),response.cookiestring,'w'):
			f=response.cookiestring
		else:f=''
		return f
	def pm_search(string):
		url='http://www.phimmoi.net/tim-kiem/%s/'%urllib.quote_plus(string)
		phimmoi(name,url,img,mode,page=1,query='readpage')
	def getid(url):return xshare_group(re.search('-(\d{3,5})/',url),1)
	def geteps(string):
		try:url=json.loads(string)['url'];part=json.loads(string)['part']
		except:url=part=''
		return url,part
	def make_eps(url,eps):
		id=getid(url);content=makerequest(phimmoixml);string=''
		string_old=xshare_group(re.search('(<a id="%s" part=".+?"/>)'%id,content),1)
		for part_id in eps:string+=str(geteps(part_id)[1])+'-'
		string_new='<a id="%s" part="%s"/>\n'%(id,string[:len(string)-1])
		string=content.replace(string_old+'\n',string_new) if string_old else content+string_new
		makerequest(phimmoixml,string,'w')
	def addirpm(name,link,img='',fanart='',mode=0,page=0,query='',isFolder=False,menu=list()):
		def xquote(href):return urllib.quote_plus(href)
		if '18+' in name and myaddon.getSetting('phim18')=="false":return
		name=unescape(re.sub(',|\|.*\||\||\<.*\>','',u2s(name)))
		item=xbmcgui.ListItem(name,iconImage=img,thumbnailImage=img)
		query=menuContext(name,link,img,fanart,mode,query,item)
		item.setInfo(type="Video", infoLabels={"title":name})
		if not fanart:fanart=joinpath(home,'fanart.jpg')
		item.setProperty('Fanart_Image',fanart)
		li='%s?name=%s&url=%s&img=%s&fanart=%s&mode=%d&page=%d&query=%s'
		li=li%(sys.argv[0],urllib.quote(name),xquote(link),xquote(img),xquote(fanart),mode,page,query)
		if not isFolder:item.setProperty('IsPlayable', 'true')
		if menu:#info={'name':'','url':'','img':'','fanart':'','query':''}
			cmd='RunPlugin(plugin://%s/?mode=%d'%(myaddon.getAddonInfo('id'),mode);items=list()
			for label,info in menu:
				name=info.get('name');url=info.get('url');img=info.get('img')
				fanart=info.get('fanart');query=info.get('query')
				command=cmd+'&name=%s&url=%s&img=%s&fanart=%s&query=%s)'%(name,url,img,fanart,query)
				items.append(('[COLOR lime]%s[/COLOR]'%label,command))
			item.addContextMenuItems(items)
		xbmcplugin.addDirectoryItem(int(sys.argv[1]),li,item,isFolder)
	def addir_pm(items,name='',menu=list()):#title,href,img,detail
		for title,href,img,detail in items:
			eps=xsearch('Tập ?(\d{,4}/\d{,4}|\?/\d{,4}|\d{,4})',detail,1)
			if not eps:
				epi=xsearch('class="eps">Trọn bộ ?(\d{1,4}) ?tập</div>',detail,1)
				if epi:eps='%s/%s'%(epi,epi)
			else:epi=eps.split('/')[0]
			try:epi=int(epi)
			except:epi=0
			dur=xsearch('>(\d{1,3}.?phút)',detail,1)
			if 'url=' in img:img=img.split('url=')[1]
			if eps:title='%s %s(%s)[/COLOR]'%(title,color['subscene'],eps)
			if dur:title='%s [COLOR gold]%s[/COLOR]'%(title,dur)
			if epi>1 or 'Phim bộ hot trong tuần' in name:query='pmfolder';isFolder=True;title=namecolor(title)
			else:query='pmplay';isFolder=False
			if 'Thuyết minh' in detail:title='[COLOR gold]TM[/COLOR] %s'%title
			label=xsearch('(HD[\w|-]*|SD[\w|-]*|Bản đẹp[\w|-]*)',detail,1)
			if label:title='%s - [COLOR green]%s[/COLOR]'%(title,label)
			addirpm(title,home+href,img,'',mode,page,query,isFolder,menu)
	def get_epi(epi):
		try:epi=int(epi)
		except:epi=0
		return epi
	def get_info(title,href,img,detail):
		eps=xsearch('Tập ?(\d{,4}/\d{,4}|\?/\d{,4}|\d{,4})',detail,1)
		if not eps:
			epi=xsearch('class="eps">Trọn bộ ?(\d{1,4}) ?tập</div>',detail,1)
			if epi:eps='%s/%s'%(epi,epi)
		else:epi=eps.split('/')[0]
		dur=xsearch('>(\d{1,3}.?phút)',detail,1)
		audio='TM' if 'Thuyết minh' in detail else ''
		label=xsearch('(HD[\w|-]*|SD[\w|-]*|Bản đẹp[\w|-]*)',detail,1)
		if 'url=' in img:img=img.split('url=')[1]
		if eps:title='%s %s(%s)[/COLOR]'%(title,color['subscene'],eps)
		if dur:title='%s [COLOR gold]%s[/COLOR]'%(title,dur)
		if get_epi(epi)>1 or 'Phim bộ hot trong tuần' in name:query='pmfolder';isFolder=True;title=namecolor(title)
		else:query='pmplay';isFolder=False
		if audio:title='[COLOR gold]TM[/COLOR] %s'%title
		if label:title='%s - [COLOR green]%s[/COLOR]'%(title,label)
		return title,home+href,img,query,isFolder
	def pm_addir(name,link,img='',fanart='',mode=0,page=0,query='',isFolder=False,menu=list()):
		def xquote(href):return urllib.quote_plus(href)
		if '18+' in name and myaddon.getSetting('phim18')=="false":return
		name=unescape(re.sub(',|\|.*\||\||\<.*\>','',u2s(name)))
		item=xbmcgui.ListItem(name,iconImage=img,thumbnailImage=img)
		item.setInfo(type="Video", infoLabels={"title":name})
		if not fanart:fanart=joinpath(home,'fanart.jpg')
		item.setProperty('Fanart_Image',fanart)
		li='%s?name=%s&url=%s&img=%s&fanart=%s&mode=%d&page=%d&query=%s'
		li=li%(sys.argv[0],urllib.quote(name),xquote(link),xquote(img),xquote(fanart),mode,page,query)
		if not isFolder:item.setProperty('IsPlayable', 'true')
		if menu:#info={'name':'','url':'','img':'','fanart':'','query':''}
			cmd='RunPlugin(plugin://%s/?mode=%d'%(myaddon.getAddonInfo('id'),mode);items=list()
			for label,info in menu:
				name=info.get('name');url=info.get('url');img=info.get('img')
				fanart=info.get('fanart');query=info.get('query')
				command=cmd+'&name=%s&url=%s&img=%s&fanart=%s&query=%s)'%(name,url,img,fanart,query)
				items.append(('[COLOR lime]%s[/COLOR]'%label,command))
			item.addContextMenuItems(items)
		xbmcplugin.addDirectoryItem(int(sys.argv[1]),li,item,isFolder)

	if query=='phimmoi.net':
		name=color['search']+"Search trên phimmoi.net[/COLOR]"
		addir(name,'http://www.phimmoi.net/tim-kiem/',icon['phimmoi'],mode=mode,query='search',isFolder=True)
		name=color['search']+'Tủ phim trên phimmoi.net của tôi[/COLOR]'
		addir(name,'http://www.phimmoi.net/tu-phim/',img,'',mode,1,'readpage',True)
		body=makerequest(joinpath(tempfolder,'phimmoi.html'))
		content=xsearch('<ul id=".+?"(.+?)</ul></div>',body,1)
		for title in re.findall('<a>(.+?)</a>',content):
			addir(namecolor(title),'',icon['phimmoi'],mode=mode,query='menubar',isFolder=True)
		for href,title in re.findall('<a href="([\w|-]+/|http://www.phimmoi.net/tags/.*?)">(.+?)</a>',content):
			addir(namecolor(title),href,icon['phimmoi'],'',mode,1,'menubar',isFolder=True)
		for title in re.findall('<h2 class="right-box-header star-icon"><span>(.+?)</span>',body):
			if title=='Phim đã đánh dấu':continue
			addir(namecolor(title),'right-box',img,'',mode,1,'menubar',True)
		for title,content in re.findall('<h2 class="hidden">(.+?)</h2>(.+?)</div></li></ul>',body):
			addir('[COLOR lime]%s[/COLOR]'%title,'',img,'',mode,1,'no')
			pattern='title="(.+?)" href="(.+?)".+?\(\'(http.+?)\'\).+?</div></a>(.+?)</div></li>'
			addir_pm(re.findall(pattern,content))#title,href,img,detail
		for label,content in re.findall('class="title-list-index">(.+?)</span>(.+?)</div></div></div>',body):
			addir('[COLOR lime]%s[/COLOR]'%label,'',img,'',mode,1,'no')
			pattern='<li><a href="(.+?)" title="(.+?)">.+?<img src="(.+?)".+?<h3(.+?)</p>'
			items=re.findall(pattern,content)
			if items:addir_pm([(s[1],s[0],s[2],s[3]) for s in items])#title,href,img,detail
			else:
				pattern='"movie-item m-block" title="(.+?)" href="(.+?)".+?(http.+?\.jpg).+?<div(.+?)</div></a></li>'
				addir_pm(re.findall(pattern,content))#title,href,img,detail
		if checkupdate('phimmoi.html',tempfolder)>8:
			endxbmc();makerequest(joinpath(tempfolder,'phimmoi.html'),make_request('http://www.phimmoi.net/'),'w')
	elif query=='search':make_mySearch('','phimmoi.net','','',mode,'get')
	elif query=="INP":pm_search(make_mySearch('',url,'','','','Input'))
	elif url=='phimmoi.net':page=1 if 'Trang tiếp theo' not in name else page;pm_search(query)
	elif query=='menubar':
		if any(s for s in ['kinh','rap','tags','trailer'] if s in url):
			if 'tags' not in url:url=home+url
			return phimmoi(name,url,img,mode,page,'readpage')
		elif url=='right-box':
			pattern='<span>%s</span>(.+?</li></ul></div></div>)'%re.sub('\[/?COLOR.*?\]','',name).strip()
			content=xsearch(pattern,makerequest(joinpath(tempfolder,'phimmoi.html')),1)
			pattern='title="(.+?)" href="(.+?)">.+?\(\'(.+?)\'\).+?</span>(.+?)</a></li>'
			addir_pm(re.findall(pattern,content),name)#title,href,img,detail
		else:
			content=xsearch('<ul id=".+?"(.+?)</ul></div>',makerequest(joinpath(tempfolder,'phimmoi.html')),1)
			gen={'Thể loại':'the-loai','Quốc gia':'quoc-gia','Phim lẻ':'phim-le','Phim bộ':'phim-bo'}
			query=gen.get(re.sub('\[/?COLOR.*?\]|\(.+?\)','',name).strip())
			pattern='<a href="(%s/.*?)">(.+?)</a>'%query
			for href,title in re.findall(pattern,content):
				addir(namecolor(title),home+href,icon['phimmoi'],'',mode,1,'readpage',True)
	elif query=='readpage':
		if url=='http://www.phimmoi.net/tu-phim/':
			hd['Cookie']=makerequest(joinpath(datapath,'phimmoi.cookie'))
			body=make_request(url,headers=hd);token=xsearch("fx\.token='(.+?)'",body,1);menu1='Remove from Tủ phim'
			if not token:
				hd['Cookie']=login_pm();body=make_request(url,headers=hd)
		else:body=make_request(url);menu1='Add to Tủ phim'
		for content in re.findall('<li class="movie-item">(.+?)</li>',body,re.DOTALL):
			title=xsearch('title="(.+?)"',content,1);href=xsearch('href="(.+?)"',content,1)
			img=xsearch('\((http.+?)\)',content,1);detail=' '.join(re.findall('<span(.+?)</span>',content))
			title,href,img,query,isFolder=get_info(title,href,img,detail)
			menu=[(menu1,{'name':menu1,'url':href,'query':'tuphim'})]
			pm_addir(title,href,img,'',mode,page,query,isFolder,menu)
		urlnext=xshare_group(re.search('<li><a href="(.+?)">Trang kế.+?</a></li>',body),1)
		if urlnext:
			pagenext=xshare_group(re.search('/page-(\d{1,3})\.html',urlnext),1)
			name='%sTrang tiếp theo: trang %s[/COLOR]'%(color['trangtiep'],pagenext)
			addir(name,home+urlnext,img,fanart,mode,page,'readpage',True)
	elif query=='tuphim':
		hd['Cookie']=makerequest(joinpath(datapath,'phimmoi.cookie'))
		token=xsearch("fx\.token='(.+?)'",make_request('http://www.phimmoi.net/tu-phim/',headers=hd),1)
		if not token:
			hd['Cookie']=login_pm()
			token=xsearch("fx\.token='(.+?)'",make_request('http://www.phimmoi.net/tu-phim/',headers=hd),1)
		data={'_fxAjax':'1','_fxResponseType':'JSON','_fxToken':'%s'%token}
		action='add' if 'Add' in name else 'remove'
		response=make_post('%s%s.html'%(url,action),hd,data,resp='j')
		if response.get('_fxStatus',0)==1:
			mes(response.get('_fxMessage','success'))
			if action=='remove':xbmc.executebuiltin("Container.Refresh")
		else:
			try:mes(response.get('_fxErrors')[0])
			except:mes(u'Đã phát sinh lỗi!')
	elif query=='pmfolder':
		body=make_request(url+'xem-phim.html');name=re.sub('\[/?COLOR.*?\]|\(.+?\)|\d{1,3} phút','',name).strip()
		for detail in re.findall('data-serverid="pcs"(.+?)</li></ul></div>',body,re.DOTALL):
			title=' '.join(s for s in xsearch('<h3 class="server-name">(.+?)</h3>',detail,1,re.DOTALL).split())
			if title and 'tập phim' not in title:addir('[COLOR lime]%s[/COLOR]'%title,'',img,'',mode,1,'no')
			label=name.replace('TM ','') if title and 'Thuyết minh' not in title else name
			for title,href in re.findall('title="(.+?)".+?href="(.+?)"',detail,re.DOTALL):
				addir(title+' '+label,home+href,img,fanart,mode,page,query='pmplay')
	elif query=='pmplay':
		href='http://www.phimmoi.net/player/v1.46/plugins/gkplugins_picasa2gdocs/plugins/plugins_player.php?url=%s'
		link_youtube=url;pyoutube="trailerUrl='(https://www.youtube.com/.+?)'"
		if '.html' not in url:url=url+'xem-phim.html'
		content=make_request(url,resp='o');hd['Cookie']=content.cookiestring
		content=sub_body(content.body,'- slider -','- Sidebar -')
		if not content:return play_youtube(xsearch(pyoutube,make_request(link_youtube),1))
		pattern='data-language="(.+?)".*href="(.+?)">.*\s.*Xem Full'
		links=dict(re.findall(pattern,content));body={};pattern="currentEpisode.url='(.+?)'"
		if not links:#Khong co ban full
			eps=[s.replace('\\','') for s in re.findall('({"episodeId":.+?})',content)]
			if not eps:body={};a=1
			elif len(eps)==1:body=make_post(href%geteps(eps[0])[0],headers=hd,resp='j');a=2
			elif xshare_group(re.search('Part (\d{1,3}) - ',name),1):
				part_id=int(xshare_group(re.search('Part (\d{1,3}) - ',name),1));epiurl='';a=3
				for epi in eps:
					if geteps(epi)[1]==part_id:epiurl=geteps(epi)[0];break
				body=make_post(href%epiurl,headers=hd,resp='j') if epiurl else ''
			elif 'xem-phim.html' not in url:
				print href%xshare_group(re.search(pattern,content),1)
				body=make_post(href%xshare_group(re.search(pattern,content),1),headers=hd,resp='j');a=4
			else:make_eps(url,eps);body=make_post(href%geteps(eps[0])[0],headers=hd,resp='j');a=5
		elif len(links)==1:#Chi co 1 ban full
			body=make_post(href%xshare_group(re.search(pattern,make_request(home+links.values()[0])),1),headers=hd,resp='j');a=6
		elif myaddon.getSetting('phimmoiaudio')=='true' and links.has_key('illustrate'):#sub Vie
			body=make_post(href%xshare_group(re.search(pattern,make_request(home+links['illustrate'])),1),headers=hd,resp='j');a=7
		elif links.has_key('subtitle'):#sub Eng
			body=make_post(href%xshare_group(re.search(pattern,make_request(home+links['subtitle'])),1),headers=hd,resp='j');a=8
		height=0;url='';maxresolution=int(myaddon.getSetting('phimmoiresolution'))
		for item in [s for s in body.get("content",list()) if 'video' in s.get('type')]:
			if item.has_key('height') and item['height']==maxresolution:url=item['url'];break
			elif item.has_key('height') and item['height']>height:height=item['height'];url=item['url']
		if not url:mess(u'[COLOR red]Không get được maxspeedlink hoặc link bị die[/COLOR]')
		else:xbmcsetResolvedUrl(url)

def get_params():#print json.dumps(json["content"],indent=2,sort_keys=True)
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
#addir:name,link,img,fanart,mode,page,query,isFolder
try:#Container.SetViewMode(num)
	myfolder=str2u(myaddon.getSetting('thumuccucbo'))
	if not os.path.exists(myfolder):myfolder=joinpath(datapath,'myfolder')
except:myfolder=joinpath(datapath,'myfolder')
subsfolder=joinpath(myfolder,'subs');tempfolder=joinpath(myfolder,'temp')
thumucrieng=''.join(s for s in myaddon.getSetting('thumucrieng').split()).upper()
if not thumucrieng or len(thumucrieng)<10:thumucrieng='RDA4FHXVE2UU'
thumucrieng='https://www.fshare.vn/folder/'+thumucrieng

xbmcplugin.setContent(int(sys.argv[1]), 'movies');params=get_params();mode=page=0;temp=[]
homnay=datetime.date.today().strftime("%d/%m/%Y");url=name=fanart=img=date=query=end=''

try:url=urllib.unquote_plus(params["url"])
except:pass
try:name=urllib.unquote(params["name"])
except:pass
try:img=urllib.unquote_plus(params["img"])
except:pass
try:fanart=urllib.unquote_plus(params["fanart"])
except:pass
try:mode=int(params["mode"])
except:pass
try:page=int(params["page"])
except:pass
try:query=urllib.unquote_plus(params["query"])
except:pass#urllib.unquote

print "Main---------- Mode: "+str(mode),"URL: "+str(url),"Name: "+str(name),"query: "+str(query),"page: "+str(page)
if not mode:#xbmc.executebuiltin("Dialog.Close(all, true)")
	init_file();open_category("FRE");endxbmc()
	if myaddon.getSetting('checkdatabase')=='true' or os.path.isfile(joinpath(data_path,'checkdatabase.txt')):
		data_download()
	data_update()
elif mode==1:vaphim(name,url,img,mode,page,query)
elif mode==2:end=google_search(url,query,mode,page)
elif mode==3:end=resolve_url(url)
elif mode==4:vp_phimmoi()
elif mode==5:vp_xemnhieu()
elif mode==6:end=phimFshare(name,url,mode,page,query)
elif mode==7:end=fptplay(name,url,img,mode,page,query)
elif mode==8:hdvietnam(name,url,img,fanart,mode,page,query)
elif mode==9:make_mySearch(name,url,img,fanart,mode,query)
elif mode==10:open_category(query)
elif mode==11:make_myFshare(name,url,img,fanart,mode,query)
elif mode==12:make_mylist(name,url,img,fanart,mode,query)
elif mode==13:end=xshare_search(name,url,query,mode,page)
elif mode==15:end=id_2url(url,name,mode,page,query)
elif mode==16:end=play_maxspeed_link(url)
elif mode==17:end=megabox(name,url,img,fanart,mode,page,query)
elif mode==18:dangcaphd(name,url,img,mode,page,query)
elif mode==19:pubvn(name,url,img,mode,page,query)
elif mode==20:end=vp_update(auto=False)
elif mode==21:vuahd(name,url,img,mode,page,query)
elif mode==22:hdviet(name,url,img,mode,page,query)
elif mode==23:end=hayhaytv(name,url,img,fanart,mode,page,query)
elif mode==24:phimmoi(name,url,img,mode,page,query)
elif mode==31:end=ifile_update()
elif mode==34:ifile_home(name,url,img,mode,page,query)
elif mode==38:doc_Trang4share(url)#38
elif mode==47:daklak47(name,url,img)
elif mode==50:htvonline(name,url,img,fanart,mode,page,query)
elif mode==90:end=doc_TrangFshare(name,url,img,fanart,query)
elif mode==91:main_menu(url,page,mode,query)
elif mode==92:vp_list(name,url,img,mode,page,query)
elif mode==93:vp_chonloc()
elif mode==94:end=subscene(name,url,query)
elif mode==95:tenlua_getlink(url)
elif mode==96:end=doc_thumuccucbo(name,url,img,fanart,mode,query)
elif mode==97:doc_list_xml(url,name,page)
elif mode==98:make_favourites(name,url,img,fanart,mode,query)
elif mode==99:myaddon.openSettings();end='ok'
if not end or end not in 'no-ok':endxbmc()
