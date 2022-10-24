version="v1.61"
echo "清理dist目录"
if [ -d "dist" ]
then
    rm -rf dist
    mkdir dist
else
    mkdir dist
fi
if [ -f "GTAV Cheat.spec" ]
then
    rm -rf GTAV Cheat.spec
fi
echo "编译dll文件"
cmake -S cpp -B cpp/build -G "MinGW Makefiles"
cmake --build cpp/build
if [ -f cpp/build/lib/libgtaLib.dll ]
then
cp cpp/build/lib/libgtaLib.dll cpp/gtaLib.dll
fi
echo "切换到python3.10"
source activate python3.10
pyuic5 ui/gtaui.ui -o src/gtaui.py
pyrcc5 ui/resource.qrc -o src/resource_rc.py
echo "同步到github"
git reset 10e0ae9314a3048bd05cf76c5ce5fe07dad0b77a
git push origin tag -d "$version"
git tag -d "$version"
git add .
git commit -m"$version"
git tag "$version"
git push -f
git push --tags
echo "本地编译exe"
pyinstaller -w ./src/app.py --uac-admin -i icon.ico --version-file=version_info.txt -n="GTAV Cheat" --add-data="teleports.txt;./" --add-binary="./cpp/gtaLib.dll;./" --clean -y
# pyinstaller -Fw ./src/app.py --uac-admin -i icon.ico --version-file=version_info.txt -n="GTAV Cheat" --add-data="teleports.txt;./" --add-binary="./cpp/gtaLib.dll;./" --clean -y
if [ -f "dist/GTAV Cheat.exe" ]
then
    cp teleports.txt "dist/teleports.txt"
fi
path=$(pwd)
cd dist
if [ -f "GTAV Cheat.exe" ]
then
7z a "GTAV_Cheat.zip" "GTAV Cheat.exe" "teleports.txt" -tZIP
fi
cd $path
if [ -f "YimMenu.dll" ]
then
    cp YimMenu.dll "dist/GTAV Cheat/YimMenu.dll"
    if [ -f "dist/GTAV Cheat.exe" ]
    then
        cp YimMenu.dll "dist/YimMenu.dll"
    fi
fi
