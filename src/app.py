import sys, threading, csv, os
from time import sleep
from functools import partial
from ctypes import windll
from ui_app import Ui_App
from gtav import Gtav
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtMultimedia import *
from work import *
import staticdata


def withThread(function):
    """线程的饰器"""

    def Threads(*args):
        threading.Thread(target=function, args=args, daemon=True)

    return Threads


def check_GTA5Cheat_is_running():
    """检测GTAOL辅助是否已在运行"""
    cheatHwnd: int = windll.user32.FindWindowW(None, "GTAOL辅助")
    if cheatHwnd > 0:
        windll.user32.MessageBoxW(None, "已有一个GTAOL辅助处于开启状态。", "失败", 0x10 | 0x0)
        sys.exit()


class Task(QThread):
    def __init__(self, fn, *args, **kwargs):
        super().__init__()
        self.fn = fn
        self.args = args
        self.kwargs = kwargs

    def run(self):
        self.fn(*self.args, **self.kwargs)


class WindowApp(QWidget):
    # 线程池
    # threadPool = ThreadPoolExecutor(max_workers=8)
    # threadPool = ThreadPool()
    # threadPool.setMaxThreadCount(threadPool.maxThreadCount())

    signalDuu = pyqtSignal()  # 播放声音信号
    signalDi = pyqtSignal()
    signalUpdate_cutTab = pyqtSignal()
    signalWorkHotkey = pyqtSignal()
    signalMessage = pyqtSignal(str, str)

    soundEffectDuu = QSoundEffect()
    soundEffectDi = QSoundEffect()

    task: Task

    def __init__(self, gtav: Gtav):
        super().__init__()
        self.ui = Ui_App()
        self.ui.setupUi(self)  # 继承父类的setupUi方法
        self.gtav = gtav
        if os.path.exists("YimMenu.dll") is False:
            self.ui.pushButton_yimInject.deleteLater()

        self.soundEffectDuu.setSource(QUrl.fromLocalFile(":/sound/sound0.wav"))
        self.soundEffectDi.setSource(QUrl.fromLocalFile(":/sound/sound1.wav"))
        self.signalDuu.connect(self.slotDuu)
        self.signalDi.connect(self.slotDi)

        self.model = QStandardItemModel()
        self.ui.tabWidget.currentChanged.connect(self.slotTabWidgetChanged)

        self.workSuspendProcess = WorkSuspendProcess(self, self.gtav)  # 挂起游戏子线程
        self.workLuckyWheel = WorkLuckyWheel(self, self.gtav)  # 幸运转盘子线程
        self.workCheckBoxWatch = WorkCheckBoxWatch(
            self, self.ui, self.model, self.gtav
        )  # 复选框监听子线程
        self.workStatHax = WorkStatHax(self, self.ui, self.gtav)  # stat输入子线程
        self.workHotkey = WorkHotkey(self, self.ui, self.gtav)  # 热键监听子线程

        # 其他初始化
        self.table_show()
        self.comboBox_weaponAmmoType_init()
        self.comboBox_vehicle_init()
        self.comboBox_vehicleAbilities_init()
        self.comboBox_session_init()
        self.comboBox_weather_init()

        for component in self.findChildren(QPushButton):
            component.clicked.connect(partial(self.slotPushButton_clicked, component))
        for component in self.findChildren(QCheckBox):
            component.stateChanged.connect(
                partial(self.slotCheckBox_stateChanged, component)
            )
        for component in self.findChildren(QComboBox):
            component.currentIndexChanged.connect(
                partial(self.slotComboBox_changed, component)
            )

        self.ui.lineEdit_vehicleCode.textChanged.connect(
            self.slotVehicleCode_textChanged
        )
        self.workStatHax.signalSet_statSubmit_text.connect(self.slotSet_statSubmit_text)
        self.workStatHax.signalStarted.connect(self.slotSet_statSubmit_disable)
        self.workStatHax.signalFinished.connect(self.slotSet_statSubmit_enable)
        self.workHotkey.signalDuu.connect(self.slotDuu)
        self.workHotkey.signalDi.connect(self.slotDi)
        self.signalWorkHotkey.connect(self.workHotkey.start)
        self.signalWorkHotkey.emit()
        self.workCheckBoxWatch.start()
        self.signalMessage.connect(self.slotMessage)

    def slotDuu(self):
        """播放音效Duu"""
        self.soundEffectDuu.play()

    def slotDi(self):
        """播放音效Di"""
        self.soundEffectDi.play()

    def slotPushButton_clicked(self, component: QWidget):
        """按钮点击"""
        if component.objectName() == "pushButton_indoorSpawn":
            if self.ui.lineEdit_vehicleHash.text() != "":
                self.task = Task(
                    self.gtav.spawn_vehicle,
                    int(self.ui.lineEdit_vehicleHash.text(), base=16),
                    2.5,
                )
                self.task.start()
        elif component.objectName() == "pushButton_outdoorSpawn":
            if self.ui.lineEdit_vehicleHash.text() != "":
                self.task = Task(
                    self.gtav.spawn_vehicle,
                    int(self.ui.lineEdit_vehicleHash.text(), base=16),
                    5.0,
                )
                self.task.start()
        elif component.objectName() == "pushButton_statSubmit":
            self.workStatHax.start()
        elif component.objectName() == "pushButton_casinoTargetChange":
            self.task = Task(self.gtav.casino)
            self.task.start()
        elif component.objectName() == "pushButton_casinoFingerprintHack":
            pass
        elif component.objectName() == "pushButton_casinoDoorHack":
            pass
        elif component.objectName() == "pushButton_skipApartmentHeist":
            self.task = Task(self.gtav.apartment_heist)
            self.task.start()
        elif component.objectName() == "pushButton_circuitBreaker":
            pass
        elif component.objectName() == "pushButton_skipDoomsdayHeist":
            self.task = Task(self.gtav.doomsday)
            self.task.start()
        elif component.objectName() == "pushButton_doomsday1Hack":
            pass
        elif component.objectName() == "pushButton_doomsday3Hack":
            self.task = Task(self.gtav.doomsday3_hack)
            self.task.start()
        elif component.objectName() == "pushButton_killEnemyNPC":
            self.task = Task(self.gtav.kill_enemy_npc)
            self.task.start()
        elif component.objectName() == "pushButton_yimInject":
            if os.path.exists("YimMenu.dll"):
                self.task = Task(
                    self.gtav.dll_inject, os.path.join(os.getcwd(), "YimMenu.dll")
                )
                self.task.start()
        elif component.objectName() == "pushButton_destroyEnemyVehicles":
            self.task = Task(self.gtav.destroy_enemy_vehicles)
            self.task.start()
        elif component.objectName() == "pushButton_pericoHack3":
            pass
        elif component.objectName() == "pushButton_pericoHack1":
            pass
        elif component.objectName() == "pushButton_pericoHack4":
            pass
        elif component.objectName() == "pushButton_pericoHack2":
            pass
        elif component.objectName() == "pushButton_pericoTargetChange":
            self.task = Task(self.gtav.perico)
            self.task.start()
        elif component.objectName() == "pushButton_readCut":
            self.task = Task(self.read_cut)
            self.task.start()
        elif component.objectName() == "pushButton_writeCut":
            self.task = Task(self.write_cut)
            self.task.start()
        elif component.objectName() == "pushButton_saveTable":
            self.task = Task(self.save_teleportsTxt)
            self.task.start()
        elif component.objectName() == "pushButton_addLocalPosition":
            self.task = Task(self.add_new_teleport_row)
            self.task.start()
        elif component.objectName() == "pushButton_teleportEnemyNPC":
            self.task = Task(self.teleport_enemy_npc_select)
            self.task.start()
        elif component.objectName() == "pushButton_teleportToSelectedPosition":
            self.task = Task(self.teleport_select)
            self.task.start()
        elif component.objectName() == "pushButton_delSelect":
            self.task = Task(self.del_select_teleport_row)
            self.task.start()
        elif component.objectName() == "pushButton_fillCurrentAmmo":
            self.task = Task(self.gtav.fill_current_ammo)
            self.task.start()
        elif component.objectName() == "pushButton_teleportToObjective":
            self.task = Task(self.gtav.teleport_to_objective)
            self.task.start()
        elif component.objectName() == "pushButton_noCops":
            self.task = Task(self.gtav.set_copLevel, 0)
            self.task.start()
        elif component.objectName() == "pushButton_solo":
            self.task = Task(self.gtav.suspend_process)
            self.task.start()
        elif component.objectName() == "pushButton_teleportToWaypoint":
            self.task = Task(self.gtav.teleport_to_waypoint)
            self.task.start()
        elif component.objectName() == "pushButton_vehicleRepairing":
            self.task = Task(self.gtav.repairing_vehicle)
            self.task.start()
        elif component.objectName() == "pushButton_killYourself":
            self.task = Task(self.gtav.set_health, 0.0)
            self.task.start()
        elif component.objectName() == "pushButton_moveForward":
            self.task = Task(self.gtav.move_forward)
            self.task.start()
        self.signalDuu.emit()

    def slotCheckBox_stateChanged(self, component: QCheckBox):
        """复选框触发"""
        if component.objectName() == "checkBox_luckyWheel":
            if self.ui.checkBox_luckyWheel.isChecked():
                if not self.workLuckyWheel.isRunning():
                    self.workLuckyWheel.start()
            else:
                if self.workLuckyWheel.isRunning():
                    self.workLuckyWheel.terminate()
        elif component.objectName() == "checkBox_continuousTeleportation":
            ...  # 写在work.py的WorkCheckBoxWatch子线程中处理
        elif component.objectName() == "checkBox_godMode":
            self.task = Task(
                self.gtav.set_godMode, self.ui.checkBox_godMode.isChecked()
            )
            self.task.start()
        elif component.objectName() == "checkBox_vehicleGodMode":
            self.task = Task(
                self.gtav.set_vehicleGodMode,
                self.ui.checkBox_vehicleGodMode.isChecked(),
            )
            self.task.start()
        elif component.objectName() == "checkBox_autoCure":
            ...
        elif component.objectName() == "checkBox_infiniteAmmo":
            self.task = Task(
                self.gtav.set_infiniteAmmo, self.ui.checkBox_infiniteAmmo.isChecked()
            )
            self.task.start()
        elif component.objectName() == "checkBox_killGTA":
            ...
        elif component.objectName() == "checkBox_antiAFK":
            self.task = Task(self.gtav.antiAFK, self.ui.checkBox_antiAFK.isChecked())
            self.task.start()
        elif component.objectName() == "checkBox_seatbelt":
            self.task = Task(
                self.gtav.set_seatbelt, self.ui.checkBox_seatbelt.isChecked()
            )
            self.task.start()
        if component.isChecked():
            self.signalDuu.emit()
        else:
            self.signalDi.emit()

    def slotComboBox_changed(self, component: QComboBox):
        """下拉选项框改变"""
        if component.objectName() == "comboBox_weather":
            self.task = Task(
                self.gtav.set_weather, int(self.weather[component.currentIndex()][1])
            )
            self.task.start()
        elif component.objectName() == "comboBox_session":
            return
        elif component.objectName() == "comboBox_vehicleAbilities":
            return
        elif component.objectName() == "comboBox_weaponAmmoType":
            self.task = Task(
                self.gtav.set_weaponAmmoType,
                int(self.weaponAmmoTypes[component.currentIndex()][1]),
            )
            self.task.start()
        elif component.objectName() == "comboBox_vehicles":
            return
        self.signalDuu.emit()

    def slotVehicleCode_textChanged(self):
        if self.ui.lineEdit_vehicleCode.text() != "":
            self.ui.lineEdit_vehicleHash.setText(
                f"0x{self.gtav.joaat(self.ui.lineEdit_vehicleCode.text().strip()):08X}"
            )
        else:
            self.ui.lineEdit_vehicleHash.clear()

    def slotSet_statSubmit_text(self, text):
        self.ui.pushButton_statSubmit.setText(text)

    def slotSet_statSubmit_disable(self):
        self.ui.pushButton_statSubmit.setFlat(True)
        self.ui.pushButton_statSubmit.setDisabled(True)

    def slotSet_statSubmit_enable(self):
        self.ui.pushButton_statSubmit.setFlat(False)
        self.ui.pushButton_statSubmit.setDisabled(False)

    def table_show(self):
        """读取表格"""
        self.ui.tableView_teleport.setAlternatingRowColors(True)
        self.ui.tableView_teleport.setSortingEnabled(False)
        self.ui.tableView_teleport.horizontalHeader().setCascadingSectionResizes(True)
        self.model.setHorizontalHeaderLabels(["名称", "x", "y", "z"])
        self.ui.tableView_teleport.setModel(self.model)
        try:
            with open("teleports.txt", "r", encoding="utf-8") as f:
                f.seek(0)
                for row in csv.reader(f):
                    self.model.appendRow(
                        [
                            QStandardItem(row[0]),
                            QStandardItem(row[1]),
                            QStandardItem(row[2]),
                            QStandardItem(row[3]),
                        ]
                    )
        except:
            return
        if self.model.rowCount() > 0:
            self.ui.tableView_teleport.selectRow(0)

    def add_new_teleport_row(self):
        """新增传送点"""
        pos = self.gtav.get_position()
        self.model.appendRow(
            [
                QStandardItem(self.ui.lineEdit_nameInput.text()),
                QStandardItem(f"{pos[0]:.3f}"),
                QStandardItem(f"{pos[1]:.3f}"),
                QStandardItem(f"{pos[2]:.3f}"),
            ]
        )
        self.ui.lineEdit_nameInput.clear()

    def del_select_teleport_row(self):
        """删除选中行"""
        self.model.removeRow(self.ui.tableView_teleport.currentIndex().row())

    def save_teleportsTxt(self):
        """保存表格"""
        with open("teleports.txt", "w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            for r in range(self.model.rowCount()):
                writer.writerow(
                    [
                        self.model.item(r, 0).text(),
                        self.model.item(r, 1).text(),
                        self.model.item(r, 2).text(),
                        self.model.item(r, 3).text(),
                    ]
                )

    def teleport_select(self):
        """传送到选定位置"""
        r = self.ui.tableView_teleport.currentIndex().row()
        (x, y, z) = (
            float(self.model.item(r, 1).text()),
            float(self.model.item(r, 2).text()),
            float(self.model.item(r, 3).text()),
        )
        self.gtav.teleport((x, y, z))

    def teleport_enemy_npc_select(self):
        """传送敌对NPC到选定位置"""
        try:
            r = self.ui.tableView_teleport.currentIndex().row()
            (x, y, z) = (
                float(self.model.item(r, 1).text()),
                float(self.model.item(r, 2).text()),
                float(self.model.item(r, 3).text()),
            )
        except:
            (x, y, z) = (0, 0, 100.0)
        self.gtav.teleport_enemy_npc((x, y, z))

    def slotTabWidgetChanged(self):
        """tab面板切换"""
        if self.ui.tabWidget.currentIndex() == 2:
            self.read_cut()  # 切换到分红面板读取分红
        else:
            return None

    def read_cut(self):
        """读取分红"""
        try:
            data = self.gtav.read_cut()
            apartmentHeistCut = data[0:4]
            doomsdayHeistCut = data[4:8]
            casinoHeistCut = data[8:12]
            pericoHeistCut = data[12:16]
            self.ui.spinBox_playerCut1_apartmentHeist.setValue(apartmentHeistCut[0])
            self.ui.spinBox_playerCut2_apartmentHeist.setValue(apartmentHeistCut[1])
            self.ui.spinBox_playerCut3_apartmentHeist.setValue(apartmentHeistCut[2])
            self.ui.spinBox_playerCut4_apartmentHeist.setValue(apartmentHeistCut[3])
            self.ui.spinBox_playerCut1_doomsdayHeist.setValue(doomsdayHeistCut[0])
            self.ui.spinBox_playerCut2_doomsdayHeist.setValue(doomsdayHeistCut[1])
            self.ui.spinBox_playerCut3_doomsdayHeist.setValue(doomsdayHeistCut[2])
            self.ui.spinBox_playerCut4_doomsdayHeist.setValue(doomsdayHeistCut[3])
            self.ui.spinBox_playerCut1_casinoHeist.setValue(casinoHeistCut[0])
            self.ui.spinBox_playerCut2_casinoHeist.setValue(casinoHeistCut[1])
            self.ui.spinBox_playerCut3_casinoHeist.setValue(casinoHeistCut[2])
            self.ui.spinBox_playerCut4_casinoHeist.setValue(casinoHeistCut[3])
            self.ui.spinBox_playerCut1_pericoHeist.setValue(pericoHeistCut[0])
            self.ui.spinBox_playerCut2_pericoHeist.setValue(pericoHeistCut[1])
            self.ui.spinBox_playerCut3_pericoHeist.setValue(pericoHeistCut[2])
            self.ui.spinBox_playerCut4_pericoHeist.setValue(pericoHeistCut[3])
        except:
            return None

    def write_cut(self):
        """改写分红"""
        try:
            apartmentHeist = (
                self.ui.spinBox_playerCut1_apartmentHeist.value(),
                self.ui.spinBox_playerCut2_apartmentHeist.value(),
                self.ui.spinBox_playerCut3_apartmentHeist.value(),
                self.ui.spinBox_playerCut4_apartmentHeist.value(),
            )
            doomsdayHeist = (
                self.ui.spinBox_playerCut1_doomsdayHeist.value(),
                self.ui.spinBox_playerCut2_doomsdayHeist.value(),
                self.ui.spinBox_playerCut3_doomsdayHeist.value(),
                self.ui.spinBox_playerCut4_doomsdayHeist.value(),
            )
            casinoHeist = (
                self.ui.spinBox_playerCut1_casinoHeist.value(),
                self.ui.spinBox_playerCut2_casinoHeist.value(),
                self.ui.spinBox_playerCut3_casinoHeist.value(),
                self.ui.spinBox_playerCut4_casinoHeist.value(),
            )
            pericoHeist = (
                self.ui.spinBox_playerCut1_pericoHeist.value(),
                self.ui.spinBox_playerCut2_pericoHeist.value(),
                self.ui.spinBox_playerCut3_pericoHeist.value(),
                self.ui.spinBox_playerCut4_pericoHeist.value(),
            )
            data = apartmentHeist + doomsdayHeist + casinoHeist + pericoHeist
            self.gtav.write_cut(data)
        except:
            self.signalMessage.emit("错误", "输入内容有误")
            return None

    def comboBox_weaponAmmoType_init(self):
        """子弹类型下拉框初始化"""
        self.ui.comboBox_weaponAmmoType.clear()
        for item in staticdata.weaponAmmoTypes:
            self.ui.comboBox_weaponAmmoType.addItem(item[0])

    def comboBox_vehicle_init(self):
        """载具下拉框初始化"""
        self.ui.comboBox_vehicles.clear()
        for item in staticdata.vehicles:
            self.ui.comboBox_vehicles.addItem(item[0])

    def comboBox_session_init(self):
        """战局下拉框初始化"""
        self.ui.comboBox_session.clear()
        for item in staticdata.sessions:
            self.ui.comboBox_session.addItem(item[0])

    def comboBox_weather_init(self):
        """天气初始化"""
        self.ui.comboBox_weather.clear()
        for item in staticdata.weather:
            self.ui.comboBox_weather.addItem(item[0])

    def comboBox_vehicleAbilities_init(self):
        """载具特殊能力下拉框初始化"""
        self.ui.comboBox_vehicleAbilities.clear()
        for item in staticdata.vehicleAbilities:
            self.ui.comboBox_vehicleAbilities.addItem(item[0])

    def change_vehicleAbility(self):
        """修改载特殊能力"""
        self.gtav.set_vehicleAbility(
            staticdata.vehicleAbilities[
                self.ui.comboBox_vehicleAbilities.currentIndex()
            ][1]
        )

    def kill_yourself(self):
        """自杀"""
        self.gtav.set_health(0.0)
        self.gtav.set_armor(0.0)

    def spawn_vehicle(self):
        """线上刷出载具"""
        self.gtav.spawn_vehicle(
            self.vehicles[self.ui.comboBox_vehicles.currentIndex()][1]
        )

    def repairing_vehicle(self):
        """修复载具"""
        self.threadPool.submit(self.gtav.vehicle.repairing_vehicle)

    def change_weaponAmmoType(self):
        """修改子弹类型"""
        self.gtav.set_weaponAmmoType(
            self.weaponAmmoTypes[self.ui.comboBox_weaponAmmoType.currentIndex()][1]
        )

    def change_weather(self):
        """修改天气"""
        self.gtav.set_weather(
            staticdata.weather[self.ui.comboBox_weather.currentIndex()][1]
        )

    def change_session(self):
        """切换战局"""
        self.gtav.change_session(
            self.sessions[self.ui.comboBox_session.currentIndex()][1]
        )

    def godmode(self, status: bool):
        """玩家无敌模式开关"""
        self.gtav.set_godMode(status)

    def indoor_spawn_vehicle(self):
        """室内刷出载具"""
        if self.ui.lineEdit_vehicleHash.text().strip():
            self.gtav.indoor_spawn_vehicle(
                int(self.ui.lineEdit_vehicleHash.text().strip(), base=16)
            )

    def outdoor_spawn_vehicle(self):
        """室外刷出载具"""
        if self.ui.lineEdit_vehicleHash.text().strip():
            self.gtav.outdoor_spawn_vehicle(
                int(self.ui.lineEdit_vehicleHash.text().strip(), base=16)
            )

    def stathax_started(self):
        self.ui.pushButton_statSubmit_text = self.ui.pushButton_statSubmit.text()
        self.ui.pushButton_statSubmit.setFlat(True)
        self.ui.pushButton_statSubmit.setEnabled(False)

    def stathax_finished(self):
        self.ui.pushButton_statSubmit.setText(self.ui.pushButton_statSubmit_text)
        self.ui.pushButton_statSubmit.setFlat(False)
        self.ui.pushButton_statSubmit.setEnabled(True)

    def stathax_starting(self):
        self.stathax.start(
            self.ui.textEdit_statText.toPlainText().replace("INT32", "", 1).strip()
        )

    def stathax_slot(self, text):
        self.ui.pushButton_statSubmit.setText(text)

    def continuous_teleportation(self):
        """持续传送敌人到指定位置"""
        while self.ui.checkBox_continuousTeleportation.isChecked():
            try:
                r = self.ui.tableView_teleport.currentIndex().row()
                (x, y, z) = (
                    float(self.model.item(r, 1).text()),
                    float(self.model.item(r, 2).text()),
                    float(self.model.item(r, 3).text()),
                )
            except:
                (x, y, z) = (0, 0, 100.0)
            self.gtav.teleport_enemy_npc((x, y, z))
            sleep(0.2)

    def autoCure(self):
        """恢复满血"""
        self.gtav.set_health(self.gtav.get_maxHealth)
        self.gtav.set_armor(self.gtav.get_maxArmor)

    # def closeEvent(self, a0: QCloseEvent):
    #     """关闭程序事件"""
    #     os._exit(0)

    def slotMessage(self, title: str, text: str):
        """消息弹窗"""
        QMessageBox.critical(self, title, text, QMessageBox.StandardButton.Ok)


if __name__ == "__main__":
    check_GTA5Cheat_is_running()
    app = QApplication(sys.argv)
    windowApp = WindowApp(Gtav())
    windowApp.show()
    sys.exit(app.exec())
