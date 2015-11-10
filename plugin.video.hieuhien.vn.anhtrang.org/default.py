#!/usr/bin/python
# -*- coding: utf-8 -*-
import urllib , urllib2 , re , zlib , os
from xbmcswift2 import Plugin , xbmc , xbmcgui , xbmcaddon
from operator import itemgetter
oo000 = Plugin ( )
ii = "plugin://plugin.video.hieuhien.vn.anhtrang.org"
oOOo = 24
if 59 - 59: Oo0Ooo . OO0OO0O0O0 * iiiIIii1IIi . iII111iiiii11 % I1IiiI
@ oo000 . route ( '/' )
def IIi1IiiiI1Ii ( ) :
 I11i11Ii ( "None" , "None" )
 oO00oOo = xbmc . translatePath ( xbmcaddon . Addon ( ) . getAddonInfo ( 'path' ) ) . decode ( "utf-8" )
 oO00oOo = xbmc . translatePath ( os . path . join ( oO00oOo , "temp.jpg" ) )
 # urllib . urlretrieve ( 'https://googledrive.com/host/0B-ygKtjD8Sc-S04wUUxMMWt5dmM/images/anhtrang.jpg' , oO00oOo )
 # OOOo0 = xbmcgui . ControlImage ( 0 , 0 , 1280 , 720 , oO00oOo )
 # Oooo000o = xbmcgui . WindowDialog ( )
 # Oooo000o . addControl ( OOOo0 )
 # Oooo000o . doModal ( )
 # IiIi11iIIi1Ii = ""
 # Oo0O = ( "Busy" , "Bận" , "Band" , "Beschäftigt" , "Bezig" , "忙" , "忙碌" )
 # while True :
  # IiI = urllib . quote ( xbmc . getInfoLabel ( "System.KernelVersion" ) . strip ( ) )
  # if not any ( b in IiI for b in Oo0O ) : break
 # while True :
  # ooOo = urllib . quote ( xbmc . getInfoLabel ( "System.FriendlyName" ) . strip ( ) )
  # if not any ( b in ooOo for b in Oo0O ) : break
 # try :
  # IiIi11iIIi1Ii = open ( '/sys/class/net/eth0/address' ) . read ( ) . strip ( )
 # except :
  # while True :
   # IiIi11iIIi1Ii = xbmc . getInfoLabel ( "Network.MacAddress" ) . strip ( )
   # if re . match ( "[0-9a-f]{2}([-:])[0-9a-f]{2}(\\1[0-9a-f]{2}){4}$" , IiIi11iIIi1Ii . lower ( ) ) : break
 # Oo = urllib2 . urlopen ( "http://www.viettv24.com/main/checkActivation.php?MacID=%s&app_id=%s&sys=%s&dev=%s" % ( IiIi11iIIi1Ii , "2" , IiI , ooOo ) ) . read ( )
 if True:
  o0O = [
 { 'label' : 'Phim mới' , 'path' : '%s/latest/%s/%s' % ( ii , urllib . quote_plus ( 'http://phim.anhtrang.org/danh-sach/new/trang-%s.html' ) , 1 ) } ,
 { 'label' : 'Phim HD' , 'path' : '%s/hd/%s/%s' % ( ii , urllib . quote_plus ( 'http://phim.anhtrang.org/danh-sach/phim-hd/trang-%s.html' ) , 1 ) } ,
 { 'label' : 'Thể loại' , 'path' : '%s/genres' % ii } ,
 { 'label' : 'Quốc gia' , 'path' : '%s/nations' % ii } ,
 { 'label' : 'Tìm kiếm' , 'path' : '%s/search' % ii }
 ]
  return oo000 . finish ( o0O )
 else :
  IiiIII111iI = xbmcgui . Dialog ( )
  IiiIII111iI . ok ( "Chú ý" , Oo )
  if 34 - 34: iii1I1I / O00oOoOoO0o0O . O0oo0OO0 + Oo0ooO0oo0oO . I1i1iI1i - II
  if 100 - 100: i11Ii11I1Ii1i . ooO - OOoO / ooo0Oo0 * i1 - OOooo0000ooo
