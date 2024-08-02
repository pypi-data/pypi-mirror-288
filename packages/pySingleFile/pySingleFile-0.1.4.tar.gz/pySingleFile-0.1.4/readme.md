# 概述
SingleFile的python实现

# 依赖
chrome浏览器 <br>
基于DrissionPage('4.0.4.21')进行修改，因此需要安装chrome

# 安装
```
pip install pySingleFile
```

# 使用示例
## 打印资源示例
```
from pySingleFile import SingleFile
u = "https://www.baidu.com/"
sf = SingleFile(u)
# 打印资源示例
sf.get_resource()

print("image资源有：")
for img in sf.images:
    print(img["url"])
    if img["content"]:
        print(img["content"][:20])
        print(img["data_uri"][:50])
        print("\n")

print("\n")
print("JavaScript资源有：")
for js in sf.javascripts:
    print(js["url"])
    if js["content"]:
        print(js["content"][:50])
        print(js["data_uri"][:50])
        print("\n")

print("\n")
print("CSS资源有：")
for css in sf.stylelinks:
    print(css["url"])
    if css["content"]:
        print(css["content"][:50])
        print(css["data_uri"][:50])
        print("\n")
```
## result
```
image资源有：
https://pss.bdstatic.com/static/superman/img/topnav/newfanyi-da0cea8f7e.png
b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00X'
data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAFgA

https://pss.bdstatic.com/static/superman/img/topnav/newxueshuicon-a5314d5c83.png
b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00X'
data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAFgA


JavaScript资源有：
https://pss.bdstatic.com/static/superman/amd_modules/tslib-c95383af0c.js
define('tslib', [
    'require',
    'amd_modules/
data:text/javascript;base64,ZGVmaW5lKCd0c2xpYicsIF

https://hectorstatic.baidu.com/cd37ed75a9387c5b.js
(function(){ var _0x3c93=['SmlrTGY=','Z0xGUXQ=','b
data:text/javascript;base64,KGZ1bmN0aW9uKCl7IHZhci



CSS资源有：
https://pss.bdstatic.com/r/www/static/font/cosmic/pc/cos-icon_99f656e.css
@font-face {
    font-family: "cos-icon"; /* Proje
data:text/css;base64,QGZvbnQtZmFjZSB7CiAgICBmb250L

https://pss.bdstatic.com/static/superman/css/ubase_sync-d600f57804.css?v=md5
.sui-scrollbar-container{position:relative;overflo
data:text/css;base64,LnN1aS1zY3JvbGxiYXItY29udGFpb
```

## 离线保存示例
```
from pySingleFile import SingleFile
u = "https://www.baidu.com/"
sf = SingleFile(u)
#  离线保存示例
sf.save()
```
## result
```
文件保存为：百度一下，你就知道.html
```