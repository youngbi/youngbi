# -*- coding: utf-8 -*-
import xbmc,xbmcplugin,xbmcgui,xbmcaddon,urllib,re,os,unicodedata,datetime,random,json

myaddon=xbmcaddon.Addon()
home=xbmc.translatePath(myaddon.getAddonInfo('path'))
datapath=xbmc.translatePath(os.path.join( xbmc.translatePath(myaddon.getAddonInfo('profile')),'data'))
#iconpath=xbmc.translatePath(os.path.join( xbmc.translatePath(myaddon.getAddonInfo('profile')),'icon'))
iconpath=xbmc.translatePath(os.path.join(home,"logos\\"))
sys.path.append(os.path.join(home,'resources','lib'));import urlfetch

search_file=os.path.join(datapath,"search.xml");data_path=os.path.join(home,'resources','data')

myfolder= myaddon.getSetting('thumuccucbo').decode('utf-8');copyxml=myaddon.getSetting('copyxml')
if not os.path.exists(myfolder):myfolder=os.path.join(datapath,'myfolder')
subsfolder=os.path.join(myfolder,'subs');tempfolder=os.path.join(myfolder,'temp')
rows=int(myaddon.getSetting('sodonghienthi'))
googlesearch=myaddon.getSetting('googlesearch')
thumucrieng='https://www.fshare.vn/folder/'+myaddon.getSetting('thumucrieng').upper()

media_ext=['aif','iff','m3u','m4a','mid','mp3','mpa','ra','wav','wma','3g2','3gp','asf','asx','avi','flv','mov','mp4','mpg','mkv','m4v','rm','swf','vob','wmv','bin','cue','dmg','iso','mdf','toast','vcd','ts','flac']
color={'fshare':'[COLOR gold]','vaphim':'[COLOR gold]','phimfshare':'[COLOR khaki]','4share':'[COLOR blue]','tenlua':'[COLOR fuchsia]','fptplay':'[COLOR orange]','trangtiep':'[COLOR lime]','search':'[COLOR lime]','ifile':'[COLOR blue]','hdvietnam':'[COLOR crimson]','xshare':'[COLOR blue]','subscene':'[COLOR green]','megabox':'[COLOR orangered]','dangcaphd':'[COLOR yellow]'};icon={}
for hd in ['xshare','4share', 'dangcaphd', 'downsub', 'favorite', 'fptplay', 'fshare', 'gsearch', 'hdvietnam', 'icon', 'id', 'ifiletv', 'isearch', 'khophim', 'maxspeed', 'megabox', 'movie', 'msearch', 'myfolder', 'myfshare', 'phimfs', 'serverphimkhac', 'setting', 'tenlua', 'vaphim']:
	icon.setdefault(hd,os.path.join(iconpath,'%s.png'%hd))
hd = {'User-Agent' : 'Mozilla/5.0 Chrome/39.0.2171.71 Firefox/33.0'}

def mess(message, timeShown=5000,title=''):
	xbmc.executebuiltin((u'XBMC.Notification(%s,%s,%s,%s)'%('Xshare [COLOR green]%s[/COLOR]'%title,message,timeShown,icon['icon'])).encode("utf-8"))

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

def joinpath(p1,p2):
	try:p=os.path.join(p1,p2)
	except:p=os.path.join(p1,str2u(p2))
	return p

def init_file():
	if not os.path.exists(xbmc.translatePath(myaddon.getAddonInfo('profile'))):
		os.mkdir(xbmc.translatePath(myaddon.getAddonInfo('profile')))
	for i in (datapath,iconpath,myfolder,subsfolder,tempfolder):
		if not os.path.exists(i):os.mkdir(i)
	xmlheader='<?xml version="1.0" encoding="utf-8">\n';p=datapath;q=myfolder
	for i in [(p,'search.xml'),(p,'hdvietnam.xml'),(p,'favourites.xml'),(q,'mylist.xml')]:
		if not os.path.isfile(joinpath(i[0],i[1])):
			if not makerequest(joinpath(i[0],i[1]),string=xmlheader,attr='w'):
				mess(u'Không tạo được file %s'%str2u(i[1]))

def xshare_group(object,group):
	return object.group(group) if object else ''

def delete_files(folder,mark='',temp='ok'):
	for file in os.listdir(folder):
		if os.path.isfile(joinpath(folder,file)) and (not mark or mark in file):
			try:os.remove(joinpath(folder,file))
			except:temp='';pass
	return temp

def endxbmc():xbmcplugin.endOfDirectory(int(sys.argv[1]))

def xbmcsetResolvedUrl(url,name=''):
	item=xbmcgui.ListItem(path=url)
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
	ok=True;name=re.sub(',|\|.*\||\||\<.*\>','',name)
	item=xbmcgui.ListItem(name,iconImage=img,thumbnailImage=img)
	query=menuContext(name,link,img,fanart,mode,query,item)
	item.setInfo(type="Video", infoLabels={"title":name})
	item.setProperty('Fanart_Image',fanart)
	u=sys.argv[0]+"?url="+urllib.quote_plus(link)+"&img="+urllib.quote_plus(img)+"&fanart="+urllib.quote_plus(fanart)+"&mode="+str(mode)+"&page="+str(page)+"&query="+query+"&name="+name
	if not isFolder:item.setProperty('IsPlayable', 'true')
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=item,isFolder=isFolder)
	return ok

def addirs(name,href,img='',fanart='',query=''):
	name=clean_string(name)
	if '18+' in name and myaddon.getSetting('phim18')=="false":return
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
		if str2u('Mục chia sẻ của') in str2u(name):name=color['trangtiep']+name+'[/COLOR]'
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
	return query

def makeContext(name,link,img,fanart,mode,query):
	make=query.split()[0]
	if make=='Rename':colo=color['fshare']
	elif make=='Remove':colo=color['hdvietnam']
	else:colo=color['trangtiep']
	context=colo+query+'[/COLOR]'
	p=(myaddon.getAddonInfo('id'),mode,name,link,img,fanart,make)
	cmd='RunPlugin(plugin://%s/?mode=%d&name=%s&url=%s&img=%s&fanart=%s&query=%s)'%(p)
	return context,cmd

