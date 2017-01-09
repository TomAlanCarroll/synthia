from gpiozero import MotionSensor
i = 0
pir = MotionSensor(4)
while True:
    if pir.motion_detected:
        print("Motion detected! " + str(i))
	i = i + 1
