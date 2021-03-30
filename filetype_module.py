import os.path
import ntpath
def checkfile(file):
    fileext = os.path.splitext(file)
    file_arrays=[".png",".jpg",".jpeg",".PNG"]
    txt=[".txt"]
    if (fileext[1] in file_arrays):
        return("file_array")
    elif (fileext[1] == ".txt"):
        return("Text")

def filesize(file):
    filestat = os.stat(file)
    return(filestat.st_size)
def filename(file):
    return(ntpath.basename(file))

def accept(filepath):
    fileext = os.path.splitext(filepath)
    checkfile(fileext[1])