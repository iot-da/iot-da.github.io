# Networks and Protocols (NP1 + NP2) Final Programming Project

As a last exercise for the two subjects (NP1 and NP2) you will work in **teams
of 2 people** on a project that shows what you have learned from these topics.
You will develop (program) a system to monitor the amount of people in a room,
by detecting their smartphones, uploading the data to an external server for
analysis and visualization. In the following sections we describe what should be
covered for the two subjects.

## Requirements for NP1

Your system should manage a sensor network, formed by your ESP32 nodes. We assume
that you could have at least one node per room and that each room has a WiFi
access point reachable. In this context:

- Your nodes should be able to connect to the AP using WiFi, with WPA2-PSK
  security.

- Your nodes should provide a provissioning option, so that you can configure
  the wifi SSID to connect to. You can use a softAP or a BLE provisioning
  method, that is up to you.

- Your nodes should use BLE to compute the number of other BLE devices in its
  range (an estimation of the number of people in its range), using the RSSI to
  compute the distance to the node (the student should research for methods to
  compute the distance).

  	+ Alternatively the student can opt for using a different technology of his
	  choice to estimate the number of people in the room.

- The node should be configured through the menuconfig system, to establish its
  parameters:
  	+ Sampling period.
	+ Server where the samples should be sent to (see requirements for NP2).
	+ Range of valid distances.
	+ etc.

### Optional Parts for NP1

Optionally you can extend the project incorporating some extra features like the
following (these are only ideas, you can also propose some others):

- Consider an scenario with larger rooms, in which one node is not enough and
  the wifi AP is not reachable on all points. In this scenario you can use the
  ESP's wifi-mesh technology to build a mesh of nodes in the room.

- Study the Over The Air (OTA) features of ESP and prepare your nodes to receive
  OTA updates from an external server. Together with NP2 you can consider to
  configure the nodes to trigger the OTA update through MQTT (or any other
  application protocol you are using).

- Add a GATT server that allows the node parameters to be configured with a BLE
  client.

## Requirements for NP2

The developed system will periodically publish the calculated data for the 
population of BLE devices in the room, sending it to an external server for 
further storage and analysis. 

Specifically, the minimum requirements related with NP2 include:

- You will select an application-level protocol among those studied in NP2 
  (or, alternatively, other similar protocols of your interest) and use it 
  for data publishing.

- Servers/brokers to which data will be sent will be configured via `menuconfig`, 
  together with the sending period and any other configurable parameter 
  considered useful.

- You will select and use one of the two data representation methods studied in 
  the course (JSON or CBOR).

- Data will be gathered by Node-RED and submitted to two different destinations:
	+ A dashboard of your election (e.g. Node-RED, Grafana, ...).
	+ A database (e.g. MongoDB), where it will be stored together with a timestamp.

### Optional Parts for NP2

Optionally you can extend the project incorporating some extra features like the
following (these are only ideas, you can also propose some others):

- Use encryption at all levels of the communication (e.g. MQTT).

- Develop an alarm system that triggers under certain conditions (e.g. when the amount of 
  BLE devices is out of a pre-established range), and sends a notification to the user using
  external services (e.g. SMS, e-mail, Telegram, ...).

- Implement bi-directional communication, with the possibility of externally modifying the 
  behavior of the ESP32 (e.g. modifying sampling or sending period).
