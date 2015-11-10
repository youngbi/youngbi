import xbmc, xbmcaddon, os

hayhaytv_vn = 'http://www.hayhaytv.vn/'
hdviet_com = 'http://movies.hdviet.com/'
dangcaphd_com = 'http://dangcaphd.com/'
megabox_vn = 'http://phim.megabox.vn/'
phimgiaitri_vn = 'http://phimgiaitri.vn/'
phimmoi_net = 'http://www.phimmoi.net/'

#url = 'http://api.vietmedia.kodi.vn/play/v1/tivi/play/2'	#vietmedia play
#url = 'http://api.vietmedia.kodi.vn/xmio/v1/play/2'		#vietmedia movie
hdonlinevn = 'http://api.vietmedia.kodi.vn/hho/v1/play/'
megaboxvn = 'http://api.vietmedia.kodi.vn/mb/v1/play/'
vuahdtv = 'http://api.vietmedia.kodi.vn/play/v1/vuahd/play/'
#phimgiaitrivn = 'http://api.vietmedia.kodi.vn/pgt/v1/play/'
phimmoinet = 'http://api.vietmedia.kodi.vn/pm/v1/play/'

home = xbmc.translatePath(xbmcaddon.Addon().getAddonInfo('path')).decode("utf-8")
logos = xbmc.translatePath(os.path.join(home,"logos\\"))
dataPath = xbmc.translatePath(os.path.join(home, 'resources'))
csn = 'http://chiasenhac.com/'
csn_logo ='http://chiasenhac.com/images/logo_csn_300x300.jpg'
nct = 'http://m.nhaccuatui.com/'
nct_logo ='http://stc.id.nixcdn.com/10/images/logo_600x600.png'

www={'hdonline':'[hdonline.vn]','vuahd':'[vuahd.tv]','hdviet':'[http://movies.hdviet.com/]','hayhaytv':'[http://www.hayhaytv.vn/]','dangcaphd':'[http://dangcaphd.com/]','megabox':'[http://phim.megabox.vn/]','phimmoi':'[vuahd.tv]','hdcaphe':'[http://phim.hdcaphe.com/]','phimgiaitri':'[http://phimgiaitri.vn/]'}
color={'trangtiep':'[COLOR lime]','cat':'[COLOR green]','search':'[COLOR red]','phimbo':'[COLOR tomato]','phimle':'[COLOR yellow]'};icon={}