@ oo000 . route ( '/latest/<murl>/<page>' )
def OOo000 ( murl , page ) :
 I11i11Ii ( "Browse" , '/latest/%s/%s' % ( murl , page ) )
 o0O = O0 ( murl , page , 'latest' )
 if xbmc . getSkinDir ( ) == 'skin.xeebo' and oo000 . get_setting ( 'thumbview' , bool ) :
  return oo000 . finish ( o0O , view_mode = 52 )
 else :
  return oo000 . finish ( o0O )
  if 34 - 34: O0o00 % o0ooo / OOO0O / iiiIIii1IIi * iII111iiiii11 * OOO0O
@ oo000 . route ( '/hd/<murl>/<page>' )
def i1iIIII ( murl , page ) :
 I11i11Ii ( "Browse" , '/hd/%s/%s' % ( murl , page ) )
 o0O = O0 ( murl , page , 'hd' )
 if xbmc . getSkinDir ( ) == 'skin.xeebo' and oo000 . get_setting ( 'thumbview' , bool ) :
  return oo000 . finish ( o0O , view_mode = 52 )
 else :
  return oo000 . finish ( o0O )
  if 26 - 26: o0ooo . ooo0Oo0 - OOoO % OO0OO0O0O0 + OOoO
@ oo000 . route ( '/genres' )
def i1iiIIiiI111 ( ) :
 I11i11Ii ( "Browse" , '/genres/' )
 o0O = [
 { 'label' : 'Hài Hước' , 'path' : '%s/genres/%s/%s' % ( ii , urllib . quote_plus ( 'http://phim.anhtrang.org/the-loai/hai-huoc-1/trang-%s.html' ) , 1 ) } ,
 { 'label' : 'Hành Động' , 'path' : '%s/genres/%s/%s' % ( ii , urllib . quote_plus ( 'http://phim.anhtrang.org/the-loai/hanh-dong-2/trang-%s.html' ) , 1 ) } ,
 { 'label' : 'Võ Thuật' , 'path' : '%s/genres/%s/%s' % ( ii , urllib . quote_plus ( 'http://phim.anhtrang.org/the-loai/vo-thuat-8/trang-%s.html' ) , 1 ) } ,
 { 'label' : 'Viễn Tưởng' , 'path' : '%s/genres/%s/%s' % ( ii , urllib . quote_plus ( 'http://phim.anhtrang.org/the-loai/vien-tuong-3/trang-%s.html' ) , 1 ) } ,
 { 'label' : 'Tâm Lý - Tình Cảm' , 'path' : '%s/genres/%s/%s' % ( ii , urllib . quote_plus ( 'http://phim.anhtrang.org/the-loai/tam-ly-tinh-cam-4/trang-%s.html' ) , 1 ) } ,
 { 'label' : 'Kinh Dị' , 'path' : '%s/genres/%s/%s' % ( ii , urllib . quote_plus ( 'http://phim.anhtrang.org/the-loai/kinh-di-5/trang-%s.html' ) , 1 ) } ,
 { 'label' : 'Hoạt Hình' , 'path' : '%s/genres/%s/%s' % ( ii , urllib . quote_plus ( 'http://phim.anhtrang.org/the-loai/hoat-hinh-6/trang-%s.html' ) , 1 ) } ,
 { 'label' : 'Chiến Tranh' , 'path' : '%s/genres/%s/%s' % ( ii , urllib . quote_plus ( 'http://phim.anhtrang.org/the-loai/chien-tranh-13/trang-%s.html' ) , 1 ) } ,
 { 'label' : 'Thể Thao - Âm Nhạc' , 'path' : '%s/genres/%s/%s' % ( ii , urllib . quote_plus ( 'http://phim.anhtrang.org/the-loai/the-thao-am-nhac-12/trang-%s.html' ) , 1 ) } ,
 { 'label' : 'Hình Sự' , 'path' : '%s/genres/%s/%s' % ( ii , urllib . quote_plus ( 'http://phim.anhtrang.org/the-loai/hinh-su-15/trang-%s.html' ) , 1 ) } ,
 { 'label' : 'Phiêu Lưu' , 'path' : '%s/genres/%s/%s' % ( ii , urllib . quote_plus ( 'http://phim.anhtrang.org/the-loai/phieu-luu-14/trang-%s.html' ) , 1 ) } ,
 { 'label' : 'Cổ Trang' , 'path' : '%s/genres/%s/%s' % ( ii , urllib . quote_plus ( 'http://phim.anhtrang.org/the-loai/co-trang-16/trang-%s.html' ) , 1 ) } ,
 { 'label' : 'Tư Liệu - Lịch Sử' , 'path' : '%s/genres/%s/%s' % ( ii , urllib . quote_plus ( 'http://phim.anhtrang.org/the-loai/tu-lieu-lich-su-11/trang-%s.html' ) , 1 ) } ,
 { 'label' : 'Hài kịch - Clip hài' , 'path' : '%s/genres/%s/%s' % ( ii , urllib . quote_plus ( 'http://phim.anhtrang.org/the-loai/hai-kich-clip-hai-10/trang-%s.html' ) , 1 ) } ,
 { 'label' : 'Kinh Điển' , 'path' : '%s/genres/%s/%s' % ( ii , urllib . quote_plus ( 'http://phim.anhtrang.org/the-loai/kinh-dien-7/trang-%s.html' ) , 1 ) } ,
 { 'label' : 'Sân Khấu - Cải Lương' , 'path' : '%s/genres/%s/%s' % ( ii , urllib . quote_plus ( 'http://phim.anhtrang.org/the-loai/san-khau-cai-luong-9/trang-%s.html' ) , 1 ) }
 ]
 return oo000 . finish ( o0O )
 if 62 - 62: Oo0Ooo - iii1I1I
