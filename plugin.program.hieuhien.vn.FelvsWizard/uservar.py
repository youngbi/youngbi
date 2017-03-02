import os, xbmc, xbmcaddon

#########################################################
### User Edit Variables #################################
#########################################################
ADDON_ID       = xbmcaddon.Addon().getAddonInfo('id')
ADDONTITLE     = 'Felvs Wizard'
EXCLUDES       = [ADDON_ID, 'repository.aftermathwizard']
# Text File with build info in it.
BUILDFILE      = 'http://felvswizard.esy.es/text/builds.txt'
# How often you would list it to check for build updates in days
# 0 being every startup of kodi
UPDATECHECK    = 0
# Text File with apk info in it.
APKFILE        = 'http://felvswizard.esy.es/text/apks.txt'

# Dont need to edit just here for icons stored locally
HOME           = xbmc.translatePath('special://home/')
PLUGIN         = os.path.join(HOME,     'addons',    ADDON_ID)
ART            = os.path.join(PLUGIN,   'resources', 'art')

#########################################################
### THEMING MENU ITEMS ##################################
#########################################################
# If you want to use locally stored icons the place them in the Resources/Art/
# folder of the wizard then use os.path.join(ART, 'imagename.png')
# do not place quotes around os.path.join
# Example:  ICONMAINT     = os.path.join(ART, 'mainticon.png')
#           ICONSETTINGS  = 'http://aftermathwizard.net/repo/wizard/settings.png'
# Leave as http:// for default icon
ICONMAINT      = 'https://archive.org/download/Maintenance_201605/Maintenance.png'
ICONBUILDS     = 'https://archive.org/download/Maintenance_201605/builds.png'
ICONCONTACT    = 'https://archive.org/download/Maintenance_201605/contact.png'
ICONAPK        = 'https://archive.org/download/Maintenance_201605/apkinstaller.png'
ICONSAVE       = 'https://archive.org/download/Maintenance_201605/SaveData.png'
ICONTRAKT      = 'https://archive.org/download/Maintenance_201605/traktdata.png'
ICONREAL       = 'https://archive.org/download/Maintenance_201605/RealDebrid.png'
ICONSETTINGS   = 'https://archive.org/download/Maintenance_201605/wizardsettingsicon.png'
# Hide the ====== seperators 'Yes' or 'No'
HIDESPACERS    = 'No'                                                                    

# You can edit these however you want, just make sure that you have a %s in each of the
# THEME's so it grabs the text from the menu item
COLOR1         = 'dodgerblue'
COLOR2         = 'white'
# Primary menu items   / %s is the menu item and is required
THEME1         = '[COLOR '+COLOR1+'][Felvs Wizard][/COLOR] [COLOR '+COLOR2+']%s[/COLOR]'    
# Build Names          / %s is the menu item and is required
THEME2         = '[COLOR '+COLOR2+']%s[/COLOR]'                                          
# Alternate items      / %s is the menu item and is required
THEME3         = '[COLOR '+COLOR1+']%s[/COLOR]'                                          
# Current Build Header / %s is the menu item and is required
THEME4         = '[COLOR '+COLOR1+']Current Build:[/COLOR] [COLOR '+COLOR2+']%s[/COLOR]' 
# Current Theme Header / %s is the menu item and is required
THEME5         = '[COLOR '+COLOR1+']Current Theme:[/COLOR] [COLOR '+COLOR2+']%s[/COLOR]' 

# Message for Contact Page
# Enable 'Contact' menu item 'Yes' hide or 'No' dont hide
HIDECONTACT    = 'No'                                                                    
# You can add \n to do line breaks
CONTACT        = 'Thank you for choosing Felvs Wizard. Contact us on facebook at https://www.facebook.com/groups/FelvsWizard/'
#########################################################

#########################################################
### AUTO UPDATE #########################################
########## FOR THOSE WITH NO REPO #######################
# Enable Auto Update 'Yes' or 'No'
AUTOUPDATE     = 'Yes'                                                                    
# Url to wizard version
WIZARDFILE     = 'http://felvswizard.esy.es/text/wizardupdate.txt'                          
#########################################################

#########################################################
### AUTO INSTALL ########################################
########## REPO IF NOT INSTALLED ########################
# Enable Auto Install 'Yes' or 'No'
AUTOINSTALL    = 'No'                                                                    
# Addon ID for the repository
REPOID         = 'repository.aftermathwizard'
# Url to Addons.xml file in your repo folder(this is so we can get the latest version)
REPOADDONXML   = 'https://raw.githubusercontent.com/aftermathbuilds/aftermathwizard/master/repository.aftermathwizard/addon.xml'
# Url to folder zip is located in
REPOZIPURL     = 'https://raw.githubusercontent.com/aftermathbuilds/aftermathwizard/master/repository.aftermathwizard/'
#########################################################

#########################################################
### NOTIFICATION WINDOW##################################
#########################################################
# Enable Notification screen Yes or No
ENABLE         = 'No'
# Url to notification file
NOTIFICATION   = 'http://aftermathwizard.net/repo/wizard/notify.txt'
# Use either 'Text' or 'Image'
HEADERTYPE     = 'Text'
# Font size of header
FONTHEADER     = 'Font14'
HEADERMESSAGE  = 'Aftermath Wizard'
# url to image if using Image 424x180
HEADERIMAGE    = ''
# Font for Notification Window
FONTSETTINGS   = 'Font13'
# Background for Notification Window
BACKGROUND     = ''
#########################################################