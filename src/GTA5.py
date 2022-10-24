import struct, threading
from cffi import FFI
from time import sleep


class Debug:
    def __init__(self, *args):
        for content in args:
            print(type(content))
            if isinstance(content, float):
                print(f"""0x{struct.unpack(">L", struct.pack(">f", content))[0]:08X}, {content}""")
            elif isinstance(content, int):
                print(f"""0x{struct.unpack(">Q", struct.pack(">q", content))[0]:08X}, {content}""")
            else:
                print(content)
        input("Debug... continue")
        return


class debug(Debug):
    def __init__(self, *args):
        super().__init__(*args)


def withThread(function):
    """线程的饰器"""

    def Threads(*args):
        threading.Thread(target=function, args=args, daemon=True).start()

    return Threads


ffi = FFI()

ntdll = ffi.dlopen("ntdll.dll")
ffi.cdef(
    """
typedef unsigned long long QWORD;

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

BOOLEAN check_valid(QWORD addr);
BYTE read_byte(SIZE_T address);
char read_char(SIZE_T address);
double read_double(SIZE_T address);
DWORD get_addr32(DWORD *addrArray, int length);
DWORD get_pid(char *processName);
DWORD read_dword(SIZE_T address);
float read_float(SIZE_T address);
HANDLE get_hProcess(DWORD pid);
int read_int(SIZE_T address);
QWORD get_addr64(QWORD *addrArray, int length);
QWORD globalAddress(SIZE_T offset);
QWORD localAddress(char *name, SIZE_T offset);
QWORD read_qword(SIZE_T address);
short read_short(SIZE_T address);
SIZE_T get_hModule(DWORD pid, char *moduleName, SIZE_T *moduleSize);
UINT keyboard_watch();
unsigned int joaat(char *input);
void change_session(int value);
void change_weather(int value);
void close_hanle(HANDLE handle);
void destroy_enemy_vehicles();
void doomsday1_key_event();
void doomsday2_key_event();
void doomsday3_key_event();
void get_file_ptr(char *fileName);
void get_process_ptr();
void inject_dll(DWORD pid, char *dllPath);
void keydown(WORD scankey);
void keyup(WORD scankey);
void kill_enemy_npc();
void kill_process(HANDLE hProcess);
void navigation_teleport();
void objective_teleport();
void read_bytes(SIZE_T address, void *buffer, SIZE_T length);
void repairing_vehicle();
void spawn_vehicle(unsigned int joaatHash);
void teleport(float *position);
void teleport_enemy_npc(float *position);
void write_byte(SIZE_T address, BYTE buffer);
void write_bytes(SIZE_T address, void *buffer, SIZE_T length);
void write_char(SIZE_T address, char buffer);
void write_double(SIZE_T address, double buffer);
void write_dword(SIZE_T address, DWORD buffer);
void write_float(SIZE_T address, float buffer);
void write_int(SIZE_T address, int buffer);
void write_qword(SIZE_T address, QWORD buffer);
void write_short(SIZE_T address, short buffer);
void write_stat(char *stat, int value);
void write_word(SIZE_T address, WORD buffer);
WORD read_word(SIZE_T address);

void NtResumeProcess(HANDLE hProcess);
void NtSuspendProcess(HANDLE hProcess);
"""
)


