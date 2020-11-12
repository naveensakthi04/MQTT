import paho.mqtt.client as mqtt
import time

""" Defining all callback functions"""


def on_connect(client, userdata, flags, rc):
    print("Connected - rc: ", rc)


def on_message(client, userdata, message):
    global FLAG
    global chat
    try:
        if str(message.topic) != publish_topic:
            msg = str(message.payload.decode("utf-8"))
            print(str(message.topic), msg)
            if msg.strip().lower() == "stop":
                FLAG = False
            else:
                chat = input("Enter message: ")
                client.publish(publish_topic, chat)
    except Exception:
        pass


def on_subscribe(client, userdata, mid, granted_qos):
    print("Subscribed: ", str(mid), str(granted_qos))


def on_unsubscribe(client, userdata, mid):
    print("Unsubscribed: ", str(mid))


def on_disconnect(client, userdata,
                  rc):  # rc = disconnections state, if rc == 0, disconnection successful, else unexpected disconnection
    if rc != 0:
        print("Unexpected disconnection")


broker_address = "mqtt.eclipse.org"
port = 1883

client = mqtt.Client()
client.on_unsubscribe = on_unsubscribe
client.on_subscribe = on_subscribe
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message

client.connect(broker_address, port)

time.sleep(1)

publish_topic = "/chat/client2"
subscribe_topic = "/chat/client1"

FLAG = True

client.loop_start()
client.subscribe(subscribe_topic)

chat = None
# time.sleep(1)
# chat = input("Enter message: ")
# client.publish(publish_topic, chat)
while True:
    try:
        if FLAG == False or chat.strip().lower() == "stop":
            break
    except Exception:
        pass
client.disconnect()
client.loop_stop()
