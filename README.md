# proposal_packages

モデルデータ操作やGraphillionの方向性ラッパーをPythonのモジュールにしたファイル

* **dat_utils.py**  
モデルデータの各パラメータをPythonで使える形式にして取り出す

* **directed_graph.py**  
Graphillionで有向グラフのパス列挙を可能にするラッパー

* **directed_link.py**  
Graphillionで双方向リンクを持つグラフののパス列挙を可能にするラッパー  
仮想ノードを１個追加する

* **directed_link_two_virtual_nodes.py**  
Graphillionで双方向リンクを持つグラフののパス列挙を可能にするラッパー  
仮想ノードを２個追加する

* **drawing.py**  
モデルデータのNetworkXグラフオブジェクトの作成、描画を行う
