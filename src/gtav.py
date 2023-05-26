import struct, threading
from cffi import FFI
from time import sleep
import sys


class Debug:
    def __call__(self, *args) -> None:
        for content in args:
            print(type(content))
            if isinstance(content, float):
                print(
                    f"""0x{struct.unpack(">L", struct.pack(">f", content))[0]:08X}, {content}"""
                )
            elif isinstance(content, int):
                print(
                    f"""0x{struct.unpack(">Q", struct.pack(">q", content))[0]:08X}, {content}"""
                )
            else:
                print(content)
        input("Debug... continue")
        return


debug = Debug()


def withThread(function):
    """线程的饰器"""

    def Threads(*args):
        threading.Thread(target=function, args=args, daemon=True).start()

    return Threads


ffi = FFI()

ffi.cdef(
    """
float get_maxArmor();
float get_maxHealth();
unsigned int get_pid(char *processName);
unsigned int joaat(char *input);
unsigned int keyboard_watch();
unsigned long long read_localAddress(char *thread, int offset);
void antiAFK(bool status);
void change_session(int value);
void destroy_enemy_vehicles();
void dll_inject(char *dllPath);
void fill_current_ammo();
void get_position(float *position);
void gtav_init();
void keydown(unsigned int scanKey);
void keyup(unsigned int scanKey);
void kill_enemy_npc();
void kill_process();
void move_forward();
void read_cut(int *data);
void repairing_vehicle();
void set_armor(float armor);
void set_copLevel(int copLevel);
void set_godMode(bool status);
void set_health(float health);
void set_infiniteAmmo(bool status);
void set_luckyWheel(int value);
void set_seatbelt(bool status);
void set_vehicleAbility(int value);
void set_vehicleGodMode(bool status);
void set_weaponAmmoType(int value);
void set_weather(int weather);
void spawn_vehicle(unsigned int hash, float d);
void stat_write(char *stat, int value);
void suspend_process();
void teleport_enemy_npc(float *position);
void teleport_to_objective();
void teleport_to_waypoint();
void teleport(float *position);
void write_cut(int *data);
void write_localAddressFloat(char *threadName, unsigned long long offset, float value);
void write_localAddressInt(char *threadName, unsigned long long offset, int value);
"""
)


