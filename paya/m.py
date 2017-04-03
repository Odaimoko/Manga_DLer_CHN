#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import io
import sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8') #改变标准输出的默认编码
sys.path.append("..")
sys.path.append(".")
# print(sys.path)

import netease_manga as netease
import ikanman_manga as ikm
import os, re
# import paya.dl_manager as dl
from const import *
with open("ikm_Kai_mitsu.js", "rb") as f:
	enc = f.read().decode("utf8")
# with open("ez.js","r") as f:
# 	enc = f.read()
# print(enc)

# toen = """eval(function(p,a,c,k,e,d){e=function(c){return(c<a?"":e(parseInt(c/a)))+((c=c%a)>35?String.fromCharCode(c+29):c.toString(36))};if(!''.replace(/^/,String)){while(c--)d[e(c)]=k[c]||e(c);k=[function(e){return d[e]}];e=function(){return'\\w+'};c=1;};while(c--)if(k[c])p=p.replace(new RegExp('\\b'+e(c)+'\\b','g'),k[c]);return p;}('1M L={"K":3,"J":"M","P":"3.0","O":N,"I":D,"C":"B","E":["H.0.2","G.0.2","F.0.2","Q.0.2","11.0.2","10.0.2","Z.0.2","12.0.2","15.0.2","14.0.2","13.0.2","Y.0.2","T.0.2","S.0.2","R.0.2","U.0.2","X.0.2","W.0.2","V.0.2","A.0.2","d.0.2","e.0.2","b.0.2","c.0.2","h.0.2","i.0.2","f.0.2","g.0.2","a.0.2","4.0.2","5.0.2","8.0.2","9.0.2","6.0.2","7.0.2","j.0.2","v.0.2","u.0.2","t.0.2","w.0.2","z.0.2","y.0.2","x.0.2","r.0.2","m.0.2","l.0.2","k.0.2","n.0.2","q.0.2","p.0.2","o.0.2","1q.0.2","1L.0.2","1K.0.2","1N.0.2","1Q.0.2","1P.0.2","1O.0.2","1J.0.2","1E.0.2","1D.0.2","1C.0.2","1F.0.2","1I.0.2","1H.0.2","1G.0.2","1R.0.2","22.0.2","23.0.2","20.0.2","21.0.2","25.0.2","26.0.2","24.0.2","1Z.0.2","1U.0.2","1T.0.2","1S.0.2","1V.0.2","1Y.0.2","1X.0.2","1W.0.2","1B.0.2","1g.0.2","1f.0.2","1e.0.2","1h.0.2","1k.0.2","1j.0.2","1i.0.2","1d.0.2","18.0.2","17.0.2","16.0.2","19.0.2","1c.0.2","1b.0.2","1a.0.2","1l.0.2","1w.0.2","1v.0.2","1u.0.2","1x.0.2","1A.0.2"],"1z":1y,"1t":1o,"1n":"/1m/s/1p/1s/","1r":1}||{};',62,131,'jpg||webp|6540|xindm_cn_029030|xindm_cn_030031|xindm_cn_033034|xindm_cn_034035|xindm_cn_031032|xindm_cn_032033|xindm_cn_028029|xindm_cn_022023|xindm_cn_023024|xindm_cn_020021|xindm_cn_021022|xindm_cn_026027|xindm_cn_027028|xindm_cn_024025|xindm_cn_025026|xindm_cn_035036|xindm_cn_046047|xindm_cn_045046|xindm_cn_044045|xindm_cn_047048|xindm_cn_050051|xindm_cn_049050|xindm_cn_048049|xindm_cn_043044||xindm_cn_038039|xindm_cn_037038|xindm_cn_036037|xindm_cn_039040|xindm_cn_042043|xindm_cn_041042|xindm_cn_040041|xindm_cn_019020|第06卷|cname|56443|files|xindm_cn_002003|xindm_cn_001002|xindm_cn_000001|cid|bname|bid|cInfo|神奇宝贝特别篇|null|burl|bpic|xindm_cn_003004|xindm_cn_014015|xindm_cn_013014|xindm_cn_012013|xindm_cn_015016|xindm_cn_018019|xindm_cn_017018|xindm_cn_016017|xindm_cn_011012|xindm_cn_006007|xindm_cn_005006|xindm_cn_004005|xindm_cn_007008|xindm_cn_010011|xindm_cn_009010|xindm_cn_008009|xindm_cn_093094|xindm_cn_092093|xindm_cn_091092|xindm_cn_094095|xindm_cn_097098|xindm_cn_096097|xindm_cn_095096|xindm_cn_090091|xindm_cn_085086|xindm_cn_084085|xindm_cn_083084|xindm_cn_086087|xindm_cn_089090|xindm_cn_088089|xindm_cn_087088|xindm_cn_098099|ps3|path|104|sqbbtbp|xindm_cn_051052|status|Vol_06|len|xindm_cn_101102|xindm_cn_100101|xindm_cn_099100|xindm_cn_102103|false|finished|xindm_cn_103104|xindm_cn_082083|xindm_cn_061062|xindm_cn_060061|xindm_cn_059060|xindm_cn_062063|xindm_cn_065066|xindm_cn_064065|xindm_cn_063064|xindm_cn_058059|xindm_cn_053054|xindm_cn_052053|var|xindm_cn_054055|xindm_cn_057058|xindm_cn_056057|xindm_cn_055056|xindm_cn_066067|xindm_cn_077078|xindm_cn_076077|xindm_cn_075076|xindm_cn_078079|xindm_cn_081082|xindm_cn_080081|xindm_cn_079080|xindm_cn_074075|xindm_cn_069070|xindm_cn_070071|xindm_cn_067068|xindm_cn_068069|xindm_cn_073074|xindm_cn_071072|xindm_cn_072073'.split('|'),0,{}))"""
func_use = "decryptDES('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')"
decode_result = """
var cInfo = {
    "bid": 6540,
    "bname": "神奇宝贝特别篇",
    "bpic": "6540.jpg",
    "burl": null,
    "cid": 56443,
    "cname": "第06卷",
    "files": ["xindm_cn_000001.jpg.webp", "xindm_cn_001002.jpg.webp", "xindm_cn_002003.jpg.webp", "xindm_cn_003004.jpg.webp", "xindm_cn_004005.jpg.webp", "xindm_cn_005006.jpg.webp", "xindm_cn_006007.jpg.webp", "xindm_cn_007008.jpg.webp", "xindm_cn_008009.jpg.webp", "xindm_cn_009010.jpg.webp", "xindm_cn_010011.jpg.webp", "xindm_cn_011012.jpg.webp", "xindm_cn_012013.jpg.webp", "xindm_cn_013014.jpg.webp", "xindm_cn_014015.jpg.webp", "xindm_cn_015016.jpg.webp", "xindm_cn_016017.jpg.webp", "xindm_cn_017018.jpg.webp", "xindm_cn_018019.jpg.webp", "xindm_cn_019020.jpg.webp", "xindm_cn_020021.jpg.webp", "xindm_cn_021022.jpg.webp", "xindm_cn_022023.jpg.webp", "xindm_cn_023024.jpg.webp", "xindm_cn_024025.jpg.webp", "xindm_cn_025026.jpg.webp", "xindm_cn_026027.jpg.webp", "xindm_cn_027028.jpg.webp", "xindm_cn_028029.jpg.webp", "xindm_cn_029030.jpg.webp", "xindm_cn_030031.jpg.webp", "xindm_cn_031032.jpg.webp", "xindm_cn_032033.jpg.webp", "xindm_cn_033034.jpg.webp", "xindm_cn_034035.jpg.webp", "xindm_cn_035036.jpg.webp", "xindm_cn_036037.jpg.webp", "xindm_cn_037038.jpg.webp", "xindm_cn_038039.jpg.webp", "xindm_cn_039040.jpg.webp", "xindm_cn_040041.jpg.webp", "xindm_cn_041042.jpg.webp", "xindm_cn_042043.jpg.webp", "xindm_cn_043044.jpg.webp", "xindm_cn_044045.jpg.webp", "xindm_cn_045046.jpg.webp", "xindm_cn_046047.jpg.webp", "xindm_cn_047048.jpg.webp", "xindm_cn_048049.jpg.webp", "xindm_cn_049050.jpg.webp", "xindm_cn_050051.jpg.webp", "xindm_cn_051052.jpg.webp", "xindm_cn_052053.jpg.webp", "xindm_cn_053054.jpg.webp", "xindm_cn_054055.jpg.webp", "xindm_cn_055056.jpg.webp", "xindm_cn_056057.jpg.webp", "xindm_cn_057058.jpg.webp", "xindm_cn_058059.jpg.webp", "xindm_cn_059060.jpg.webp", "xindm_cn_060061.jpg.webp", "xindm_cn_061062.jpg.webp", "xindm_cn_062063.jpg.webp", "xindm_cn_063064.jpg.webp", "xindm_cn_064065.jpg.webp", "xindm_cn_065066.jpg.webp", "xindm_cn_066067.jpg.webp", "xindm_cn_067068.jpg.webp", "xindm_cn_068069.jpg.webp", "xindm_cn_069070.jpg.webp", "xindm_cn_070071.jpg.webp", "xindm_cn_071072.jpg.webp", "xindm_cn_072073.jpg.webp", "xindm_cn_073074.jpg.webp", "xindm_cn_074075.jpg.webp", "xindm_cn_075076.jpg.webp", "xindm_cn_076077.jpg.webp", "xindm_cn_077078.jpg.webp", "xindm_cn_078079.jpg.webp", "xindm_cn_079080.jpg.webp", "xindm_cn_080081.jpg.webp", "xindm_cn_081082.jpg.webp", "xindm_cn_082083.jpg.webp", "xindm_cn_083084.jpg.webp", "xindm_cn_084085.jpg.webp", "xindm_cn_085086.jpg.webp", "xindm_cn_086087.jpg.webp", "xindm_cn_087088.jpg.webp", "xindm_cn_088089.jpg.webp", "xindm_cn_089090.jpg.webp", "xindm_cn_090091.jpg.webp", "xindm_cn_091092.jpg.webp", "xindm_cn_092093.jpg.webp", "xindm_cn_093094.jpg.webp", "xindm_cn_094095.jpg.webp", "xindm_cn_095096.jpg.webp", "xindm_cn_096097.jpg.webp", "xindm_cn_097098.jpg.webp", "xindm_cn_098099.jpg.webp", "xindm_cn_099100.jpg.webp", "xindm_cn_100101.jpg.webp", "xindm_cn_101102.jpg.webp", "xindm_cn_102103.jpg.webp", "xindm_cn_103104.jpg.webp"],
    "finished": false,
    "len": 104,
    "path": "/ps3/s/sqbbtbp/Vol_06/",
    "status": 1
} || {};
"""

