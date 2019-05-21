# -*- coding: utf-8 -*-
import sys
import numpy as np
import matplotlib.pyplot as plt
import csv
from matplotlib.font_manager import FontProperties
from matplotlib import gridspec
from datetime import datetime



ROVERNAME = 'PRECURSOR' #機体名宣言
FILENAME = "data_log_100.csv" #読み込みファイル名宣言
lines = sum(1 for line in open(FILENAME)) #CSVファイルの行数を取得
latitude = [] #緯度
longitude = [] #経度



#main.pyから吐かれるcsvの中身
#['latitude','longitude','pressure[hPa]','temperature[degC]', 
#'humidity[percent]', 'altitude', 'heading', 'roll', 'pitch', 
#'mag_x', 'mag_y', 'mag_z', 'gyro_x', 'gyro_y', 'gyro_z', 
#'accel_x', 'accel_y', 'accel_z', 'distance', 'direction']
    
# ファイルを読み込みモードでオープン
try:
    with open(FILENAME, 'r') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        header = next(csv_reader)

        for row in csv_reader: #緯度経度情報をリストに追加
            latitude.append(float(row[0]))
            longitude.append(float(row[1]))

except FileNotFoundError as e:
    print(e)



#グラフ表記の準備
titlefont = 16
axisfont = 12

xmax = max(longitude)
xmin = min(longitude)
ymax = max(latitude)
ymin = min(latitude)

#取得した時間を図のタイトルに指定
plt.figure(num=datetime.now().strftime('%Y%m%d %H%M%S'))

#グラフ表示範囲の指定
plt.xlim(xmin - 0.001, xmax + 0.001)
plt.ylim(ymin - 0.001, ymax + 0.001)

#タイトルラベル表示
fp = FontProperties(fname='C:\WINDOWS\Fonts\msgothic.ttc', size = titlefont)
plt.title(ROVERNAME + "航路ログ", fontsize = titlefont, fontproperties=fp)

#軸ラベル表示
plt.xlabel('longitude', fontsize = axisfont)
plt.ylabel('latitude', fontsize = axisfont)
#グリッド表示
plt.grid(color='gray')
#枠消し
direct = ["right", "left", "top", "bottom"]
for w in direct:
    plt.gca().spines[w].set_color("none")

#航路表示
plt.plot(longitude, latitude)#横軸=経度　縦軸=緯度

# X軸の数字をオフセットを使わずに表現する
plt.gca().get_xaxis().get_major_formatter().set_useOffset(False)
# X軸の数字をオフセットを使わずに表現する
plt.gca().get_yaxis().get_major_formatter().set_useOffset(False)

#始点終点表示
plt.plot(longitude[0], latitude[0], marker='x', color='green', markersize=20)
plt.plot(longitude[-1], latitude[-1], marker='x', color='red', markersize=20)
#始点終点tagの表記
plt.text(longitude[0], latitude[0]-0.0005, 'Start', fontsize=20, color='green', fontproperties=fp)
plt.text(longitude[-1], latitude[-1]-0.0005, 'Goal', fontsize=20, color='red', fontproperties=fp)



plt.show()




'''
このサイトがほぼ正解
http://python-remrin.hatenadiary.jp/entry/2017/05/27/114816

テスト用のデータほしい
＞＞＞グーグルマイマップってのでKMLファイルがエクスポートできるらしくて
そこからCSVファイルに変換する
＞＞＞gpxというファイルが逐一座標を記録してくれるらしい
ファイル出力サイト
https://www.330k.info/software/create_gpx_with_google_maps/
gpx2csv変換サイト
http://usoinfo.if.land.to/osmtool/fileview.php?file=CV5cc4872c1e1562ac.csv&ret=gpslog2csv.php
'''