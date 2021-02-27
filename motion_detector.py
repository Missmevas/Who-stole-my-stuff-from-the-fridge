import RPi.GPIO as GPIO
import time
import sys
from picamera import PiCamera
from time import sleep
import boto3

def calculate_avg(average_nr, average_sum):
    average_distance = round(average_sum/average_nr, 2)
    return average_distance

def get_readings():
    PIO.setup(PIN_TRIGGER, GPIO.OUT)
    GPIO.setup(PIN_ECHO, GPIO.IN)

    GPIO.output(PIN_TRIGGER, GPIO.LOW)

    sys.stdout.write("Waiting for sensor to settle\n")

    time.sleep(2)

    sys.stdout.write ("Calculating distance\n")

    GPIO.output(PIN_TRIGGER, GPIO.HIGH)

    time.sleep(0.001)

    GPIO.output(PIN_TRIGGER, GPIO.LOW)

    while GPIO.input(PIN_ECHO)==0:
        pulse_start_time = time.time()
    while GPIO.input(PIN_ECHO)==1:
        pulse_end_time = time.time()

    if pulse_end_time!=0 and pulse_start_time!=0:

        pulse_duration = pulse_end_time - pulse_start_time
        distance = round(pulse_duration * 17015, 2)
        
        return distance        
        
if __name__ == "__main__":
    camera = PiCamera() # initialize RPi Camera
    try:
        GPIO.setmode(GPIO.BOARD)
        PIN_TRIGGER = 11
        PIN_ECHO = 16
        detected_motion=0
        average_nr=10
        average_sum=0

        bucketname = 'bucket_name'
        s3 = boto3.resource('s3')

        sys.stdout.write("Configuration process ...\n")
        while detected_motion<10: # calculate the average of first 10 readings
            current_distance = get_readings
            average_sum+=current_distance
            print("Distance: ", get_readings(),"cm")

         
        average_distance = calculate_avg(average_nr, average_sum)
        print("Configuration finished. Average distance:", average_distance)   
        detected_motion=0
        camera.start_preview() 
        
        while detected_motion<5:
            
            print("Distance: ", get_readings(detected_motion),"cm")
                 
            if distance> average_distance+5 and distance<400:
                detected_motion+=1
                sleep(2)
                filename='/home/pi/Desktop/%s.jpg' % detected_motion #save picture on the disk
                camera.capture(filename) # capture a picture with connected camera
                s3.Bucket(bucketname).upload_file(Filename=filename, Key=filename) #upload picture to given S3 bucket
                
    finally:
        camera.stop_preview() #turn the camera off
        GPIO.cleanup()