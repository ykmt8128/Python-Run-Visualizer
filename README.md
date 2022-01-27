# Python Run Visualizer

GitHubリポジトリ https://github.com/ykmt8128/Python-Run-Visualizer

## 起動方法

以下の二つの方法があります。基本的に一つ目を推奨します。
- このリポジトリをクローンし、`PythonRunVisualizer.exe`を実行
- このリポジトリをクローンし、python3で`main.py`を実行

## 環境要件

少なくとも以下の環境で動作することを確認しています。
- Python 3.8.10
- Windows 10 Home
- 各ライブラリについては`requirements.txt`参照

## 使い方

- `開く`ボタンでPythonファイルを選択すると、選択したファイルを実行し、実行順序を可視化したGIFアニメーションを作成し、表示します。
- `サンプルファイルを開く`ボタンを押すと、サンプルファイルで実行順序を可視化したGIFアニメーションを作成し、表示します。
- `GIFを保存`ボタンを押すと、生成されたGIFを保存できます。
- `終了`ボタンを押すと、アプリケーションを終了します。
- `オンラインインタプリタで実行する`にチェックを入れると、外部のオンラインPython実行サービスでプログラムを実行します。ローカルの環境で実行したくない場合やPythonをインストールしていない場合でも使用できます。

## 注意点

- 動作環境にインストールされているフォントによっては、正常に動作しなかったり、一部の文字が表示できない可能性があります。
- 「オンラインインタプリタで実行する」にチェックを入れない場合はローカルの環境でプログラムが実行されるため、PC環境に影響を与えるプログラムを実行させる際は気を付けてください。
- 実行するプログラムで使用しているライブラリやソースコードの長さ、出力文字列の長さ、エラーの発生、実行時間などによっては正常に動作しないことがあります。

## 使用ライブラリのライセンス

- PySimpleGUI  
https://github.com/PySimpleGUI/PySimpleGUI/blob/master/license.txt
- Pillow  
https://github.com/python-pillow/Pillow/blob/main/LICENSE
- Pygments  
https://github.com/pygments/pygments/blob/master/LICENSE 
- glotio-api  
https://github.com/raster0x2a/glotio-api/blob/master/LICENSE