class Gtalib:
    try:
        dll = ffi.dlopen("gtaLib.dll")
    except:
        try:
            dll = ffi.dlopen("./cpp/gtaLib.dll")
        except:
            dll = ffi.dlopen("../cpp/gtaLib.dll")

    WorldPTR = dll.WorldPTR
    BlipPTR = dll.BlipPTR
    ReplayInterfacePTR = dll.ReplayInterfacePTR
    LocalScriptsPTR = dll.LocalScriptsPTR
    GlobalPTR = dll.GlobalPTR
    PlayerCountPTR = dll.PlayerCountPTR
    PickupDataPTR = dll.PickupDataPTR

    pid = dll.pid
    hProcess = dll.hProcess
    hModule = dll.hModule
    moduleSize = dll.moduleSize

    @staticmethod
    def joaat(codeString: str) -> int:
        pointer = ffi.new("char[]", codeString.encode("utf-8"))
        return __class__.dll.joaat(pointer)

    @staticmethod
    def globalAddress(param: int) -> int:
        return (getattr(__class__.dll, "globalAddress"))(param)

    @staticmethod
    def localAddress(param: str, offset: int = 0) -> int:
        return (getattr(__class__.dll, "localAddress"))(ffi.new("char[]", param.encode("utf-8")), offset)

    @staticmethod
    def get_hProcess(pid: int):
        return __class__.dll.get_hProcess(pid)

    @staticmethod
    def get_pid(param: bytes) -> int:
        return __class__.dll.get_pid(param)

    @staticmethod
    def get_hModule(pid: int, moduleName: bytes, moduleSize) -> int:
        return __class__.dll.get_hModule(pid, moduleName, moduleSize)

    @staticmethod
    def read_byte(param: int) -> int:
        return __class__.dll.read_byte(param)

    @staticmethod
    def read_char(param: int) -> int:
        return __class__.dll.read_char(param)

    @staticmethod
    def read_double(param: int) -> float:
        return __class__.dll.read_double(param)

    @staticmethod
    def read_dword(param: int) -> int:
        return __class__.dll.read_dword(param)

    @staticmethod
    def read_float(param: int) -> float:
        return __class__.dll.read_float(param)

    @staticmethod
    def read_int(param: int) -> int:
        return __class__.dll.read_int(param)

    @staticmethod
    def read_qword(param: int) -> int:
        return __class__.dll.read_qword(param)

    @staticmethod
    def read_word(param: int) -> int:
        return __class__.dll.read_word(param)

    @staticmethod
    def read_short(param: int) -> int:
        return __class__.dll.read_short(param)

    @staticmethod
    def write_byte(address: int, param: int):
        __class__.dll.write_byte(address, param)

    @staticmethod
    def write_char(address: int, param: int):
        __class__.dll.write_char(address, param)

    @staticmethod
    def write_double(address: int, param: float):
        __class__.dll.write_double(address, param)

    @staticmethod
    def write_dword(address: int, param: int):
        __class__.dll.write_dword(address, param)

    @staticmethod
    def write_float(address: int, param: float):
        __class__.dll.write_float(address, param)

    @staticmethod
    def write_int(address: int, param: int):
        __class__.dll.write_int(address, param)

    @staticmethod
    def write_qword(address: int, param: int):
        __class__.dll.write_qword(address, param)

    @staticmethod
    def write_word(address: int, param: int):
        __class__.dll.write_word(address, param)

    @staticmethod
    def write_short(address: int, param: int):
        __class__.dll.write_short(address, param)

    @staticmethod
    def get_addr(param: tuple) -> int:
        addArray = ffi.new("QWORD[]", param)
        return __class__.dll.get_addr64(addArray, len(addArray))

    @staticmethod
    def inject_dll(prama: bytes):
        __class__.dll.inject_dll(__class__.dll.pid, ffi.new("char[]", prama.encode("utf-8")))

    @staticmethod
    def get_process_ptr():
        __class__.dll.get_process_ptr()


gtalib = Gtalib


class Keyboard:
    hotkeyPool = dict()

    def keyboard_watch(self):
        try:
            return Gtalib.dll.keyboard_watch()
        except:
            return 0

    def add_hotkey(self, code: int, fun):
        if code == 0:
            return
        self.hotkeyPool.update({str(code): fun})

    def remove_hotkey(self, code):
        if code == 0:
            return
        self.hotkeyPool.pop(str(code))

    def run(self):
        while True:
            code = self.keyboard_watch()
            if str(code) in self.hotkeyPool.keys():
                self.hotkeyPool.get(str(code))()
                sleep(0.15)
            else:
                sleep(0.05)


class Base:
    WorldPTR = gtalib.dll.WorldPTR
    BlipPTR = gtalib.dll.BlipPTR
    ReplayInterfacePTR = gtalib.dll.ReplayInterfacePTR
    LocalScriptsPTR = gtalib.dll.LocalScriptsPTR
    GlobalPTR = gtalib.dll.GlobalPTR
    PlayerCountPTR = gtalib.dll.PlayerCountPTR
    PickupDataPTR = gtalib.dll.PickupDataPTR
    WeatherPTR = gtalib.dll.WeatherPTR

    hProcess = gtalib.dll.hProcess
    hModule = gtalib.dll.hModule
    moduleSize = gtalib.dll.moduleSize

    oPed = 0x8
    oVehicle = 0xD30
    oWeapon = 0x10D0

    def __init__(self) -> None:
        pass

    @staticmethod
    def check_valid(addr: int) -> bool:
        return gtalib.dll.check_valid(addr)


