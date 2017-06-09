## 前提

需要库：[bs4](https://pypi.python.org/pypi/beautifulsoup4#downloads) [js2py](https://github.com/PiotrDabkowski/Js2Py) [Pillow](https://pypi.python.org/pypi/Pillow/4.1.1)。
如果安装python时将python目录加入了系统路径，管理员模式运行

```
pip install beautifulsoup4
pip install js2py
pip install Pillow
```
就可以安装好。

暂时没有制作图形界面，所以使用方法很原始。

## 使用方法

现在只有网易漫画和ikanman两个网站，而且都是从第一话开始下载全部。

如果是网易，paya/m.py里，在`if __name__ == "__main__":`下面

```
tenma = "4458002705630123103"	#比如这是天才麻将少女的书本id
ne_book = netease.DLer(tenma)
ne_book._dl()
```

默认下载于上一级目录，可以在const.py里面改。
注意这个会从第一话开始下载全部的内容。
使用的话，进paya文件夹，python m.py就可以。

```
cd paya
python m.py
```

如果是ikanman，把netease换成ikm。