class Gtalib:
    def __init__(self) -> None:
        try:
            self.lib = ffi.dlopen("gtaLib.dll")
        except:
            raise FileExistsError("没有找到gtaLib.dll文件")

    def joaat(self, codeString: str) -> int:
        """joaat算法"""
        pointer = ffi.new("char[]", codeString.encode("utf-8"))
        return getattr(self.lib, sys._getframe().f_code.co_name)(pointer)

    def dll_inject(self, prama: str):
        """注入dll"""
        dllPath = ffi.new("char[]", prama.encode("utf-8"))
        getattr(self.lib, sys._getframe().f_code.co_name)(dllPath)

    def get_maxArmor(self) -> float:
        """
        return float 最大护甲数值
        """
        return getattr(self.lib, sys._getframe().f_code.co_name)()

    def get_maxHealth(self) -> float:
        """return float 最大生命数值"""
        return getattr(self.lib, sys._getframe().f_code.co_name)()

    def get_pid(self, processName: str) -> int:
        """获取进程pid"""
        pro = ffi.new("char[]", processName.encode("utf-8"))
        return getattr(self.lib, sys._getframe().f_code.co_name)(pro)

    def keyboard_watch(self) -> int:
        """键盘监听事件"""
        return getattr(self.lib, sys._getframe().f_code.co_name)()

    def antiAFK(self, status: bool):
        """挂机防踢"""
        getattr(self.lib, sys._getframe().f_code.co_name)(status)

    def change_session(self, value: int):
        """切换战局"""
        getattr(self.lib, sys._getframe().f_code.co_name)(value)

    def destroy_enemy_vehicles(self):
        """摧毁敌人载具"""
        getattr(self.lib, sys._getframe().f_code.co_name)()

    def fill_current_ammo(self):
        """补充弹药"""
        getattr(self.lib, sys._getframe().f_code.co_name)()

    def get_position(self):
        """获取当前位置坐标"""
        pos = ffi.new("float[3]", [0] * 3)
        getattr(self.lib, sys._getframe().f_code.co_name)(pos)
        return tuple(pos)

    def gtav_init(self):
        """gtav初始化"""
        getattr(self.lib, sys._getframe().f_code.co_name)()

    def keydown(self, scanKey: int):
        """按下键盘"""
        getattr(self.lib, sys._getframe().f_code.co_name)(scanKey)

    def keyup(self, scanKey: int):
        """松开键盘"""
        getattr(self.lib, sys._getframe().f_code.co_name)(scanKey)

    def kill_enemy_npc(self):
        """杀死敌人"""
        getattr(self.lib, sys._getframe().f_code.co_name)()

    def kill_process(self):
        """终止进程"""
        getattr(self.lib, sys._getframe().f_code.co_name)()

    def move_forward(self):
        """向前移动"""
        getattr(self.lib, sys._getframe().f_code.co_name)()

    def read_cut(self) -> tuple:
        """读取分红"""
        data = ffi.new("int[]", (0,) * 16)
        getattr(self.lib, sys._getframe().f_code.co_name)(data)
        return tuple(data)

    def repairing_vehicle(self):
        """修复载具"""
        getattr(self.lib, sys._getframe().f_code.co_name)()

    def set_armor(self, armor: float):
        """设置护甲数值"""
        getattr(self.lib, sys._getframe().f_code.co_name)(armor)

    def set_copLevel(self, copLevel: int = 0):
        """设置通辑等级"""
        getattr(self.lib, sys._getframe().f_code.co_name)(copLevel)

    def set_godMode(self, status: bool):
        """设置无敌状态"""
        getattr(self.lib, sys._getframe().f_code.co_name)(status)

    def set_health(self, health):
        """设置生命数值"""
        getattr(self.lib, sys._getframe().f_code.co_name)(health)

    def set_infiniteAmmo(self, status: bool):
        """设置弹药无限状态"""
        getattr(self.lib, sys._getframe().f_code.co_name)(status)

    def set_luckyWheel(self, value: int = 18):
        """设置幸运转盘结果"""
        getattr(self.lib, sys._getframe().f_code.co_name)(value)

    def set_seatbelt(self, status: bool):
        """设置安全带状态"""
        getattr(self.lib, sys._getframe().f_code.co_name)(status)

    def set_vehicleAbility(self, value: int):
        """设置载具能力"""
        getattr(self.lib, sys._getframe().f_code.co_name)(value)

    def set_vehicleGodMode(self, status: bool):
        """设置载具无敌状态"""
        getattr(self.lib, sys._getframe().f_code.co_name)(status)

    def set_weaponAmmoType(self, value: int):
        """设置武器弹药类型"""
        getattr(self.lib, sys._getframe().f_code.co_name)(value)

    def set_weather(self, weather: int):
        """设置天气"""
        getattr(self.lib, sys._getframe().f_code.co_name)(weather)

    def spawn_vehicle(self, hashCode, d = 5.0):
        """刷出载具"""
        getattr(self.lib, sys._getframe().f_code.co_name)(hashCode, d)

    def stat_write(self, stat: str, value: str):
        """stat写入"""
        try:
            data = ffi.new("char[]", stat.encode("utf-8"))
            v = int(value)
            getattr(self.lib, sys._getframe().f_code.co_name)(data, v)
        except:
            pass

    def suspend_process(self):
        """挂起进程"""
        getattr(self.lib, sys._getframe().f_code.co_name)()

    def teleport_enemy_npc(self, position: "tuple[float,float,float]"):
        """传送敌人到指定位置"""
        getattr(self.lib, sys._getframe().f_code.co_name)(ffi.new("float[3]", position))

    def teleport_to_objective(self):
        """传送到目标点"""
        getattr(self.lib, sys._getframe().f_code.co_name)()

    def teleport_to_waypoint(self):
        """传送到导航点"""
        getattr(self.lib, sys._getframe().f_code.co_name)()

    def teleport(self, position: "tuple[float,float,float]"):
        """传送到指定位置"""
        getattr(self.lib, sys._getframe().f_code.co_name)(ffi.new("float[3]", position))

    def write_cut(self, data: tuple):
        """写入分红"""
        getattr(self.lib, sys._getframe().f_code.co_name)(ffi.new("int[16]", data))

    def write_localAddressFloat(self, threadName: str, offset: int, value: int):
        """localAddress int写入"""
        thn = ffi.new("char[]", threadName.encode("utf-8"))
        getattr(self.lib, sys._getframe().f_code.co_name)(thn, offset, value)

    def write_localAddressInt(self, threadName: str, offset: int, value: int):
        """localAddress float写入"""
        thn = ffi.new("char[]", threadName.encode("utf-8"))
        getattr(self.lib, sys._getframe().f_code.co_name)(thn, offset, value)

    def read_localAddress(self, threadName: str, offset: int) -> int:
        """localAddress 8Bytes地址获取"""
        thn = ffi.new("char[]", threadName.encode("utf-8"))
        return getattr(self.lib, sys._getframe().f_code.co_name)(thn, offset)