class Player(Base):
    def __init__(self) -> None:
        super().__init__()
        self.playerLifePTR = (__class__.__base__.WorldPTR, __class__.oPed, 0x280)  # 血量 float
        self.playerMaxLifePTR = (__class__.__base__.WorldPTR, __class__.oPed, 0x2A0)  # 最大血量 float
        self.playerGodmodePTR = (__class__.__base__.WorldPTR, __class__.oPed, 0x189)  # 无敌模式 byte
        self.playerVestPTR = (__class__.__base__.WorldPTR, __class__.oPed, 0x1530)  # 护甲 float
        self.playerMaxVestPTR = (__class__.__base__.WorldPTR, __class__.oPed, 0x1558)  # 满状态护甲 float
        self.playerCopsPTR = (__class__.__base__.WorldPTR, __class__.oPed, 0x10C8, 0x888)  # 通缉等级 int
        self.playerSeatbeltPTR = (__class__.__base__.WorldPTR, __class__.oPed, 0x145C)  # 安全带 byte -56:关闭 -55:开启
        self.playerInVehiclePTR = (__class__.__base__.WorldPTR, __class__.oPed, 0xE52)  # 判断玩家是否在载具上 byte 1:在 0:不在
        self.playerLocationXPTR = (__class__.__base__.WorldPTR, __class__.oPed, 0x30, 0x50)  # 当前玩家x坐标 float
        self.playerCameraLocationXPTR = (__class__.__base__.WorldPTR, __class__.oPed, 0x90)  # 当前相机x坐标 float

    @property
    def playerLife(self):
        return gtalib.read_float(gtalib.get_addr(self.playerLifePTR))

    @playerLife.setter
    def playerLife(self, value: float):
        gtalib.write_float(gtalib.get_addr(self.playerLifePTR), value)

    @property
    def playerMaxLife(self):
        return gtalib.read_float(gtalib.get_addr(self.playerMaxLifePTR))

    @playerMaxLife.setter
    def playerMaxLife(self, value: float):
        gtalib.write_float(gtalib.get_addr(self.playerMaxLifePTR), value)

    @property
    def playerVest(self):
        return gtalib.read_float(gtalib.get_addr(self.playerVestPTR))

    @playerVest.setter
    def playerVest(self, value: float):
        gtalib.write_float(gtalib.get_addr(self.playerVestPTR), value)

    @property
    def playerMaxVest(self):
        return gtalib.read_float(gtalib.get_addr(self.playerMaxVestPTR))

    @playerMaxVest.setter
    def playerMaxVest(self):
        pass

    @property
    def playerGodmode(self):
        return gtalib.read_byte(gtalib.get_addr(self.playerGodmodePTR))

    @playerGodmode.setter
    def playerGodmode(self, value: int):
        gtalib.write_byte(gtalib.get_addr(self.playerGodmodePTR), value)

    @property
    def playerCops(self):
        return gtalib.read_int(gtalib.get_addr(self.playerCopsPTR))

    @playerCops.setter
    def playerCops(self, value: int):
        gtalib.write_int(gtalib.get_addr(self.playerCopsPTR), value)

    @property
    def playerSeatbelt(self):
        pass

    @playerSeatbelt.setter
    def playerSeatbelt(self, value: int):
        gtalib.write_byte(gtalib.get_addr(self.playerSeatbeltPTR), value)

    @property
    def playerLocation(self):
        addressX = gtalib.get_addr(self.playerLocationXPTR)
        addressY = addressX + 4
        addressZ = addressX + 8
        x = gtalib.read_float(addressX)
        y = gtalib.read_float(addressY)
        z = gtalib.read_float(addressZ)
        return (x, y, z)

    @playerLocation.setter
    def playerLocation(self, value: "tuple[float,float,float]"):
        addressX = gtalib.get_addr(self.playerLocationXPTR)
        addressY = addressX + 4
        addressZ = addressX + 8
        gtalib.write_float(addressX, value[0])
        gtalib.write_float(addressY, value[1])
        gtalib.write_float(addressZ, value[2])

    @property
    def playerCameraLocation(self):
        pass

    @playerCameraLocation.setter
    def playerCameraLocation(self, value: "tuple[float,float,float]"):
        addressX = gtalib.get_addr(self.playerCameraLocationXPTR)
        addressY = addressX + 4
        addressZ = addressX + 8
        gtalib.write_float(addressX, value[0])
        gtalib.write_float(addressY, value[1])
        gtalib.write_float(addressZ, value[2])

    @property
    def playerInVehicle(self):
        return gtalib.read_byte(gtalib.get_addr(self.playerInVehiclePTR))

    @playerInVehicle.setter
    def playerInVehicle(self):
        pass


