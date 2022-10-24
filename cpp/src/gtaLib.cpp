#define GTALIB_EXPORTS
#include <windows.h>
#include <stdio.h>
#include <ctype.h>
#include <string.h>
#include <sys/stat.h>
#include <time.h>
#include <winuser.h>
#include <memoryapi.h>
#include <processthreadsapi.h>
#include <tlhelp32.h>
#include <string>
#include <vector>
#include "gtaLib.h"

DWORD pid;
HANDLE hProcess;
QWORD BlipPTR;
QWORD GlobalPTR;
QWORD LocalScriptsPTR;
QWORD PickupDataPTR;
QWORD PlayerCountPTR;
QWORD ReplayInterfacePTR;
QWORD WorldPTR;
QWORD WeatherPTR;
SIZE_T hModule;
SIZE_T moduleSize;

/**
 * @brief 特征码结构体
 * name string 名称
 * mask string 特征码
 */
MASK masks[] = {
    {"WorldPTR", "48 8B 05 ? ? ? ? 45 ? ? ? ? 48 8B 48 08 48 85 C9 74 07"},
    {"BlipPTR", "4C 8D 05 ? ? ? ? 0F B7 C1"},
    {"ReplayInterfacePTR", "48 8D 0D ? ? ? ? 48 8B D7 E8 ? ? ? ? 48 8D 0D ? ? ? ? 8A D8 E8"},
    {"LocalScriptsPTR", "48 8B 05 ? ? ? ? 8B CF 48 8B 0C C8 39 59 68"},
    {"GlobalPTR", "4C 8D 05 ? ? ? ? 4D 8B 08 4D 85 C9 74 11"},
    {"PlayerCountPTR", "48 8B 0D ? ? ? ? E8 ? ? ? ? 48 8B C8 E8 ? ? ? ? 48 8B CF"},
    {"PickupDataPTR", "48 8B 05 ? ? ? ? 48 8B 1C F8 8B"},
    {"WeatherPTR", "48 83 EC ? 8B 05 ? ? ? ? 8B 3D ? ? ? ? 49"}};
char VERSION_MASK[] = "31 2E 36 31 00";
/**
 * @brief 键盘事件监听 需要单独线程运行
 *
 * @return UINT
 */
UINT keyboard_watch()
{
    if (GetAsyncKeyState(VK_F1) & 0x8000)
    {
        return VK_F1;
    }
    else if (GetAsyncKeyState(VK_F3) & 0x8000)
    {
        return VK_F3;
    }
    else if (GetAsyncKeyState(VK_F4) & 0x8000)
    {
        return VK_F4;
    }
    else if (GetAsyncKeyState(VK_F5) & 0x8000)
    {
        return VK_F5;
    }
    else if (GetAsyncKeyState(VK_F6) & 0x8000)
    {
        return VK_F6;
    }
    else if (GetAsyncKeyState(VK_F7) & 0x8000 && !(GetAsyncKeyState(VK_LCONTROL) & 0x8000))
    {
        return VK_F7;
    }
    else if (GetAsyncKeyState(VK_LCONTROL) & 0x8000 && GetAsyncKeyState(VK_F7) & 0x8000)
    {
        return VK_LCONTROL << 8 | VK_F7;
    }
    else if (GetAsyncKeyState(VK_F8) & 0x8000)
    {
        return VK_F8;
    }
    else if (GetAsyncKeyState(VK_LCONTROL) & 0x8000 && GetAsyncKeyState(VK_F9) & 0x8000)
    {
        return VK_LCONTROL << 8 | VK_F9;
    }
    else if (GetAsyncKeyState(VK_LCONTROL) & 0x8000 && GetAsyncKeyState(VK_F11) & 0x8000)
    {
        return VK_LCONTROL << 8 | VK_F11;
    }
    else if (GetAsyncKeyState(VK_LCONTROL) & 0x8000 && GetAsyncKeyState(VK_OEM_3) & 0x8000) // LCTRL+~
    {
        return VK_LCONTROL << 8 | VK_OEM_3;
    }
    else if (GetAsyncKeyState(VK_LCONTROL) & 0x8000 && GetAsyncKeyState(VK_DELETE) & 0x8000)
    {
        return VK_LCONTROL << 8 | VK_DELETE;
    }
    else if (GetAsyncKeyState('Q') & 0x8000)
    {
        return 'Q';
    }
    else if (GetAsyncKeyState('F') & 0x8000)
    {
        return 'F';
    }
    else if (GetAsyncKeyState(VK_LCONTROL) & 0x8000 && GetAsyncKeyState('R') & 0x8000)
    {
        return VK_LCONTROL << 8 | 'R';
    }
    else if (GetAsyncKeyState(VK_LCONTROL) & 0x8000 && GetAsyncKeyState('1') & 0x8000)
    {
        return VK_LCONTROL << 8 | '1';
    }
    else if (GetAsyncKeyState(VK_LCONTROL) & 0x8000 && GetAsyncKeyState('2') & 0x8000)
    {
        return VK_LCONTROL << 8 | '2';
    }
    else if (GetAsyncKeyState(VK_DIVIDE) & 0x8000) // NUM /
    {
        return VK_DIVIDE;
    }
    else if (GetAsyncKeyState(VK_MULTIPLY) & 0x8000) // NUM *
    {
        return VK_MULTIPLY;
    }
    return 0;
}

/**
 * @brief joaat运算
 *
 * @param input 输入字符串指针
 * @return unsigned int
 */
