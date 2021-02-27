import paho.mqtt.client as mqtt 

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc)) #notify about established connection
    client.subscribe("message")

def on_message(client, userdata, msg):
    print("Your message:" + str(msg.payload)) #display received message
    client.disconnect()

client = mqtt.Client() 

''' replace with username for authentification '''
client.username_pw_set("user","user") 

''' connect with EC2 instance through encrypted port 8883 '''
client.connect("ec2(...).eu-west-2.compute.amazonaws.com", 8883, 60)

client.on_connect = on_connect
client.on_message = on_message
client.loop_forever() #do not disconnect