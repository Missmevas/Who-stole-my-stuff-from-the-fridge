import paho.mqtt.client as mqtt

client = mqtt.Client()
client.username_pw_set("user","user") # authentification
client.connect("ec2(...).eu-west-2.compute.amazonaws.com",8883,60) #connect with EC2 instance on port 8883
msg = input("Enter your message:")
client.publish("message", msg); # publish the message typed by the user
client.disconnect(); #disconnect from server