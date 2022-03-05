# Laboratory 4. MQTT (II). Client deployments on the ESP32

## Objectives

* To get familiar with the MQTT component in ESP-IDF.

* To deploy a complete MQTT client on the ESP32, including routines for publication and subscription.

* To implement QoS and LWT on the ESP32.

## The MQTT component in ESP-IDF

The ESP-MQTT component is an implementation of the MQTT protocol (in its
client part), that allows the implementation of complete MQTT clients on the
ESP32, including routines for publication and subscription to brokers.

The component supports MQTT over TCP by default, and advanced functionalities
such as SSL/TLS support or MQTT over Websockets. In addition, it allows the
deployment of multiple instances of MQTT clients on the same boar; the component
implements advanced parameters supported by MQTT, such as authentication
(using username and password), *last will* messages and three
levels of QoS.

### Events

As other components, the interactiin between the MQTT client and the application
is based on the reception and treatment of events, being the most important:

* `MQTT_EVENT_BEFORE_CONNECT`: The client has been initialized and is about to
commence the connection process with the remote broker.
* `MQTT_EVENT_CONNECTED`: The client has successfully established a connection with the
broker and it is ready to send and receive data.
* `MQTT_EVENT_DISCONNECTED`: The client has aborted the connection.
* `MQTT_EVENT_SUBSCRIBED`: The broker has confirmed the request for subscription from the client.
Data will contain the ID of the subscription message.
* `MQTT_EVENT_UNSUBSCRIBED`: The broker confirms the request of desubsuscription from the client. 
Data will contain the ID of the desubscription message.
* `MQTT_EVENT_PUBLISHED`: The broker has sent an ACK for the reception of a message
previously published by a client. This event will only be produced when QoS is
1 or 2, as the level 0 for QoS does not use ACKs. Data associated with the event will contain
the ID of the published message.
* `MQTT_EVENT_DATA`: The client has received a message published by the broker. Data associated
to the event will contain the ID of the message, name of the topic and received data (an its length).

### API

* `esp_mqtt_client_handle_t esp_mqtt_client_init(const esp_mqtt_client_config_t *config)`

Initialization routine for the MQTT client. It returns a connection handler, or NULL in case of error.
The `config` paramter is a structure with the parameters that will rule the connection, being 
the most important
(see [the component documentation](https://docs.espressif.com/projects/esp-idf/en/latest/esp32/api-reference/protocols/mqtt.html#_CPPv424esp_mqtt_client_config_t)
for additional parameters):

  - `esp_event_loop_handle_t event_loop_handle`: hanlder for MQTT events.
  - `const char *uri`: URI of the MQTT *broker*.
  - `uint32_t port`: port of the MQTT *broker*.
  - `const char *username`: username, in case it is supported by the broker.
  - `const char *password`: password, in case it is supported by the broker.
  - `const char *lwt_topic`: topic of the LWT message (*Last Will and Testament*).
  - `const char *lwt_msg`: contents of the LWT message.
  - `int lwt_qos`: QoS of the LWT message.
  - `int lwt_retain`: flag *retain* for the LWT message.
  - `int lwt_msg_len`: length of the LWT message.
  - `int keepalive`: value for the *keepalive* timer (by default 120 seconds).

* `esp_err_t esp_mqtt_client_start(esp_mqtt_client_handle_t client)`

Boot routine for the MQTT client. Its only parameter is the handler returned by the previous routine.

* `int esp_mqtt_client_subscribe(esp_mqtt_client_handle_t client, const char *topic, int qos)`

Subscribes the client to a topic with a given QoS via the third parameter. The client must
be connected to the broker to send the subscription message.

* `int esp_mqtt_client_unsubscribe(esp_mqtt_client_handle_t client, const char *topic)`

*Desubscribes* the client from a given topic. The client must be connected to the 
broker to send the corresponding message.

* `int esp_mqtt_client_publish(esp_mqtt_client_handle_t client, const char *topic, const char *data, int len, int qos, int retain)`

The client publishes a message on the broker. The client does not need to be connected
to the broker to send the publication message. In that case, if 
`qos=0`, messages will be discarded,  
and if `qos>=1`, messages will be queued waiting to be sent.
The routine returs the identifier of the published message (if `qos=0`, the return value will be always 0)
or `-1` in case of error.

Parameters of interest:

  - `client`: MQTT client handler.
  - `topic`: topic (as a string) under whigh the message will be published.
  - `data`: contents of the message to publish (it is possible to publish a message withouth contents if `NULL` is used).
  - `len`: lenght, in bytes, of the data to send. If `0` is provided, it is calculated based on the length of the `data` string.
  - `qos`: desired QoS level.
  - `retain`: flag *Retain*.

!!! note "Task"
    Analyze the example `examples/protocols/mqtt/tcp`, and configure it so that
    it uses as a broker the mosquitto broker you deployed in your Virtual Machine
    (first, make sure that both the Virtual Machine and the ESP32 belong to the same network).
    
    Perform tests for publication and subscription in the Virtual Machine that 
    allow you to visualize the messages published by the ESP32 in your terminal,
    and the messages published from the terminal in the monitor output of the 
    ESP32.

    Modify the example and analyze the generated traffic (via Wireshark)
    for the following cases:

    1. Publication of messages with QoS levels 0, 1 and 2. 
    2. Activation and deactivatio of the *retain* flag in the publication from the ESP32.
    3. Configuration of a LWT message with the topic */disconnected*. For that,
    reduce the valua of *keepalive* to 10 seconds, so that the detection of a 
    disconnection is faster. You should observe the submission of a message
    with the selected topic upon the timer expiration, starting from a forced
    disconnection of the ESP32 (you will need to be subscribed to it from Linux).

!!! danger "Task"
    Modify the example so that it is integrated in your building monitoring
    and alarm system. The firmware will proceed by creating a task that, periodically
    (every *interval* seconds) publishes a random value for the four monitored values.

    In addition, you will need to design a system based on MQTT so that you can control,
    externally, the behavior of the sensor, attending to:

    1. The time (*interval*) that will pass between publications will be configurable via
    a message published from your terminal, to which the ESP32 will be subscribed.
    2. The sensorization (and data publicaiton) will be activated or deactivated on demand, 
    via a publication from your Linux terminal and subscription from the ESP32 to a specific topic.

    For example, imagine that your sensor publishes messages under the topic
    `/BUILDING_3/P_4/N/12/(TEMP|HUM|LUX|VIBR)`. To control the interval of 
    publication time from that ESP32, and fix it to 1 second, we could publish a 
    message using:

    `mosquitto_pub -t /BUILDING_3/P_4/N/12/interval` -m "1000" -h IP_BROKER

    To disable the sensor:

    `mosquitto_pub -t /BUILDING_3/P_4/N/12/disable` -m "" -h IP_BROKER

    To enable the sensor:

    `mosquitto_pub -t /BUILDING_3/P_4/N/12/enable` -m "" -h IP_BROKER

    3. Optionally, you can extend your solution so that each sensor is activated or deactivated
    individually on demand. For that to happen, choose and document the selected topic that you 
    should employ.
