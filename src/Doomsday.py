from time import sleep
from KeySend import keydown, keyup, keypress

# 0x29  # ` on ANSI keyboards (ISO key is overridden in CRDKeyboard)
# 0x29	# ^ on ISO keyboards
# 0x02  # 1
# 0x03  # 2
# 0x04  # 3
# 0x05  # 4
# 0x06  # 5
# 0x07  # 6
# 0x08  # 7
# 0x09  # 8
# 0x0A  # 9
# 0x0B  # 0
# 0x0C  # -
# 0x0D  # =
# 0x0F  # Tab
# 0x10  # Q
# 0x11  # W
# 0x12  # E
# 0x13  # R
# 0x14  # T
# 0x15  # Y
# 0x16  # U
# 0x17  # I
# 0x18  # O
# 0x19  # P
# 0x1A  # [
# 0x1B  # ]
# 0x1E  # A
# 0x1F  # S
# 0x20  # D
# 0x21  # F
# 0x22  # G
# 0x23  # H
# 0x24  # J
# 0x25  # K
# 0x26  # L
# 0x27  # ;
# 0x28  # '
# 0x2B  # \
# 0x2C  # Z
# 0x2D  # X
# 0x2E  # C
# 0x2F  # V
# 0x30  # B
# 0x31  # N
# 0x32  # M
# 0x33  # ,
# 0x34  # .
# 0x35  # /

# Non-printing keys.

# F-keys
# 0x3b	# f1
# 0x3c	# f2
# 0x3d	# f3
# 0x3e	# f4
# 0x3f	# f5
# 0x40	# f6
# 0x41	# f7
# 0x42	# f8
# 0x43	# f9
# 0x44	# f10
# 0x57	# f11
# 0x58	# f12
# 0x46	# Scroll lock (f15)

# Print Screen and Pause/Break is hardcoded in CRDKeyboard

# Misc keys
# 0x01	# esc
# 0x1c	# return
# 0x1c	# enter
# 0x39	# space

# Right group
# 0xd2	# insert
# 0xd3	# delete
# 0x0e	# backspace
# 0xcb	# left arrow
# 0xcd	# right arrow
# 0xc8	# up arrow
# 0xd0	# down arrow
# 0xc7	# home
# 0xcf	# end
# 0xc9	# page up
# 0xd1	# page down

# Numpad
# 0x45	# Numlock toggle, using 'clear' button
# 0xd	# Numeric =, just use normal equals
# 0xb5	# Numeric /
# 0x37	# Numeric *
# 0x4a	# Numeric -
# 0x4e	# Numeric +
# 0x53	# Numeric .
# 0x52	# Numeric 0
# 0x4f	# Numeric 1
# 0x50	# Numeric 2
# 0x51	# Numeric 3
# 0x4b	# Numeric 4
# 0x4c	# Numeric 5
# 0x4d	# Numeric 6
# 0x47	# Numeric 7
# 0x48	# Numeric 8
# 0x49	# Numeric 9
# 0x9c	# Numeric enter


W = 0x11
A = 0x1E
S = 0x1F
D = 0x20
Space = 0x39


class Doomsday:
    """末日豪劫按键精灵"""
    def mission_1(self):
        pass

    def mission_2(self):
        keydown(Space)
        sleep(0.03)
        keydown(D)
        sleep(0.03)
        keyup(Space)
        sleep(0.03)
        keyup(D)

    def mission_3(self):
        keydown(Space)
        sleep(0.1)
        keydown(S)
        sleep(0.03)
        keydown(D)
        sleep(0.03)
        keyup(Space)
        sleep(0.03)
        keyup(D)
        sleep(0.03)
        keyup(S)

    def start(self, mission: int):
        sleep(0.5)
        if mission == 1:
            self.mission_1()
        elif mission == 2:
            self.mission_2()
        elif mission == 3:
            self.mission_3()