@ oo000 . route ( '/genres/<murl>/<page>' )
def IIIiI11ii ( murl , page = 1 ) :
 I11i11Ii ( "Browse" , '/genres/%s/%s' % ( murl , page ) )
 o0O = O0 ( murl , page , 'genres' )
 if xbmc . getSkinDir ( ) == 'skin.xeebo' and oo000 . get_setting ( 'thumbview' , bool ) :
  return oo000 . finish ( o0O , view_mode = 52 )
 else :
  return oo000 . finish ( o0O )
  if 52 - 52: OOooo0000ooo + OOoO % iII111iiiii11 / Oo0Ooo
@ oo000 . route ( '/nations' )
def iiIIi1IiIi11 ( ) :
 I11i11Ii ( "Browse" , '/nations' )
 o0O = [
 { 'label' : 'Việt Nam' , 'path' : '%s/nations/%s/%s' % ( ii , urllib . quote_plus ( 'http://phim.anhtrang.org/quoc-gia/viet-nam-3/trang-%s.html' ) , 1 ) } ,
 { 'label' : 'Trung Quốc' , 'path' : '%s/nations/%s/%s' % ( ii , urllib . quote_plus ( 'http://phim.anhtrang.org/quoc-gia/trung-quoc-4/trang-%s.html' ) , 1 ) } ,
 { 'label' : 'Hàn Quốc' , 'path' : '%s/nations/%s/%s' % ( ii , urllib . quote_plus ( 'http://phim.anhtrang.org/quoc-gia/han-quoc-5/trang-%s.html' ) , 1 ) } ,
 { 'label' : 'Nhật Bản' , 'path' : '%s/nations/%s/%s' % ( ii , urllib . quote_plus ( 'http://phim.anhtrang.org/quoc-gia/nhat-ban-6/trang-%s.html' ) , 1 ) } ,
 { 'label' : 'Mỹ - Châu Âu' , 'path' : '%s/nations/%s/%s' % ( ii , urllib . quote_plus ( 'http://phim.anhtrang.org/quoc-gia/my-chau-au-7/trang-%s.html' ) , 1 ) } ,
 { 'label' : 'Châu Á' , 'path' : '%s/nations/%s/%s' % ( ii , urllib . quote_plus ( 'http://phim.anhtrang.org/quoc-gia/chau-a-8/trang-%s.html' ) , 1 ) } ,
 { 'label' : 'Ấn Độ' , 'path' : '%s/nations/%s/%s' % ( ii , urllib . quote_plus ( 'http://phim.anhtrang.org/quoc-gia/an-do-9/trang-%s.html' ) , 1 ) }
 ]
 return oo000 . finish ( o0O )
 if 11 - 11: OOO0O / OO0OO0O0O0 - I1IiiI
@ oo000 . route ( '/nations/<murl>/<page>' )
def o00O00O0O0O ( murl , page ) :
 I11i11Ii ( "Browse" , '/nations/%s/%s' % ( murl , page ) )
 o0O = O0 ( murl , page , 'nations' )
 if xbmc . getSkinDir ( ) == 'skin.xeebo' and oo000 . get_setting ( 'thumbview' , bool ) :
  return oo000 . finish ( o0O , view_mode = 52 )
 else :
  return oo000 . finish ( o0O )
  if 90 - 90: iii1I1I + ooO / II % iii1I1I - OO0OO0O0O0
