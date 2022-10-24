path=$(pwd)
if [ -d build ]
then
    rm -rf build
fi
cmake -S . -B build -G "MinGW Makefiles"
cmake --build build
if [ -f ./build/lib/libgtaLib.dll ]
then
    cp ./build/lib/libgtaLib.dll $path/gtaLib.dll
else
    echo "未找到libgtaLib.dll"
fi
cd $path
