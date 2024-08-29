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
(全てpipで入ります)
- requests
- bs4
- pandas
- plotly


## 使い方
### CPUについて確認する場合
```python
### Passmark　ベンチマークスコアを取得する
python get_passmark_scores.py
### 価格.comからCPUの最安価格を取得してくる
python get_cpu_price_list.py
### 価格パフォーマンスをグラフ化する
python get_cpu_value_performance.py
```

### GPUについて確認する場合
```python
### 3DMark ベンチマークスコアを取得する
python get_3dmark_scores.py
### 価格.comからGPUの最安価格を取得してくる
python get_gpu_price_list.py
### 価格パフォーマンスをグラフ化する
python get_gpu_value_performance.py
```

## サンプル
### CPUのデータ
![CPU]()
### GPUのデータ
![GPU]()

