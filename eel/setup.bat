@echo off

@REM �Q�l�T�C�g: https://qiita.com/yaju/items/3cea48dc3559450f194b
set dialog="about:<input type=file id=FILE><script language=vbscript>FILE.Click:
set dialog=%dialog%CreateObject("Scripting.FileSystemObject").GetStandardStream(1).WriteLine(FILE.value):
set dialog=%dialog%Close:resizeTo 0,0</script>"

python3 -V
if errorlevel 1 (
    echo python��PATH�ɑ��݂��܂���Bpython.exe��I�����ĉ������B
    set file=
    for /f "tokens=* delims=" %%p in ('mshta.exe %dialog%') do set "file=%%p"
) else (
    set file=python3
)

"%file%" tools/setup.py

echo �Z�b�g�A�b�v���������܂����B
echo start.bat���_�u���N���b�N����UI���N�����ĉ������B
echo.

pause
