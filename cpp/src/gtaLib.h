#pragma once
#ifdef __GNUC__
#define EXPORT
#else
#ifdef GTALIB_EXPORTS
#define EXPORT __declspec(dllexport)
#else
#define EXPORT __declspec(dllimport)
#endif

#endif
#ifndef GTALIB_EXPORTS
#include <windows.h>
#include <string>
#include <vector>
#endif

#define len(T) sizeof(T) / sizeof(T[0])

typedef unsigned long long QWORD;

using std::stoi;
using std::vector;

extern DWORD pid;
extern HANDLE hProcess;
extern QWORD BlipPTR;
extern QWORD GlobalPTR;
extern QWORD LocalScriptsPTR;
extern QWORD PickupDataPTR;
extern QWORD PlayerCountPTR;
extern QWORD ReplayInterfacePTR;
extern QWORD WorldPTR;
extern QWORD WeatherPTR;
extern SIZE_T hModule;
extern SIZE_T moduleSize;

struct MASK
{
    char name[32];
    char mask[128];
};

char *wchar2char(const WCHAR *wchar);
vector<char *> split(char *str, const char *s);
vector<WORD> bytecodearray2bytenumberarray(vector<char *> bytecodearray);
template <typename T>
T read_memory(SIZE_T address);
template <typename T>
void write_memory(SIZE_T address, T buffer);
template <typename T>
T pointer_memory(QWORD *addrArray, int length);
template <typename T>
void pointer_memory(QWORD *addrArray, int length, T value);
template <typename T>
T get_address_ptr(T *addrArray, int length);
template <typename T>
T read_ga(QWORD offset);
template <typename T>
void write_ga(QWORD offset, T value);
byte pread_byte(QWORD *addrArray, int length);
double pread_double(QWORD *addrArray, int length, double value);
DWORD pread_dword(QWORD *addrArray, int length);
float pread_float(QWORD *addrArray, int length);
int pread_int(QWORD *addrArray, int length);
QWORD pread_qword(QWORD *addrArray, int length);
short pread_short(QWORD *addrArray, int length);
SIZE_T memoryMaskCode_search(byte *memory, SIZE_T length, char *maskCode);
void pread_bytes(QWORD *addrArray, int length, void *buffer, SIZE_T size);
void pwrite_byte(QWORD *addrArray, int length, byte value);
void pwrite_bytes(QWORD *addrArray, int length, void *buffer, SIZE_T size);
void pwrite_double(QWORD *addrArray, int length, double value);
void pwrite_dword(QWORD *addrArray, int length, DWORD value);
void pwrite_float(QWORD *addrArray, int length, float value);
void pwrite_int(QWORD *addrArray, int length, int value);
void pwrite_qword(QWORD *addrArray, int length, QWORD value);
void pwrite_short(QWORD *addrArray, int length, short value);
void pwrite_word(QWORD *addrArray, int length, WORD value);
WORD pread_word(QWORD *addrArray, int length);

extern "C"
{
    EXPORT BOOLEAN __stdcall check_valid(QWORD addr);
    EXPORT BYTE __stdcall read_byte(SIZE_T address);
    EXPORT char __stdcall read_char(SIZE_T address);
    EXPORT double __stdcall read_double(SIZE_T address);
    EXPORT DWORD __stdcall get_addr32(DWORD *addrArray, int length);
    EXPORT DWORD __stdcall get_pid(char *processName);
    EXPORT DWORD __stdcall read_dword(SIZE_T address);
    EXPORT float __stdcall read_float(SIZE_T address);
    EXPORT HANDLE __stdcall get_hProcess(DWORD pid);
    EXPORT int __stdcall read_int(SIZE_T address);
    EXPORT QWORD __stdcall get_addr64(QWORD *addrArray, int length);
    EXPORT QWORD __stdcall globalAddress(SIZE_T offset);
    EXPORT QWORD __stdcall localAddress(char *name, SIZE_T offset);
    EXPORT QWORD __stdcall read_qword(SIZE_T address);
    EXPORT short __stdcall read_short(SIZE_T address);
    EXPORT SIZE_T __stdcall get_hModule(DWORD pid, char *moduleName, SIZE_T *moduleSize);
    EXPORT UINT __stdcall keyboard_watch();
    EXPORT unsigned int __stdcall joaat(char *input);
    EXPORT void __stdcall change_session(int value);
    EXPORT void __stdcall change_weather(int value);
    EXPORT void __stdcall close_hanle(HANDLE handle);
    EXPORT void __stdcall destroy_enemy_vehicles();
    EXPORT void __stdcall doomsday1_key_event();
    EXPORT void __stdcall doomsday2_key_event();
    EXPORT void __stdcall doomsday3_key_event();
    EXPORT void __stdcall get_file_ptr(char *fileName);
    EXPORT void __stdcall get_process_ptr();
    EXPORT void __stdcall inject_dll(DWORD pid, char *dllPath);
    EXPORT void __stdcall keydown(WORD scankey);
    EXPORT void __stdcall keyup(WORD scankey);
    EXPORT void __stdcall kill_enemy_npc();
    EXPORT void __stdcall kill_process(HANDLE hProcess);
    EXPORT void __stdcall navigation_teleport();
    EXPORT void __stdcall objective_teleport();
    EXPORT void __stdcall read_bytes(SIZE_T address, void *buffer, SIZE_T length);
    EXPORT void __stdcall repairing_vehicle();
    EXPORT void __stdcall spawn_vehicle(unsigned int joaatHash);
    EXPORT void __stdcall teleport(float *position);
    EXPORT void __stdcall teleport_enemy_npc(float *position);
    EXPORT void __stdcall using_GTAHaX();
    EXPORT void __stdcall write_byte(SIZE_T address, BYTE buffer);
    EXPORT void __stdcall write_bytes(SIZE_T address, void *buffer, SIZE_T length);
    EXPORT void __stdcall write_char(SIZE_T address, char buffer);
    EXPORT void __stdcall write_double(SIZE_T address, double buffer);
    EXPORT void __stdcall write_dword(SIZE_T address, DWORD buffer);
    EXPORT void __stdcall write_float(SIZE_T address, float buffer);
    EXPORT void __stdcall write_int(SIZE_T address, int buffer);
    EXPORT void __stdcall write_qword(SIZE_T address, QWORD buffer);
    EXPORT void __stdcall write_short(SIZE_T address, short buffer);
    EXPORT void __stdcall write_stat(char *stat, int value);
    EXPORT void __stdcall write_word(SIZE_T address, WORD buffer);
    EXPORT WORD __stdcall read_word(SIZE_T address);
}