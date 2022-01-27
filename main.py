import subprocess
import os
import sys
import shutil
import asyncio
from asyncio.tasks import current_task

import PySimpleGUI as sg

import PIL
from PIL import Image, ImageFont, ImageDraw, ImageFile

from pygments.lexers import PythonLexer
from pygments.formatters import ImageFormatter
from pygments import highlight

from glotio import Runner


# 実行パスからの相対パスをもとに絶対パスを返す
def get_path(filename):
    current_path = os.path.dirname(os.path.abspath(sys.argv[0]))
    return os.path.join(current_path, filename)

# トレースログをもとにハイライトと出力をコマンド化したリスト形式に変換
def parse_trace(trace_stdout, filename):
    trace_step = []
    for line in trace_stdout.split("\n"):
        # 実行している行のログ
        if line.startswith(f"{filename}("):
            line_num = int(line[len(f"{filename}("):line.index(")")])
            trace_step.append(["highlight", line_num])
        # 概要ログ
        elif line.startswith(f" --- "):
            pass
        # 出力ログ
        else:
            trace_step.append(["stdout", line])
    
    return trace_step

# GIFを生成し、成功=0, 失敗=-1を返す
def make_gif(source_filepath, is_online=False):
    filename = os.path.basename(source_filepath)

    # Pythonのソースコードを読み込み
    try:
        with open(source_filepath, encoding="utf-8") as f:
            sourcecode = f.read()
    except Exception as e:
        print(e)
        return -1

    # オンラインインタプリタを使用
    if is_online:
        cmd = f"python3 -m trace --trace {filename}"
        glot = Runner("c42f1611-017f-4990-842b-a6b08b035d95")
        glot.set_lang("python")
        glot.set_code(sourcecode, filename=filename)
        glot.set_command(cmd)
        result = glot.run()["stdout"]
    # ローカル環境のPythonを使用
    else:
        cmd = f"python3 -m trace --trace {source_filepath}"
        result = subprocess.run(cmd, shell=True, text=True, stdout=subprocess.PIPE).stdout
    
    print(result)
    trace_step = parse_trace(result, filename)

    # tmp以下の一時ファイルを削除
    shutil.rmtree(get_path("tmp"))
    os.mkdir("tmp")

    # GIFの各フレームの画像を生成
    image_list = []
    image_num = 0
    stdout = ""
    for step in trace_step:
        if step[0] == "highlight":
            # フォーマッタを定義
            formatter = ImageFormatter(linenos=False, hl_lines=(step[1],), hl_color="#bbbbbb")
            tmp_image_path = get_path(os.path.join("tmp", f"highlighted{image_num}.png"))
            image_num += 1
            # ハイライト表示を追加して保存
            highlight(sourcecode, PythonLexer(), formatter, tmp_image_path)
            # フレームの画像を加工し、プログラムの出力を記述
            frame_image = PIL.Image.open(tmp_image_path)
            resized_frame_image = Image.new(frame_image.mode, (frame_image.width + 200, frame_image.height), "white")
            resized_frame_image.paste(frame_image, (0, 0))
            draw = ImageDraw.Draw(resized_frame_image)
            font = ImageFont.truetype("meiryo.ttc", 14)
            draw.text((frame_image.width + 8, 8), stdout, (0, 0, 0), font=font)
            resized_frame_image.save(tmp_image_path)

            image_list.append(resized_frame_image)

        elif step[0] == "stdout":
            stdout += step[1] + "\n"
    
    # 各フレームの画像を結合してGIFに変換
    try:
        image_list[0].save(get_path("highlighted.gif"),
            save_all=True, append_images=image_list[1:], duration=1000, loop=0)
    except Exception as e:
        print(e)
        return -1
    
    return 0

def main():
    # GUIの設定
    sg.theme("DarkBlue14")
    TITLE = "Python Run Visualizer"
    image_elem = sg.Image(None, key="-RESULT_GIF-")

    layout = [
        [sg.Text(TITLE)],
        [sg.Button("使い方"), sg.Button("開く"), sg.Button("サンプルファイルを開く"), sg.Button("GIFを保存"), sg.Button("終了")],
        [sg.Checkbox("オンラインインタプリタで実行する", default=False, key="-IS_ONLINE-"),],
        [image_elem],
    ]

    window = sg.Window(TITLE, layout, size=(900, 600))

    gif_set_flag = False
    num = 0
    while True:  # Event Loop
        event, values = window.read(timeout=1000, timeout_key='-UPDATE_GIF-')
        if event in (sg.WIN_CLOSED, '終了'):
            break
        elif event == "開く":
            source_filepath = sg.popup_get_file("Pythonファイルを選択")
            # キャンセル時
            if source_filepath is None:
                continue
            elif not os.path.isfile(source_filepath):
                sg.popup(f"ファイルパスが正しくありません。 {source_filepath}", title="Error")
                continue
            
            make_gif_result = make_gif(source_filepath, is_online=values["-IS_ONLINE-"])
            if make_gif_result == 0:
                gif_set_flag = True
            else:
                sg.popup("正常にGIFを生成できませんでした。", title="Error")
        
        elif event == "サンプルファイルを開く":
            source_filepath = get_path("sample.py")
            if not os.path.isfile(source_filepath):
                sg.popup(f"ファイルパスが正しくありません。 {source_filepath}", title="Error")
                continue
            
            make_gif_result = make_gif(source_filepath, is_online=values["-IS_ONLINE-"])
            if make_gif_result == 0:
                gif_set_flag = True
            else:
                sg.popup("正常にGIFを生成できませんでした。", title="Error")

        elif event == "使い方":
            image_elem.update(get_path("usage.png"))

        elif event == "GIFを保存":
            save_file_path = sg.popup_get_file('GIFを保存', save_as=True, file_types=(("GIF Files", ".gif"),))
            if save_file_path is None:
                continue
            elif not os.path.isdir(os.path.dirname(save_file_path)):
                sg.popup("ファイルパスが正しくありません。", title="Error")
                continue
            elif not os.path.exists(get_path("highlighted.gif")):
                sg.popup("先にGIFを生成してください。", title="Error")
                continue

            shutil.copy(get_path("highlighted.gif"), save_file_path)

        # フレームの更新
        if event == '-UPDATE_GIF-' and gif_set_flag:
            tmp_path = get_path(os.path.join("tmp", f"highlighted{num}.png"))
            if os.path.isfile(tmp_path):
                image_elem.update(tmp_path)
                num += 1
            else:
                gif_set_flag = False
                num = 0

    window.close()

if __name__ == "__main__":
    main()
