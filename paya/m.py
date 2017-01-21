#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import paya.netease_manga as netease
import paya.ikanman_manga as ikm
import os
# print("biu")
# print(os.getcwd())
# print(os.path.abspath('.'))
# os.chdir("C:/")
# print(os.getcwd())
# from bs4_410 import BeautifulSoup

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