def searchContext(name,link,img,fanart,mode):
	command=[(makeContext(name,link,img,fanart,9,'Rename item'))]
	command.append((makeContext(name,link,img,fanart,9,'Remove item')))
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


def make_request(url,headers={'User-Agent':'Mozilla/5.0 Chrome/39.0.2171.71 Firefox/33.0'},resp='b'):
	try:
		response = urlfetch.get(url,headers=headers)
		if resp=='o':resp=response
		else:
			if resp=='j':resp=response.json
			elif resp=='s':resp=response.status
			else:resp=response.body
			response.close()
		return resp
	except: 
		mess(u'[COLOR red]Lỗi kết nối tới: %s[/COLOR]'%xshare_group(re.search('//(.+?)/',str2u(url)),1))
		print 'Make Request Error: %s'%url;resp=''
	return resp#unicode:body=response.text

def make_post(url,headers={'User-Agent':'Mozilla/5.0 Chrome/39.0.2171.71 Firefox/33.0'},data=''):
	try:
		if data:response=urlfetch.post(url=url,headers=headers,data=data)
		else:response=urlfetch.post(url=url,headers=headers)
	except:mess(u'Không truy cập được %s'%str2u(url));response=''
	return response

def makerequest(file,string='',attr='r'):
	file=str2u(file)
	if attr=='r':
		try:f=open(file);body=f.read();f.close()
		except:mess(u'Lỗi đọc file: %s'%str2u(os.path.basename(file)));body=''
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
	if int(response.getheaders()[0][1])<10485760:#size<10MB
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
		mess(u'Google: nghi ngờ lạm dụng Dịch vụ. Tự động chuyển sang web search',1000)
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
	pattern='<a server="(...)" category="(.+?)" mode="(..)" color="(.*?)" icon="(.*?)">(.+?)</a>'
	items=re.findall(pattern,makerequest(joinpath(data_path,'category.xml')))
	for server,category,mode,colo,icon,name in items:
		if (server!=query) or (("18" in category) and (myaddon.getSetting('phim18')=="false")):continue
		if query=='VPH' and mode!='10':q='vaphim.xml'
		elif query=='IFI' and mode!='10':q='ifiletv.xml'
		else:q=category
		name='[COLOR '+colo+']'+name+'[/COLOR]';icon=joinpath(iconpath,icon)
		addir(name,category,icon,home+'/fanart.jpg',mode=int(mode),page=0,query=q,isFolder=(mode!='16'))

def main_menu(category,page,mode,query): #Doc list tu vaphim.xml hoac ifiletv.xml
	items = doc_xml(joinpath(datapath,query),para=category);pages=len(items)/rows+1
	del items[0:page*rows];count=0;down=len(items)
	for id,img,fanart,href,name in items:
		down-=1;addirs(name,href,img,fanart);count+=1
		if count>rows and down>10:break
	if down>10:
		page+=1;name=color['trangtiep']+'Trang tiep theo...trang %d/%d[/COLOR]'%(page+1,pages)
		addir(name,category,icon['icon'],mode=mode,page=page,query=query,isFolder=True)


def clean_string(string):
	return ' '.join(s for s in re.sub('Fshare|-|4share|Tenlua|&.+?;','',string).split())

		
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
			if ('phimfshare' in url) or ('hdvietnam' in url):
				r='href="(.+?)" img="(.+?)">(.*%s.*)</a>'%para[7:];items=[]
				for href,img,name in re.compile(r, re.I).findall(no_accent(body)):
					items.append((img,img,href,name))
			else:
				r='img="(.*?)" fanart="(.*?)" href="(.+?)">(.*%s.*)</a>'%para[7:]
				items=re.compile(r, re.I).findall(no_accent(body))
		else:
			if not para:r='<a id_tip="(.*?)" id="(.+?)" category="(.*?)" img="(.*?)" fanart="(.*?)" href="(.+?)">(.+?)</a>'
			elif para=='post1': r='id="(.+?)"'
			else: #Doc theo category
				r='<a.*id="(.+?)" category=".*%s.*" img="(.*?)" fanart="(.*?)" href="(.+?)">(.+?)</a>'%para
			items = sorted(re.findall(r,body),key=lambda l:l[0], reverse=True)
	else:#Doc cac list xml khac
		r='<a.+id="(.*?)".+href="(.+?)".+img="(.*?)".+fanart="(.*?)".*>(.+?)</a>'
		items = re.compile(r).findall(body)
		if len(items)<1:items = re.findall('.+()href="(.+?)".+img="(.*?)".*()>(.+?)</a>',body)
		if len(items)<1:items = re.findall('.+()href="(.+?)".*()()>(.+?)</a>',body)
		if (copyxml=="true") and ('http' in url) and (len(items)>0) :
			filename=re.sub('\.xml.*','.xml',filename.replace('[COLOR orange]List xml[/COLOR]-',''))
			filename=re.sub('\[.{1,10}\]','',filename);f_fullpath=joinpath(myfolder,filename)
			if not os.path.isfile(f_fullpath):
				string='<?xml version="1.0" encoding="utf-8">\n'
				for id,href,img,fanart,name in items:
					string+='<a id="%s" href="%s" img="%s" fanart="%s">%s</a>\n'%(id,href,img,fanart,name)
				if makerequest(f_fullpath,string=string,attr='w'):
					mess(u'Đã tải file %s vào MyFolder'%str2u(filename))
	return items

def read_items_old(filename,id_old=[]):
	items_old = doc_xml(joinpath(datapath,filename))
	for i in items_old:id_old.append((i[1]))
	return items_old, id_old

def read_all_filexml(fn="vaphim.xml",string_search='',lists=[],index=[]):
	if string_search:lists = lists+doc_xml(joinpath(datapath,fn),para='search:'+string_search)
	else:lists = lists+doc_xml(joinpath(datapath,fn))
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

