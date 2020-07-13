# Libraries
import RPi.GPIO as GPIO
import time

# GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)
SOUND_SPEED = 34300


class UltraSonicHandler:

    def __init__(self, pin_trig: int = 18, pin_echo: int = 23, max_distance: float = 100.0):
        self.pin_trig = pin_trig
        self.pin_echo = pin_echo
        self.setup_pins()
        self.max_wait_arrival = (max_distance * 2) / SOUND_SPEED

    def setup_pins(self):
        GPIO.setup(self.pin_trig, GPIO.OUT)
        GPIO.setup(self.pin_echo, GPIO.IN)

    def __call__(self) -> float:
        # set Trigger to HIGH
        GPIO.output(self.pin_trig, True)

        # set Trigger after 0.01ms to LOW
        time.sleep(0.01)
        GPIO.output(self.pin_trig, False)

        start = time.time()
        stop = start

        # save start
        while GPIO.input(self.pin_echo) == 0:
            start = time.time()

        # calculate how much we have to wait in the worst case scenario
        expected_arrival = time.time() + self.max_wait_arrival
        # save time of arrival
        while GPIO.input(self.pin_echo) == 1 and time.time() < expected_arrival:
            stop = time.time()

        # time difference between start and arrival
        elapsed = stop - start
        # multiply with the sonic speed (34300 cm/s)
        # and divide by 2, because there and back
        distance = (elapsed * SOUND_SPEED) / 2

        return distance


handler = UltraSonicHandler()

if __name__ == '__main__':
    try:
        while True:
            dist = handler()
            print("Measured Distance = %.1f cm" % dist)
            time.sleep(0.01)
            # print(handler.fsp)

        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()
