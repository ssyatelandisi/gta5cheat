from ctypes import *


class Handle:
    def __init__(self):
        """句柄操作类\n"""
        self.ntdll = windll.ntdll  # 可使用NtReadVirtualMemory|NtWriteVirtualMemory读|写内存数据
        self.kernel32 = windll.kernel32
        self.user32 = windll.user32
        self.psapi = windll.psapi
        self.__pid = c_int(0)

    @property
    def hwnd(self):
        """
        窗口句柄\n
        """
        return self.__hwnd

    @hwnd.setter
    def hwnd(self, i_hwnd):
        self.__hwnd = i_hwnd

    @property
    def pid(self):
        """
        进程id c_long\n
        """
        return self.__pid

    @pid.setter
    def pid(self, i_pid):
        self.__pid = i_pid

    @property
    def hProcess(self):
        """进程句柄"""
        return self.__hProcess

    @hProcess.setter
    def hProcess(self, i_hProcess):
        self.__hProcess = i_hProcess

    @property
    def addrProcess(self):
        """进程地址"""
        return self.__addrProcess

    @addrProcess.setter
    def addrProcess(self, i_addrProcess):
        self.__addrProcess = i_addrProcess

    def find_window(self, lpClassName: str, lpWindowName: str):
        """
        lpClassName str: 窗口类名\n
        lpWindowName str: 窗口标题\n
        return 窗口句柄\n
        """
        return self.user32.FindWindowW(lpClassName, lpWindowName)

    def get_window_thread_process_id(self, hwnd):
        """获取进程id给pid\n
        hwnd: 窗口句柄\n
        """
        self.user32.GetWindowThreadProcessId(hwnd, byref(self.pid))

    def open_process(self, dwDesiredAccess, bInheritHandle, dwProcessId):
        """获取进程句柄\n
        dwDesiredAccess int: 访问权限\n
        bInheritHandle c_bool: 是否继承\n
        dwProcessId c_int: 进程id\n
        return 进程句柄\n
        """
        return self.kernel32.OpenProcess(dwDesiredAccess, bInheritHandle, dwProcessId)

    def query_module(self, moduleName: str):
        """获取进程中指定模块地址\n
        moduleName str: 模块名\n
        return int: 模块内存地址 | 0\n
        """
        moduleName = moduleName.lower()
        lphModule = (c_ulonglong * 1024)()
        lpcbNeeded = c_ulonglong()
        self.psapi.EnumProcessModules(
            self.hProcess,
            byref(lphModule),
            sizeof(lphModule),
            byref(lpcbNeeded),
        )  # 枚举所有模块地址
        for i in range(lpcbNeeded.value // sizeof(lpcbNeeded)):
            lpFilename = (c_char_p * 1024)()
            self.psapi.GetModuleBaseNameA(
                self.hProcess,
                c_ulonglong(lphModule[i]),
                byref(lpFilename),
                sizeof(lpFilename),
            )  # 获取地址的模块信息
            fileNameEx = bytes(lpFilename).strip(b"\x00").decode("gbk")
            if fileNameEx.lower() == moduleName:
                return lphModule[i]
        return 0

    def query_process(self, processName: str):
        """获取指定进程名所有pid数据\n
        processName: 进程名\n
        return list: pid列表\n
        """
        result = list()
        lpidProcess = (c_ulong * 1024)()
        cb = c_ulong(sizeof(lpidProcess))
        lpcbNeeded = c_ulong()
        self.psapi.EnumProcesses(byref(lpidProcess), cb, byref(lpcbNeeded))
        for pid in lpidProcess[: lpcbNeeded.value // sizeof(lpcbNeeded)]:
            hProcess = self.open_process(0x1F0FFF, c_bool(False), pid)
            if hProcess == 0:
                continue
            else:
                processName = processName.lower()
                lphModule = (c_ulonglong * 1024)()
                lpcbNeeded = c_ulonglong()
                self.psapi.EnumProcessModules(
                    hProcess,
                    byref(lphModule),
                    sizeof(lphModule),
                    byref(lpcbNeeded),
                )  # 枚举所有模块地址
                lpFilename = (c_char_p * 1024)()
                self.psapi.GetModuleBaseNameA(
                    hProcess,
                    c_ulonglong(lphModule[0]),
                    byref(lpFilename),
                    sizeof(lpFilename),
                )  # 获取首位地址的模块信息
                fileNameEx = bytes(lpFilename).strip(b"\x00").decode("gbk")
                if fileNameEx.lower() == processName:
                    result.append(pid)
        return result

    def query_pid(self, pid):
        """获取指定pid的进程名和内存地址\n
        pid int: 进程pid\n
        return tuple: (地址, 进程名)
        """
        hProcess = self.open_process(0x1F0FFF, c_bool(False), pid)
        lphModule = (c_ulonglong * 1024)()
        lpcbNeeded = c_ulonglong()
        self.psapi.EnumProcessModules(
            hProcess,
            byref(lphModule),
            sizeof(lphModule),
            byref(lpcbNeeded),
        )  # 枚举所有模块地址
        lpFilename = (c_char_p * 1024)()
        self.psapi.GetModuleBaseNameA(
            hProcess,
            c_longlong(lphModule[0]),
            byref(lpFilename),
            sizeof(lpFilename),
        )  # 获取首位地址的模块信息
        return (lphModule[0], bytes(lpFilename).strip(b"\x00").decode("gbk"))

    def enum_process_modules(self, hProcess):
        """枚举进程所有模块地址\n
        return tuple: 所有模块地址\n
        """
        lphModule = (c_ulonglong * 1024)()
        lpcbNeeded = c_ulonglong()
        self.psapi.EnumProcessModules(
            hProcess,
            byref(lphModule),
            sizeof(lphModule),
            byref(lpcbNeeded),
        )  # 枚举所有模块地址
        return tuple(lphModule[: lpcbNeeded.value // sizeof(lpcbNeeded)])

    def getMemoryAddress(self, pointer, buffer=c_ulonglong()):
        """获取内存地址\n
        pointer tuple: 指针偏移元组\n
        buffer 返回结果缓冲\n
        return int: 内存地址\n
        """
        addr = self.addrProcess
        for effest in pointer[0:-1]:
            self.kernel32.ReadProcessMemory(
                int(self.hProcess),
                c_ulonglong(addr + effest),
                byref(buffer),
                sizeof(buffer),
                None,
            )
            addr = buffer.value
        result = addr + pointer[-1]
        return result

    def readMemoryValue(self, address: int, buffer=c_int(), length=4):
        """读取内存值\n
        address int: 内存地址\n
        buffer 读取数据(ctypes类型)\n
        length int: 读取长度\n
        return Any\n
        """
        self.kernel32.ReadProcessMemory(
            int(self.hProcess),
            c_ulonglong(address),
            byref(buffer),
            length,
            None,
        )
        return buffer.value

    def writeMemoryValue(self, address: int, buffer=c_int(), length=4):
        """修改内存值\n
        address int: 内存地址\n
        buffer 写入数据(ctypes类型)\n
        length int: 写入长度\n
        """
        self.kernel32.WriteProcessMemory(
            int(self.hProcess),
            c_ulonglong(address),
            byref(buffer),
            length,
            None,
        )

    def kill_process(self):
        """结束当前进程"""
        self.kernel32.TerminateProcess(self.hProcess, 0)
        self.kernel32.CloseHandle(self.hProcess)

    def suspend_process(self):
        """挂起当前进程"""
        self.ntdll.NtSuspendProcess(int(self.hProcess))

    def resume_process(self):
        """恢复当前挂起进程"""
        self.ntdll.NtResumeProcess(int(self.hProcess))
