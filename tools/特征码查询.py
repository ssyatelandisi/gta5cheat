# https://www.bilibili.com/read/cv12624041
import binascii
import struct
import re
import os
import psutil  # pip install psutil
import ctypes


class CEPattern:
    def __init__(self, string: str):
        self.string = string

    @property
    def string(self):
        return self.__string

    @string.setter
    def string(self, string):
        if type(string) is not str:
            raise TypeError("输入的不是字符串类型")
        else:
            self.__string: str = string.strip()

    @property
    def regex(self):
        return re.sub(r"\?", r"..", self.string).replace(" ", "")

    @property
    def regexEx(self):
        result = re.finditer(r"(\.\.)+", self.regex)
        m = list()
        for item in result:
            m.append(item.group())
        m = set(m)
        register: str = self.regex
        for item in m:
            register = register.replace(item, f"({item})")
        return re.compile(register)

    @property
    def regexN(self):
        result = re.finditer(r"(\.\.)+", self.regex)
        for item in result:
            return item.span()

    def upper(self):
        self.string = self.string.upper()

    def lower(self):
        self.string = self.string.lower()


def ce_hex(string: str):
    """
    "15a37d01" -> int("017da315", 16)
    """
    return struct.unpack("<Q", binascii.a2b_hex(f"{string:<016}"))[0]


def find(pattern: CEPattern, string: str):
    m = re.search(pattern.regexEx, string)
    if m is not None:
        if len(m.groups()) > 0:
            offest = m.span(0)[0] // 2 + (m.span(1)[0] - m.span(0)[0]) // 2 + ce_hex(m.group(1)) + len(m.group(1)) // 2  # 指令长度  # 特征变量长度
            return offest
        else:
            # todo
            print("todo")
            return m.span(0)[0] // 2


GTA5 = (
    ("WorldPTR", "48 8B 05 ? ? ? ? 45 ? ? ? ? 48 8B 48 08 48 85 C9 74 07"),
    ("BlipPTR", "4C 8D 05 ? ? ? ? 0F B7 C1"),
    (
        "ReplayInterfacePTR",
        "48 8D 0D ? ? ? ? 48 8B D7 E8 ? ? ? ? 48 8D 0D ? ? ? ? 8A D8 E8",
    ),
    ("LocalScriptsPTR", "48 8B 05 ? ? ? ? 8B CF 48 8B 0C C8 39 59 68"),
    ("GlobalPTR", "4C 8D 05 ? ? ? ? 4D 8B 08 4D 85 C9 74 11"),
    ("PlayerCountPTR", "48 8B 0D ? ? ? ? E8 ? ? ? ? 48 8B C8 E8 ? ? ? ? 48 8B CF"),
    ("PickupDataPTR", "48 8B 05 ? ? ? ? 48 8B 1C F8 8B"),
)

"""
autoAssemble([[
aobscanmodule(WorldPTR,GTA5.exe,48 8B 05 ? ? ? ? 45 ? ? ? ? 48 8B 48 08 48 85 C9 74 07)
registersymbol(WorldPTR)
aobscanmodule(BlipPTR,GTA5.exe,4C 8D 05 ? ? ? ? 0F B7 C1)
registersymbol(BlipPTR)
aobscanmodule(ReplayInterfacePTR,GTA5.exe,48 8D 0D ? ? ? ? 48 8B D7 E8 ? ? ? ? 48 8D 0D ? ? ? ? 8A D8 E8)
registerSymbol(ReplayInterfacePTR)
aobscanmodule(LocalScriptsPTR,GTA5.exe,48 8B 05 ? ? ? ? 8B CF 48 8B 0C C8 39 59 68)
registerSymbol(LocalScriptsPTR)
aobscanmodule(GlobalPTR,GTA5.exe,4C 8D 05 ? ? ? ? 4D 8B 08 4D 85 C9 74 11)
registersymbol(GlobalPTR)
aobscanmodule(PlayerCountPTR,GTA5.exe,48 8B 0D ? ? ? ? E8 ? ? ? ? 48 8B C8 E8 ? ? ? ? 48 8B CF)
registersymbol(PlayerCountPTR)
aobscanmodule(PickupDataPTR,GTA5.exe,48 8B 05 ? ? ? ? 48 8B 1C F8 8B)
registersymbol(PickupDataPTR)]])
"""


def get_buffer(processName):
    """获取指定进程长度大小的内存数据\n
    processName str: 进程名\n
    """
    for pid in psutil.pids():  # 列出所有pid，遍历pid进程
        process = psutil.Process(pid)
        if process.name().lower() == processName.lower():
            break
    moduleSize = 0
    for moduleInfo in process.memory_maps():
        if moduleInfo.path.lower().endswith(processName.lower()):
            moduleSize = moduleInfo.rss
    if moduleSize == 0:
        return
    kernel32 = ctypes.windll.kernel32
    psapi = ctypes.windll.psapi
    pHandle = kernel32.OpenProcess(0x1F0FFF, 0, process.pid)
    lphModule = (ctypes.c_longlong * 1024)()
    lpcbNeeded = ctypes.c_longlong()
    psapi.EnumProcessModules(
        pHandle,
        ctypes.byref(lphModule),
        ctypes.sizeof(lphModule),
        ctypes.byref(lpcbNeeded),
    )
    processEnterAddr = lphModule[0]
    buffer = ctypes.c_buffer(moduleSize)
    kernel32.ReadProcessMemory(
        pHandle,
        ctypes.c_longlong(processEnterAddr),
        buffer,
        ctypes.c_longlong(moduleSize),
        None,
    )
    return buffer


if __name__ == "__main__":

    """fileNameEx为火绒剑导出的gta5.exe内存转储文件"""
    # fileNameEx = input("输入火绒剑导出的gta5.exe内存转储文件名\n>")
    # print("")
    # try:
    #     with open(fileNameEx, "rb") as f:
    #         data = f.read()
    #         o = binascii.b2a_hex(data).decode(encoding="ascii")
    #         for item in GTA5:
    #             pattern = CEPattern(item[1])
    #             pattern.lower()
    #             print(f"{item[0]:<18}: gta5.exe + 0x{find(pattern, o):0X}")
    # except FileNotFoundError:
    #     print(f"{fileNameEx}文件不存在")
    # os.system("pause")

    """读取进程内存"""
    # buffer = get_buffer("gta5.exe")
    # bufferString = binascii.b2a_hex(buffer).decode(encoding="ascii")
    # for item in GTA5:
    #     pattern = CEPattern(item[1])
    #     pattern.lower()
    #     print(
    #         f"{item[0]:18}: gta5.exe + 0x{find(pattern, bufferString):>08X}"
    #     )
    # os.system("pause")

    """调用dll方法"""
    gtaLib = ctypes.WinDLL("../cpp/gtaLib.dll")
    gtaLib.get_file_ptr.argtypes = (ctypes.c_void_p,)
    gtaLib.get_file_ptr(ctypes.c_buffer("gta5.exe".encode("utf-8")))
