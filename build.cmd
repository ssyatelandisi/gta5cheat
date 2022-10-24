@REM pip install pyqt5 pyqt5-tools pyinstaller
if exist "dist" (
    del /q dist\*.*
)
if exist "GTAV Cheat.spec" (
    del /q *.spec
)
pyinstaller -w .\src\app.py --uac-admin -i icon.ico --version-file=version_info.txt -n="GTAV Cheat" --add-data="teleports.txt;.\\" --add-binary=".\cpp\gtaLib.dll;.\\" --clean -y
pyinstaller -Fw .\src\app.py --uac-admin -i icon.ico --version-file=version_info.txt -n="GTAV Cheat" --add-binary="teleports.txt;.\\" --add-binary=".\cpp\gtaLib.dll;.\\" --clean -y
if exist "teleports.txt" (
    copy teleports.txt "dist\GTAV Cheat\teleports.txt" /y
    copy teleports.txt "dist\teleports.txt" /y
)
if exist "YimMenu.dll" (
    copy YimMenu.dll "dist\GTAV Cheat\YimMenu.dll" /y
    copy YimMenu.dll "dist\YimMenu.dll" /y
)
pause