class Keyboard(Gtalib):
    def __init__(self):
        super().__init__()
        self.hotkeyPool = dict()

    def keyboard_watch(self):
        try:
            return getattr(self.lib, sys._getframe().f_code.co_name)()
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


class Gtav(Gtalib):
    def __init__(self) -> None:
        super().__init__()
        self.gtav_init()

    def apartment_heist(self):
        """跳过公寓抢劫任务前置"""
        self.stat_write("MPx_HEIST_PLANNING_STAGE", -1)  # 跳过准备前置 4人开始进入动画后触发生效

    def doomsday_cooldown(self):
        """末日3冷却"""
        self.stat_write("MPx_HEISTCOOLDOWNTIMER2", -1)  # 末日3冷却

    def doomsday(self):
        """跳过末日前置"""
        self.stat_write("MPx_GANGOPS_FLOW_MISSION_PROG", -1)  # 跳过前置，M-设施管理-关闭后开启抢劫策划大屏

    def casino(self):
        """赌场豪劫改目标为钻石"""
        self.stat_write("MPx_H3OPT_TARGET", 3)  # 目标钻石

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
            self.stat_write(tp[0], tp[1])
            sleep(1)

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
            self.stat_write(tp[0], tp[1])

    def circuitBreaker(self):
        """全服银行电路"""
        self.write_localAddressInt("fm_mission_controller", 11731 + 24, 7)

    def doomsday2_hack(self):
        """末日2"""
        self.write_localAddressInt("fm_mission_controller", 1537, 2)

    def doomsday3_hack(self):
        """末日3破解"""
        self.write_localAddressInt("fm_mission_controller", 1398, 3)

    def casinoFingerprint_hack(self):
        """赌场指纹"""
        self.write_localAddressInt("fm_mission_controller", 52929, 5)

    def casinoDoor_hack(self):
        """赌场门禁"""
        self.write_localAddressInt("fm_mission_controller", 54726, 1)
        sleep(0.1)
        self.write_localAddressInt("fm_mission_controller", 54747, 5)
        sleep(0.1)
        self.write_localAddressInt("fm_mission_controller", 54726 + 17, 10)
        sleep(0.1)

    def pericoHack1(self):
        """机场塔楼电压柜"""
        pass

    def pericoHack2(self):
        """下水道栅栏"""
        self.write_localAddressInt("fm_mission_controller_2020", 27500, 6)

    def pericoHack3(self):
        """指纹破解"""
        self.write_localAddressInt("fm_mission_controller_2020", 23385, 5)

    def pericoHack4(self):
        """主目标玻璃切割"""
        self.write_localAddressFloat("fm_mission_controller_2020", 28736 + 3, 100.0)


class Doomsday(Keyboard):
    SPACE = 0x39
    S = 0x1F
    D = 0x20

    def mission(self, value: int):
        if value == 1 or value == 2:
            self.keydown(self.SPACE)
            sleep(0.030)
            self.keydown(self.D)
            sleep(0.030)
            self.keyup(self.SPACE)
            sleep(0.030)
            self.keyup(self.D)
            sleep(0.150)
        elif value == 3:
            self.keydown(self.SPACE)
            sleep(0.100)
            self.keydown(self.S)
            sleep(0.030)
            self.keydown(self.D)
            sleep(0.030)
            self.keyup(self.SPACE)
            sleep(0.030)
            self.keyup(self.D)
            sleep(0.030)
            self.keyup(self.S)
            sleep(0.150)


if __name__ == "__main__":
    gtav = Gtalib()
    gtav.gtav_init()
    gtav.set_copLevel()
