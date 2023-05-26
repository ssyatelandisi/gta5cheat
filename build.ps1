if (Test-Path "dist") {
    Remove-Item dist -Recurse
}
if (Test-Path "GTAV Cheat.spec") {
    Remove-Item *.spec -Recurse
}
pyinstaller -w .\src\app.py --uac-admin -i icon.ico --version-file=version_info.txt -n="GTAV Cheat" --add-data="teleports.txt;.\\" --add-binary=".\cpp\gtaLib.dll;.\\" --clean -y
pyinstaller -Fw .\src\app.py --uac-admin -i icon.ico --version-file=version_info.txt -n="GTAV Cheat" --add-binary="teleports.txt;.\\" --add-binary=".\cpp\gtaLib.dll;.\\" --clean -y
if (Test-Path "teleports.txt") {
    Copy-Item -Path teleports.txt -Destination "dist\GTAV Cheat\teleports.txt"
    Copy-Item -Path teleports.txt -Destination "dist\teleports.txt"
}
if (Test-Path "YimMenu.dll") {
    Copy-Item -Path YimMenu.dll -Destination "dist\GTAV Cheat\YimMenu.dll"
    Copy-Item -Path YimMenu.dll -Destination "dist\YimMenu.dll"
}
