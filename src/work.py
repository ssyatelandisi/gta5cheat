from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from gtav import Gtav, Doomsday
from ui_app import Ui_App
import staticdata


class WorkSuspendProcess(QThread):
    def __init__(self, parent, gtav: Gtav):
        super().__init__(parent)
        self.gtav = gtav

    def run(self):
        self.gtav.suspend_process()


class WorkLuckyWheel(QThread):
    def __init__(self, parent, gtav: Gtav):
        super().__init__(parent)
        self.gtav = gtav

    def run(self):
        while True:
            self.gtav.set_luckyWheel(18) #18: 展台载具
            QThread.msleep(100)


class WorkStatHax(QThread):
    signalSet_statSubmit_text = pyqtSignal(str)
    signalStarted = pyqtSignal()
    signalFinished = pyqtSignal()

    def __init__(self, parent, ui: Ui_App, gtav: Gtav):
        super().__init__(parent)
        self.ui = ui
        self.gtav = gtav
        self.defaultContent = self.ui.pushButton_statSubmit.text()

    def run(self):
        if self.ui.textEdit_statText.toPlainText() == "":
            return
        else:
            rows = (
                self.ui.textEdit_statText.toPlainText()
                .strip()
                .replace("INT32\n", "", 1)
                .split("\n")
            )
            self.signalStarted.emit()
            for i in range(len(rows)):
                if i % 2 == 0:
                    self.signalSet_statSubmit_text.emit(
                        str(i // 2 + 1) + "/" + str(len(rows) // 2)
                    )
                else:
                    try:
                        self.gtav.stat_write(
                            rows[i - 1].strip().replace("$", "", 1), rows[i].strip()
                        )
                        QThread.sleep(1)
                    except Exception as e:
                        print(e)
            self.signalSet_statSubmit_text.emit(self.defaultContent)
            self.signalFinished.emit()


class WorkCheckBoxWatch(QThread):
    def __init__(self, parent, ui: Ui_App, model: QStandardItemModel, gtav: Gtav):
        super().__init__(parent)
        self.ui = ui
        self.gtav = gtav
        self.model = model

    def run(self):
        while True:
            self.gtav.set_godMode(self.ui.checkBox_godMode.isChecked())
            self.gtav.antiAFK(self.ui.checkBox_antiAFK.isChecked())
            self.gtav.set_seatbelt(self.ui.checkBox_seatbelt.isChecked())
            if self.ui.checkBox_continuousTeleportation.isChecked():
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
            if self.ui.checkBox_autoCure.isChecked():
                self.gtav.set_health(self.gtav.get_maxHealth())
                self.gtav.set_armor(self.gtav.get_maxArmor())
            QThread.msleep(250)


class WorkHotkey(QThread):
    signalDuu = pyqtSignal()
    signalDi = pyqtSignal()
    doomsday = Doomsday()

    def __init__(self, parent, ui: Ui_App, gtav: Gtav):
        super().__init__(parent)
        self.hotkeyPool = dict()
        self.ui = ui
        self.gtav = gtav

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
            code = self.gtav.keyboard_watch()
            if code == 0x1131:  # LCTRL+1
                self.doomsday.mission(2)
                self.signalDuu.emit()
                QThread.msleep(150)
            elif code == 0x1132:  # LCTRL+2
                self.doomsday.mission(3)
                self.signalDuu.emit()
                QThread.msleep(150)
            elif code == 0x1152:  # LCTRL+R
                self.ui.pushButton_fillCurrentAmmo.click()
                QThread.msleep(150)
            elif code == 0x112E:  # LCTRL+DEL
                self.ui.pushButton_killYourself.click()
                QThread.msleep(150)
            elif code == 0x70:  # F1
                if self.ui.checkBox_killGTA.isChecked():
                    self.gtav.kill_process()
                    self.signalDuu.emit()
                    QThread.msleep(150)
            elif code == 0x72:  # F3
                self.ui.pushButton_moveForward.click()
                QThread.msleep(150)
            elif code == 0x73:  # F4
                self.ui.pushButton_teleportToWaypoint.click()
                QThread.msleep(150)
            elif code == 0x74:  # F5
                self.ui.pushButton_teleportToObjective.click()
                QThread.msleep(150)
            elif code == 0x75:  # F6
                self.parent().change_vehicleAbility()
                self.signalDuu.emit()
                QThread.msleep(150)
            elif code == 0x1176:  # LCTRL+F7
                self.ui.checkBox_godMode.setChecked(False)
                QThread.msleep(150)
            elif code == 0x76:  # F7
                self.ui.checkBox_godMode.setChecked(True)
                QThread.msleep(150)
            elif code == 0x77:  # F8
                self.ui.pushButton_noCops.click()
                QThread.msleep(150)
            elif code == 0x1178:  # LCTRL+F9
                self.ui.pushButton_vehicleRepairing.click()
                QThread.msleep(150)
            elif code == 0x117A:  # LCTRL+F11
                self.gtav.change_session(
                    staticdata.sessions[self.ui.comboBox_session.currentIndex()][1]
                )
                self.signalDuu.emit()
                QThread.msleep(150)
            elif code == 0x11C0:  # LCTRL+~
                self.gtav.spawn_vehicle(
                    self.gtav.joaat(
                        staticdata.vehicles[self.ui.comboBox_vehicles.currentIndex()][1]
                    )
                )
                self.signalDuu.emit()
                QThread.msleep(150)
            elif code == 0x6F:  # /
                self.ui.pushButton_killEnemyNPC.click()
                QThread.msleep(150)
            elif code == 0x6A:  # *
                self.ui.pushButton_destroyEnemyVehicles.click
                QThread.msleep(150)
            else:
                QThread.msleep(50)
