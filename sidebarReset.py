from genericpath import isfile
import os, sys
from posixpath import basename

class fileClass(object):
    def __init__(self, fileRoot, fileName, isFile) -> None:
        self.fileRoot = fileRoot
        self.fileName = fileName
        self.isFile = isFile

# open file
saveFilePath = "_sidebar.md"
fh = open(saveFilePath, 'w', encoding='utf-8')

baseRoot = '.'
resList = []

# output all files and folders
for root, dirs, files in os.walk('.', topdown=True):
    for name in files:
        if root != baseRoot:
            resList.append(fileClass(root, name, True))
    for name in dirs:
        if name != '.git' and root.find('\\.git') == -1:
            resList.append(fileClass(root, name, False))

folderList = ['.',]
# step1 find all folder
for file in resList:
    if file.isFile == False:
        folderList.append(os.path.join(file.fileRoot, file.fileName))

#文件在目录前的顺序排序
folderList.sort()

fileList = []
# step2 find all file
for file in resList:
    if file.isFile == True:
        fileList.append(os.path.join(file.fileRoot, file.fileName))

sortList = []
for folder in folderList:
    sortList.append(folder)
    for file in fileList:
        if folder == os.path.dirname(file):
            sortList.append(file)
    
for file in sortList:
    str = ''
    if file == baseRoot:
        continue

    relativePath = file[2:]
    tabStr = relativePath.count('\\') * '\t'
    if os.path.isdir(file):
        str = tabStr + '- ' + os.path.basename(file)
    elif os.path.isfile(file):
        relativePath = file[2:]
        str = tabStr + '- [' + os.path.basename(file)[:-3] + '](' + file[2:] + ')'

    fh.write(str)
    fh.write('\n')

fh.close()