unsigned int joaat(char *input)
{
    unsigned int num1 = 0U;
    int i = 0;
    while (input[i] != '\0')
    {
        unsigned int num2 = num1 + (unsigned int)tolower(input[i]);
        unsigned int num3 = num2 + (num2 << 10);
        num1 = num3 ^ num3 >> 6;
        i++;
    }
    unsigned int num4 = num1 + (num1 << 3);
    unsigned int num5 = num4 ^ num4 >> 11;
    return num5 + (num5 << 15);
}

/**
 * @brief global地址
 *
 * @param offset 偏移
 * @return QWORD
 */
QWORD globalAddress(SIZE_T offset)
{
    QWORD addr[2] = {GlobalPTR + 8 * ((offset >> 0x12) & 0x3F), 8 * (offset & 0x3FFFF)};
    return get_addr64(addr, 2);
}

/**
 * @brief local地址
 *
 * @param name 线程名
 * @return QWORD
 */
QWORD localAddress(char *name, SIZE_T offset)
{
    QWORD p = read_qword(LocalScriptsPTR);
    for (SIZE_T i = 0; i < 54; i++)
    {
        QWORD pointer = read_qword(p + i * 0x8);
        char buffer[MAX_PATH] = {0};
        if (ReadProcessMemory(hProcess, (LPCVOID)(pointer + 0xD4), buffer, MAX_PATH, NULL))
        {
            if (stricmp(name, buffer) == 0)
            {
                return read_qword(pointer + 0xB0) + offset * 8;
            }
        }
    }
    return 0;
}

/**
 *
 * @brief 由进程名获取进程id
 *
 * @param processName 进程名
 * @return DWORD 进程id
 */
DWORD get_pid(char *processName)
{
    // 创建进程快照
    HANDLE hProcessSnapshot = CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0); //进程快照
    if (hProcessSnapshot == INVALID_HANDLE_VALUE)
    {
        MessageBoxA(NULL, "创建进程快照失败", "错误", MB_ICONERROR | MB_OK);
        throw "创建模块快照失败";
    }
    PROCESSENTRY32 process;                  //进程结构体
    process.dwSize = sizeof(PROCESSENTRY32); //进程结构体长度
    if (Process32First(hProcessSnapshot, &process) != TRUE)
    {
        MessageBoxA(NULL, "获取进程失败", "错误", MB_ICONERROR | MB_OK);
        throw "获取进程快照失败";
    }
    do
    {
        if (stricmp((char *)process.szExeFile, processName) == 0) //查找进程
        {
            return process.th32ProcessID;
        }
    } while (Process32Next(hProcessSnapshot, &process));
    char msg0[] = "没有找到";
    char *msg1 = strcat(msg0, processName);
    char *msg2 = strcat(msg1, (char *)"进程。");
    MessageBoxA(NULL, msg1, "错误", MB_ICONERROR | MB_OK);
    return 0;
}

/**
 * @brief 获取进程句柄
 *
 * @param pid 进程id
 * @return HANDLE 进程句柄
 */
HANDLE get_hProcess(DWORD pid)
{
    if (pid == 0)
    {
        MessageBoxA(NULL, "PID错误", "错误", MB_ICONERROR | MB_OK);
        return 0;
    }
    return OpenProcess(PROCESS_ALL_ACCESS, FALSE, pid);
}

/**
 * @brief 关闭释放句柄
 *
 * @param handle
 */
void close_hanle(HANDLE handle)
{
    CloseHandle(handle);
}

/**
 * @brief 结束进程
 *
 * @param hProcess
 */
void kill_process(HANDLE hProcess)
{
    if (hProcess == 0)
    {
        return;
    }
    TerminateProcess(hProcess, 0);
}

/**
 * @brief 获取模块句柄
 *
 * @param pid 进程id
 * @param moduleName 模块名称
 * @param [in,out] moduleSize 模块大小
 * @return HMODULE 模块句柄
 */
SIZE_T get_hModule(DWORD pid, char *moduleName, SIZE_T *moduleSize)
{
    HANDLE hModuleSnapshot = CreateToolhelp32Snapshot(TH32CS_SNAPMODULE, pid);
    if (hModuleSnapshot == INVALID_HANDLE_VALUE)
    {
        MessageBoxA(NULL, "创建模块快照失败", "错误", MB_ICONERROR | MB_OK);
        throw "创建模块快照失败";
    }
    MODULEENTRY32 module;                  //模块结构体
    module.dwSize = sizeof(MODULEENTRY32); //模块结构体长度
    if (Module32First(hModuleSnapshot, &module) != TRUE)
    {
        MessageBoxA(NULL, "获取模块失败", "错误", MB_ICONERROR | MB_OK);
        throw "获取模块快照失败";
    }
    do
    {
        if (stricmp((char *)module.szModule, moduleName) == 0) //查找模块
        {
            if (moduleSize != 0)
            {
                *moduleSize = module.modBaseSize;
            }
            return (SIZE_T)module.hModule;
        }
    } while (Module32Next(hModuleSnapshot, &module));
    if (moduleSize != 0)
    {
        *moduleSize = 0;
    }
    return 0;
}

/**
 * @brief 字符串分割
 *
 * @param str 字符串
 * @param s 分隔符
 * @return vector<char*>
 */
vector<char *> split(char *str, const char *s)
{
    vector<char *> temp;
    char *strCopy = new char[strlen(str) + 1];
    strcpy(strCopy, str);
    char *res = strtok(strCopy, s);
    while (res != NULL)
    {
        temp.push_back(res);
        res = strtok(NULL, s);
    }
    return temp;
}

