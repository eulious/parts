@echo off

@REM 参考サイト: https://qiita.com/yaju/items/3cea48dc3559450f194b
set dialog="about:<input type=file id=FILE><script language=vbscript>FILE.Click:
set dialog=%dialog%CreateObject("Scripting.FileSystemObject").GetStandardStream(1).WriteLine(FILE.value):
set dialog=%dialog%Close:resizeTo 0,0</script>"

python3 -V
if errorlevel 1 (
    echo pythonがPATHに存在しません。python.exeを選択して下さい。
    set file=
    for /f "tokens=* delims=" %%p in ('mshta.exe %dialog%') do set "file=%%p"
) else (
    set file=python3
)

"%file%" tools/setup.py

echo セットアップが完了しました。
echo start.batをダブルクリックしてUIを起動して下さい。
echo.

pause