class Vehicle(Base):
    def __init__(self) -> None:
        super().__init__()
        self.vehicleLifePTR = (__class__.__base__.WorldPTR, __class__.oPed, __class__.oVehicle, 0x280)  # 载具血量
        self.vehicleGodmodePTR = (__class__.__base__.WorldPTR, __class__.oPed, __class__.oVehicle, 0x189)  # 载具能力 int
        self.vehicleLocationXPTR = (__class__.__base__.WorldPTR, __class__.oPed, __class__.oVehicle, 0x30, 0x50)  # 当前载具x坐标 float
        self.vehicleAbilityPTR = (__class__.__base__.WorldPTR, __class__.oPed, __class__.oVehicle, 0x20, 0x58B)  # 载具能力 int
        self.vehicleAbilityBarPTR = (__class__.__base__.WorldPTR, __class__.oPed, __class__.oVehicle, 0x320)  # 载具能力条 flaot
        self.vehicleAbilityRecoveryPTR = (__class__.__base__.WorldPTR, __class__.oPed, __class__.oVehicle, 0x324)  # 载具能力恢复速度 flaot
        self.vehicleCleanlinessPTR = (__class__.WorldPTR, __class__.oPed, __class__.oVehicle, 0x9F8)  # 载具干净度 float 0~15

    @property
    def vehicleLife(self):
        return gtalib.read_float(gtalib.get_addr(self.vehicleLifePTR))

    @vehicleLife.setter
    def vehicleLife(self, value: float):
        gtalib.write_float(gtalib.get_addr(self.vehicleLifePTR), value)

    @property
    def vehicleGodmode(self):
        return gtalib.read_byte(gtalib.get_addr(self.vehicleLifePTR))

    @vehicleGodmode.setter
    def vehicleGodmode(self, value: int):
        gtalib.write_byte(gtalib.get_addr(self.vehicleGodmodePTR), value)

    @property
    def vehicleLocation(self):
        addressX = gtalib.get_addr(self.vehicleLocationXPTR)
        addressY = addressX + 4
        addressZ = addressX + 8
        x = gtalib.read_float(addressX)
        y = gtalib.read_float(addressY)
        z = gtalib.read_float(addressZ)
        return (x, y, z)

    @vehicleLocation.setter
    def vehicleLocation(self, value: "tuple[float,float,float]"):
        addressX = gtalib.get_addr(self.vehicleLocationXPTR)
        addressY = addressX + 4
        addressZ = addressX + 8
        gtalib.write_float(addressX, value[0])
        gtalib.write_float(addressY, value[1])
        gtalib.write_float(addressZ, value[2])

    @property
    def vehicleAbility(self):
        pass

    @vehicleAbility.setter
    def vehicleAbility(self, value: int):
        gtalib.write_word(gtalib.get_addr(self.vehicleAbilityPTR), value)
        if value == 0x40:
            """助推器恢复速度"""
            gtalib.write_float(gtalib.get_addr(self.vehicleAbilityRecoveryPTR), 5.0)

    @property
    def vehicleAbilityBar(self):
        return gtalib.read_float(gtalib.get_addr(self.vehicleAbilityBarPTR))

    @vehicleAbilityBar.setter
    def vehicleAbilityBar(self, value: float):
        gtalib.write_float(gtalib.get_addr(self.vehicleAbilityBarPTR), value)

    @property
    def vehicleCleanliness(self):
        pass

    @vehicleCleanliness.setter
    def vehicleCleanliness(self, value: float):
        gtalib.write_float(gtalib.get_addr(self.vehicleCleanlinessPTR), value)

    def repairing_vehicle(self):
        """修复载具"""
        gtalib.dll.repairing_vehicle()


class Weapon(Base):
    def __init__(self) -> None:
        super().__init__()
        self.weaponInfiniteAmmoPTR = (__class__.__base__.WorldPTR, __class__.oPed, __class__.oWeapon, 0x78)
        self.weaponAmmoBase = (__class__.__base__.WorldPTR, __class__.oPed, __class__.oWeapon, 0x20, 0x60)
        self.weaponReloadSpeedPTR = (__class__.__base__.WorldPTR, __class__.oPed, __class__.oWeapon, 0x20, 0x134)
        self.weaponAmmoTypePTR = (__class__.__base__.WorldPTR, __class__.oPed, 0x10D8, 0x20, 0x24)

    @property
    def weaponInfiniteAmmo(self):
        pass

    @weaponInfiniteAmmo.setter
    def weaponInfiniteAmmo(self, value: int):  # 0 默认 10 无限
        gtalib.write_byte(gtalib.get_addr(self.weaponInfiniteAmmoPTR), value)

    @property
    def weaponAmmo(self):
        gtalib.read_word(gtalib.get_addr(self.weaponAmmoBase))

    @weaponAmmo.setter
    def weaponAmmo(self, value: int):
        gtalib.write_word(gtalib.get_addr(self.weaponAmmoBase), value)

    @property
    def weaponReloadSpeed(self):
        pass

    @weaponReloadSpeed.setter
    def weaponReloadSpeed(self, value: float):
        gtalib.write_float(gtalib.get_addr(self.weaponReloadSpeedPTR), value)

    @property
    def weaponAmmoType(self):
        pass

    @weaponAmmoType.setter
    def weaponAmmoType(self, value: int):
        """设置子弹类型\n
        value int: -1 默认| 18 MK2爆炸子弹
        """
        ammoTypeAddr = gtalib.get_addr(self.weaponAmmoTypePTR)
        if value == -1:
            gtalib.write_int(ammoTypeAddr - 4, 3)  # 影响类型
        else:
            gtalib.write_int(ammoTypeAddr - 4, 5)
        gtalib.write_int(ammoTypeAddr, value)

    def full_current_ammo(self):
        weaponAmmoBase = gtalib.read_qword(gtalib.get_addr((__class__.WorldPTR, __class__.oPed, 0x10D8, 0x20, 0x60)))
        maxAmmo = gtalib.read_int(weaponAmmoBase + 0x28)
        offset0 = weaponAmmoBase
        ammo_type = 0
        while ammo_type == 0:
            offset0 = gtalib.read_qword(offset0 + 0x08)
            offset1 = gtalib.read_qword(offset0 + 0x00)
            if (offset0 & offset1) == 0:
                return
            ammo_type = gtalib.read_byte(offset1 + 0x0C)
        gtalib.write_word(offset1 + 0x18, maxAmmo)