/**byte
 * @brief WCHAR转char
 *
 * @param wchar
 * @return char*
 */
char *wchar2char(const WCHAR *wchar)
{
    int len = WideCharToMultiByte(CP_ACP, 0, wchar, wcslen(wchar), NULL, 0, NULL, NULL);
    char *m_char = new char[len + 1];
    WideCharToMultiByte(CP_ACP, 0, wchar, wcslen(wchar), m_char, len, NULL, NULL);
    m_char[len] = '\0';
    return m_char;
}

/**
 * @brief 字节码向量转数值向量
 *
 * @param bytecodearray
 * @return vector<WORD>
 */
vector<WORD> bytecodearray2bytenumberarray(vector<char *> BYTEcodearray)
{
    vector<WORD> temp;
    for (unsigned int i = 0; i < BYTEcodearray.size(); i++)
    {
        if (stricmp(BYTEcodearray[i], "?") == 0 || stricmp(BYTEcodearray[i], "??") == 0)
        {
            temp.push_back(256);
        }
        else
        {
            temp.push_back((WORD)stoi(BYTEcodearray[i], 0, 16));
        }
    }
    return temp;
}

/**
 * @brief 有限个内存字节数组特征码查找
 *
 * @param memory
 * @param length
 * @param maskCode
 * @return SIZE_T
 */
SIZE_T memoryMaskCode_search(BYTE *memory, SIZE_T length, char *maskCode)
{
    if (length > 0x10000000) // 256M
    {
        printf("内存占用过高");
        return -1;
    }
    vector<char *> BYTECodeArray = split(maskCode, " ");
    vector<WORD> BYTENumberArray = bytecodearray2bytenumberarray(BYTECodeArray);

    SIZE_T posStart = 0;
    SIZE_T posEnd = posStart + length - BYTENumberArray.size();
    unsigned int curIndex = 0;
    while (posStart <= posEnd)
    {
        if (memory[posStart] == BYTENumberArray[curIndex] || BYTENumberArray[curIndex] == 256)
        {
            curIndex += 1;
            if (curIndex >= BYTENumberArray.size())
            {
                posStart = posStart - BYTENumberArray.size() + 1;
                return posStart;
            }
        }
        else if (memory[posStart] == BYTENumberArray[0] || BYTENumberArray[0] == 256)
        {
            curIndex = 1;
        }
        else
        {
            curIndex = 0;
        }
        posStart++;
    }
    return -1;
}

/**
 * @brief 进程模块内存特征码定位
 *
 */
void get_process_ptr()
{
    char processName[] = "gta5.exe";
    pid = get_pid(processName);
    if (pid == 0)
    {
        return;
    }
    hProcess = get_hProcess(pid);
    if (hProcess == 0)
    {
        return;
    }
    hModule = get_hModule(pid, processName, &moduleSize);
    if (hModule == 0)
    {
        return;
    }
    BYTE *memory = new BYTE[moduleSize];
    ReadProcessMemory(hProcess, (LPCVOID)hModule, memory, moduleSize, NULL);
    for (unsigned int i = 0; i < sizeof(masks) / sizeof(masks[0]); i++)
    {
        SIZE_T pos = memoryMaskCode_search(memory, moduleSize, masks[i].mask);
        if (pos != 0)
        {
            DWORD match;
            QWORD ptr;
            switch (i)
            {
            case 0:
                memcpy(&match, &memory[pos + 3], 4);
                ptr = hModule + pos + match + 3 + 4;
                WorldPTR = ptr;
                break;
            case 1:
                memcpy(&match, &memory[pos + 3], 4);
                ptr = hModule + pos + match + 3 + 4;
                BlipPTR = ptr;
                break;
            case 2:
                memcpy(&match, &memory[pos + 3], 4);
                ptr = hModule + pos + match + 3 + 4;
                ReplayInterfacePTR = ptr;
                break;
            case 3:
                memcpy(&match, &memory[pos + 3], 4);
                ptr = hModule + pos + match + 3 + 4;
                LocalScriptsPTR = ptr;
                break;
            case 4:
                memcpy(&match, &memory[pos + 3], 4);
                ptr = hModule + pos + match + 3 + 4;
                GlobalPTR = ptr;
                break;
            case 5:
                memcpy(&match, &memory[pos + 3], 4);
                ptr = hModule + pos + match + 3 + 4;
                PlayerCountPTR = ptr;
                break;
            case 6:
                memcpy(&match, &memory[pos + 3], 4);
                ptr = hModule + pos + match + 3 + 4;
                PickupDataPTR = ptr;
                break;
            case 7:
                memcpy(&match, &memory[pos + 6], 4);
                ptr = hModule + pos + match + 6 + 4;
                WeatherPTR = ptr;
                break;
            default:
                break;
            }
            printf("%-18s: gta5.exe + 0x%08llX\n", masks[i].name, ptr - hModule);
        }
    }
    if (memoryMaskCode_search(memory, moduleSize, VERSION_MASK) == -1)
    {
        MessageBoxA(NULL, "gtaLib.dll版本与当前游戏版本不匹配，可能导致部分功能无效。", "警告", MB_ICONWARNING | MB_OK);
    }
    delete[] memory;
}

/**
 * @brief 从文件获取ptr偏移方法2
 *
 * @param fileName 文件名
 */