import js2py

x = """
var escape = function(text){pyimport urllib; return urllib.parse.quote(text)};
var unescape = function(text){pyimport urllib; return urllib.parse.unquote(text)};
//var encodeURIComponent = function(text){pyimport urllib; return urllib.parse.quote(text, safe='~()*!.\\'')};
var encodeURIComponent = function(text){pyimport paya; return paya.const.encodeURIComponent(text)};
var decodeURIComponent = unescape;
var writeto = function(content){pyimport paya; paya.const.writeTo(content);}
"""


# print(js2py.eval_js(x+"writeto('比例来了')")) # 用于测试写在JS里写文件
# the_same = """eval(function(p,a,c,k,e,d){e=function(c){return(c<a?"":e(parseInt(c/a)))+((c=c%a)>35?String.fromCharCode(c+29):c.toString(36))};if(!''.replace(/^/,String)){while(c--)d[e(c)]=k[c]||e(c);k=[function(e){return d[e]}];e=function(){return'\\w+'};c=1;};while(c--)if(k[c])p=p.replace(new RegExp('\\b'+e(c)+'\\b','g'),k[c]);return p;}('v f={"g":4,"d":"3","e":"4.0","j":k,"h":i,"c":"5","7":["8.0.2","b.0.2","a.0.2","9.0.2","6.0.2","l.0.2","w.0.2","q.0.2","u.0.2","x.0.2","B.0.2","y.0.2"],"A":t,"o":n,"m":"/p/z/3[s]/5/","r":1}||{};',38,38,'jpg||webp|éé­è¡|9082|çªå¤ç¯1|005|files|001|004|003|002|cname|bname|bpic|cInfo|bid|cid|90440|burl|null|006|path|12|len|ps3|008|status|è®¸è¾°|false|009|var|007|010|012||finished|011'.split('|'),0,{}))"""
# true_list = [ord(c) for c in the_same]
# print("real encode",bytes(true_list))
# print("encode result",the_same.encode("utf8"))
# @log_time("这个操作")
# def f():
# 	print("他会i数据库连接")
# 	time.sleep(2)
# 	print("微积分")
# f()
if __name__ == "__main__":
	# 使用多线程： 用每个线程下载不同的图片（每一话新开pool）
	# initializeAlready(already_tenma, already_tenma_file)
	# try_getJson()
	createFolder(data_dir)
	# 163
	L_Dart = "4603479161120104695"  # 神契 幻奇谭
	# getBookName("163", L_Dart)
	# id_book = str(input())
	id_book = "4617223306170106339"
	tenma = "4458002705630123103"
	douluo3  = "4645740535490115552"
	ganglian = "4475930658180096982"
	gude = "4317064958460053300"
	ne_book = netease.NetEase_DLer(ganglian)
	ne_book._dl()

	# ikm
	shinohayu = "10360"
	with_liz = "13304"
	toku = "6540"
	cike = "8632"
	zhenhunjie = "9082"
	konan = "2027"
	# print(ikm.ikanman_DLer.getBookName(shinohayu))
	# print(ikm.ikanman_DLer.getBookName(toku))
	# ik_book_pm = ikm.ikanman_DLer(toku)
	# ik_book_shino = ikm.ikanman_DLer(shinohayu)
	# ik_book_shino.dl_whole_book()
	# dman = dl.DLManager()