class Heist(Base):
    @property
    def apartmentHeist(self):
        return tuple(gtalib.read_int(gtalib.globalAddress(1933908 + 3008 + i + 1)) for i in range(4))

    @apartmentHeist.setter
    def apartmentHeist(self, values: tuple):
        for i in range(4):
            gtalib.write_int(gtalib.globalAddress(1933908 + 3008 + i + 1), values[i])

    @property
    def doomsdayHeist(self):
        return tuple(gtalib.read_int(gtalib.globalAddress(1962546 + 812 + 50 + i + 1)) for i in range(4))

    @doomsdayHeist.setter
    def doomsdayHeist(self, values: tuple):
        for i in range(4):
            gtalib.write_int(gtalib.globalAddress(1962546 + 812 + 50 + i + 1), values[i])

    @property
    def casinoHeist(self):
        return tuple(gtalib.read_int(gtalib.globalAddress(1966534 + 1497 + 736 + 92 + i + 1)) for i in range(4))

    @casinoHeist.setter
    def casinoHeist(self, values: tuple):
        for i in range(4):
            gtalib.write_int(gtalib.globalAddress(1966534 + 1497 + 736 + 92 + i + 1), values[i])
            1973321 + 823 + 56

    @property
    def pericoHeist(self):
        return tuple(gtalib.read_int(gtalib.globalAddress(1973321 + 823 + 56 + i + 1)) for i in range(4))

    @pericoHeist.setter
    def pericoHeist(self, values: tuple):
        for i in range(4):
            gtalib.write_int(gtalib.globalAddress(1973321 + 823 + 56 + i + 1), values[i])


class GTAHax(Base):
    def __init__(self):
        super().__init__()

    def write_stat(self, stat: str, value: int):
        if stat.startswith("MPx_"):
            playerNumber = gtalib.read_int(gtalib.globalAddress(1574918))
            stat = stat.replace("MPx_", f"MP{playerNumber}_", 1)
        joaatHash = gtalib.joaat(stat)
        statResotreHash = gtalib.read_dword(gtalib.globalAddress(1655453 + 4))
        statResotreValue = gtalib.read_int(gtalib.globalAddress(1020252 + 5526))
        gtalib.write_dword(gtalib.globalAddress(1659575 + 4), joaatHash)
        gtalib.write_int(gtalib.globalAddress(1020252 + 5526), value)
        gtalib.write_int(gtalib.globalAddress(1648034 + 1139), -1)
        sleep(1.0)
        gtalib.write_dword(gtalib.globalAddress(1659575 + 4), statResotreHash)
        gtalib.write_int(gtalib.globalAddress(1020252 + 5526), statResotreValue)

    def stat_value(self, stat: str, value: str):
        """stat value GTAHax效果\n
        stat str: MPx_XXXX\n
        value int: 数值
        """
        if stat == "" or value == "":
            return None
        statBytes = ffi.new("char[]", stat.encode("utf-8"))
        gtalib.dll.write_stat(statBytes, int(value))

    def set_level_30(self):
        """设置等级30级"""
        stats = (
            ("MPx_CHAR_ABILITY_1_UNLCK", 1),
            ("MPx_CHAR_ABILITY_2_UNLCK", 1),
            ("MPx_CHAR_ABILITY_3_UNLCK", 1),
            ("MPx_CHAR_FM_ABILITY_1_UNLCK", 1),
            ("MPx_CHAR_FM_ABILITY_2_UNLCK", 1),
            ("MPx_CHAR_FM_ABILITY_3_UNLCK", 1),
            ("MPx_CHAR_SET_RP_GIFT_ADMIN", 177100),  # 30级别
        )
        for tp in stats:
            self.stat_value(tp[0], tp[1])
            sleep(1)


class Weather(Base):
    @property
    def weather(self):
        pass

    @weather.setter
    def weather(self, value):
        gtalib.dll.change_weather(value)


class StatusData:
    luckyWheel = False