void get_file_ptr(char *fileName)
{
    FILE *fp;
    if ((fp = fopen(fileName, "rb")) == NULL)
    {
        char msg[128];
        strcpy(msg, fileName);
        strcat(msg, "文件不存在");
        printf("%s\n", msg);
        return;
    }
    struct stat statbuf;
    stat(fileName, &statbuf);
    SIZE_T fileSize = (SIZE_T)statbuf.st_size;
    BYTE *fileMemory = new BYTE[fileSize];
    fread(fileMemory, fileSize, 1, fp);

    for (MASK mask : masks)
    {
        SIZE_T pos = memoryMaskCode_search(fileMemory, fileSize, mask.mask);
        DWORD match;
        memcpy(&match, &fileMemory[pos + 3], 4);
        printf("%-18s: %s + 0x%08llX\n", mask.name, fileName, pos + 3 + match + 4);
    }
    delete[] fileMemory;
}

/**
 * @brief 检查地址有效性
 *
 * @param addr
 * @return BOOLEAN
 */
BOOLEAN check_valid(QWORD addr)
{
    if (0x00400000 <= addr && addr <= hModule + moduleSize)
    {
        return TRUE;
    }
    else
    {
        return FALSE;
    }
}

template <typename T>
T read_memory(SIZE_T address)
{
    T buffer = 0;
    ReadProcessMemory(hProcess, (LPCVOID)address, &buffer, sizeof(buffer), NULL);
    return buffer;
}

template <typename T>
void write_memory(SIZE_T address, T buffer)
{
    WriteProcessMemory(hProcess, (LPVOID)address, &buffer, sizeof(buffer), NULL);
}

template <typename T>
T pointer_memory(QWORD *addrArray, int length)
{
    QWORD addr = addrArray[0];
    for (int i = 1; i < length; i++)
    {
        addr = read_memory<QWORD>(addr) + addrArray[i];
    }
    return read_memory<T>(addr);
}

template <typename T>
void pointer_memory(QWORD *addrArray, int length, T value)
{
    QWORD addr = addrArray[0];
    for (int i = 1; i < length; i++)
    {
        addr = read_memory<QWORD>(addr) + addrArray[i];
    }
    write_memory<T>(addr, value);
}

int read_int(SIZE_T address)
{
    return read_memory<int>(address);
}

void write_int(SIZE_T address, int buffer)
{
    write_memory(address, buffer);
}

float read_float(SIZE_T address)
{
    return read_memory<float>(address);
}

void write_float(SIZE_T address, float buffer)
{
    write_memory(address, buffer);
}

double read_double(SIZE_T address)
{
    return read_memory<double>(address);
}

void write_double(SIZE_T address, double buffer)
{
    write_memory(address, buffer);
}

char read_char(SIZE_T address)
{
    return read_memory<char>(address);
}

void write_char(SIZE_T address, char buffer)
{
    write_memory(address, buffer);
}

BYTE read_byte(SIZE_T address)
{
    return read_memory<BYTE>(address);
}

void write_byte(SIZE_T address, BYTE buffer)
{
    write_memory(address, buffer);
}

WORD read_word(SIZE_T address)
{
    return read_memory<WORD>(address);
}

void write_word(SIZE_T address, WORD buffer)
{
    write_memory<WORD>(address, buffer);
}

DWORD read_dword(SIZE_T address)
{
    return read_memory<DWORD>(address);
}

void write_dword(SIZE_T address, DWORD buffer)
{
    write_memory(address, buffer);
}

QWORD read_qword(SIZE_T address)
{
    return read_memory<QWORD>(address);
}

void write_qword(SIZE_T address, QWORD buffer)
{
    write_memory(address, buffer);
}

short read_short(SIZE_T address)
{
    return read_memory<SHORT>(address);
}

void write_short(SIZE_T address, short buffer)
{
    write_memory(address, buffer);
}

void read_bytes(SIZE_T address, void *buffer, SIZE_T length)
{
    ReadProcessMemory(hProcess, (LPCVOID)address, (LPVOID)buffer, (SIZE_T)length, NULL);
}

void write_bytes(SIZE_T address, void *buffer, SIZE_T length)
{
    WriteProcessMemory(hProcess, (LPVOID)address, (LPCVOID)buffer, (SIZE_T)length, NULL);
}

inline BYTE pread_byte(QWORD *addrArray, int length)
{
    return pointer_memory<BYTE>(addrArray, length);
}

inline void pwrite_byte(QWORD *addrArray, int length, BYTE value)
{
    pointer_memory<BYTE>(addrArray, length, value);
}

inline WORD pread_word(QWORD *addrArray, int length)
{
    return pointer_memory<WORD>(addrArray, length);
}

inline void pwrite_word(QWORD *addrArray, int length, WORD value)
{
    pointer_memory<WORD>(addrArray, length, value);
}

inline short pread_short(QWORD *addrArray, int length)
{
    return pointer_memory<SHORT>(addrArray, length);
}

inline void pwrite_short(QWORD *addrArray, int length, short value)
{
    pointer_memory<SHORT>(addrArray, length, value);
}

inline DWORD pread_dword(QWORD *addrArray, int length)
{
    return pointer_memory<DWORD>(addrArray, length);
}

inline void pwrite_dword(QWORD *addrArray, int length, DWORD value)
{
    pointer_memory<DWORD>(addrArray, length, value);
}

inline int pread_int(QWORD *addrArray, int length)
{
    return pointer_memory<int>(addrArray, length);
}

inline void pwrite_int(QWORD *addrArray, int length, int value)
{
    pointer_memory<int>(addrArray, length, value);
}