def data_download_fromFshare(data1,data2):
	pattern='href="(.+?)" title="%s"'%data1;href='https://www.fshare.vn/folder/GZCI8AHAQJ75'
	data=xshare_group(re.search(pattern,make_request(href)),1).replace('http:','https:')
	url=resolve_url(data,True);kq=''
	if url=='fail':
		pattern='href="(.+?)" title="%s"'%data2
		data=xshare_group(re.search(pattern,make_request(href)),1).replace('http:','https:')
		response=make_request(data,headers=hd,resp='o')
		if response.status==302:url=response.headers['location']
	if url!='fail':
		body=make_request(url)
		if body:
			tempfile = joinpath(tempfolder,os.path.basename(url))
			if os.path.splitext(tempfile)[1]=='.zip' and makerequest(tempfile,string=body,attr='wb'):
				xbmc.sleep(500);f1=tempfile.encode('utf-8');f2=tempfolder.encode('utf-8')
				try:xbmc.executebuiltin('XBMC.Extract("%s","%s")' % (f1,f2), True);kq='ok'
				except:pass
			elif makerequest(re.sub('-hot','',tempfile),string=body,attr='wb'):kq='ok'
	return kq

def data_download():
	delete_files(tempfolder);init_file();download=downloadresult=''
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
	def fptplay_2s(string):
		return ' '.join(re.sub('&.+;',xshare_group(re.search('&(\w).+;',s),1),s) for s in string.split())
	def fptplay_getlink(id,name,mode,dir=True):
		response=make_post('http://fptplay.net/show/getlink?id=%s&episode=1&mobile=web'%id)
		if response and dir:
			json=response.json;url = json['quality'][0]['url'][0]['url']
			img = json['quality'][0]['thumb'];title = json['quality'][0]['title']
			if len(json['quality'])==1:addir(name.strip(),url,img,img,mode=mode,query='play')
			else:addir(color['fptplay']+name.strip()+"[/COLOR]",id,img,img,mode=mode,query='FP4',isFolder=True)
		elif response:
			for i in response.json['quality']:
				url = i['url'][0]['url']
				img = i['thumb']
				title = re.sub('\[.{,20}\]','',name.strip())+' - '+i['title'].encode('utf-8')
				addir(title,url,img,img,mode=mode,query='play')

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
	elif query=="FPS":make_mySearch('',url,'','',mode,'get')
	elif query=="INP":
		query=make_mySearch('',url,'','','','Input')
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
		items=re.findall(pattern,make_request(url));temp=[]
		for href,name in items:
			if href not in temp:temp.append(href)
			else:continue
			name=color['fptplay']+fptplay_2s(name)+"[/COLOR]";id=xshare_group(re.search('(\w{22,26})',href),1)
			data='type=new&keyword=undefined&page=1&stucture_id=%s'%id;url='http://fptplay.net/show/more?%s'%data
			addir(name,url,icon["fptplay"],mode=mode,query="FP3",isFolder=True)
	elif query=="FP3":
		body=make_post(url).body
		if not body:mess(u'Lỗi get data từ fptplay.net');return 'no'
		items=re.findall('<a href=".+-(\w+)\.html".+class="title">(.+?)</a>',body)
		for id,title in items:fptplay_getlink(id,fptplay_2s(title),mode)
		if len(items)>35:
			page=xshare_group(re.search('page=(\d{1,3})',url),1);page=str(int(page)+1);
			url=re.sub('page=\d{1,3}','page='+page,url)
			name=color['trangtiep']+"Trang tiếp theo - Trang %s[/COLOR]"%page
			addir(name,url,icon["fptplay"],mode=mode,query="FP3",isFolder=True)
		elif not items:mess(u'Không tìm thấy dữ liệu');return 'no'
	elif query=="FP4":fptplay_getlink(url,name,mode,dir=False)
	elif query=='play':xbmcsetResolvedUrl(url)
	return ''