class GTAV(Gtalib, Base):
    def __init__(self) -> None:
        super().__init__()
        self.statusData = StatusData()
        gtalib.dll.get_process_ptr()
        assert gtalib.dll.pid != 0
        assert gtalib.dll.hProcess != 0
        assert gtalib.dll.hModule != 0
        Base.pid = gtalib.dll.pid
        Base.hProcess = gtalib.dll.hProcess
        Base.hModule = gtalib.dll.hModule
        Base.moduleSize = gtalib.dll.moduleSize
        Base.WorldPTR = gtalib.dll.WorldPTR
        Base.BlipPTR = gtalib.dll.BlipPTR
        Base.ReplayInterfacePTR = gtalib.dll.ReplayInterfacePTR
        Base.LocalScriptsPTR = gtalib.dll.LocalScriptsPTR
        Base.GlobalPTR = gtalib.dll.GlobalPTR
        Base.PlayerCountPTR = gtalib.dll.PlayerCountPTR
        Base.PickupDataPTR = gtalib.dll.PickupDataPTR
        Base.WeatherPTR = gtalib.dll.WeatherPTR
        self.player = Player()
        self.vehicle = Vehicle()
        self.weapon = Weapon()
        self.heist = Heist()
        self.gtahax = GTAHax()
        self.weather = Weather()

    def leave_me_alone(self, t: float = 10.0):
        """挂起进程卡单人公开战局\n
        t float: 秒钟
        """
        ntdll.NtSuspendProcess(gtalib.dll.hProcess)
        sleep(t)
        ntdll.NtResumeProcess(gtalib.dll.hProcess)

    def change_session(self, value: int):
        """战局切换\n
        value int: 战局模式\n
        * 1:创建公共战局\n
        * 11:仅限邀请战局\n
        * 10:单人战局\n
        * 6:私人好友战局\n
        * -1:离开线上
        """
        gtalib.dll.change_session(value)

    def kill_yourself(self):
        """自杀"""
        self.player.playerVest = 0
        self.player.playerLife = 0

    def cure_yourself(self):
        """治疗"""
        self.player.playerVest = self.player.playerMaxVest
        self.player.playerLife = self.player.playerMaxLife

    def no_cops(self):
        """清除通缉"""
        self.player.playerCops = 0

    def add_cops(self):
        """添加通缉"""
        cops = self.player.playerCops
        if cops < 5:
            self.player.playerCops = cops + 1

    @property
    def navigationLocation(self) -> tuple:
        """获取导航定位座标\n
        return tuple[float,float,float]
        """
        for i in range(2000, 0, -1):
            addr = gtalib.read_qword(Base.BlipPTR + i * 8)
            if not self.check_valid(addr):
                continue
            if gtalib.read_int(addr + 0x40) == 0x08 and gtalib.read_int(addr + 0x48) == 0x54:
                return (gtalib.read_float(addr + 0x10), gtalib.read_float(addr + 0x14), gtalib.read_float(addr + 0x18))
        return (64000.0, 64000.0, 64000.0)

    def navigation_teleport(self):
        """导航传送"""
        gtalib.dll.navigation_teleport()

    @property
    def objectiveLocation(self) -> tuple:
        """获取任务点座标\n
        return tunple[float,float,float]:(x, y ,z)
        """
        for i in range(2000, 0, -1):
            addr = gtalib.read_qword(Base.BlipPTR + i * 8)
            if not self.check_valid(addr):
                continue
            buf0 = gtalib.read_int(addr + 0x40)
            buf1 = gtalib.read_int(addr + 0x48)
            if (buf0 == 432 or buf0 == 443) and (buf1 == 59):
                return (gtalib.read_float(addr + 0x10), gtalib.read_float(addr + 0x14), gtalib.read_float(addr + 0x18))
            elif buf0 == 1 and (buf1 == 5 or buf1 == 60 or buf1 == 66):
                return (gtalib.read_float(addr + 0x10), gtalib.read_float(addr + 0x14), gtalib.read_float(addr + 0x18))
            elif (buf0 == 1 or buf0 == 225 or buf0 == 427 or buf0 == 478 or buf0 == 501 or buf0 == 523 or buf0 == 556) and (
                buf1 == 1 or buf1 == 2 or buf1 == 3 or buf1 == 54 or buf1 == 78
            ):
                return (gtalib.read_float(addr + 0x10), gtalib.read_float(addr + 0x14), gtalib.read_float(addr + 0x18))
        return (64000.0, 64000.0, 64000.0)

    def teleport(self, pos: tuple):
        """座标传送"""
        position = ffi.new("float[]", pos)
        gtalib.dll.teleport(position)

    def objective_teleport(self):
        """目标点传送"""
        gtalib.dll.objective_teleport()

    def forward(self):
        """往前移动"""
        if self.player.playerInVehicle == 1:
            return None
        heading0 = gtalib.read_float(gtalib.get_addr((Base.WorldPTR, __class__.oPed, 0x30, 0x20)))
        heading1 = gtalib.read_float(gtalib.get_addr((Base.WorldPTR, __class__.oPed, 0x30, 0x30)))
        (x, y, z) = self.player.playerLocation
        x = x + heading1 * 2.5
        y = y + heading0 * 2.5
        self.player.playerCameraLocation = (x, y, z)
        self.player.playerLocation = (x, y, z)

    def get_in_personal_vehicle(self):
        """传送到载具上"""
        pass

    def outdoor_spawn_vehicle(self, joaatHash: int):
        """室外创建载具\n
        joaatHash int: 载具hash
        """
        gtalib.dll.spawn_vehicle(joaatHash)

    def indoor_spawn_vehicle(self, joaatHash: int):
        """室内刷出载具\n
        joaatHash int: 载具hash
        """
        offset = 2725439
        heading0 = gtalib.read_float(gtalib.get_addr((Base.WorldPTR, __class__.oPed, 0x30, 0x20)))
        heading1 = gtalib.read_float(gtalib.get_addr((Base.WorldPTR, __class__.oPed, 0x30, 0x24)))
        (x, y, z) = self.player.playerLocation
        x = x - (heading1 * 3)
        y = y + (heading0 * 3)
        z = z + 0.5
        gtalib.write_float(gtalib.globalAddress(offset + 7 + 0), x)
        gtalib.write_float(gtalib.globalAddress(offset + 7 + 1), y)
        gtalib.write_float(gtalib.globalAddress(offset + 7 + 2), z)
        gtalib.write_dword(gtalib.globalAddress(offset + 27 + 66), joaatHash)
        gtalib.write_int(gtalib.globalAddress(offset + 27 + 28), 1)
        gtalib.write_int(gtalib.globalAddress(offset + 27 + 60), 1)
        gtalib.write_int(gtalib.globalAddress(offset + 27 + 95), 14)
        gtalib.write_int(gtalib.globalAddress(offset + 27 + 94), 2)
        gtalib.write_int(gtalib.globalAddress(offset + 5), 1)
        gtalib.write_int(gtalib.globalAddress(offset + 2), 1)
        gtalib.write_int(gtalib.globalAddress(offset + 3), 0)
        gtalib.write_int(gtalib.globalAddress(offset + 27 + 74), 1)
        gtalib.write_int(gtalib.globalAddress(offset + 27 + 75), 1)
        gtalib.write_int(gtalib.globalAddress(offset + 27 + 76), 0)
        gtalib.write_dword(gtalib.globalAddress(offset + 27 + 60), 4030726305)
        gtalib.write_int(gtalib.globalAddress(offset + 27 + 5), -1)
        gtalib.write_int(gtalib.globalAddress(offset + 27 + 6), -1)
        gtalib.write_int(gtalib.globalAddress(offset + 27 + 7), -1)
        gtalib.write_int(gtalib.globalAddress(offset + 27 + 8), -1)
        gtalib.write_int(gtalib.globalAddress(offset + 27 + 19), 4)
        gtalib.write_int(gtalib.globalAddress(offset + 27 + 21), 4)
        gtalib.write_int(gtalib.globalAddress(offset + 27 + 22), 3)
        gtalib.write_int(gtalib.globalAddress(offset + 27 + 23), 3)
        gtalib.write_int(gtalib.globalAddress(offset + 27 + 24), 58)
        gtalib.write_int(gtalib.globalAddress(offset + 27 + 26), 5)
        gtalib.write_int(gtalib.globalAddress(offset + 27 + 26), 1)
        gtalib.write_int(gtalib.globalAddress(offset + 27 + 65), 2)
        gtalib.write_int(gtalib.globalAddress(offset + 27 + 69), -1)
        gtalib.write_int(gtalib.globalAddress(offset + 27 + 33), -1)
        gtalib.write_int(gtalib.globalAddress(offset + 27 + 25), 8)
        gtalib.write_int(gtalib.globalAddress(offset + 27 + 19), -1)
        gtalib.write_byte(gtalib.globalAddress(offset + 27 + 77) + 1, 2)

    def generate_vehicle(self, joaatHash: int):
        """创建载具\n
        joaatHash int: 载具hash
        """
        gtalib.dll.spawn_vehicle(joaatHash)

    def kill_enemy_npc(self):
        """杀死敌对NPC"""
        gtalib.dll.kill_enemy_npc()

    def destroy_enemy_vehicles(self):
        """摧毁敌方载具"""
        gtalib.dll.destroy_enemy_vehicles()

    def teleport_enemy_npc(self, pos: tuple):
        """传送敌对npc到指定位置"""
        position = ffi.new("float[]", pos)
        gtalib.dll.teleport_enemy_npc(position)

    def antiAFK(self, status: bool):
        """挂机防踢"""
        offset = 262145
        if status is True:
            gtalib.write_int(gtalib.globalAddress(offset + 87), 2000000000)
            gtalib.write_int(gtalib.globalAddress(offset + 88), 2000000000)
            gtalib.write_int(gtalib.globalAddress(offset + 89), 2000000000)
            gtalib.write_int(gtalib.globalAddress(offset + 90), 2000000000)

            gtalib.write_int(gtalib.globalAddress(offset + 8041), 2000000000)
            gtalib.write_int(gtalib.globalAddress(offset + 8042), 2000000000)
            gtalib.write_int(gtalib.globalAddress(offset + 8043), 2000000000)
            gtalib.write_int(gtalib.globalAddress(offset + 8044), 2000000000)
        else:
            gtalib.write_int(gtalib.globalAddress(offset + 87), 120000)
            gtalib.write_int(gtalib.globalAddress(offset + 88), 300000)
            gtalib.write_int(gtalib.globalAddress(offset + 89), 600000)
            gtalib.write_int(gtalib.globalAddress(offset + 90), 900000)

            gtalib.write_int(gtalib.globalAddress(offset + 8041), 30000)
            gtalib.write_int(gtalib.globalAddress(offset + 8042), 60000)
            gtalib.write_int(gtalib.globalAddress(offset + 8043), 90000)
            gtalib.write_int(gtalib.globalAddress(offset + 8044), 120000)

    def kill_process(self):
        """杀死进程"""
        gtalib.dll.kill_process(gtalib.dll.hProcess)

    def apartment_heist(self):
        """跳过公寓抢劫任务前置"""
        self.gtahax.stat_value("MPx_HEIST_PLANNING_STAGE", -1)  # 跳过准备前置 4人开始进入动画后触发生效

    def doomsday_cooldown(self):
        """末日3冷却"""
        self.gtahax.stat_value("MPx_HEISTCOOLDOWNTIMER2", -1)  # 末日3冷却

    def doomsday(self):
        """跳过末日前置"""
        self.gtahax.stat_value("MPx_GANGOPS_FLOW_MISSION_PROG", -1)  # 跳过前置，M-设施管理-关闭后开启抢劫策划大屏

    def casino(self):
        """赌场豪劫"""
        self.gtahax.stat_value("MPx_H3OPT_TARGET", 3)  # 目标钻石

    def perico(self):
        """佩里克岛豪劫"""
        stats = (
            ("MPx_H4CNF_BOLTCUT", 6276),  # 螺栓切割器
            ("MPx_H4CNF_UNIFORM", 4386),  # 保安服
            ("MPx_H4CNF_GRAPPEL", 16936),  # 抓钩
            ("MPx_H4CNF_TROJAN", 1),  # 卡车
            ("MPx_H4LOOT_CASH_I", 0),
            ("MPx_H4LOOT_CASH_I_SCOPED", 0),
            ("MPx_H4LOOT_CASH_C", 0),
            ("MPx_H4LOOT_CASH_C_SCOPED", 0),
            ("MPx_H4LOOT_COKE_I", 0),
            ("MPx_H4LOOT_COKE_I_SCOPED", 0),
            ("MPx_H4LOOT_COKE_C", 0),
            ("MPx_H4LOOT_COKE_C_SCOPED", 0),
            ("MPx_H4LOOT_GOLD_I", 16777215),
            ("MPx_H4LOOT_GOLD_I_SCOPED", 16777215),
            ("MPx_H4LOOT_GOLD_C", 255),
            ("MPx_H4LOOT_GOLD_C_SCOPED", 255),
            ("MPx_H4LOOT_WEED_I", 0),
            ("MPx_H4LOOT_WEED_I_SCOPED", 0),
            ("MPx_H4LOOT_WEED_C", 0),
            ("MPx_H4LOOT_WEED_C_SCOPED", 0),
            ("MPx_H4LOOT_PAINT", 0),
            ("MPx_H4LOOT_PAINT_SCOPED", 0),
            ("MPx_H4CNF_TARGET", 5),  # 主要目标设为猎豹雕像
            ("MPx_H4_PROGRESS", 131055),  # 困难模式
        )
        for tp in stats:
            self.gtahax.stat_value(tp[0], tp[1])

    def luckyWheel(self):
        """幸运轮盘抽车"""
        while self.statusData.luckyWheel:
            if gtalib.dll.check_valid(gtalib.localAddress("casino_lucky_wheel", 273 + 14)):
                gtalib.write_int(gtalib.localAddress("casino_lucky_wheel", 273 + 14), 18)
            sleep(0.1)

    def circuitBreaker(self):
        """全服银行电路"""
        gtalib.write_int(gtalib.localAddress("fm_mission_controller", 11731 + 24), 7)

    def doomsday2_hack(self):
        gtalib.write_int(gtalib.localAddress("fm_mission_controller", 1537), 2)

    def doomsday3_hack(self):
        gtalib.write_int(gtalib.localAddress("fm_mission_controller", 1398), 3)

    def casinoFingerprint_hack(self):
        """赌场指纹"""
        gtalib.write_int(gtalib.localAddress("fm_mission_controller", 52929), 5)

    def casinoDoor_hack(self):
        """赌场门禁"""
        gtalib.write_int(gtalib.localAddress("fm_mission_controller", 54726), 1)
        sleep(0.1)
        gtalib.write_int(gtalib.localAddress("fm_mission_controller", 54747), 5)
        sleep(0.1)
        gtalib.write_int(gtalib.localAddress("fm_mission_controller", 54726 + 17), 10)
        sleep(0.1)

    def pericoHack1(self):
        """机场塔楼电压柜"""
        gtalib.write_int(
            gtalib.localAddress("fm_mission_controller_2020", 1715),
            gtalib.read_int(gtalib.localAddress("fm_mission_controller_2020", 1716)),
        )

    def pericoHack2(self):
        """下水道栅栏"""
        gtalib.write_int(gtalib.localAddress("fm_mission_controller_2020", 27500), 6)

    def pericoHack3(self):
        """指纹破解"""
        gtalib.write_int(gtalib.localAddress("fm_mission_controller_2020", 23385), 5)

    def pericoHack4(self):
        """主目标玻璃切割"""
        gtalib.write_float(gtalib.localAddress("fm_mission_controller_2020", 28736 + 3), 100.0)

    def yim_inject(self, prama: str):
        """YimMenu.dll注入"""
        gtalib.inject_dll(prama)


class Doomsday:
    @staticmethod
    def start(mission: int):
        if mission == 1:
            gtalib.dll.doomsday1_key_event()
        elif mission == 2:
            gtalib.dll.doomsday2_key_event()
        elif mission == 3:
            gtalib.dll.doomsday3_key_event()


if __name__ == "__main__":
    gtav = GTAV()
