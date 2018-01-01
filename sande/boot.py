#!/usr/bin/env python

import os
import subprocess
import shutil
import time


# Set our Current Working Directory to the location of this file
full_path = os.path.realpath(__file__)
BASEDIRECTORY = os.path.join(os.path.dirname(full_path))
AUTOEXEC = "/home/pi/.kodi/userdata/autoexec.py"
os.chdir(BASEDIRECTORY)

#defines
BASICIMAGES = os.path.join(BASEDIRECTORY, "Images")
DEPLOYEDIMAGES = os.path.join(BASEDIRECTORY, "Deployed")
NOCONTENT = os.path.join(BASEDIRECTORY, "NoContent")
EXCLUDESET = ["desktop.ini"]


def startkodi():
    subprocess.Popen(["kodi"])
    

def writeautoexec(contents):
    slideshow = """
import os
import xbmc

path = "/home/pi/sande/Images"
xbmc.executebuiltin("RecursiveSlideShow("+path+")")
"""

    file = open(AUTOEXEC, "w")
    file.write(slideshow)
    file.close()


def copyfiles(src, tgt):
    srcfiles = [file for file in os.listdir(src)]
    tgtfiles = [file for file in os.listdir(tgt)]
    
    # Any file in tgt but not src remove
    for file in os.listdir(tgt):
        if not file in srcfiles:
            os.remove(os.path.join(tgt, file))
                 
    for file in os.listdir(src):
        if not file in EXCLUDESET and not file in tgtfiles:
            shutil.copy(os.path.join(src, file), os.path.join(tgt, file))
            

def createfolder(folder):
    os.mkdir(folder)

def deletefolder(folderpath):
    try: 
        if os.path.isdir(folderpath):  
            shutil.rmtree(folderpath)
    except:
        print "Error deleting"


def startbrowser(folder):
    print "Running"

    subprocess.Popen(["python","-m","SimpleHTTPServer","8080"])

    #*nix
    try:
      subprocess.Popen(["chromium-browser","--incognito","--start-fullscreen","http://127.0.0.1:8080/"+folder])
    except:
      pass
      
    try:
      #windows
      subprocess.Popen(["C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe","--incognito","--start-fullscreen","http://127.0.0.1:8080/"])
    except:
      pass
      
    print "Navigate to 127.0.0.1:8080/"


def nocontent():
    shutil.copytree(NOCONTENT, DEPLOYEDIMAGES)
    startbrowser("Deployed")




#### Main script ####

# Modes
# 1) Images off a USB
# 2) 'Deployed' off a USB
# 2a) 'Delete' off a USB
# 3) Preexisting deployed
# 4) Preexisting images


# Let boot finish
print "Sleeping to finish boot"
time.sleep(10)
print "Continuing"


# Most basic mode - if there is a folder called "Images" on a USB drive, copy those images locally and display them
drive_list = os.listdir('/media/pi/.' )

found = None
delete = False


for drive in drive_list:
    try:
        if "Images" in os.listdir('/media/pi/'+drive+"/."):
            found = '/media/pi/'+drive+"/Images/."
        if "images" in os.listdir('/media/pi/'+drive+"/."):
            found = '/media/pi/'+drive+"/images/."
        if "DELETE" in os.listdir('/media/pi/'+drive+"/."):
            delete = True
    except:
        pass
        
if (delete):
    print "Deleteing"
    deletefolder(DEPLOYEDIMAGES)
    deletefolder(BASICIMAGES)
    
if found != None:
    # We found a USB drive with an Images folder
    if not "index.html" in os.listdir(found):
        print "Basic images"
        # We found a basic image deployment
        deletefolder(DEPLOYEDIMAGES)
        createfolder("Images")
        copyfiles(found, BASICIMAGES)
        writeautoexec("")
        startkodi()
    else:
        print "Deployment"
        # We found a full deployment
        deletefolder(BASICIMAGES)
        deletefolder(DEPLOYEDIMAGES)
        createfolder("Deployed")
        copyfiles(found, DEPLOYEDIMAGES)
        startbrowser("Deployed")
    
else:
    # We didn't find anything interesting. Use the current deployed folder (if it exists), else the current images folder
    if os.path.isdir(DEPLOYEDIMAGES):
        print "Old deployment"
        startbrowser("Deployed")
    elif os.path.isdir(BASICIMAGES):
        print "Old images"
        writeautoexec("")
        startkodi()
    else:
        print "No content"
        nocontent()
    
    



    
 