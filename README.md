## このプログラムについて
・energy_xにE1_minからE1_maxの間もしくは、2000~2005番に入っているデータの最大値+ x_energyがE1_minからE1_maxのデータが入ってた場合、その行のデータ全体を、親データとします。
・親データと同じストリップ_xとストリップ_yの場所に energy_xがE2_minからE2_maxの間もしくは、2000~2005番に入っているデータの最大値+ x_energyがE2_minからE2_maxのデータが入ってた場合かつ、このデータのtimestampと親データのtimestampの差が定数time以下の時、その行のデータ全体を娘１データとします。
・親データと同じストリップ_xとストリップ_yの場所に energy_xがE3_minからE3_maxの間もしくは、2000~2005番に入っているデータの最大値+ x_energyがE3_minからE3_maxのデータが入ってた場合かつ、このデータのtimestampと親データのtimestampの差が定数time以下の時、その行のデータ全体を娘２データとします。
・その他娘も同様の判定を行い候補とします。現在、娘5まで対応しています。
### その他しぼりこみ条件
・energy_xまたはenergy_yに-1が入っていた場合、そのデータは候補にはしません。
・TDCにエネルギーが記録されていた場合、そのデータは候補にはしません。


### 入力するファイルのデータ構造
一行で下記のものカンマ区切りとなっていることを想定しています。

イベントNo, 0,  ストリップx, energy_x,  ストリップy,  energy_y、 side_0~15, Energy0~15, TDC_0~4, ts0~4, Timestamp

イベントNo  : 自然数のカウントアップ
ストリップx,ストリップy : 自然数
energy_x,energy_y,Energy0~15,ts0~4 [MeV]
side_0~15 : 2000 ~ 2015
TDC_0~4 : 3000 ~ 3004
Timestamp [10ns]

### 出力するデータ
```
----setting---
daughter1 : 7 ~ 10 time=5
daughter2 : ...
——-----
親データの 行の内容
娘１データの行の内容
娘２データの行の内容
-------
...

```

## 使い方
1. 判定に用いる変数を入力してください。
1. 読み込むファイルを指定してください。
1. runを投下してください。
1. 処理が終了すると、ファイルダイアログが開きます。ファイルの保存先、ファイル名の指定をしてください。

###　判定に用いる変数について
min,max[MeV]
time[s]
上記で入力できるようになっています。

### 現在の入力値の保存
SAVE -> SAVE NOW SETTINGS
daughter1~5のmin,max,timeを保存します。

### file選択時の初期ディレクトリの変更
現在はsettings.jsonからになっています。
in_dir:入力ファイル選択時に初期ディレクトリ
out_dir:保存先の選択時の初期ディレクトリ

### 処理終了後にファイルダイアログをキャンセルしてしまった時の対応
project配下にtemp.txtがいるので、他の処理を始める前にそちらをコピーまたは移動して利用してください。