@ oo000 . route ( '/search/' )
def iIii1 ( ) :
 I11i11Ii ( "Browse" , '/search/' )
 oOOoO0 = oo000 . keyboard ( heading = 'Tìm kiếm' )
 if oOOoO0 :
  O0OoO000O0OO = "http://phim.anhtrang.org/tim-kiem/keyword/1/trang-%s.html" . replace ( "keyword" , oOOoO0 ) . replace ( " " , "-" )
  iiI1IiI = '%s/search/%s/%s' % ( ii , urllib . quote_plus ( O0OoO000O0OO ) , 1 )
  oo000 . redirect ( iiI1IiI )
  if 13 - 13: O0oo0OO0 . Oo0Ooo - iiiIIii1IIi - I1i1iI1i
@ oo000 . route ( '/search/<murl>/<page>' )
def ii1I ( murl , page ) :
 I11i11Ii ( "Browse" , '/search/%s/%s' % ( murl , page ) )
 o0O = O0 ( murl , page , 'search' )
 if xbmc . getSkinDir ( ) == 'skin.xeebo' and oo000 . get_setting ( 'thumbview' , bool ) :
  return oo000 . finish ( o0O , view_mode = 52 )
 else :
  return oo000 . finish ( o0O )
  if 76 - 76: OO0OO0O0O0 / II . O00oOoOoO0o0O * i1 - OOoO
@ oo000 . route ( '/mirrors/<murl>' )
def Oooo ( murl ) :
 I11i11Ii ( "Browse" , '/mirrors/%s' % ( murl ) )
 o0O = [ ]
 for O00o in O00 ( murl ) :
  i11I1 = { }
  i11I1 [ "label" ] = O00o [ "name" ] . strip ( ": " )
  i11I1 [ "path" ] = '%s/eps/%s' % ( ii , urllib . quote_plus ( O00o [ "eps" ] ) )
  o0O . append ( i11I1 )
 return oo000 . finish ( o0O )
 if 8 - 8: iiiIIii1IIi - O0o00 % iiiIIii1IIi - i1 * O00oOoOoO0o0O
@ oo000 . route ( '/eps/<eps_list>' )
def iI11i1I1 ( eps_list ) :
 I11i11Ii ( "Browse" , '/eps/' )
 Oo = o0o0OOO0o0 ( eps_list )
 ooOOOo0oo0O0 = re . compile ( '&file=/xml.php\?id=(\d+)' ) . findall ( Oo ) [ 0 ]
 Oo = o0o0OOO0o0 ( "http://phim.anhtrang.org/xml.php?id=%s" % ooOOOo0oo0O0 )
 o0 = re . compile ( "<item><title>(.+?)</title>" ) . findall ( Oo ) [ 0 ]
 o0O = [ ]
 for I11II1i in re . compile ( '<item>(.+?)</item>' ) . findall ( Oo ) :
  IIIII = re . compile ( "(\w+)-\w+.html" ) . findall ( I11II1i ) [ 0 ]
  i11I1 = { }
  if IIIII . isdigit ( ) :
   i11I1 [ "label" ] = "Part %03d - %s" % ( int ( IIIII ) , o0 )
  else :
   ooooooO0oo = re . split ( "(\d+)" , IIIII . strip ( ) )
   if len ( ooooooO0oo ) > 1 :
    i11I1 [ "label" ] = "Part %03d%s - %s" % ( int ( ooooooO0oo [ 1 ] ) , ooooooO0oo [ 2 ] , o0 )
   else :
    i11I1 [ "label" ] = "Part %s - %s" % ( ooooooO0oo [ 0 ] , o0 )
    if 49 - 49: II * iiiIIii1IIi / I1IiiI / Oo0Ooo / II
  i11I1 [ "is_playable" ] = True
  iiI1IiI = re . compile ( "<jwplayer:[h]*[d]*[.]*file\d*>(.+?)</jwplayer:[h]*[d]*[.]*file\d*>" ) . findall ( I11II1i )
  if oo000 . get_setting ( 'HQ' , bool ) :
   i11I1 [ "path" ] = '%s/play/%s' % ( ii , urllib . quote_plus ( iiI1IiI [ - 1 ] ) )
  else :
   i11I1 [ "path" ] = '%s/play/%s' % ( ii , urllib . quote_plus ( iiI1IiI [ 0 ] ) )
  o0O . append ( i11I1 )
 o0O = sorted ( o0O , key = itemgetter ( 'label' ) )
 return oo000 . finish ( o0O )
 if 28 - 28: OOoO - O0o00 . O0o00 + I1i1iI1i - iII111iiiii11 + OO0OO0O0O0
