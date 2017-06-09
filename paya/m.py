#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import io
import sys

sys.path.append("..")  # 使用方法：python 本目录的本文件
sys.path.append(".")
import paya.netease_manga as netease
import paya.ikanman_manga as ikm
import os, re
# import paya.dl_manager as dl
from paya.const import *
import tkinter
import paya.gui

# @log_time("这个操作")
# def f():
# 	print("他会i数据库连接")
# 	time.sleep(2)
# 	print("微积分")
# f()
# lang = init_locale(lang_zh)
if __name__ == "__main__":
	sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8') #改变标准输出的默认编码

	# 使用多线程： 用每个线程下载不同的图片（每一话新开pool）
	createFolder(data_dir)
	# 163
	L_Dart = "4603479161120104695"  # 神契 幻奇谭
	id_book = "4617223306170106339"
	tenma = "4458002705630123103"
	douluo3  = "4645740535490115552"
	ganglian = "4475930658180096982"
	gude = "4317064958460053300"
	# ne_book = netease.DLer(ganglian)
	# ne_book._dl()
	# print(ne_book.get_eplist_for_one_chap(0))

	# search_text.set("搜索本地漫画")

	# ikm
	shinohayu = "10360"
	# with_liz = "13304"
	# toku = "6540"
	# cike = "8632"
	# zhenhunjie = "9082"
	# konan = "2027"
	# saki_ni = "5120"
	renai = "18557"
	# print(ikm.ikanman_DLer.getBookName(shinohayu))
	# print(ikm.ikanman_DLer.getBookName(toku))
	ik_book_renai = ikm.DLer(renai)
	# ik_book_pm = ikm.DLer(renai)
	# ik_book_shino = ikm.DLer(shinohayu)
	# ik_book_shino.dl_whole_book()
	ik_book_renai.dl_whole_book()
	# dman = dl.DLManager()

