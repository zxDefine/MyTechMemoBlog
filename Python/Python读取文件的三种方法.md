# Python读取文件的三种方法
假设有文件text.json文件内容如下。
```json
{
    "name": "zxDefine",
    "url": "https://zxdefine.github.io/MyTechMemoBlog/#/"
}
```
## read()方法
read()方法可以一次读取文件全部内容,该方法返回字符串。
```python
fh = open('text.json', 'r', encoding='utf-8')
lines = fh.read()
print(lines)
print(type(lines))
fh.close()
```
输出结果:
```json
{
    "name": "zxDefine",
    "url": "https://zxdefine.github.io/MyTechMemoBlog/#/"
}
<class 'str'>
```
## readline()方法
readline()方法每次读取一行内容,**读取时占用内存小,比较时候大文件**,该方法返回一个字符串。
```python
fh = open('text.json', 'r', encoding='utf-8')
lines = fh.read()
print(lines)
fh.close()
```
输出结果:
```json
{
<class 'str'>
    "name": "zxDefine",
<class 'str'>
    "url": "https://zxdefine.github.io/MyTechMemoBlog/#/"
<class 'str'>
}
<class 'str'>
```
## readlines()方法
readlines()方法读取整个文件所有行,并保存在一个列表(list)变量中,每次读取一行,但**读取大文件比较占内存**。
```python
fh = open('text.json', 'r', encoding='utf-8')
lines = fh.readlines()
for line in lines:
    print(line)
    print(type(line))
fh.close()
```
输出结果:
```json
{
<class 'str'>
    "name": "zxDefine",
<class 'str'>
    "url": "https://zxdefine.github.io/MyTechMemoBlog/#/"
<class 'str'>
}
<class 'str'>
```
还有一种方式,类似readlines()
```python
fh = open('text.json', 'r', encoding='utf-8')
print(type(fh))
for line in fh:
    print(line)
    print(type(line))
fh.close()
```
输出结果:
```json
<class '_io.TextIOWrapper'>
{
<class 'str'>
    "name": "zxDefine",
<class 'str'>
    "url": "https://zxdefine.github.io/MyTechMemoBlog/#/"
<class 'str'>
}
<class 'str'>
```