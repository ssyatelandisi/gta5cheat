windres resource\gtaLib_resource.rc -o resource\gtaLib_resource.o
g++ -shared -fPIC src\gtaLib.cpp resource\gtaLib_resource.o -O3 -std=c++11 -finput-charset=UTF-8 -fexec-charset=GBK -static -s -o gtaLib.dll
if exist "resource\*.o" (
    del resource\*.o
)
pause