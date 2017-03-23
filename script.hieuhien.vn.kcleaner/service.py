# ============================================================
# KCleaner - Version 1.6 by D. Lanik (2017)
# ------------------------------------------------------------
# Clean up Kodi
# ------------------------------------------------------------
# License: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
# ============================================================

import time
import xbmc
import xbmcaddon
import os
from distutils.util import strtobool
from default import DeleteFiles
from default import CompactDatabases
from default import CleanTextures
from default import deleteAddonData

# ============================================================
# Define Settings Monitor Class
# ============================================================


class SettingMonitor(xbmc.Monitor):
    def __init__(self, *args, **kwargs):
        xbmc.Monitor.__init__(self)

    def onSettingsChanged(self):
        GetSetting()

# ============================================================
# Get settings
# ============================================================


def GetSetting():
    global booBackgroundRun

    __addon__ = xbmcaddon.Addon(id='script.hieuhien.vn.kcleaner')
    df = str(__addon__.getSetting("autoclean")).title()

    booBackgroundRun = bool(strtobool(df))
    xbmc.log('KCLEANER SERVICE >> SETTINGS CHANGED ' + df + " >> " + str(booBackgroundRun))

# ============================================================
# Run cleaning according to settings
# ============================================================


def AutoClean():
    global __addon__
    global __addonname__

    intMbDel = 0
    intMbCom = 0
    intMbTxt = 0
    intMbAdn = 0

    auto_cache = bool(strtobool(str(__addon__.getSetting('auto_cache').title())))
    auto_packages = bool(strtobool(str(__addon__.getSetting('auto_packages').title())))
    auto_thumbnails = bool(strtobool(str(__addon__.getSetting('auto_thumbnails').title())))
    auto_addons = bool(strtobool(str(__addon__.getSetting('auto_addons').title())))
    auto_compact = bool(strtobool(str(__addon__.getSetting('auto_compact').title())))
    auto_textures = bool(strtobool(str(__addon__.getSetting('auto_textures').title())))
    auto_userdata = bool(strtobool(str(__addon__.getSetting('auto_userdata').title())))

    actionToken = []

    if auto_cache:
        actionToken.append("cache")
    if auto_packages:
        actionToken.append("packages")
    if auto_thumbnails:
        actionToken.append("thumbnails")
    if auto_addons:
        actionToken.append("addons")

    if os.path.exists('/private/var/mobile/Library/Caches/AppleTV/Video/Other'):
        actionToken.append("atv")

    intC, intMbDel = DeleteFiles(actionToken, 1)

    if auto_textures:
        intC, intMbTxt = CleanTextures(1)

    if auto_compact:
        intC, intMbCom = CompactDatabases(1)

    if auto_userdata:
        intC, intMbAdn = deleteAddonData(1)

    intMbTot = intMbDel + intMbCom + intMbTxt + intMbAdn
    mess = __addon__.getLocalizedString(30112)                             # Mb
    mess2 = " (%0.2f %s)" % (intMbTot, mess,)
    strMess = __addon__.getLocalizedString(30031) + mess2                  # Cleanup [COLOR red]done[/COLOR].
    xbmc.executebuiltin("XBMC.Notification(%s,%s,5000,%s)" % (__addonname__.encode('utf8'), strMess, __addon__.getAddonInfo('icon')))

# ============================================================
# ------------------------------------------------------------
# Main
# ------------------------------------------------------------
# ============================================================


__addon__ = xbmcaddon.Addon(id='script.hieuhien.vn.kcleaner')
__addonwd__ = xbmc.translatePath(__addon__.getAddonInfo('path').decode("utf-8"))
__addondir__ = xbmc.translatePath(__addon__.getAddonInfo('profile').decode('utf8'))
__addonname__ = __addon__.getAddonInfo('name')
__version__ = __addon__.getAddonInfo('version')

booBackgroundRun = False

if __name__ == '__main__':
    xbmc.log("KCLEANER SERVICE >> STARTED VERSION %s" % (__version__))

    booBackgroundRun = bool(strtobool(str(__addon__.getSetting('autoclean').title())))

    if booBackgroundRun:
        auto_interval = int(__addon__.getSetting('auto_interval'))

        if auto_interval == 0:
            lastrundays = 1
        elif auto_interval == 1:
            lastrundays = 7
        elif auto_interval == 2:
            lastrundays = 30
        elif auto_interval == 3:
            lastrundays = 90
        else:
            lastrundays = 0

        auto_lastrun = __addon__.getSetting('auto_lastrun')
        date_now = int(round(time.time()))

        if auto_lastrun != "":
            date_auto_lastrun = int(auto_lastrun)
            time_difference = date_now - date_auto_lastrun
            time_difference_days = int(time_difference) / 86400
        else:
            __addon__.setSetting('auto_lastrun', str(int(date_now - 31536000)))
            time_difference_days = 365

        autostart_delay = int(__addon__.getSetting('autostart_delay'))

        xbmc.log("KCLEANER SERVICE >> LAST RUN " + str(time_difference_days) + " DAYS AGO, SET TO RUN EVERY " + str(lastrundays) + " DAYS, WITH DELAY OF " + str(autostart_delay) + " MINUTE(S)")

        if time_difference_days > lastrundays:
            xbmc.sleep(autostart_delay * 60000)
            xbmc.log('KCLEANER SERVICE >> RUNNING AUTO...')
            AutoClean()
            __addon__.setSetting('auto_lastrun', str(int(round(time.time()))))

    monitor = xbmc.Monitor()
    monsettings = SettingMonitor()

    iCounter = 0

    while True:
        t = time.ctime()
        if monitor.waitForAbort(2):    # Sleep/wait for abort
            xbmc.log('KCLEANER SERVICE >> EXIT')
            break                      # Abort was requested while waiting. Exit the while loop.
        else:
            if booBackgroundRun:
                iCounter += 1

                if iCounter > 1800:
                    iCounter = 0
                    date_now = int(round(time.time()))
                    time_difference = date_now - date_auto_lastrun
                    time_difference_days = int(time_difference) / 86400

                    xbmc.log("KCLEANER SERVICE >> LAST RUN " + str(time_difference_days) + " DAYS AGO, SET TO RUN EVERY " + str(lastrundays) + " DAYS (NOW: " + str(date_now) + ")")

                    if time_difference_days > lastrundays:
                        xbmc.log('KCLEANER SERVICE >> RUNNING AUTO...')
                        AutoClean()
                        date_auto_lastrun = int(round(time.time()))
                        __addon__.setSetting('auto_lastrun', str(date_auto_lastrun))


# ------------------------------------------------------------
# ------------------------------------------------------------
# ------------------------------------------------------------
# ------------------------------------------------------------
# ------------------------------------------------------------
# ------------------------------------------------------------
# ------------------------------------------------------------
# ------------------------------------------------------------
# ------------------------------------------------------------
# ------------------------------------------------------------