@ oo000 . route ( '/play/<url>' )
def oOoOooOo0o0 ( url ) :
 I11i11Ii ( "Play" , '/play/%s' % ( url ) )
 OOOO = xbmcgui . DialogProgress ( )
 OOOO . create ( 'Hieuhien.vn' , 'Loading video. Please wait...' )
 oo000 . set_resolved_url ( OOO00 ( url ) )
 OOOO . close ( )
 del OOOO
 if 21 - 21: iII111iiiii11 - iII111iiiii11
def OOO00 ( url ) :
 if "youtube" in url :
  ooOOOo0oo0O0 = re . compile ( '(youtu\.be\/|youtube-nocookie\.com\/|youtube\.com\/(watch\?(.*&)?v=|(embed|v|user)\/))([^\?&"\'>]+)' ) . findall ( url )
  iIii11I = ooOOOo0oo0O0 [ 0 ] [ len ( ooOOOo0oo0O0 [ 0 ] ) - 1 ] . replace ( 'v/' , '' )
  return 'plugin://plugin.video.youtube/?action=play_video&videoid=%s' % iIii11I
 if "picasa" in url :
  return url
  if 69 - 69: ooO % o0ooo - II + o0ooo - OO0OO0O0O0 % iII111iiiii11
def O0 ( url , page , route_name ) :
 Iii111II = int ( page ) + 1
 Oo = o0o0OOO0o0 ( url % page )
 ooOOOo0oo0O0 = re . compile ( '<div class="poster">(.*?)<a href="(.+?)" title="(.+?)"><img src="(.+?)"[^>]*/>' ) . findall ( Oo )
 o0O = [ ]
 for iiii11I , Ooo0OO0oOO , o0 , ii11i1 in ooOOOo0oo0O0 :
  i11I1 = { }
  i11I1 [ "label" ] = "%s (%s)" % ( o0 , iiii11I . replace ( '<span class="process"><span>' , "" ) . replace ( "</span></span>" , "" ) )
  i11I1 [ "thumbnail" ] = ii11i1 . replace ( "http://" , "https://" )
  i11I1 [ "path" ] = '%s/%s/%s' % ( ii , "mirrors" , urllib . quote_plus ( Ooo0OO0oOO ) )
  o0O . append ( i11I1 )
 if len ( o0O ) == oOOo :
  o0O . append ( { 'label' : 'Next >>' , 'path' : '%s/%s/%s/%s' % ( ii , route_name , urllib . quote_plus ( url ) , Iii111II ) , 'thumbnail' : 'http://icons.iconarchive.com/icons/rafiqul-hassan/blogger/128/Arrow-Next-icon.png' } )
 return o0O
 if 29 - 29: i11Ii11I1Ii1i % O00oOoOoO0o0O + OOO0O / II + OOoO * II
def O00 ( murl ) :
 Oo = o0o0OOO0o0 ( murl )
 ooOOOo0oo0O0 = re . compile ( '<p><a href="(.+?)" class="watch_now">XEM PHIM</a>' ) . findall ( Oo )
 Oo = o0o0OOO0o0 ( ooOOOo0oo0O0 [ 0 ] )
 ooOOOo0oo0O0 = re . compile ( '<tr class="listserver"><td valign="top" class="name">(.+?)</td>(.+?)</tr>' ) . findall ( Oo )
 i1I1iI = [ ]
 for oo0OooOOo0 , o0OO00oO in ooOOOo0oo0O0 :
  I11i1I1I = re . compile ( '<a href="(.+?)">' ) . findall ( o0OO00oO ) [ 0 ]
  O00o = { }
  O00o [ "name" ] = oo0OooOOo0
  O00o [ "eps" ] = I11i1I1I
  i1I1iI . append ( O00o )
 return i1I1iI
 if 83 - 83: i11Ii11I1Ii1i / OOO0O
