#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import paya.netease_manga as netease
import paya.ikanman_manga as ikm
import os,re

# with open("ez.js","r") as f:
# 	enc = f.read()

decode_result  = """
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



# print(js2py.eval_js(x))
# print(context.execute("var c = 2;"))
# di =  js2py.eval_js(decode_result).to_dict()
# for it in di["files"]:
# 	print(it)


if __name__ == "__main__":
	# 使用多线程： 用每个线程下载不同的图片（每一话新开pool）
	# initializeAlready(already_tenma, already_tenma_file)
	# try_getJson()

	# 163
	tenma = "4458002705630123103"
	L_Dart = "4603479161120104695"  # 神契 幻奇谭
	# getBookName("163", L_Dart)
	# id_book = str(input())
	id_book = "4617223306170106339"
	# ne_book = netease.NetEase_DLer(id_book)
	# ne_book._dl()

	# ikm
	shinohayu = "10360"
	with_liz = "13304"
	toku = "6540"
	cike = "8632"
	zhenhunjie = "9082"
	# print(ikm.ikanman_DLer.getBookName(shinohayu))
	# print(ikm.ikanman_DLer.getBookName(toku))
	ik_book_pm = ikm.ikanman_DLer(toku)
	ik_book_shino = ikm.ikanman_DLer(zhenhunjie)
	ik_book_shino.dl_whole_book()
