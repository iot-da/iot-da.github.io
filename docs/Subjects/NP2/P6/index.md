# Laboratory 4. MQTT (I). Deployment of clients and servers/brokers. Traffic analysis

## Objectives

* To familiarize with the use of brokers and clients for subscription/publication using MQTT.

* To deploy a system based on MQTT locally, including broker and clients.

* To use Eclipse Paho to integrate functionality for MQTT in Python programs.

* To familiarize with the use of MQTT wildcards.

## Publication/subscription on a broker in the cloud

In this first part, we will use a server/broker available in the cloud for its use
from users (*test.mosquitto.org*). 
This server is usually employed for testing and debugging, and you need to realize that
all the information published on it can be read by any subscriptor. Take this into account
when publishing important information via MQTT.

The server listens on the following ports:


* **1883**: MQTT, no encryption.
* **8883**: MQTT, with encryption.
* **8884**: MQTT, with encryption, user certificate required.
* **8080**: MQTT over WebSockets, without encryption.
* **8081**: MQTT over WebSockets, with encryption.

In order to perform publications/subscriptions on the broker, we will use
the [*mosquitto*](https://mosquitto.org) distribution from the Eclipse IoT projecto.
Even thourgh *mosquitto* is mainly an implementation of an MQTT broker, we will use it in this
step as a client; this will allow us to subscribe or publish on any MQTT topic.

First, install *mosquitto*:

```sh
sudo apt-get install mosquitto mosquitto-clients mosquitto-dev libmosquitto*
```

Provided there were no errors, you will find two binaries ready for execution:

* `mosquitto_sub`: to subscribe to a given topic via a broker.
* `mosquitto_pub`: to publish a message associated to a given topic via a  broker.

!!! note "Task"
    Observe the help of both commands, using the argument `--help`. Identify  
    the parameters that allow specifying the destination broker, the topic to use and, when publishing
    the message to send.

Let us subscribe to the topic `#` in the broker, using the order:

```sh
mosquitto_sub -h test.mosquitto.org  -t "#"
```

!!! note "Task"
    Pause the output (Ctrl+C) as soon as you can. What are the messages you are observing?

Next, we will complete a process of publication/subscription with a known topic (e.g. 
`/MIOT/yourname/`). In order to publish a message under this topic:

```sh
mosquitto_pub -h test.mosquitto.org -t "/MIOT/tunombre" -m "Hola, soy tunombre"
```

!!! note "Task"
    Subscribe to the topic `/MIOT/yourname` and observe if you can receive the results
    after the corresponding publication. How could you subscribe to all messages published
    by your classmates?

!!! danger "Task"
    Perform an analysis of the message excghanges necessary for a process of 
    publication/subscription on the test broker. Study the type of protocol
    of the transport layer that is used by MQTT, data and control messages, protocol
    overhead and, in general, any aspect that you consider of interest.

## Deploying a local broker using Eclipse Mosquitto

The use of a remote server presents advantages (ease of use), but a series of 
inconvenients (security, lack of configuration mechanisms, ...).

In this section, we will configure a *mosquitto* borker to deploy a local
MQTT infrastructure under our control.

Booting a broker (server) in mosquitto is performed via the command `mosquitto`:

```sh
mosquitto [-c config file] [ -d | --daemon ] [-p port number] [-v]
```

However, in many Linux distributions, the broker boots by default on system boot, 
and it is executed continously in background. In order to check the status of 
the broker, you can execute:

```sh
sudo service mosquitto status
```

You will observe a message that indicates that the service is active. The options
`restart`, `start` or `stop` will allow you to control the status of the broker.

!!! note "Task"
    Check that, with the broker online, you can perform a subscription/publication
    process on it.

The mosquitto broker allows a monitorization of statistics and information of its
status using the MQTT protocol. Hence, the topics `$SYS` return, periodically
or when an event occurs, the information of the status of the broker. You can
query more details in the manual page of *mosquitto*
(command `man mosquitto`), under the section *BROKER STATUS*.

!!! note "Task"
    Query the status of the broker while you perform subscription/publication processes,
    reporting received/sent bytes, number of active/inactive connections, and number of 
    sent/received bytes by the broker.

## Developing a local client using Eclipse Paho

The clients `mosquitto_pub` and `mosquitto_sub` are bsically tools for development and
testing, but it is interesting to know libraries that allow the integration
of MQTT into existing programs. One of them is [Eclipse Paho](https://www.eclipse.org/paho). 
Paho is an infrastructure devleloped by the Eclipse IoT project to support implementations
of protocols of instant messaging (M2M and IoT), even though as of today, it is exclusively
focused on MQTT.

In our case, we will use the Python version of the library, that can be installed via:

```sh
pip install paho-mqtt
```

All documentation for the module is available via [this link](https://pypi.org/project/paho-mqtt/#usage-and-api).

The deployment of simple example for a client that connects to a broker and subscribes to the
`$SYS` topic, printing all received messages, would result, using Paho from Python, in:

```python
import paho.mqtt.client as mqtt

# Callback function invoked qhen the client receives a CONNACK from the broker.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribin in on_connect() makes sure that if connection is lost and restablished,
    # the subscription will be renewed
    client.subscribe("$SYS/#")

# Callback function upon publication message reception (PUBLISH) from the broker.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("mqtt.eclipse.org", 1883, 60)

# Blocking call that processes network traffic, invokes callbacks and handles broker reconnections.
client.loop_forever()
```

The client class can be used to:

* Create an instance of an MQTT client.
* Connect to a *broker* using the functions of the `connect*()` family.
* Invoke functions of the `loop*()` family to maintain data traffic with the server.
* Use `subscribe()` to subscribe to a topic or receiving messages.
* Use `publish()` to publish messages in the broker.
* Use `disconnect()` to disconnect from the broker.

The callbacks will be invoked automatically to allow processing events. Among other, we highlight:

* `ON_CONNECT`: invoked when the broker responds to our connection request. Example:
```python
def on_connect(client, userdata, flags, rc):
    print("Connection returned result: "+connack_string(rc))
```

* `ON_DISCONNECT`: invoked when the client disconnects from the broker. Example:
```python
def on_disconnect(client, userdata, rc):
    if rc != 0:
        print("Unexpected disconnection.")
```

* `ON_MESSAGE`: invoked when a message on a topic is received and the client is subscribed:
Example:
```python
def on_message(client, userdata, message):
    print("Received message '" + str(message.payload) + "' on topic '"
        + message.topic + "' with QoS " + str(message.qos))
```

In order to publish on a punctual manner on a broker (without keeping a connection
open), it is possible to use the following sequence of orders:

```python
import paho.mqtt.publish as publish

publish.single("paho/test/single", "payload", hostname="mqtt.eclipse.org")
```

Similarly, we can subscribe only to a topic with a blocking call as:

```python
import paho.mqtt.subscribe as subscribe

msg = subscribe.simple("paho/test/simple", hostname="mqtt.eclipse.org")
print("%s %s" % (msg.topic, msg.payload))
```

All the information and documentation for the module can be found [here](https://pypi.org/project/paho-mqtt/).

### Wildcards

In addition of using complete topics for the subscription process, topics can include wildcards
in their structure. 
`+` is the wildcard used to obtain correspondences with a unique level of the hierarchy. Hence
for a topic `a/b/c/d`, the following subscriptions would match:

* `a/b/c/d`
* `+/b/c/d`
* `a/+/c/d`
* `a/+/+/d`
* `+/+/+/+`

But not the following:

* `a/b/c`
* `b/+/c/d`
* `+/+/+`

The second wildcard supported is `#`, and permits matchings on any successive level of the 
hierarchy. Hence for a topic `a/b/c/d`, the following subscriptions would match:

* `a/b/c/d`
* `#`
* `a/#`
* `a/b/#`
* `a/b/c/#`
* `+/b/c/#`

!!! danger "Task"
    Each student will propose a solution to monitor traffic on an intelligent building
    via MQTT. For that, the building will be composed by:

    * An identifier: `BUILDING_NAME`.
    * A set of floors, identified by the string `P_NUMFLOOR`.
    * For each plant, four wings (north -N-, south -S-, east -E-, west -O-)
    * At each wing, a set of rooms, identified by a numeric value.
    * For each room, four sensors: TEMP (temperature), HUM (humidity), LUX (luminosity), VIBR (vibration).
    
    First, design the hierarcy of topics that allows a correct monitorization of the buildings.

    Second, you will develop a Python client that publishes, periodically and in a random manner,
    JSON objects (optionally, you can use CBOR) that include values for temperature, humidity, luminosity
    or vibration for a specific room of the building, also chosen randomly, via a topic. These messages
    will be  separated in time a random number of seconds.
 
    Third, define the wildcards that allow querying for different types of information in a hierarchical
    fashion. For example:

    * All messages of temperature for the building.
    * All messages of vibration for the west wing of the second floor of the building.
    * All sensorization messages for the room number 4 of the south wing of floor 7 in the building.
    * ...

    Last, develop a Python program that acts as an alarm, and that shows on screen messages only if a 
    received value is above a pre-established threshold. In that case, the program will show
    the building, floor, wing, room and sensor that produced the alarm, together with its numeric value.

    You can use the  [JSON module](https://docs.python.org/3/library/json.html)
    to parse the receive objects.