@ oo000 . cached ( TTL = 60 )
def o0o0OOO0o0 ( url ) :
 iIIIIii1 = urllib2 . Request ( url )
 iIIIIii1 . add_header ( 'Accept' , 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8' )
 iIIIIii1 . add_header ( 'User-Agent' , 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.65 Safari/537.36' )
 iIIIIii1 . add_header ( 'Accept-Encoding' , 'gzip, deflate, sdch' )
 oo000OO00Oo = urllib2 . urlopen ( iIIIIii1 )
 O0OOO0OOoO0O = oo000OO00Oo . read ( )
 oo000OO00Oo . close ( )
 if "gzip" in oo000OO00Oo . info ( ) . getheader ( 'Content-Encoding' ) :
  O0OOO0OOoO0O = zlib . decompress ( O0OOO0OOoO0O , 16 + zlib . MAX_WBITS )
 O0OOO0OOoO0O = '' . join ( O0OOO0OOoO0O . splitlines ( ) ) . replace ( '\'' , '"' )
 O0OOO0OOoO0O = O0OOO0OOoO0O . replace ( '\n' , '' )
 O0OOO0OOoO0O = O0OOO0OOoO0O . replace ( '\t' , '' )
 O0OOO0OOoO0O = re . sub ( '  +' , ' ' , O0OOO0OOoO0O )
 O0OOO0OOoO0O = O0OOO0OOoO0O . replace ( '> <' , '><' )
 return O0OOO0OOoO0O
 if 70 - 70: O0o00 * O0oo0OO0 * ooo0Oo0 / i1
oO = xbmc . translatePath ( xbmcaddon . Addon ( 'plugin.video.hieuhien.vn.anhtrang.org' ) . getAddonInfo ( 'profile' ) )
if 93 - 93: Oo0ooO0oo0oO % ooO . Oo0ooO0oo0oO * o0ooo % i1 . iii1I1I
if os . path . exists ( oO ) == False :
 os . mkdir ( oO )
iI1ii1Ii = os . path . join ( oO , 'visitor' )
if 92 - 92: I1i1iI1i
if os . path . exists ( iI1ii1Ii ) == False :
 from random import randint
 i1OOO = open ( iI1ii1Ii , "w" )
 i1OOO . write ( str ( randint ( 0 , 0x7fffffff ) ) )
 i1OOO . close ( )
 if 59 - 59: iii1I1I + iII111iiiii11 * I1i1iI1i + I1IiiI
def Oo0OoO00oOO0o ( utm_url ) :
 OOO00O = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'
 import urllib2
 try :
  iIIIIii1 = urllib2 . Request ( utm_url , None ,
 { 'User-Agent' : OOO00O }
 )
  oo000OO00Oo = urllib2 . urlopen ( iIIIIii1 ) . read ( )
 except :
  print ( "GA fail: %s" % utm_url )
 return oo000OO00Oo
 if 84 - 84: ooO * Oo0ooO0oo0oO / ooo0Oo0 - OO0OO0O0O0
def I11i11Ii ( group , name ) :
 try :
  try :
   from hashlib import md5
  except :
   from md5 import md5
  from random import randint
  import time
  from urllib import unquote , quote
  from os import environ
  from hashlib import sha1
  IiI1 = "1.0"
  Oo0O00Oo0o0 = open ( iI1ii1Ii ) . read ( )
  O00O0oOO00O00 = "AnhTrang.org"
  i1Oo00 = "UA-52209804-2"
  i1i = "www.viettv24.com"
  iiI111I1iIiI = "http://www.google-analytics.com/__utm.gif"
  if name == "None" :
   IIIi1I1IIii1II = iiI111I1iIiI + "?" + "utmwv=" + IiI1 + "&utmn=" + str ( randint ( 0 , 0x7fffffff ) ) + "&utmp=" + quote ( O00O0oOO00O00 ) + "&utmac=" + i1Oo00 + "&utmcc=__utma=%s" % "." . join ( [ "1" , "1" , Oo0O00Oo0o0 , "1" , "1" , "2" ] )
   if 65 - 65: i1 . iiiIIii1IIi / OO0OO0O0O0 - i1
   if 21 - 21: O00oOoOoO0o0O * iiiIIii1IIi
   if 91 - 91: O0o00
   if 15 - 15: iii1I1I
   if 18 - 18: Oo0Ooo . I1IiiI % iII111iiiii11 / OO0OO0O0O0
  else :
   if group == "None" :
    IIIi1I1IIii1II = iiI111I1iIiI + "?" + "utmwv=" + IiI1 + "&utmn=" + str ( randint ( 0 , 0x7fffffff ) ) + "&utmp=" + quote ( O00O0oOO00O00 + "/" + name ) + "&utmac=" + i1Oo00 + "&utmcc=__utma=%s" % "." . join ( [ "1" , "1" , Oo0O00Oo0o0 , "1" , "1" , "2" ] )
    if 75 - 75: I1i1iI1i % II % II . o0ooo
    if 5 - 5: II * OOO0O + I1i1iI1i . OOoO + I1i1iI1i
    if 91 - 91: OO0OO0O0O0
    if 61 - 61: iii1I1I
    if 64 - 64: OOO0O / I1i1iI1i - OO0OO0O0O0 - ooo0Oo0
   else :
    IIIi1I1IIii1II = iiI111I1iIiI + "?" + "utmwv=" + IiI1 + "&utmn=" + str ( randint ( 0 , 0x7fffffff ) ) + "&utmp=" + quote ( O00O0oOO00O00 + "/" + group + "/" + name ) + "&utmac=" + i1Oo00 + "&utmcc=__utma=%s" % "." . join ( [ "1" , "1" , Oo0O00Oo0o0 , "1" , "1" , "2" ] )
    if 86 - 86: ooo0Oo0 % I1i1iI1i / O00oOoOoO0o0O / I1i1iI1i
    if 42 - 42: Oo0ooO0oo0oO
    if 67 - 67: o0ooo . OOooo0000ooo . OO0OO0O0O0
    if 10 - 10: i11Ii11I1Ii1i % i11Ii11I1Ii1i - iiiIIii1IIi / OOoO + i1
    if 87 - 87: ooO * i11Ii11I1Ii1i + OOoO / iiiIIii1IIi / OOooo0000ooo
    if 37 - 37: OOooo0000ooo - OOO0O * ooO % Oo0Ooo - o0ooo
  print "============================ POSTING ANALYTICS ============================"
  Oo0OoO00oOO0o ( IIIi1I1IIii1II )
  if 83 - 83: ooo0Oo0 / O00oOoOoO0o0O
  if not group == "None" :
   iIIiIi1iIII1 = iiI111I1iIiI + "?" + "utmwv=" + IiI1 + "&utmn=" + str ( randint ( 0 , 0x7fffffff ) ) + "&utmhn=" + quote ( i1i ) + "&utmt=" + "events" + "&utme=" + quote ( "5(" + O00O0oOO00O00 + "*" + group + "*" + name + ")" ) + "&utmp=" + quote ( O00O0oOO00O00 ) + "&utmac=" + i1Oo00 + "&utmcc=__utma=%s" % "." . join ( [ "1" , "1" , "1" , Oo0O00Oo0o0 , "1" , "2" ] )
   if 78 - 78: OO0OO0O0O0 . ooO . iii1I1I % OOoO
   if 49 - 49: i1 / Oo0ooO0oo0oO . iii1I1I
   if 68 - 68: Oo0Ooo % i11Ii11I1Ii1i + Oo0Ooo
   if 31 - 31: iii1I1I . O00oOoOoO0o0O
   if 1 - 1: O0oo0OO0 / II % OOooo0000ooo * O0o00 . Oo0Ooo
   if 2 - 2: i11Ii11I1Ii1i * ooo0Oo0 - iiiIIii1IIi + O00oOoOoO0o0O . ooO % OOooo0000ooo
   if 92 - 92: OOooo0000ooo
   if 25 - 25: O0oo0OO0 - O00oOoOoO0o0O / iII111iiiii11 / II
   try :
    print "============================ POSTING TRACK EVENT ============================"
    Oo0OoO00oOO0o ( iIIiIi1iIII1 )
   except :
    print "============================  CANNOT POST TRACK EVENT ============================"
    if 12 - 12: O00oOoOoO0o0O * OOooo0000ooo % I1IiiI % iiiIIii1IIi
 except :
  print "================  CANNOT POST TO ANALYTICS  ================"
  if 20 - 20: OOoO % i1 / i1 + i1
if __name__ == '__main__' :
 oo000 . run ( )
# dd678faae9ac167bc83abf78e5cb2f3f0688d3a3
