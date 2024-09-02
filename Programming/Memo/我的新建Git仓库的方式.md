# 新建一个本地跟GitHub的仓库,并关联.

## 1.初始化本地项目的目录
在项目的根目录下执行初始化命令,把项目的目录初始化为Git的仓库.
```
git init
```

## 2.在Github上新建一个仓库
## 3.在本地仓库下执行关联命令
```
git remote add main git@github.com:zxDefine/{XXXXXXXXXXX}.git
```
其中**main**是远程库的名字,是Git的默认叫法,可修改.**git@github.com:zxDefine/{XXXXXXXXXXX}.git**是远程库的链接地址,这里使用的SSH方式链接.
然后可以执行添加并上传命令
```
git add .
git commit -m "first commint init."
```

## 4.在Sourcetree上添加仓库
## 5.先从远程pull一次,以同步远程跟本地仓库
## 6.然后push本地仓库的文件到远程仓库