def megabox(name,url,mode,page,query):
	home='http://phim.megabox.vn/'
	def megabox_load_menu(items,mode):
		for href,name,img in items:
			if 'megabox.vn/clip-' in href:continue
			if os.path.splitext(href)[1][1:].lower()=='m3u8':
				addir(name.strip(),href+'|'+urllib.urlencode(hd),img,img,mode=mode,query='MGP')
				continue
			try:
				response=make_request(href,resp='o')
				if response.status==301:body=make_request(response.headers['location'])
				elif response.status==200:body=response.body
				else:continue
			except:continue
			links=re.findall('<a onclick=.getListEps\((.+?)\).{,20} href=.{,25}>(.+?)</a>',body)
			if len(links)==1:
				for link in links:
					folder='http://phim.megabox.vn/content/ajax_episode?id=%s&start=%s'%(link[0].split(',')[0].strip(),link[0].split(',')[1].strip())
					name='%s%s[/COLOR]: Tập %s'%(color['megabox'],name.strip(),link[1])
					addir(name,folder,img,img,mode=mode,query=os.path.dirname(href),isFolder=True)
			else:
				link=xshare_group(re.search("changeStreamUrl\('(.+?)'\)",body),1)
				if link:addir(name.strip(),link+'|'+urllib.urlencode(hd),img,img,mode=mode,query='MGP')
				else:addir(color['megabox']+name.strip()+'[/COLOR]',href,img,img,mode=mode,query='MG2',isFolder=True)

	if query=='megabox.vn':make_mySearch('',url,'','',mode,'get')
	elif query=="INP":
		query=make_mySearch('',url,'','','','Input')
		if query:return megabox(query,url,mode,page,query)
		else:return 'no'
	elif query==name:
		search_string = urllib.quote_plus(query)
		body=make_post('http://phim.megabox.vn/tim-kiem?keyword=%s'%search_string).body;items=[]
		if not body:return 'no'
		pattern='a class=".+?" href="(.+?)".*<h3 class=.H3title.>(.+?)</h3>.*\s.*src="(.+?)"|<div class="gb-view-all">.?<a href="(.+?)">(.+?)</a>'
		links=re.findall(pattern,body)
		if not links:mess(u'Không tìm thấy dữ liệu phù hợp');return 'no'
		for href,name,img,link,title in links:
			if not link:items.append((href,name,img))
			else:
				megabox_load_menu(items,mode);items=[]
				if 'phim-le' in link:title=color['search']+title+' - phim lẻ[/COLOR]'
				else:title=color['search']+title+' - phim bộ[/COLOR]'
				addir(title,link,icon['megabox'],mode=mode,query="MG4",isFolder=True)
		if items:megabox_load_menu(items,mode)
	elif query in 'MGL-MGS':
		href='http://phim.megabox.vn/phim-le' if query=='MGL' else 'http://phim.megabox.vn/phim-bo'
		body=make_request(href)
		if url in 'MGL-MGS':
			body=body[body.find('<ul id="gen">'):body.find('<ul id="country">')]
			name=color['megabox']+'Tất cả thể loại[/COLOR]'
			addir(name,'MGQ',icon['megabox'],mode=mode,page=0,query="MGL",isFolder=True)
			for value,name in re.findall("<li value='(\d{1,2})' >(.+?)</li>",body):
				name=color['megabox']+name+'[/COLOR]'
				addir(name,'MGQ',icon['megabox'],mode=mode,page=int(value),query=query,isFolder=True)
		elif url=='MGQ':
			body=body[body.find('<ul id="country">'):body.find('<ul id="other">')]
			name=color['megabox']+'Tất cả Quốc gia[/COLOR]'
			url=href+'?cat=1&gen=%d'%page
			addir(name,url,icon['megabox'],mode=mode,query="MG4",isFolder=True)
			for value,name in re.findall("<li value='(\d{1,2})' >(.+?)</li>",body):
				name=color['megabox']+name+'[/COLOR]'
				url=href+'?cat=1&gen=%d&country=%s'%(page,value)
				addir(name,url,icon['megabox'],mode=mode,page=int(value),query="MG4",isFolder=True)
	elif query=='MGB':
		body=make_request(home,headers=hd);open_category("MGB")
		for href,name in re.findall('<li><a href="(.+?)" title="">(.+?)</a></li>',body):
			if 'Clip' in name:continue
			addir(color['megabox']+name+'[/COLOR]',href,icon['megabox'],mode=mode,query='MG4',isFolder=True)
	elif query=='MG0':
		body=make_request(home)
		for name in re.findall('"H2title">(.+?)</h2>',body):
			if 'Phim sắp chiếu' in name or 'clip' in name:continue
			if 'Phim Lẻ Mới Nhất' in name:
				content=make_request('http://phim.megabox.vn/ajaxschedule/home/?data=1',resp='j')
				href=re.search('"H2title"><a href="(.+?)" title="">(.+?)</h2>',content['event'].encode('utf-8'))
				if href:
					title=color['megabox']+xshare_group(href,2)+'[/COLOR]'
					addir(title,xshare_group(href,1),icon['megabox'],mode=mode,query='MG1',isFolder=True)
			href=re.search('href="(.+?)">(.+?)</a>',name)
			if not href:
				name=color['megabox']+re.sub('<.{,4}>','',name)+'[/COLOR]'
				addir(name,home,icon['megabox'],home,mode=mode,query='MG1',isFolder=True)
			else:
				name=color['megabox']+xshare_group(href,2)+'[/COLOR]'
				addir(name,xshare_group(href,1),icon['megabox'],mode=mode,query='MG1',isFolder=True)
	elif query=='MG1':
		if home not in url:url=home+url
		body=make_request(url)
		if 'megabox' in name.lower():
			#pattern="<li><a href='(.+?)'.?><img src='(.+?)' alt='Banner - (.+?)''.?></a>"
			pattern="<li><a href='(.+?)'.?><img src='(.+?)'.+?<a href='.+?'>(.+?)</a>"
			items1=re.findall(pattern,body);items=[]
			for href,img,name in items1:items.append((href,name,img))
			megabox_load_menu(items,mode)
		elif 'top 10 phim' in name.lower():
			pattern='<a class="tooltip thumb" href="(.+?)".+<h3 class=.H3title.>(.+?)</h3>.*\s.*<img src="(.+?)"'
			megabox_load_menu(re.findall(pattern,body),mode)
		elif 'xem' in name.lower():#xem nhieu nhat
			pattern='<a class=.thumb. title="" href="(.+?)">.*\s.*<img alt=.Poster (.+?). src="(.+?)"/>'
			items=re.findall(pattern,body)
			if 'phim le' in no_accent(name).lower():del items[20:]
			elif 'phim bo' in no_accent(name).lower():del items[:20];del items[20:]
			elif 'show' in no_accent(name).lower():
				temp=[]
				for i in items:
					if 'megabox.vn/show' in i[0]:temp.append((i))
				items=temp
			megabox_load_menu(items,mode)
		elif url!=home:
			pattern='a class=".+?" href="(.+?)".*<h3 class=.H3title.>(.+?)</h3>.*\s.*src="(.+?)"'
			megabox_load_menu(re.findall(pattern,body),mode)
	elif query=='MG2':
		body=make_request(url)
		if '/tag/' in url:
			pattern='href="(.+?)".+<h3 class=.H3title.>(.+?)</h3>.*\s.*src="(.+?)"'
			megabox_load_menu(re.findall(pattern,body),mode)
		else:
			img=xshare_group(re.search('<img alt=.+? src="(.+?)"/>',body),1)
			links=re.findall('<a onclick=.getListEps\((.+?)\).{,20} href=.{,25}>(.+?)</a>',body)
			for link in links:
				href='http://phim.megabox.vn/content/ajax_episode?id=%s&start=%s'%(link[0].split(',')[0].strip(),link[0].split(',')[1].strip())
				title='%s Tập: %s'%(name,link[1].encode('utf-8'))
				addir(title,href,img,img,mode=mode,query=os.path.dirname(url),isFolder=True)
	elif query=='MG3':
		tap=xshare_group(re.search('(\d{1,3}-\d{1,3})',name),1)
		if tap:
			for i in range(int(tap.split('-')[0]),int(tap.split('-')[1])+1):
				addir(re.sub('Banner - ','',name),link+'|'+urllib.urlencode(hd),img,img,mode=mode,query='MGP')
		body=make_request(url)
		img=xshare_group(re.search('<img alt=.+? src="(.+?)"/>',body),1)
		links=re.findall('<a onclick=.+?>(.+?)</a>',body)
		for link in links:
			addir(name+': Tập %s'%link,url,img,img,mode=mode,query='MG3',isFolder=True)
	elif query=='MG4':
		if home not in url:url=home+url
		body=make_request(url)
		pattern='a class=".+?" href="(.+?)".*<h3 class=.H3title.>(.+?)</h3>.*\s.*src="(.+?)"'
		items=re.findall(pattern,body)
		if not items:mess(u'Không tìm thấy dữ liệu phù hợp');return 'no'
		megabox_load_menu(items,mode)
		page_control=re.findall('>(\d{,3})</a></li><li class="next"><a href="(.+?(\d{1,3}).*?)">|<li class="last"><a href=".+?(\d{1,3}).*?">',body)
		if len(page_control)==2:
			name=color['trangtiep']+u'Trang tiếp theo: trang %s/%s[/COLOR]'%(page_control[0][2],page_control[0][0])
			addir(name,page_control[0][1],mode=mode,query='MG4',isFolder=True)
		elif len(page_control)==4:
			name=color['trangtiep']+u'Trang tiếp theo: trang %s/%s[/COLOR]'%(page_control[0][2],page_control[1][3])
			addir(name,page_control[0][1],mode=mode,query='MG4',isFolder=True)
	elif query=='MGP':xbmcsetResolvedUrl(url)
	elif query=='MBP':
		response=make_request(url,resp='o')
		if response.status==200:
			link=xshare_group(re.search("changeStreamUrl\('(.+?)'\)",response.body),1)
		elif response.status==301:
			link=xshare_group(re.search("changeStreamUrl\('(.+?)'\)",make_request(response.headers['location'])),1)
		else:mess(u'Không get được megabox maxspeed link');return 'no' 
		xbmcsetResolvedUrl(link+'|'+urllib.urlencode(hd))
	elif len(query)>3:
		for item in make_request(url,resp='j'):
			name=item['name']
			img='http://img.phim.megabox.vn/728x409'+item['image_banner']
			href=query+'/%s-%s.html'%(item['cat_id'],item['content_id'])
			addir(name,href,img,img,mode=mode,query='MBP')
	return ''

