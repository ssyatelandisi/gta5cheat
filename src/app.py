import sys, threading, csv, os
from time import sleep
from ctypes import windll
from winsound import Beep
from gtaui import Ui_Form
from GTA5 import GTAV, GTAHax, Doomsday, Keyboard
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox, QCheckBox, QTableWidgetItem
from PyQt5.QtCore import Qt, QThread, QRunnable, QThreadPool, pyqtSignal, pyqtSlot
from PyQt5 import QtGui


def withThread(function):
    """线程的饰器"""

    def Threads(*args):
        threading.Thread(target=function, args=args, daemon=True).start()

    return Threads


class Task(QRunnable):
    def __init__(self, fn):
        super().__init__()
        self.setAutoDelete(True)
        self.fn = fn
        # self.args = args
        # self.kwargs = kwargs

    @pyqtSlot()
    def run(self):
        self.fn()


class StatHaxTask(QThread):
    signal = pyqtSignal(str)

    def __init__(self, gtavHax: GTAHax):
        super().__init__()
        self.setTerminationEnabled(False)
        self.__text = ""
        self.__gtavHax = gtavHax

    def setText(self, text):
        self.__text = text

    def run(self):
        if self.__text:
            lines = self.__text.splitlines(False)
            i = 0
            count = len(lines)
            while i < count // 2:
                try:
                    self.__gtavHax.write_stat(lines[i * 2].strip("$"), int(lines[i * 2 + 1].strip()))
                except:
                    return
                self.signal.emit(f"{i}/{count//2}")
                self.msleep(1000)
                i += 1


class ThreadPool(QThreadPool):
    """线程池"""

    def __init__(self):
        super().__init__()

    def submit(self, task: Task):
        self.start(Task(task))


