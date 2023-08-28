#!/usr/bin/env python3

import sys
from shutil import rmtree
from os.path import exists
from platform import system
from traceback import print_stack
from subprocess import call
from urllib.request import urlopen
from tkinter.filedialog import askdirectory

IS_MAC = system() == "Darwin"
IS_WINDOWS = system() == "Windows"
IS_LINUX = system() == "Linux"


def ask(text: str):
    while True:
        print(f"{text}(y/n):", end="")
        x = input()
        if x == "y" or x == "yes" or x == "Y":
            return True
        elif x == "N" or x == "no":
            return False


if exists("venv"):
    if ask("以前の環境が存在します。再度セットアップしますか？"):
        rmtree("venv")
    else:
        sys.exit(0)

try:
    assert urlopen("https://pypi.orga/", timeout=5).status == 200
    PACKAGE_DIR = ""
except Exception as e:
    print_stack()
    print()
    print("インターネットの接続に失敗しました。")
    print("パッケージが存在するディレクトリを選択して下さい")
    PACKAGE_DIR = askdirectory()
    if PACKAGE_DIR == "":
        sys.exit(0)


trusted = "--trusted-host pypi.python.org --trusted-host files.pythonhosted.org --trusted-host pypi.org"
print("環境を作成しています...")
call(f'"{sys.executable}" -m venv venv', shell=True)
pip = '".\\venv\\Scripts\\pip.exe"' if IS_WINDOWS else "./venv/bin/pip"

if PACKAGE_DIR:
    command = f'{pip} install -r tools/requirements.txt --no-index --find-links="{PACKAGE_DIR}"'
else:
    call(f"{pip} install {trusted} -U pip", shell=True)
    command = f"{pip} install {trusted} -r tools/requirements.txt"
call(command, shell=True, stdout=sys.stdout)

print("=========================================")
print("環境構築が完了しました。")
if IS_WINDOWS:
    code = 'Set ws = CreateObject("Wscript.Shell")\n'
    code += 'ws.run ".\\venv\\Scripts\\python.exe hello.py", vbhide'
    open("start.vbs", "wt").write(code)
    print("start.vbsをダブルクリックして実行して下さい")
elif IS_LINUX or IS_MAC:
    code = "#!/bin/bash\n\n"
    code += "cd `dirname $0`\n"
    code += "nohup ./venv/bin/python3 app.py > /dev/null 2>&1 &\n"
    code += "echo このウィンドウは閉じても構いません。"
    if IS_MAC:
        open("start.command", "wt").write(code)
        call("chmod +x start.command", shell=True)
        print("start.commandをダブルクリックして実行して下さい")

print("このウィンドウは閉じても構いません。")