def hdviet(name,url,img,mode,page,query):
	color['hdviet']='[COLOR darkorange]';icon['hdviet']=os.path.join(iconpath,'hdviet.png')
	home='http://movies.hdviet.com/';direct_link='https://api-v2.hdviet.com/movie/play?movieid=%s'
	def namecolor(name):return '%s%s[/COLOR]'%(color['hdviet'],name)
	def login():
		u=myaddon.getSetting('userhdviet');p=myaddon.getSetting('passhdviet')
		import hashlib;data=urllib.urlencode({'email':u,'password':hashlib.md5(p).hexdigest()})
		response=make_post('http://movies.hdviet.com/dang-nhap.html',hd,data)
		try:resp=response.json
		except:resp={u'r': u'Lỗi đăng nhập hdviet.com', u'e': 3}
		#mess(u'HDViet.com: '+resp['r'],1000);
		return (response.cookiestring if resp['e']==0 else '')
	def additems(body):
		links=re.findall('<a href="(.{,200})"><img src="(.+?)"(.+?)"h2-ttl3">(.+?)<span>(.+?)</span>',body)
		for link,img,temp,ttl3,title in links:
			title=ttl3.replace('&nbsp;','')+'-'+title
			isFolder=xshare_group(re.search('"labelchap2">(\d{1,3})</span>',temp),1)
			link=xshare_group(re.search('id="tooltip(\d{,10})"',temp),1).strip()
			if not isFolder:addir(title,link,img,fanart,mode,page,query='play')
			elif isFolder=='1':hdviet(title,link,img,mode,page,'folder')
			else:addir(namecolor(title),link,img,fanart,mode,page,query='folder',isFolder=True)
	def getResolvedUrl(id):
		response=make_request(direct_link%id,headers=hd,resp='j')
		return response['r'] if response else ''
	def hdviet_search(string):
		url='http://movies.hdviet.com/tim-kiem.html?keyword=%s'%urllib.quote(string)
		hdviet(name,url,img,mode,page,query='timkiem')
	if query=='hdviet.com':
		name=color['search']+"Search trên hdviet.com[/COLOR]"
		addir(name,'http://movies.hdviet.com/tim-kiem.html',icon['icon'],mode=mode,query='search',isFolder=True)
		body=make_request(home)
		items=re.findall('"mainitem" menuid="(.+?)" href="(.+?)" title=".+?">(.+?)</a>',body)
		for id,href,name in items:
			addir(namecolor(name),home,icon['hdviet'],fanart,mode,page,query=id,isFolder=True)
		addir(namecolor('Thể loại phim'),'the-loai',icon['icon'],mode=mode,query='the-loai-phim',isFolder=True)
		items=re.findall('"h2-ttl cf">.+?<a href="(.+?)" title=".+?" >(.+?)</a>',body)
		tempbody=body[body.find('h2-ttl cf')+10:]
		for href,name in items:
			addir(namecolor(name),href,icon['hdviet'],fanart,mode,page,query='1',isFolder=True)
			subbody=tempbody[:tempbody.find('h2-ttl cf')];tempbody=tempbody[tempbody.find('h2-ttl cf')+10:]
			additems(subbody)
	elif query=='search':make_mySearch('','hdviet.com','','',mode,'get')
	elif query=="INP":hdviet_search(make_mySearch('',url,'','','','Input'))
	elif url=='hdviet.com':page=1 if 'Trang tiếp theo' not in name else page;hdviet_search(query)
	elif query=='the-loai-phim':
		for href,name in re.findall('<p><a href="(.+?)" title=".+?">(.+?)</a></p>',make_request(home)):
			addir(namecolor(name),href,icon['hdviet'],fanart,mode,page,query='theloai',isFolder=True)
	elif query=='3' and url==home:#Phim lẻ
		items=re.findall('<a href="(.+?)" .?menuid="(.+?)" .?title=".+?" >(.+?)</a>',make_request(home))
		for href,id,name in items:
			addir(namecolor(name),href,icon['hdviet'],fanart,mode,page,query=id,isFolder=True)
	elif query=='10' and url==home:#Phim bộ
		body=make_request(home)
		items=re.findall('<a href="(.+?)" menuid="(.+?)" title=".+?">(.+?)</a>',body)
		items+=re.findall('<a class="childparentlib" menuid="(.+?)" href="(.+?)" title=".+?">(\s.*.+?)</a>',body)
		for href,id,name in items:
			if 'au-my' in href:name='Phim bộ Âu Mỹ %s'%name.strip()
			elif 'hong-kong' in href:name='Phim bộ Hồng Kông %s'%name.strip()
			elif 'trung-quoc' in href:name='Phim bộ Trung Quốc %s'%name.strip()
			else:name='Phim bộ %s'%name.strip()
			if href in '38-39-40':temp=href;href=id;id=temp
			addir(namecolor(name),href,icon['hdviet'],fanart,mode,page,query=id,isFolder=True)
	elif query=='folder':
		href='http://movies.hdviet.com/lay-danh-sach-tap-phim.html?id=%s'%url
		response=make_request(href,resp='j')
		if not response:return
		for eps in range(1,int(response["Sequence"])+1):
			title='Tập %s/%s-%s'%(format(eps,'0%dd'%len(response['Episode'])),str(response['Episode']),re.sub('\[.?COLOR.{,12}\]','',name))
			addir(title,'%s_e%d'%(url,eps),img,fanart,mode,page,query='play')
	elif query=='play':
		links=getResolvedUrl(url);linksub='';maxspeedlink=''
		if not links:mess(u'[COLOR red]HDViet.com: Get link thất bại[/COLOR]');return
		link=re.sub('_320_480_','_320_1920_vip_',links['LinkPlay'])
		epi=xshare_group(re.search('/(\d{1,6}_e\d{1,4})_',link),1)
		if epi:link=link.replace(epi,url)
		href=link+'?audioindex=1' if myaddon.getSetting('hdvietaudio')=='true' else link
		allresolution=make_request(href)
		if len(allresolution)<100:
			href=link;allresolution=make_request(href)
			if len(allresolution)<100:mess(u'[COLOR red]HDViet.com: Get maxspeed link thất bại[/COLOR]');return
		hd['Cookie']=login();resolutions=['1920','1792','1280','1024','800','640','480']
		if not hd['Cookie']:resolution=4
		else:
			body=make_request('http://movies.hdviet.com/dang-ky-hdvip.html',headers=hd)
			maxresolution=myaddon.getSetting('hdvietresolution')
			if xshare_group(re.search('<span>HDVip</span>: (\d{1,3}) ngày</a>',body),1):
				resolution=0 if maxresolution=='1080' else 2
			else:resolution=3
		make_post('http://movies.hdviet.com/dang-xuat.html',headers=hd).close
		if resolution>2 and 'thai' not in myaddon.getSetting('userhdviet'):
			#mess(u'[COLOR red]Hãy gia hạn acc VIP để có độ phân giải tối đa nhé.[/COLOR]',title=u'HDViet thông báo')
			xbmc.sleep(5000)
		for res in range(resolution,len(resolutions)):
			maxspeedlink=xshare_group(re.search('(http.+%s.+)\s'%resolutions[res],allresolution),1)
			if maxspeedlink:break
		if not maxspeedlink: maxspeedlink=href
		try:linksub='xshare' if links["AudioExt"][0]['Label']==u'Thuyết Minh' else linksub
		except:pass
		if not linksub:
			for source in ['Subtitle','SubtitleExt','SubtitleExtSe']:
				try:
					linksub=links['%s'%source]['VIE']['Source']
					if linksub:
						ep1=xshare_group(re.search('/(e\d{1,3})/',linksub,re.I),1)
						ep2=xshare_group(re.search('_(e\d{1,3})_',maxspeedlink,re.I),1)
						if ep1 and ep2:linksub=linksub.replace(ep1,ep2.upper())
						if download_subs(linksub):break
				except:pass
		xbmcsetResolvedUrl(maxspeedlink,urllib.unquote(os.path.splitext(os.path.basename(linksub))[0]))
	else:
		body=make_request(url);body=body[body.find('box-movie-list'):body.find('h2-ttl cf')];additems(body)
		pages=re.findall('<li class=""><a href="(.+?)">(.+?)</a></li>',body[body.find('class="active"'):])
		if pages:
			pagenext=pages[0][1];pageend=pages[len(pages)-1][1]
			name='%sTrang tiếp theo: trang %s/%s[/COLOR]'%(color['trangtiep'],pagenext,pageend)
			addir(name,pages[0][0],img,fanart,mode,page,query,isFolder=True)