inline float pread_float(QWORD *addrArray, int length)
{
    return pointer_memory<float>(addrArray, length);
}

inline void pwrite_float(QWORD *addrArray, int length, float value)
{
    pointer_memory<float>(addrArray, length, value);
}

inline QWORD pread_qword(QWORD *addrArray, int length)
{
    return pointer_memory<QWORD>(addrArray, length);
}

inline void pwrite_qword(QWORD *addrArray, int length, QWORD value)
{
    pointer_memory<QWORD>(addrArray, length, value);
}

inline double pread_double(QWORD *addrArray, int length, double value)
{
    return pointer_memory<double>(addrArray, length);
}

inline void pwrite_double(QWORD *addrArray, int length, double value)
{
    pointer_memory<double>(addrArray, length, value);
}

inline void pread_bytes(QWORD *addrArray, int length, void *buffer, SIZE_T size)
{
    ReadProcessMemory(hProcess, (LPCVOID)get_address_ptr<QWORD>(addrArray, length), buffer, size, NULL);
}

inline void pwrite_bytes(QWORD *addrArray, int length, void *buffer, SIZE_T size)
{
    WriteProcessMemory(hProcess, (LPVOID)get_address_ptr<QWORD>(addrArray, length), buffer, size, NULL);
}

template <typename T>
T get_address_ptr(T *addrArray, int length)
{
    T addr = addrArray[0];
    for (int i = 1; i < length; i++)
    {
        addr = read_memory<T>(addr) + addrArray[i];
    }
    return addr;
}

QWORD get_addr64(QWORD *addrArray, int length)
{
    return get_address_ptr<QWORD>(addrArray, length);
}

DWORD get_addr32(DWORD *addrArray, int length)
{
    return get_address_ptr<DWORD>(addrArray, length);
}

/**
 * @brief dll注入
 *
 * @param hProcess
 * @param dllPath
 */
void inject_dll(DWORD pid, char *dllPath)
{
    HANDLE hProcess = get_hProcess(pid);
    if (hProcess == 0)
    {
        return;
    }
    char dllPathCopy[MAX_PATH];
    strcpy(dllPathCopy, dllPath);
    vector<char *> dllPathSplit = split(dllPathCopy, "\\");
    if (get_hModule(pid, dllPathSplit[dllPathSplit.size() - 1], nullptr) != 0)
    {
        char msg[128];
        strcpy(msg, dllPathSplit[dllPathSplit.size() - 1]);
        strcat(msg, "已经存在，终止注入\n");
        printf("%s\n", msg);
        return;
    }
    SIZE_T length = strlen(dllPath);
    LPVOID startAddress = VirtualAllocEx(hProcess, NULL, length + 1, MEM_COMMIT, PAGE_READWRITE);
    if (!WriteProcessMemory(hProcess, startAddress, dllPath, length, NULL))
    {
        return;
    }
    PTHREAD_START_ROUTINE LoadLibrary = (PTHREAD_START_ROUTINE)GetProcAddress(GetModuleHandleA("Kernel32.dll"), "LoadLibraryA");
    HANDLE hThread = CreateRemoteThreadEx(hProcess, NULL, 0, LoadLibrary, (LPVOID)startAddress, 0, NULL, NULL);
    WaitForSingleObject(hThread, INFINITE); //等待hThread线程执行完
    CloseHandle(hThread);
    CloseHandle(hProcess);
}

/**
 * @brief 按下按键
 *
 * @param scanKey 键盘扫描码 [可通过MapVirtualKeyA('a',MAPVK_VK_TO_VSC)转换获得: a->0x1E]
 */
void keydown(WORD scanKey)
{
    INPUT in;
    in.type = INPUT_KEYBOARD;
    in.ki.wScan = scanKey;
    in.ki.dwFlags = 0;
    in.ki.time = 0;
    in.ki.dwExtraInfo = 0;
    in.ki.dwFlags = KEYEVENTF_SCANCODE; //如果指定了，wScan会识别按键，而wVk会被忽略。
    SendInput(1, &in, sizeof(in));
}

/**
 * @brief 释放按键
 *
 * @param scanKey 键盘扫描码 [可通过MapVirtualKeyA('a',MAPVK_VK_TO_VSC)转换获得: a->0x1E]
 */
void keyup(WORD scanKey)
{
    INPUT in;
    in.type = INPUT_KEYBOARD;
    in.ki.wScan = scanKey;
    in.ki.dwFlags = 0;
    in.ki.time = 0;
    in.ki.dwExtraInfo = 0;
    in.ki.dwFlags = KEYEVENTF_SCANCODE | KEYEVENTF_KEYUP; //如果指定了，wScan会识别按键，而wVk会被忽略。 | 如果指定了，则说明该键正在被释放。如果没有指定，则表示该键正在被按下。
    SendInput(1, &in, sizeof(in));
}

/**
 * @brief 末日1买左卡右
 *
 */
void doomsday1_key_event()
{
    unsigned int SPACE = MapVirtualKeyA(VK_SPACE, MAPVK_VK_TO_VSC);
    unsigned int D = MapVirtualKeyA('D', MAPVK_VK_TO_VSC);
    keydown(SPACE);
    Sleep(30);
    keydown(D);
    Sleep(30);
    keyup(SPACE);
    Sleep(30);
    keyup(D);
}

/**
 * @brief 末日2买左卡右
 *
 */
