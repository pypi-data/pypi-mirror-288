import math
import numpy as np

from genlib.ican import InetCAN


class Driving:
    """
    Forwarding standard:
        FRONT_LIGHT, FRONT_RIGHT, LEFT
        
      1)   /-----\   2)
          /   F   \
          |       |  
          \   R   /  
           \...../   
              3)
    """

    ID_DRIVING = 0x010

    THROTTLE_0POINT = 100
    WHEEL_POS_LEFT = 0x01
    WHEEL_POS_RIGHT = 0x02
    WHEEL_POS_REAR = 0x04
    WHEEL_POS_ALL = WHEEL_POS_LEFT | WHEEL_POS_RIGHT | WHEEL_POS_REAR
    SPIN_RIGHT = 0x01
    SPIN_LEFT = 0x02

    def __init__(self, ip=None):
        self.__ican = InetCAN("127.0.0.1", "") if ip is None else InetCAN(ip, "")
        self.__angle = 0
        self.__steering = 0.0
        self.__throttle = 0
        self.__wheel_pos = self.WHEEL_POS_ALL
        self.__spin = None
        self.stop()

    def __calculate_omni_wheel(self):
        if self.__spin:
            offset = np.sign(self.__throttle) * 7

            if self.__spin == self.SPIN_RIGHT:
                for i in range(3):
                    self.__wheel_vec[i] = self.THROTTLE_0POINT - round(
                        (self.throttle + offset) * 0.935
                    )
            elif self.__spin == self.SPIN_LEFT:
                for i in range(3):
                    self.__wheel_vec[i] = Driving.THROTTLE_0POINT + round(
                        (self.throttle + offset) * 0.935
                    )
        else:
            offset = np.sign(self.__throttle) * 25

            if (self.__angle == 0) or (self.__angle == 180):
                weight = (self.__throttle + offset) * 0.92  # 1.15 * 100 / 125
            else:
                weight = (self.__throttle + offset) * 0.8  # 100 / 125

            Vx = 1 * math.sin(math.radians(self.__angle)) * weight
            Vy = math.cos(math.radians(self.__angle)) * weight

            self.__wheel_vec[0] = Driving.THROTTLE_0POINT - round(
                (1 / 2) * Vx + (math.sqrt(3) / 2) * Vy
            )
            self.__wheel_vec[1] = Driving.THROTTLE_0POINT - round(
                (1 / 2) * Vx - (math.sqrt(3) / 2) * Vy
            )
            self.__wheel_vec[2] = Driving.THROTTLE_0POINT - round(-1 * Vx)

    def __transfer(self):
        self.__ican.write(
            Driving.ID_DRIVING, [self.WHEEL_POS_ALL] + self.__wheel_vec, False
        )

    def move(self, angle, throttle=None):
        if throttle is not None:
            self.__throttle = throttle

        if not (self.__angle == 0) or (self.__angle == 180):
            assert abs(self.__throttle) >= 20, "Throttle must be >= 20 "

        self.__angle = angle
        self.__spin = None

        self.__calculate_omni_wheel()
        self.__transfer()

        return self.__wheel_vec

    def spinRight(self, throttle=None):
        if throttle:
            self.__throttle = throttle

        self.__spin = self.SPIN_RIGHT

        self.__calculate_omni_wheel()
        self.__transfer()

    def spinLeft(self, throttle=None):
        if throttle:
            self.__throttle = throttle

        self.__spin = self.SPIN_LEFT

        self.__calculate_omni_wheel()
        self.__transfer()

    def stop(self):
        self.__wheel_vec = [
            self.THROTTLE_0POINT,
            self.THROTTLE_0POINT,
            self.THROTTLE_0POINT,
        ]
        self.__transfer()

    @property
    def throttle(self):
        return self.__throttle

    @throttle.setter
    def throttle(self, throttle):
        if self.__throttle == throttle:
            return

        self.__throttle = throttle
        self.__transfer()

    def steering(self, angle, throttle):
        if self.__angle == angle and self.__throttle == throttle:
            return

        rad_angle = math.radians(angle)
        wheel_angle_offset = math.radians(120)

        wheel0 = round(
            throttle * (math.cos(rad_angle) + math.sin(rad_angle) / math.sqrt(3))
        )
        wheel1 = round(
            throttle
            * (
                math.cos(rad_angle + wheel_angle_offset)
                + math.sin(rad_angle + wheel_angle_offset) / math.sqrt(3)
            )
        )
        wheel2 = round(
            throttle
            * (
                math.cos(rad_angle - wheel_angle_offset)
                + math.sin(rad_angle - wheel_angle_offset) / math.sqrt(3)
            )
        )

        self.__wheel_vec[0] = Driving.THROTTLE_0POINT + wheel0
        self.__wheel_vec[1] = Driving.THROTTLE_0POINT + wheel1
        self.__wheel_vec[2] = Driving.THROTTLE_0POINT + wheel2
        self.__transfer()

        return self.__wheel_vec

    def forward(self, throttle=None):
        self.move(0, throttle)

    def backward(self, throttle=None):
        self.move(180, throttle)