def hayhaytv(name,url,img,mode,page,query):
	color['hayhaytv']='[COLOR tomato]';icon['hayhaytv']=os.path.join(iconpath,'hayhaytv.png')
	home='http://www.hayhaytv.vn/';ajax=home+'ajax_hayhaytv.php'
	def namecolor(name):return '%s%s[/COLOR]'%(color['hayhaytv'],name)
	def login():
		u=myaddon.getSetting('userhayhay');p=myaddon.getSetting('passhayhay')
		data=urllib.urlencode({'email':u,'password':p,'remember_account':0})
		response=make_post('http://www.hayhaytv.vn/ajax_jsonp.php?p=jsonp_login',data=data)
		makerequest(joinpath(data_path,'hayhaytv.cookie'),response.cookiestring,attr="wb")
		return response.cookiestring
	def getmaxspeedlink(url,headers):
		body=make_request(url,headers=headers)
		id=xshare_group(re.search('FILM_ID\D{3,7}(\d{3,6})',body),1) if ".sub'" in body else ''
		url=xshare_group(re.search("initVideoUrl.+'(.+?)'",body),1)
		if 'cdnviet.com' not in url:url=xshare_group(re.search("initVideoUrlOld.+'(.+?)'",body),1)
		return url,id
	def getdata(id):#Đoạn code này sử dụng mã bảo mật từ add-on HayHayTV.vn
		url='https://www.fshare.vn/folder/5VNFUPO32P6F'
		hd=xshare_group(re.search('<title>.*xx(.+?)xx.*</title>',make_request(url)),1).split('-')
		data='device=xshare&secure_token=1.0&request='+urllib.quote('{"movie_id":"%s"}'%id)
		response=make_post('http://api.hayhaytv.vn/movie/movie_detail',{hd[0]:'%s %s'%(hd[1],hd[2])},data)
		try:json=response.json['data']
		except:json={}
		return json
	def getitems(body):
		p='<a data-tooltip.{,100}href="(.+?)".{,500}data-original="(.+?)".{,300}'
		p+='class="orange_color">(.+?)</span>.{,100}<span>(.*?)</span>'
		for href,img,name_e,name_v in re.findall(p,body,re.DOTALL):
			name=name_v+'-'+color['subscene']+name_e+'[/COLOR]' if name_v else name_e
			addir(name,href,img,fanart,mode,page,query='play')
	def hayhaytv_search(string):
		url='http://www.hayhaytv.vn/tim-kiem/%s/trang-1'%'-'.join(s for s in string.split())
		hayhaytv(name,url,img,mode,page=1,query='M3')

	if query=='hayhaytv.vn':
		name=color['search']+"Search trên hayhaytv.vn[/COLOR]"
		addir(name,'http://www.hayhaytv.vn/tim-kiem/',icon['icon'],mode=mode,query='search',isFolder=True)
		body=make_request(home)
		for href,name in re.findall('menu_fa_text.+?" href="(.+?)".*>(.+?)</a>',body):
			if name in 'PHIM LẺ-PHIM BỘ-SHOW':
				addir(namecolor(name),href,icon['hayhaytv'],fanart,mode,page,query='M1',isFolder=True)
		body=body[body.find('"title_h1_st1"'):body.find('"slider_box_sim slider_clip_box"')]
		items=re.findall('"title_h1_st1">.{,20}<a.{,20}href="(.+?)".{,20}>(.+?)</a>.{,20}</h2>',body,re.DOTALL)
		mucs={'su-kien':'q=su-kien&p=eventfilms&key=32386E61&page=1','phim-le':'p=phimle&page=1',
			'phim-bo':'p=phimbo&page=1','phim-chieu-rap':'p=phimle&phimchieurap&page=1','shows':'p=tvshow&page=1'}
		for href,name in items:
			muc=xshare_group(re.search('http://www.hayhaytv.vn/([\w|-]{1,20})',href),1)
			if muc and mucs[muc]:
				href='http://www.hayhaytv.vn/ajax_ht.php?'+mucs[muc] if 'su-kien' in href else ajax+'?'+mucs[muc]
				name=' '.join(s for s in name.replace('\n','').split() if s)
			else:name=name.replace('JJ','Just Japan')
			addir(namecolor(name),href,img,fanart,mode,page=1,query='M3' if 'su-kien' in href else 'M2',isFolder=True)
	elif query=='search':make_mySearch('','hayhaytv.vn','','',mode,'get')
	elif query=="INP":hayhaytv_search(make_mySearch('',url,'','','','Input'))
	elif url=='hayhaytv.vn':page=1 if 'Trang tiếp theo' not in name else page;hayhaytv_search(query)
	elif query=='M1':
		theloai=os.path.basename(url).replace('-','')
		if theloai=='shows':theloai='tvshow'
		body=make_request('http://www.hayhaytv.vn/tim-kiem');pattern='http.+/\w{1,6}-'
		body=body[body.find(url):];body=body[:body.find('mar-r20')]
		for href,name in re.findall('href="(.+?)".*?>(.+?)</a></li>',body):
			if href==url:href='%s?p=%s&page=1'%(ajax,theloai)
			else:id=re.sub(pattern,'',href);href='%s?p=%s&q=filter&id=%s&page=1'%(ajax,theloai,id)
			addir(namecolor(name),href,img,fanart,mode,page=1,query='M2',isFolder=True)
	elif query=='M2':
		if 'ajax' in url:
			body=make_post(re.sub('page=\d{1,3}','page=%d'%page,url)).body
			pattern='tooltip="(.+?)" href="(.+?)">\s.*"(http://img.+?)".*\s.*color">(.*?)<.*\s.*>(.*?)</span>'
			items=re.findall(pattern,body)
			ids=dict((re.findall('id="(sticky\d{1,3})".{,250}Số tập[\D]{,30}(\d{1,4})',body,re.DOTALL)))
			for stic,href,img,name_e,name_v in items:
				name=name_v+'-'+name_e if name_v else name_e
				if ids.has_key(stic) and ids[stic].strip()>'1':#? in ids.values()
					addir(namecolor(name),href,img,fanart,mode,page=1,query='folder'+ids[stic],isFolder=True)
				else:addir(name,href,img,fanart,mode,page,query='play')
			if len(items)>31 or ('p=tvshow' in url and len(items)>11):
				name='%sTrang tiếp theo: trang %s[/COLOR]'%(color['trangtiep'],page+1)
				addir(name,url,img,fanart,mode,page+1,query,isFolder=True)
			return
		elif 'jj' in url:#Just Japan
			pattern='href="(.+?)">\s.*src="(.+?)".*\s.*\s.*\s.*>(.*?)</a></p>\s.*>(.*?)</a></p>'
			for href,img,name_e,name_v in re.findall(pattern,make_request(url)):
				name=name_v+'-'+color['subscene']+name_e+'[/COLOR]' if name_v else name_e
				addir(name,href,img,fanart,mode,page,query='play')
	elif query=='M3':
		body=make_request(url);body=body[body.find('slide_child_div_dt'):];body=body[:body.find('class="paging"')]
		pattern='href="(.+?)".*\s.*alt="poster phim (.+?)" src="(.+?)"'
		items=re.findall(pattern,body)
		for href,name,img in items:
			if re.search('Tap-\d{1,3}',href):
				addir(namecolor(name),href,img,fanart,mode,page=1,query='folder',isFolder=True)
			else:addir(name,href,img,fanart,mode,page,query='play')
		if len(items)>14 or (len(items)>7 and 'su-kien' in url):
			temp='trang-' if 'trang-' in url else 'page=';url=re.sub('%s\d{1,3}'%temp,'%s%d'%(temp,page+1),url)
			name='%sTrang tiếp theo: trang %s[/COLOR]'%(color['trangtiep'],page+1)
			addir(name,url,img,fanart,mode,page+1,query,isFolder=True)
	elif query[:6]=='folder':
		if 'xem-show' in url:pattern='href="(.+?)".*src=".+?"\D*(\d{1,3})<'
		else:pattern='<a class=".*?" href="(.+?)"\D*(\d{1,3})<'
		resp=make_request(url,resp='o');body=resp.body if resp.status==200 else make_request(resp.headers['location'])
		items=re.findall(pattern,body)
		if not query[6:]:
			json=getdata(xshare_group(re.search('FILM_ID\D{3,7}(\d{3,6})',body),1))
			if json:query+=json['total_episode'].encode('utf-8')
		for href,epi in items:
			addir('Tập %s/%s-%s'%(epi,query[6:],re.sub('\[.?COLOR.{,12}\]','',name)),href,img,fanart,mode,page,query='play')
	elif query=='play':
		hd['Cookie']=makerequest(joinpath(data_path,'hayhaytv.cookie'))
		href,id=getmaxspeedlink(url,hd);sub=''
		if not href:hd['Cookie']=login();href,id=getmaxspeedlink(url,hd)
		if href:
			if id:
				json=getdata(id)
				if json:sub=download_subs(json['vn_subtitle'])
			xbmcsetResolvedUrl(href,json['vn_subtitle'] if sub else '')

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
try:mode=int(params["mode"])
except:pass
try:page=int(params["page"])
except:pass
try:query=urllib.unquote_plus(params["query"])
except:pass#urllib.unquote
print "Main---------- Mode: "+str(mode),"URL: "+str(url),"Name: "+str(name),"query: "+str(query),"page: "+str(page)