void doomsday2_key_event()
{
    unsigned int SPACE = 0x39; // MapVirtualKeyA(VK_SPACE, MAPVK_VK_TO_VSC);
    unsigned int D = 0x20;     // MapVirtualKeyA('D', MAPVK_VK_TO_VSC);
    keydown(SPACE);
    Sleep(30);
    keydown(D);
    Sleep(30);
    keyup(SPACE);
    Sleep(30);
    keyup(D);
}

/**
 * @brief 末日3买左卡右下
 *
 */
void doomsday3_key_event()
{
    unsigned int SPACE = 0x39; // MapVirtualKeyA(VK_SPACE, MAPVK_VK_TO_VSC);
    unsigned int S = 0x1F;     // MapVirtualKeyA('S', MAPVK_VK_TO_VSC);
    unsigned int D = 0x20;     // MapVirtualKeyA('D', MAPVK_VK_TO_VSC);
    keydown(SPACE);
    Sleep(100);
    keydown(S);
    Sleep(30);
    keydown(D);
    Sleep(30);
    keyup(SPACE);
    Sleep(30);
    keyup(D);
    Sleep(30);
    keyup(S);
}

/**
 * @brief 定点传送
 *
 * @param position 坐标点x, y, z
 */
void teleport(float *position)
{
    QWORD playerInVehicle[] = {WorldPTR, 0x08, 0x0E52};
    QWORD playerXArray[] = {WorldPTR, 0x08, 0x30, 0x50};
    QWORD playerCameraXArray[] = {WorldPTR, 0x08, 0x90};
    QWORD vehicleXArray[] = {WorldPTR, 0x08, 0xD30, 0x30, 0x50};
    QWORD vehicleCameraXArray[] = {WorldPTR, 0x08, 0xD30, 0x90};
    if (pread_byte(playerInVehicle, len(playerInVehicle)) == 1)
    {
        pwrite_bytes(vehicleXArray, len(vehicleXArray), (void *)position, 12);
        pwrite_bytes(vehicleCameraXArray, len(vehicleCameraXArray), (void *)position, 12);
    }
    else
    {
        pwrite_bytes(playerXArray, len(playerXArray), (void *)position, 12);
        pwrite_bytes(playerCameraXArray, len(playerCameraXArray), (void *)position, 12);
    }
}

/**
 * @brief 导航点传送
 *
 */
void navigation_teleport()
{
    for (int i = 2000; i > 0; i--)
    {
        QWORD addr = read_qword(BlipPTR + i * 8);
        if (!check_valid(addr))
        {
            continue;
        }
        if (read_int(addr + 0x40) == 0x08 && read_int(addr + 0x48) == 0x54)
        {
            float z = (read_float(addr + 0x18) > 19.99 && read_float(addr + 0x18) < 20.01f) ? -255.0f : read_float(addr + 0x18) + 1.0f;
            float position[] = {read_float(addr + 0x10), read_float(addr + 0x14), z};
            teleport(position);
        }
    }
}

/**
 * @brief 目标点传送
 *
 */
void objective_teleport()
{
    for (int i = 2000; i > 0; i--)
    {
        QWORD addr = read_qword(BlipPTR + i * 8);
        if (!check_valid(addr))
        {
            continue;
        }
        QWORD buf0 = read_int(addr + 0x40);
        QWORD buf1 = read_int(addr + 0x48);
        if ((buf0 == 432 || buf0 == 443) && (buf1 == 59))
        {
            float position[] = {read_float(addr + 0x10), read_float(addr + 0x14), read_float(addr + 0x18) + 1.0f};
            teleport(position);
            return;
        }
        else if (buf0 == 1 && (buf1 == 5 || buf1 == 60 || buf1 == 66))
        {
            float position[] = {read_float(addr + 0x10), read_float(addr + 0x14), read_float(addr + 0x18) + 1.0f};
            teleport(position);
            return;
        }
        else if ((buf0 == 1 || buf0 == 225 || buf0 == 427 || buf0 == 478 || buf0 == 501 || buf0 == 523 || buf0 == 556) && (buf1 == 1 || buf1 == 2 || buf1 == 3 || buf1 == 54 || buf1 == 78))
        {
            float position[] = {read_float(addr + 0x10), read_float(addr + 0x14), read_float(addr + 0x18) + 1.0f};
            teleport(position);
            return;
        }
    }
}

/**
 * @brief
 *
 * @tparam T
 * @param offset
 * @return T
 */
template <typename T>
T read_ga(QWORD offset)
{
    return read_memory<T>(globalAddress(offset));
}

/**
 * @brief
 *
 * @tparam T
 * @param offset
 * @param value
 */
template <typename T>
void write_ga(QWORD offset, T value)
{
    write_memory<T>(globalAddress(offset), value);
}

/**
 * @brief stat赋值
 *
 * @param str
 * @param value
 */
void write_stat(char *stat, int value)
{
    char *s = new CHAR[strlen(stat)];
    strcpy(s, stat);
    if (memcmp(s, (char *)"MPx_", 4) == 0)
    {
        int playerNum = read_ga<int>(1574918);
        if (playerNum == 0)
        {
            s[2] = '0';
        }
        else if (playerNum == 1)
        {
            s[2] = '1';
        }
        else
        {
            return;
        }
    }
    unsigned int hash = joaat(s);
    delete[] s;
    DWORD Stat_ResotreHash = read_ga<DWORD>(1655453 + 4);
    int Stat_ResotreValue = read_ga<int>(1020252 + 5526);
    write_ga<DWORD>(1659575 + 4, hash);
    write_ga<int>(1020252 + 5526, value);
    write_ga<int>(1648034 + 1139, -1);
    Sleep(1000);
    write_ga<DWORD>(1659575 + 4, Stat_ResotreHash);
    write_ga<int>(1020252 + 5526, Stat_ResotreValue);
}

