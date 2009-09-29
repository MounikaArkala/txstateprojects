""" removeall.py:

   Clean up a directory tree from root.
   The directory need not be empty.
   The starting directory is not deleted.
   Written by: Anand B Pillai <abpillai@lycos.com> """

import sys
import os, stat  

ERROR_STR= """Error removing %(path)s, %(error)s """

def rmgeneric(path, __func__):

    try:
        __func__(path)
        print 'Removed ', path
    except OSError, (errno, strerror):
        print ERROR_STR % {'path' : path, 'error': strerror }

def remove_perms(path):
    fileAtt = os.stat(path)[0]  
    if (not fileAtt & stat.S_IWRITE):  
       # File is read-only, so make it writeable  
       os.chmod(path, stat.S_IWRITE)
    os.remove(path)

def removeall(path):

    if not os.path.isdir(path):
        return
    
    files=os.listdir(path)

    for x in files:
        fullpath=os.path.join(path, x)
        if os.path.isfile(fullpath):
            f=remove_perms
            rmgeneric(fullpath, f)
        elif os.path.isdir(fullpath):
            removeall(fullpath)
            f=os.rmdir
            rmgeneric(fullpath, f)



import shutil, os
if raw_input("Contents of Upload directory will be destroyed!  Continue? (y/n)").lower().strip()[0] == "y":
    if os.path.exists("Upload"):
        try:
            shutil.rmtree("Upload")
        except:
            print "unable to remove Upload directory, aborting!"
            raise SystemError
    shutil.copytree(".", "Upload")
    for i in os.walk("Upload"):
            print os.path.join(i[0], ".svn")
            removeall(os.path.join(i[0], ".svn"))
            shutil.rmtree(os.path.join(i[0], ".svn"))