if not mode:
	init_file();open_category("FRE");endxbmc();
	#if myaddon.getSetting('checkdatabase')=='true' or os.path.isfile(joinpath(data_path,'checkdatabase.txt')):
		#data_download()
elif mode==2:end=google_search(url,query,mode,page)
elif mode==3:end=resolve_url(url)
elif mode==4:vp_phimmoi()
elif mode==5:vp_xemnhieu()
elif mode==6:end=phimFshare(name,url,mode,page,query)
elif mode==7:end=fptplay(name,url,img,mode,page,query)
elif mode==8:hdvietnam(name,url,img,fanart,mode,page,query)
elif mode==9:make_mySearch(name,url,img,fanart,mode,query)
elif mode==10:open_category(query);endxbmc();vp_make_datanew()
elif mode==11:make_myFshare(name,url,img,fanart,mode,query)
elif mode==12:make_mylist(name,url,img,fanart,mode,query)
elif mode==13:end=xshare_search(name,url,query,mode,page)
elif mode==15:end=id_2url(url,name,mode,page,query)
elif mode==16:end=play_maxspeed_link()
elif mode==17:end=megabox(name,url,mode,page,query)
elif mode==18:dangcaphd(name,url,img,mode,page,query)
elif mode==19:pubvn(name,url,img,mode,page,query)
elif mode==20:end=vp_update()
elif mode==21:vuahd(name,url,img,mode,page,query)
elif mode==22:hdviet(name,url,img,mode,page,query)
elif mode==23:hayhaytv(name,url,img,mode,page,query)
elif mode==31:end=ifile_update()
elif mode==34:ifile_home(name,url,img,mode,page,query)
elif mode==38:doc_Trang4share(url)#38
elif mode==47:daklak47(name,url,img)
elif mode==90:end=doc_TrangFshare(name,url,img,fanart,query)
elif mode==91:main_menu(url,page,mode,query)
elif mode==94:end=subscene(name,url,query)
elif mode==95:lay_link_tenlua(url)
elif mode==96:end=doc_thumuccucbo(name,url,img,fanart,mode,query)
elif mode==97:doc_list_xml(url,name,page)
elif mode==98:make_favourites(name,url,img,fanart,mode,query)
elif mode==99:myaddon.openSettings();end='ok'
if not end or end not in 'no-ok':endxbmc()
#https://urlfetch.readthedocs.org/en/v0.5.3/examples.html
#http://hdonline.vn/ 1.207 hhtv 2, fpt 4, hplus.com.vn 5, phimhd3s 8, 
#addir(name,url,img,fanart,mode,page,query,isFolder)
#addirs(name,href,img='',fanart='',query='')
#ID co pass: THZA19WGMT Pass: thanhcoti 8357 8490 9262 9580
#Nếu có thể bác làm thêm mấy Addons trả phí, có Acc và pass có đăng nhập như kiểu fshare cho mấy Apk hot như HDon, vuahd...
#mình thấy pub.vn cũng nhiều phim và đường truyền rất lẹ ,nên nếu làm được trang này thì hay hơn là vuahd đó
# add thêm phần phụ lục (WEB-DL, HDTV; Bluray Remux; mHD, SD; Bluray nguyên gốc) vào trong phần Chia sẻ phim - Fshare.vn
#acc VIP còn hạn đền tháng 11. bác kiểm tra giúp e nhé :
#mail : anhvustore1@gmail.com
#pass : anhvustore
