# Windows下安装youtube-dl以及使用

## 安装
* 安装Python,先去[Python官网](https://www.python.org/)下载最新版Python.
* 使用pip安装youtube-dl
```
pip install youtube-dl //直接安装youtube-dl
pip install --upgrade youtube-dl //安装youtube-dl并更新
```

## 使用
### 查看视频的类型
```
youtube-dl -F [url]
```
这会列出url视频的所有下载类型列表.,可以知道url视频都有那些格式存在,可以有选择的下载.

### 下载
通过上一步获取到了所有视频格式的清单,最左边一列就是编号对应着不同的格式.由于YouTube的1080p及以上的分辨率都是音频视频分离的,所以需要分别下载视频和音频,可以使用137+140这样的组合同时下载.
```
youtube-dl -f [format code] [url]
```
**需要注意的是,下载地址就是命令行所执行的当前目录.**