/**
 * @brief 定点传送敌对NPC
 *
 * @param position
 */
void teleport_enemy_npc(float *position)
{
    QWORD addrArray[] = {ReplayInterfacePTR, 0x18, 0};
    QWORD pedInterface = get_addr64(addrArray, len(addrArray));
    int maxPeds = read_int(pedInterface + 0x108);
    QWORD pedAddr = read_qword(pedInterface + 0x100);
    for (int i = 0; i < maxPeds; i++)
    {
        QWORD pedList = read_qword(pedAddr + i * 0x10);
        if (!check_valid(pedList))
        {
            continue;
        }
        QWORD playerAddr = read_qword(pedList + 0x010C8);
        if (check_valid(playerAddr)) //跳过自己
        {
            continue;
        }
        QWORD navigation = read_qword(pedList + 0x30);
        if (!check_valid(navigation))
        {
            continue;
        }
        BYTE enemyFlags = read_byte(pedList + 0x18C);
        if (enemyFlags > 1)
        {
            if (read_float(pedList + 0x280) < 100.0f) //跳过已死亡
            {
                continue;
            }
            write_bytes(navigation + 0x50, (void *)position, 12);
            write_bytes(pedList + 0x90, (void *)position, 12);
        }
    }
}

/**
 * @brief 杀死有威胁的NPC
 *
 */
void kill_enemy_npc()
{
    QWORD addrArray[] = {ReplayInterfacePTR, 0x18, 0};
    QWORD pedInterface = get_addr64(addrArray, len(addrArray));
    int maxPeds = read_int(pedInterface + 0x108);
    QWORD pedAddr = read_qword(pedInterface + 0x100);
    for (int i = 0; i < maxPeds; i++)
    {
        QWORD pedList = read_qword(pedAddr + i * 0x10);
        if (!check_valid(pedList))
        {
            continue;
        }
        QWORD playerAddr = read_qword(pedList + 0x010C8);
        if (check_valid(playerAddr)) //跳过自己
        {
            continue;
        }
        BYTE enemyFlags = read_byte(pedList + 0x18C);
        if (enemyFlags > 1)
        {
            write_float(pedList + 0x280, 99.0f);
        }
    }
}

/**
 * @brief 摧毁有威胁的NPC载具
 *
 */
void destroy_enemy_vehicles()
{
    QWORD addrArray[] = {ReplayInterfacePTR, 0x18, 0};
    QWORD pedInterface = get_addr64(addrArray, len(addrArray));
    int maxPeds = read_int(pedInterface + 0x108);
    QWORD pedAddr = read_qword(pedInterface + 0x100);
    for (int i = 0; i < maxPeds; i++)
    {
        QWORD pedList = read_qword(pedAddr + i * 0x10);
        if (!check_valid(pedList))
        {
            continue;
        }
        QWORD playerAddr = read_qword(pedList + 0x010C8);
        if (check_valid(playerAddr)) //跳过自己
        {
            continue;
        }
        BYTE enemyFlags = read_byte(pedList + 0x18C);
        if (enemyFlags > 1)
        {
            QWORD vehicleAddr = read_qword(pedList + 0xD30);
            write_float(vehicleAddr + 0x280, -1.0f);
            write_float(vehicleAddr + 0x840, -1.0f);
            write_float(vehicleAddr + 0x844, -1.0f);
            write_float(vehicleAddr + 0x908, -1.0f);
        }
    }
}

/**
 * @brief 线上修复载具
 *
 */
void repairing_vehicle()
{
    if (read_ga<int>(2703735 + 3576) != 0)
    {
        write_ga<int>(2703735 + 3576, 5); // 消除牛鲨睾酮效果
        return;
    }
    QWORD playerInVehicle[] = {WorldPTR, 0x08, 0x0E52};
    if (pread_byte(playerInVehicle, len(playerInVehicle)) != 1) //在载具上
    {
        return;
    }
    QWORD bstTrigger[] = {GlobalPTR + 0x8 * 0xA, 0x17BE28};
    pwrite_int(bstTrigger, len(bstTrigger), 1); // 空投牛鲨睾酮
    QWORD vehicleLifeArray[] = {WorldPTR, 0x08, 0xD30, 0x280};
    pwrite_float(vehicleLifeArray, len(vehicleLifeArray), 999.0f); //载具满血无法接到牛鲨睾酮
    QWORD fixVehValueArray[] = {PickupDataPTR, 0x228};
    DWORD fixVehValue = pread_dword(fixVehValueArray, len(fixVehValueArray));
    QWORD bstValueArray[] = {PickupDataPTR, 0x160};
    int bstValue = pread_int(bstValueArray, len(bstValueArray));
    QWORD pickupInterfaceArray[] = {ReplayInterfacePTR, 0x20};
    QWORD pickupInterface = pread_qword(pickupInterfaceArray, len(pickupInterfaceArray));
    int pickupCount = read_int(pickupInterface + 0x110);
    QWORD pickupList = read_qword(pickupInterface + 0x100);
    QWORD vehicleXArray[] = {WorldPTR, 0x08, 0xD30, 0x30, 0x50};
    QWORD vehicleCleanlinessArray[] = {WorldPTR, 0x08, 0xD30, 0x9F8};
    for (int i = 0; i < pickupCount; i++)
    {
        QWORD pickup = read_qword(pickupList + i * 0x10);
        int pickupValue = read_int(pickup + 0x490);
        if (pickupValue == bstValue)
        {
            write_dword(pickup + 0x490, fixVehValue);
            float position[3];
            pread_bytes(vehicleXArray, len(vehicleXArray), (LPVOID *)position, 12);
            write_bytes(pickup + 0x90, (void *)position, 12);
            pwrite_float(vehicleCleanlinessArray, len(vehicleCleanlinessArray), 0.0f); // 清洁载具外表
        }
    }
}