class WindowApp(Ui_Form, QWidget):
    """继承自Ui_Form"""

    # 线程池
    # threadPool = ThreadPoolExecutor(max_workers=8)
    threadPool = ThreadPool()
    threadPool.setMaxThreadCount(threadPool.maxThreadCount())
    keyboard = Keyboard()
    gtahax = GTAHax()
    # 子弹类型
    weaponAmmoTypes = [("默认", -1), ("MKⅡ爆炸子弹", 18), ("信号弹", 22), ("燃油泵", 34), ("原子能枪", 70)]
    # 载具
    vehicles = [
        ("801巴提", "Bati"),
        ("骷髅马", "Kuruma2"),
        ("阿库拉", "Akula"),
        ("长崎小艇", "Dinghy2"),
        ("图拉尔多", "Toreador"),
        ("狂焰", "Pyro"),
        ("P-996 天煞", "Lazer"),
        ("暴君MK2", "Oppressor2"),
    ]
    # 战局
    sessions = [
        ("仅限邀请战局", 11),
        ("创建公共战局", 1),
        ("私人好友战局", 6),
        ("单人战局", 10),
        ("离开线上", -1),
    ]
    # 天气
    weather = [
        ("默认", -1),
        ("格外晴朗", 0),
        ("晴朗", 1),
        ("多云", 2),
        ("阴霾", 3),
        ("大雾", 4),
        ("阴天", 5),
        ("下雨", 6),
        ("雷雨", 7),
        ("雨转晴", 8),
        ("阴雨", 9),
        ("下雪", 10),
        ("暴雪", 11),
        ("小雪", 12),
        ("圣诞", 13),
        ("万圣节", 14),
    ]
    # 载具能力
    vehicleAbilities = [("普通载具能力", 0x0), ("载具助推器", 0x40), ("载具跳跃", 0x20)]

    def __init__(self):
        super().__init__()
        self.setupUi(self)  # 继承父类的setupUi方法
        self.check_GTA5Cheat_is_running()  # 检查GTA5 Cheat是否已开启
        self.check_GTA5_is_running()  # 判断gta5.exe运行
        if os.path.exists("YimMenu.dll") is False:
            self.pushButton_yimInject.deleteLater()
        # 常用面板
        self.checkBox_seatbelt.stateChanged.connect(lambda: self.fun_checkBox_clicked(self.checkBox_seatbelt))
        self.checkBox_autoCure.stateChanged.connect(lambda: self.fun_checkBox_clicked(self.checkBox_autoCure))
        self.checkBox_godMode.stateChanged.connect(lambda: self.fun_checkBox_clicked(self.checkBox_godMode))
        self.checkBox_vehicleGodMode.stateChanged.connect(lambda: self.fun_checkBox_clicked(self.checkBox_vehicleGodMode))
        self.checkBox_antiAFK.stateChanged.connect(lambda: self.fun_checkBox_clicked(self.checkBox_antiAFK))
        self.checkBox_infiniteAmmo.stateChanged.connect(lambda: self.fun_checkBox_clicked(self.checkBox_infiniteAmmo))
        self.comboBox_weaponAmmoType.currentIndexChanged.connect(self.change_weaponAmmoType)
        self.pushButton_navigationTeleport.clicked.connect(lambda: self.fun_pushButton_clicked(self.pushButton_navigationTeleport))
        self.pushButton_noCops.clicked.connect(lambda: self.fun_pushButton_clicked(self.pushButton_noCops))
        self.pushButton_fullAmmo.clicked.connect(lambda: self.fun_pushButton_clicked(self.pushButton_fullAmmo))
        self.pushButton_killYourself.clicked.connect(lambda: self.fun_pushButton_clicked(self.pushButton_killYourself))
        self.pushButton_forward.clicked.connect(lambda: self.fun_pushButton_clicked(self.pushButton_forward))
        self.pushButton_vehicleRepairing.clicked.connect(lambda: self.fun_pushButton_clicked(self.pushButton_vehicleRepairing))
        self.pushButton_objectiveTeleport.clicked.connect(lambda: self.fun_pushButton_clicked(self.pushButton_objectiveTeleport))
        self.pushButton_solo.clicked.connect(lambda: self.fun_pushButton_clicked(self.pushButton_solo))
        self.pushButton_killEnemyNPC.clicked.connect(lambda: self.fun_pushButton_clicked(self.pushButton_killEnemyNPC))
        self.pushButton_destroyEnemyVehicles.clicked.connect(lambda: self.fun_pushButton_clicked(self.pushButton_destroyEnemyVehicles))
        self.pushButton_yimInject.clicked.connect(lambda: self.fun_pushButton_clicked(self.pushButton_yimInject))

        # 传送面板
        self.checkBox_continuousTeleportation.stateChanged.connect(lambda: self.fun_checkBox_clicked(self.checkBox_continuousTeleportation))
        self.pushButton_addLocal.clicked.connect(lambda: self.fun_pushButton_clicked(self.pushButton_addLocal))
        self.pushButton_delSelect.clicked.connect(lambda: self.fun_pushButton_clicked(self.pushButton_delSelect))
        self.pushButton_saveTable.clicked.connect(lambda: self.fun_pushButton_clicked(self.pushButton_saveTable))
        self.pushButton_teleportSelect.clicked.connect(lambda: self.fun_pushButton_clicked(self.pushButton_teleportSelect))

        # 分红面板
        self.tabWidget.currentChanged.connect(self.tabWidgetChanged)
        self.pushButton_readCut.clicked.connect(lambda: self.fun_pushButton_clicked(self.pushButton_readCut))
        self.pushButton_writeCut.clicked.connect(lambda: self.fun_pushButton_clicked(self.pushButton_writeCut))

        # 测试面板
        self.pushButton_killEnemyNPC.clicked.connect(lambda: self.fun_pushButton_clicked(self.pushButton_killEnemyNPC))
        self.pushButton_destroyEnemyVehicles.clicked.connect(lambda: self.fun_pushButton_clicked(self.pushButton_destroyEnemyVehicles))
        self.pushButton_teleportEnemyNPC.clicked.connect(lambda: self.fun_pushButton_clicked(self.pushButton_teleportEnemyNPC))
        self.pushButton_apartmentHeist.clicked.connect(lambda: self.fun_pushButton_clicked(self.pushButton_apartmentHeist))
        self.pushButton_circuitBreaker.clicked.connect(lambda: self.fun_pushButton_clicked(self.pushButton_circuitBreaker))
        self.pushButton_doomsday.clicked.connect(lambda: self.fun_pushButton_clicked(self.pushButton_doomsday))
        self.pushButton_doomsday3Hack.clicked.connect(lambda: self.fun_pushButton_clicked(self.pushButton_doomsday3Hack))
        self.pushButton_doomsday1Hack.clicked.connect(lambda: self.fun_pushButton_clicked(self.pushButton_doomsday1Hack))
        self.pushButton_doomsday3Cooldown.clicked.connect(lambda: self.fun_pushButton_clicked(self.pushButton_doomsday3Cooldown))
        self.pushButton_casinoTargetChange.clicked.connect(lambda: self.fun_pushButton_clicked(self.pushButton_casinoTargetChange))
        self.pushButton_casinoFingerprintHack.clicked.connect(lambda: self.fun_pushButton_clicked(self.pushButton_casinoFingerprintHack))
        self.pushButton_casinoDoorHack.clicked.connect(lambda: self.fun_pushButton_clicked(self.pushButton_casinoDoorHack))
        self.pushButton_pericoTargetChange.clicked.connect(lambda: self.fun_pushButton_clicked(self.pushButton_pericoTargetChange))
        self.pushButton_pericoHack1.clicked.connect(lambda: self.fun_pushButton_clicked(self.pushButton_pericoHack1))
        self.pushButton_pericoHack2.clicked.connect(lambda: self.fun_pushButton_clicked(self.pushButton_pericoHack2))
        self.pushButton_pericoHack3.clicked.connect(lambda: self.fun_pushButton_clicked(self.pushButton_pericoHack3))
        self.pushButton_pericoHack4.clicked.connect(lambda: self.fun_pushButton_clicked(self.pushButton_pericoHack4))
        self.checkBox_luckyWheel.stateChanged.connect(lambda: self.fun_checkBox_clicked(self.checkBox_luckyWheel))

        # STAT面板
        self.stathax = StatHaxTask(self.gtav.gtahax)
        self.stathax.signal.connect(self.stathax_slot)
        self.stathax.started.connect(self.stathax_started)
        self.stathax.finished.connect(self.stathax_finished)
        self.pushButton_statSubmit.clicked.connect(lambda: self.fun_pushButton_clicked(self.pushButton_statSubmit))

        # 天气和载具面板
        self.comboBox_weather.currentIndexChanged.connect(self.change_weather)
        self.lineEdit_vehicleCode.textChanged.connect(self.vehicleCodeInput)
        self.pushButton_indoorSpawn.clicked.connect(lambda: self.fun_pushButton_clicked(self.pushButton_indoorSpawn))
        self.pushButton_outdoorSpawn.clicked.connect(lambda: self.fun_pushButton_clicked(self.pushButton_outdoorSpawn))

        # 其他初始化
        self.table_show()
        self.comboBox_weaponAmmoType_init()
        self.comboBox_vehicle_init()
        self.comboBox_vehicleAbility_init()
        self.comboBox_session_init()
        self.comboBox_weather_init()
        self.hotkey()
        self.threadPool.submit(self.keyboard.run)
        self.threadPool.submit(self.checkBox_watch)

    def check_GTA5Cheat_is_running(self):
        """检测GTAOL辅助是否已在运行"""
        cheatHwnd = windll.user32.FindWindowW("Qt5152QWindowIcon", "GTAOL辅助")
        if cheatHwnd > 0:
            QMessageBox.warning(self, "警告", "GTAOL辅助已经在运行，请勿重复开启！", QMessageBox.StandardButton.Close)
            QApplication.instance().quit()
            sys.exit()

    def check_GTA5_is_running(self):
        """判断gta是否在运行"""
        try:
            self.gtav = GTAV()
        except:
            # QMessageBox.critical(self, "错误", "没有找到GTA5.exe在运行", QMessageBox.Ok)
            QApplication.instance().quit()
            sys.exit()

    def fun_checkBox_clicked(self, item: QCheckBox):
        """复选框触发\n
        item: 复选框\n
        """
        if item.objectName() == "checkBox_antiAFK":
            self.threadPool.submit(lambda: self.gtav.antiAFK(item.isChecked()))
        if item.objectName() == "checkBox_seatbelt":
            self.gtav.player.playerSeatbelt = 0xC9 if item.isChecked() else 0xC8
        elif item.objectName() == "checkBox_autoCure":
            if item.isChecked():
                self.threadPool.submit(lambda: self.gtav.cure_yourself())
        elif item.objectName() == "checkBox_godMode":
            self.gtav.player.playerGodmode = 1 if item.isChecked() else 0
        elif item.objectName() == "checkBox_vehicleGodMode":
            if self.gtav.player.playerInVehicle == 1:
                self.gtav.vehicle.vehicleGodmode = 1 if item.isChecked() else 0
        elif item.objectName() == "checkBox_killGTA":
            pass
        elif item.objectName() == "checkBox_infiniteAmmo":
            self.gtav.weapon.weaponInfiniteAmmo = 10 if item.isChecked() else 0
        elif item.objectName() == "checkBox_luckyWheel":
            self.gtav.statusData.luckyWheel = item.isChecked()
            if item.isChecked():
                self.threadPool.submit(self.gtav.luckyWheel)
        elif item.objectName() == "checkBox_continuousTeleportation":
            if item.isChecked():
                self.threadPool.submit(self.continuous_teleportation)
        if item.isChecked():
            self.beep(1600, 500)
        else:
            self.beep(600, 500)

    def fun_pushButton_clicked(self, item):
        """按钮点击\n
        item: 按钮\n
        """
        if item.objectName() == "pushButton_forward":
            self.threadPool.submit(self.gtav.forward)
        if item.objectName() == "pushButton_navigationTeleport":
            self.threadPool.submit(self.gtav.navigation_teleport)
        if item.objectName() == "pushButton_objectiveTeleport":
            self.threadPool.submit(self.gtav.objective_teleport)
        elif item.objectName() == "pushButton_noCops":
            self.threadPool.submit(self.gtav.no_cops)
        elif item.objectName() == "pushButton_killYourself":
            self.threadPool.submit(self.gtav.kill_yourself)
        elif item.objectName() == "pushButton_solo":
            self.threadPool.submit(lambda: self.gtav.leave_me_alone(10.0))
        elif item.objectName() == "pushButton_fullAmmo":
            self.threadPool.submit(self.gtav.weapon.full_current_ammo)
        elif item.objectName() == "vehicle_repairing":
            self.threadPool.submit(self.gtav.vehicle.repairing_vehicle)
        elif item.objectName() == "pushButton_addLocal":
            self.add_new_teleport_row()  # 不能在线程中更新UI
        elif item.objectName() == "pushButton_delSelect":
            self.del_select_teleport_row()  # 不能在线程中更新UI
        elif item.objectName() == "pushButton_saveTable":
            self.threadPool.submit(self.save_teleportsTxt)
        elif item.objectName() == "pushButton_teleportSelect":
            self.threadPool.submit(self.teleport_select)
        elif item.objectName() == "pushButton_vehicleRepairing":
            self.threadPool.submit(self.repairing_vehicle)
        elif item.objectName() == "pushButton_readCut":
            self.threadPool.submit(self.read_cut)
        elif item.objectName() == "pushButton_writeCut":
            self.threadPool.submit(self.write_cut)
        elif item.objectName() == "pushButton_apartmentHeist":
            self.threadPool.submit(self.gtav.apartment_heist)
        elif item.objectName() == "pushButton_doomsday":
            self.threadPool.submit(self.gtav.doomsday)
        elif item.objectName() == "pushButton_doomsday3Cooldown":
            self.threadPool.submit(self.gtav.doomsday_cooldown)
        elif item.objectName() == "pushButton_casinoTargetChange":
            self.threadPool.submit(self.gtav.casino)
        elif item.objectName() == "pushButton_pericoTargetChange":
            self.threadPool.submit(self.gtav.perico)
        elif item.objectName() == "pushButton_killEnemyNPC":
            self.threadPool.submit(self.gtav.kill_enemy_npc)
        elif item.objectName() == "pushButton_destroyEnemyVehicles":
            self.threadPool.submit(self.gtav.destroy_enemy_vehicles)
        elif item.objectName() == "pushButton_teleportEnemyNPC":
            self.threadPool.submit(self.teleport_enemy_npc_select)
        elif item.objectName() == "pushButton_doomsday2Hack":
            self.threadPool.submit(self.gtav.doomsday3_hack)
        elif item.objectName() == "pushButton_doomsday3Hack":
            self.threadPool.submit(self.gtav.doomsday2_hack)
        elif item.objectName() == "pushButton_casinoFingerprintHack":
            self.threadPool.submit(self.gtav.casinoFingerprint_hack)
        elif item.objectName() == "pushButton_casinoDoorHack":
            self.threadPool.submit(self.gtav.casinoDoor_hack)
        elif item.objectName() == "pushButton_circuitBreaker":
            self.threadPool.submit(self.gtav.circuitBreaker)
        elif item.objectName() == "pushButton_pericoHack1":
            self.threadPool.submit(self.gtav.pericoHack1)
        elif item.objectName() == "pushButton_pericoHack2":
            self.threadPool.submit(self.gtav.pericoHack2)
        elif item.objectName() == "pushButton_pericoHack3":
            self.threadPool.submit(self.gtav.pericoHack3)
        elif item.objectName() == "pushButton_pericoHack4":
            self.threadPool.submit(self.gtav.pericoHack4)
        elif item.objectName() == "pushButton_yimInject":
            self.threadPool.submit(lambda: self.gtav.yim_inject(os.path.join(os.getcwd(), "YimMenu.dll")))
        elif item.objectName() == "pushButton_statSubmit":
            self.stathax_starting()
        elif item.objectName() == "pushButton_indoorSpawn":
            self.threadPool.submit(self.indoor_spawn_vehicle)
        elif item.objectName() == "pushButton_outdoorSpawn":
            self.threadPool.submit(self.outdoor_spawn_vehicle)
        self.beep(1600, 500)

    def hotkey(self):
        """快捷键绑定"""
        self.keyboard.add_hotkey(0xA231, lambda: self.shortcut_touch("doomsday2"))  # LCTRL+1
        self.keyboard.add_hotkey(0xA232, lambda: self.shortcut_touch("doomsday3"))  # LCTRL+2
        self.keyboard.add_hotkey(0xA252, lambda: self.shortcut_touch("full_current_ammo"))  # LCTRL+R
        self.keyboard.add_hotkey(0xA22E, lambda: self.shortcut_touch("kill_yourself"))  # LCTRL+DEL
        self.keyboard.add_hotkey(0x70, lambda: self.shortcut_touch("f1_kill_GTA5"))  # F1
        self.keyboard.add_hotkey(0x72, lambda: self.shortcut_touch("forwaord"))  # F3
        self.keyboard.add_hotkey(0x73, lambda: self.shortcut_touch("navigation_teleport"))  # F4
        self.keyboard.add_hotkey(0x74, lambda: self.shortcut_touch("objective_teleport"))  # F5
        self.keyboard.add_hotkey(0x75, lambda: self.shortcut_touch("vehicleAbility"))  # F6
        self.keyboard.add_hotkey(0x76, lambda: self.shortcut_touch("godMode"))  # F7
        self.keyboard.add_hotkey(0xA276, lambda: self.shortcut_touch("godModeOff"))  # LCTRL+F7
        self.keyboard.add_hotkey(0x77, lambda: self.shortcut_touch("noCaps"))  # F8
        self.keyboard.add_hotkey(0xA278, lambda: self.shortcut_touch("vehicle_repairing"))  # LCTRL+F9
        self.keyboard.add_hotkey(0xA27A, lambda: self.shortcut_touch("change_session"))  # LCTRL+F11
        self.keyboard.add_hotkey(0xA2C0, lambda: self.shortcut_touch("generate_vehicle"))  # LCTRL+~
        self.keyboard.add_hotkey(0x6F, lambda: self.shortcut_touch("kill_enemy_npc"))  # /
        self.keyboard.add_hotkey(0x6A, lambda: self.shortcut_touch("destroy_enemy_vehicles"))  # *

    def shortcut_touch(self, pramas):
        """快捷键事件处理"""
        if pramas == "doomsday2":
            self.threadPool.submit(Doomsday.start, 2)
        elif pramas == "doomsday3":
            self.threadPool.submit(Doomsday.start, 3)
        elif pramas == "kill_yourself":
            self.threadPool.submit(self.gtav.kill_yourself)
        elif pramas == "forwaord":
            self.threadPool.submit(self.gtav.forward)
        elif pramas == "f1_kill_GTA5":
            self.threadPool.submit(self.f1_kill_GTA5)
        elif pramas == "navigation_teleport":
            self.threadPool.submit(self.gtav.navigation_teleport)
        elif pramas == "objective_teleport":
            self.threadPool.submit(self.gtav.objective_teleport)
        elif pramas == "vehicleAbility":
            self.threadPool.submit(self.change_vehicleAbility)
        elif pramas == "godMode":
            self.threadPool.submit(lambda: self.player_godmode(True))
            return
        elif pramas == "godModeOff":
            self.threadPool.submit(lambda: self.player_godmode(False))
            return
        elif pramas == "noCaps":
            self.threadPool.submit(self.gtav.no_cops)
        elif pramas == "change_session":
            self.threadPool.submit(lambda: self.gtav.change_session(self.sessions[self.comboBox_session.currentIndex()][1]))
        elif pramas == "generate_vehicle":
            self.threadPool.submit(
                lambda: self.gtav.generate_vehicle(self.gtav.joaat(self.vehicles[self.comboBox_vehicleList.currentIndex()][1]))
            )
        elif pramas == "vehicle_repairing":
            self.threadPool.submit(self.gtav.vehicle.repairing_vehicle)
        elif pramas == "kill_enemy_npc":
            self.threadPool.submit(self.gtav.kill_enemy_npc)
        elif pramas == "destroy_enemy_vehicles":
            self.threadPool.submit(self.gtav.destroy_enemy_vehicles)
        elif pramas == "full_current_ammo":
            self.threadPool.submit(self.gtav.weapon.full_current_ammo)
        self.beep(1600, 500)

    def table_show(self):
        """读取表格"""
        self.tableWidget.setAlternatingRowColors(True)
        self.tableWidget.setSortingEnabled(False)
        for r in range(self.tableWidget.rowCount()):
            self.tableWidget.removeRow(0)  # 移除预置内容
        with open("teleports.txt", "a+", encoding="utf-8") as f:
            f.seek(0)
            r = 0
            for row in csv.reader(f):
                self.tableWidget.insertRow(r)
                c = 0
                for item in row:
                    Qitem = QTableWidgetItem(str(item))
                    self.tableWidget.setItem(r, c, Qitem)
                    if c == 0:
                        self.tableWidget.selectRow(0)
                    c += 1
                r += 1

    def add_new_teleport_row(self):
        """新增传送点"""
        row = self.tableWidget.rowCount()
        self.tableWidget.insertRow(row)
        self.tableWidget.setItem(row, 0, QTableWidgetItem(self.lineEdit_nameInput.text()))
        pos = self.gtav.player.playerLocation
        i = 1
        for value in pos:
            item = QTableWidgetItem(f"{value:.3f}")
            item.setFlags(Qt.ItemIsEnabled)
            self.tableWidget.setItem(row, i, item)
            i += 1
        self.lineEdit_nameInput.clear()

    def del_select_teleport_row(self):
        """删除选中行"""
        self.tableWidget.removeRow(self.tableWidget.currentRow())

    def save_teleportsTxt(self):
        """保存表格"""
        with open("teleports.txt", "w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            for i in range(self.tableWidget.rowCount()):
                rows = []
                for j in range(self.tableWidget.columnCount()):
                    rows.append(self.tableWidget.item(i, j).text())
                writer.writerow(rows)

    def teleport_select(self):
        """传送到选定位置"""
        row = self.tableWidget.currentRow()
        (x, y, z) = (
            float(self.tableWidget.item(row, 1).text()),
            float(self.tableWidget.item(row, 2).text()),
            float(self.tableWidget.item(row, 3).text()),
        )
        self.gtav.teleport((x, y, z))

    def teleport_enemy_npc_select(self):
        """传送敌对NPC到选定位置"""
        try:
            row = self.tableWidget.currentRow()
            (x, y, z) = (
                float(self.tableWidget.item(row, 1).text()),
                float(self.tableWidget.item(row, 2).text()),
                float(self.tableWidget.item(row, 3).text()),
            )
        except:
            (x, y, z) = (0, 0, 100.0)
        self.gtav.teleport_enemy_npc((x, y, z))

    def tabWidgetChanged(self):
        """tab面板切换"""
        if self.tabWidget.currentIndex() == 2:
            self.read_cut()  # 切换到分红面板读取分红
        else:
            return None

    def read_cut(self):
        """读取分红"""
        try:
            apartmentHeistCut = self.gtav.heist.apartmentHeist
            doomsdayHeistCut = self.gtav.heist.doomsdayHeist
            casinoHeistCut = self.gtav.heist.casinoHeist
            pericoHeistCut = self.gtav.heist.pericoHeist
            self.spinBox_playerCut1_apartmentHeist.setValue(apartmentHeistCut[0])
            self.spinBox_playerCut2_apartmentHeist.setValue(apartmentHeistCut[1])
            self.spinBox_playerCut3_apartmentHeist.setValue(apartmentHeistCut[2])
            self.spinBox_playerCut4_apartmentHeist.setValue(apartmentHeistCut[3])
            self.spinBox_playerCut1_doomsdayHeist.setValue(doomsdayHeistCut[0])
            self.spinBox_playerCut2_doomsdayHeist.setValue(doomsdayHeistCut[1])
            self.spinBox_playerCut3_doomsdayHeist.setValue(doomsdayHeistCut[2])
            self.spinBox_playerCut4_doomsdayHeist.setValue(doomsdayHeistCut[3])
            self.spinBox_playerCut1_casinoHeist.setValue(casinoHeistCut[0])
            self.spinBox_playerCut2_casinoHeist.setValue(casinoHeistCut[1])
            self.spinBox_playerCut3_casinoHeist.setValue(casinoHeistCut[2])
            self.spinBox_playerCut4_casinoHeist.setValue(casinoHeistCut[3])
            self.spinBox_playerCut1_pericoHeist.setValue(pericoHeistCut[0])
            self.spinBox_playerCut2_pericoHeist.setValue(pericoHeistCut[1])
            self.spinBox_playerCut3_pericoHeist.setValue(pericoHeistCut[2])
            self.spinBox_playerCut4_pericoHeist.setValue(pericoHeistCut[3])
        except:
            return None

    def write_cut(self):
        """改写分红"""
        try:
            self.gtav.heist.apartmentHeist = (
                self.spinBox_playerCut1_apartmentHeist.value(),
                self.spinBox_playerCut2_apartmentHeist.value(),
                self.spinBox_playerCut3_apartmentHeist.value(),
                self.spinBox_playerCut4_apartmentHeist.value(),
            )
            self.gtav.heist.doomsdayHeist = (
                self.spinBox_playerCut1_doomsdayHeist.value(),
                self.spinBox_playerCut2_doomsdayHeist.value(),
                self.spinBox_playerCut3_doomsdayHeist.value(),
                self.spinBox_playerCut4_doomsdayHeist.value(),
            )
            self.gtav.heist.casinoHeist = (
                self.spinBox_playerCut1_casinoHeist.value(),
                self.spinBox_playerCut2_casinoHeist.value(),
                self.spinBox_playerCut3_casinoHeist.value(),
                self.spinBox_playerCut4_casinoHeist.value(),
            )
            self.gtav.heist.pericoHeist = (
                self.spinBox_playerCut1_pericoHeist.value(),
                self.spinBox_playerCut2_pericoHeist.value(),
                self.spinBox_playerCut3_pericoHeist.value(),
                self.spinBox_playerCut4_pericoHeist.value(),
            )
        except:
            QMessageBox.critical(self, "错误", "输入内容有误", QMessageBox.Ok)
            return None

    def comboBox_weaponAmmoType_init(self):
        """子弹类型下拉框初始化"""
        self.comboBox_weaponAmmoType.clear()
        for item in self.weaponAmmoTypes:
            self.comboBox_weaponAmmoType.addItem(item[0])

    def comboBox_vehicle_init(self):
        """载具下拉框初始化"""
        self.comboBox_vehicleList.clear()
        for item in self.vehicles:
            self.comboBox_vehicleList.addItem(item[0])

    def comboBox_session_init(self):
        """战局下拉框初始化"""
        self.comboBox_session.clear()
        for item in self.sessions:
            self.comboBox_session.addItem(item[0])

    def comboBox_weather_init(self):
        """天气初始化"""
        self.comboBox_weather.clear()
        for item in self.weather:
            self.comboBox_weather.addItem(item[0])

    def comboBox_vehicleAbility_init(self):
        """载具特殊能力下拉框初始化"""
        self.comboBox_vehicleAbility.clear()
        for item in self.vehicleAbilities:
            self.comboBox_vehicleAbility.addItem(item[0])

    def change_vehicleAbility(self):
        """修改载特殊能力"""
        if self.gtav.player.playerInVehicle == 1:
            self.gtav.vehicle.vehicleAbility = self.vehicleAbilities[self.comboBox_vehicleAbility.currentIndex()][1]

    def repairing_vehicle(self):
        """修复载具"""
        self.threadPool.submit(self.gtav.vehicle.repairing_vehicle)

    def change_weaponAmmoType(self):
        """修改子弹类型"""
        self.gtav.weapon.weaponAmmoType = self.weaponAmmoTypes[self.comboBox_weaponAmmoType.currentIndex()][1]

    def change_weather(self):
        """修改天气"""
        self.gtav.weather.weather = self.weather[self.comboBox_weather.currentIndex()][1]

    def player_godmode(self, boolean: bool):
        """玩家无敌模式开关"""
        if boolean is True:
            self.gtav.player.playerGodmode = 1
        else:
            self.gtav.player.playerGodmode = 0
        self.gtav.statusData.playerGodmode = boolean
        self.checkBox_godMode.setChecked(boolean)

    def vehicleCodeInput(self):
        """载具代码输入事件"""
        self.lineEdit_vehicleHash.setText(f"0x{self.gtav.joaat(self.lineEdit_vehicleCode.text().strip()):0X}")

    def indoor_spawn_vehicle(self):
        """室内刷出载具"""
        if self.lineEdit_vehicleHash.text().strip():
            self.gtav.indoor_spawn_vehicle(int(self.lineEdit_vehicleHash.text().strip(), base=16))

    def outdoor_spawn_vehicle(self):
        """室外刷出载具"""
        if self.lineEdit_vehicleHash.text().strip():
            self.gtav.outdoor_spawn_vehicle(int(self.lineEdit_vehicleHash.text().strip(), base=16))

    def stathax_started(self):
        self.pushButton_statSubmit_text = self.pushButton_statSubmit.text()
        self.pushButton_statSubmit.setFlat(True)
        self.pushButton_statSubmit.setEnabled(False)

    def stathax_finished(self):
        self.pushButton_statSubmit.setText(self.pushButton_statSubmit_text)
        self.pushButton_statSubmit.setFlat(False)
        self.pushButton_statSubmit.setEnabled(True)

    def stathax_starting(self):
        self.stathax.setText(self.textEdit_statText.toPlainText().replace("INT32", "", 1).strip())
        self.stathax.start()

    def stathax_slot(self, text):
        self.pushButton_statSubmit.setText(text)

    def beep(self, v: int, t: int):
        """提试音\n
        v int: 频率\n
        t int: 时间（毫秒）\n
        """
        Beep(v, t)

    def f1_kill_GTA5(self):
        """F1一键杀死进程"""
        if self.checkBox_killGTA.isChecked() is True:
            self.gtav.kill_process()
        else:
            return None

    def continuous_teleportation(self):
        """持续传送敌人到指定位置"""
        while self.checkBox_continuousTeleportation.isChecked():
            try:
                row = self.tableWidget.currentRow()
                (x, y, z) = (
                    float(self.tableWidget.item(row, 1).text()),
                    float(self.tableWidget.item(row, 2).text()),
                    float(self.tableWidget.item(row, 3).text()),
                )
            except:
                (x, y, z) = (0, 0, 100.0)
            self.gtav.teleport_enemy_npc((x, y, z))
            sleep(0.2)

    def checkBox_watch(self):
        """checkBox监听"""
        while self:
            if self.checkBox_godMode.isChecked():
                self.gtav.player.playerGodmode = 1
            if self.checkBox_autoCure.isChecked():
                self.gtav.cure_yourself()
            if self.checkBox_vehicleGodMode.isChecked():
                self.gtav.vehicle.vehicleGodmode = 1
            if self.checkBox_antiAFK.isChecked():
                self.gtav.antiAFK(True)
            if self.checkBox_infiniteAmmo.isChecked():
                self.gtav.weapon.weaponInfiniteAmmo = 10
            if self.checkBox_seatbelt.isChecked():
                self.gtav.player.playerSeatbelt = 0xC9
            sleep(0.5)

    def closeEvent(self, a0: QtGui.QCloseEvent):
        """关闭程序事件"""
        os._exit(0)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    windowApp = WindowApp()
    windowApp.show()
    sys.exit(app.exec())
