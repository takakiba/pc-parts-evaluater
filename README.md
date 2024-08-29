# pc-parts-evaluater
CPUとGPUの日本におけるコストパフォーマンスを調査する

## 目的
PCパーツ選びをしていると，値段とスペックのバランスがどうなのかわからずコスパのいい構成になっているのか自信を持てないことがある．
海外のサイトではベンチマークと価格を併記してあるものの，日本市場でそのままの値段が当てはまるかは怪しい．
そこで，Webスクレイピングを使ってベンチマークと日本での市場価格をそれぞれ取得し，各パーツの価格パフォーマンスを簡単に確認するツールを作成した．


## 制作環境
Mac
Python 3.9.19

## 必要なライブラリ
- requests
- bs4
- pandas
- plotly
(全てpipで入ります)

## 使い方
```python
### CPUについて確認する場合
### Passmark　ベンチマークスコアを取得する
python get_passmark_scores.py
### 価格.comからCPUの最安価格を取得してくる
python get_cpu_price_list.py
### 価格パフォーマンスをグラフ化する
python get_cpu_value_performance.py
```