/**
 * @brief 线上刷出载具
 *
 * @param joaatHash
 */
void spawn_vehicle(unsigned int joaatHash)
{
    int offset = 2725439;
    QWORD heading0Array[] = {WorldPTR, 0x8, 0x30, 0x20};
    QWORD heading1Array[] = {WorldPTR, 0x8, 0x30, 0x30};
    float heading0 = pread_float(heading0Array, len(heading0Array));
    float heading1 = pread_float(heading1Array, len(heading1Array));
    QWORD playerPositionAddary[] = {WorldPTR, 0x08, 0x30, 0x50};
    float playerPosition[3];
    pread_bytes(playerPositionAddary, len(playerPositionAddary), playerPosition, 12);
    playerPosition[0] += heading1 * 5.0f;
    playerPosition[1] += heading0 * 5.0f;
    playerPosition[2] += 0.5;
    write_ga<float>(offset + 7 + 0, playerPosition[0]);
    write_ga<float>(offset + 7 + 1, playerPosition[1]);
    write_ga<float>(offset + 7 + 2, playerPosition[2]);
    write_ga<DWORD>(offset + 27 + 66, joaatHash);
    write_ga<int>(offset + 3, 0);
    write_ga<int>(offset + 5, 1);
    write_ga<int>(offset + 2, 1);
    write_ga<int>(offset + 27 + 5, -1);
    write_ga<int>(offset + 27 + 6, -1);
    write_ga<int>(offset + 27 + 7, -1);
    write_ga<int>(offset + 27 + 8, -1);
    write_ga<int>(offset + 27 + 15, 1);
    write_ga<int>(offset + 27 + 19, -1);
    write_ga<int>(offset + 27 + 20, 2);
    write_ga<int>(offset + 27 + 21, 3);
    write_ga<int>(offset + 27 + 22, 6);
    write_ga<int>(offset + 27 + 23, 9);
    write_ga<int>(offset + 27 + 24, 0);
    write_ga<int>(offset + 27 + 25, 14);
    write_ga<int>(offset + 27 + 26, 19);
    write_ga<int>(offset + 27 + 27, 1);
    write_ga<int>(offset + 27 + 28, 1);
    write_ga<int>(offset + 27 + 30, 1);
    write_ga<int>(offset + 27 + 32, 0);
    write_ga<int>(offset + 27 + 33, -1);
    write_ga<int>(offset + 27 + 60, 1);
    write_ga<int>(offset + 27 + 65, 0);
    write_ga<int>(offset + 27 + 67, 1);
    write_ga<int>(offset + 27 + 69, -1);
    write_ga<DWORD>(offset + 27 + 77, 4030726305);
    write_ga<BYTE>(offset + 27 + 77 + 1, 2);
    write_ga<int>(offset + 27 + 95, 14);
    write_ga<int>(offset + 27 + 94, 2);
}

/**
 * @brief 切换战局
 *
 * @param value
 */
void change_session(int value)
{
    if (value == -1)
    {
        write_ga<int>(1574589 + 2, value); // valueAddress
        write_ga<int>(1574589, 1);         // triggerAddress
    }
    else
    {
        write_ga<int>(1575015, value);
        write_ga<int>(1574589, 1);
    }
    Sleep(200);
    write_ga<int>(1574589, 0);
}

/**
 * @brief 调用外部的GTAHaX程序
 *
 */
void using_GTAHaX()
{
    FILE *fp;
    if ((fp = fopen("GTAHaXUI.exe", "rb")) == NULL)
    {
        return;
    }
    STARTUPINFOA si{0};
    PROCESS_INFORMATION pi{0};
    si.cb = sizeof(si);
    if (!CreateProcessA(
            NULL,
            (LPSTR) "GTAHaXUI.exe",
            NULL,
            NULL,
            FALSE,
            CREATE_NEW_CONSOLE,
            NULL,
            NULL,
            &si,
            &pi))
    {
        printf("打开GTAHaXUI.exe失败 (%d).\n", GetLastError());
        return;
    }
    else
    {
        Sleep(1000);
        HWND hW = FindWindowA((LPCSTR) "#32770", (LPCSTR) "man why can't life always be this easy");
        HWND btn = FindWindowExA(hW, NULL, (LPCSTR) "Button", (LPCSTR) "Import from file");
        SendMessageA(btn, WM_LBUTTONDOWN, 0, 0);
        Sleep(20);
        SendMessageA(btn, WM_LBUTTONUP, 0, 0);
        return;
    }
    WaitForSingleObject(pi.hProcess, INFINITE);
    CloseHandle(pi.hProcess);
    CloseHandle(pi.hThread);
}

/**
 * @brief 修改天气
 *
 * @param value
 */
void change_weather(int value)
{
    if (value == -1)
    {
        write_int(WeatherPTR + 0x24, -1);
    }
    else if (value == 13)
    {
        write_int(WeatherPTR + 0x24, 13);
    }
    write_int(WeatherPTR + 0x104, value);
}
