import Wi_Fi
import pressure_sensor
from force_sensor import read_moment
import speed_sensor
import machine
from mqtt import MQTTClient
from time import sleep, sleep_ms
from motor_control import motor

#Connect to Wi-Fi
try:
    Wi_Fi.connect()
except KeyboardInterrupt:
    machine.reset()

#MQTT credentials
AIO_SERVER = "io.adafruit.com"
AIO_PORT = 1883
AIO_USER = "user_name"
AIO_KEY = "xxxxxxxxxxxxxxxxxxxxx"
AIO_CLIENT_ID = "Master pico"
AIO_ANGULAR_SPEED_FEED = "user_name/feeds/angular-speed"
AIO_PRESSURE_FEED = "user_name/feeds/pressure"
AIO_MOTOR_TORQUE_FEED = "user_name/feeds/torque"
AIO_COMPRESSOR_TORQUE_FEED = "user_name/feeds/compressor-shaft"
AIO_OUTER_RING_TORQUE_FEED = "user_name/feeds/outer-ring"

#Initilize MQTT client
client = MQTTClient(AIO_CLIENT_ID, AIO_SERVER, port=AIO_PORT, user=AIO_USER, password=AIO_KEY)

#Connect to server
client.connect()

#Initilize pressure sensor
psensor = pressure_sensor.SparkFunMicroPressure()

#Initilize speed sensor
ssensor = speed_sensor.AngularSpeedSensor(27)

#Initilize index
k = 1

# Initilize maximum allowed pressure
max_pressure = 150000 #Pascals

#Start motor
m1 = motor(pwmPin = 0, dirPin = 1)
for i in range(1,11):
    m1.drive(speed = 0-i, duration_ms = 100)
while True:
    m1.speed(-10)
    sleep(1)
    
    #Print index
    print(k)
    k = k + 1
    
    #Read values and publish
    M1, Mc, M2 = read_moment()
    print("Motor shaft:\t", M1)
    print("Compressor shaft:\t", Mc)
    print("Outer ring:\t", M2)
    client.publish(topic=AIO_MOTOR_TORQUE_FEED, msg=str(M1))
    sleep(1)
    client.publish(topic=AIO_COMPRESSOR_TORQUE_FEED, msg=str(Mc))
    sleep(1)
    client.publish(topic=AIO_OUTER_RING_TORQUE_FEED, msg=str(M2))
    sleep(1)
    
    pressure_value = psensor.read_pressure()
    print("Pressure:\t", pressure_value)
    client.publish(topic=AIO_PRESSURE_FEED, msg=str(pressure_value))
    sleep(1)
    
    angular_speed_value = ssensor.read_angular_speed()
    print("Angular speed:\t", angular_speed_value)
    client.publish(topic=AIO_ANGULAR_SPEED_FEED, msg=str(angular_speed_value))
    
    print("-----------")
    
    #When the pressure exceedes max_pressure
    if pressure_value > max_pressure:
        break
    
for i in range(1,11):
    m1.drive(speed = -10+i, duration_ms = 100)
