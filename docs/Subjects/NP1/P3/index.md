# Lab 3. WiFi. Advanced Concepts (WiFi Mesh, provisioning and low power mode)

## Goals

This lab assignment is divided into three main parts, that address
three advanced topics related to WiFi. The goals for each of these parts are the
following:

* WiFi MESH
    - Review the basic concepts for building a self-managed WiFi Mesh network.
    - Present the basic API for creating applications based on the
      ESP-MESH stack.
	- Observe an ESP-MESH network in operation, as well as its autoconfiguration
	  capabilities.

* Provisioning
	- Understand and experiment with different modes of provisioning of WiFi
	  credentials, via `BLE` and via` softAP`.
	- Check the clear exchange of keys by making provisions from the command
	  line, as well as observe the utility (and the necessity) of exanging
	  encrypted credentials.

* Energy saving
    - Understand the three power operating modes for the WiFi radio of the ESP32.
	- Observe the influence of these operating modes in the latency of the
	  connection.

## Part 1. WiFi Mesh (ESP MESH)

The ESP-MESH stack is built on top of the WiFi driver (that is, it obviously
makes use of the WiFi services), and in some cases also makes use of IP stack
services (*lwIP*), as for example in the root node, which is the only node that
has IP communication with an edge router . The following diagram shows the Mesh
stack situation in ESP-IDF:

![](img/mesh-software-stack.png)

Like any other ESP-IDF component, ESP-MESH communicates with applications
through its own events:

![](img/mesh-events-delivery.png)

The type `mesh_event_id_t` defines all the possible events that may arise in the
different phases of the life cycle of a network (for example, for a given node,
connection or disconnection from its parent node, or from one of its child
nodes). Event handlers for the ESP-MESH events are registered with the
`esp_event_handler_register()`. Some typical events are for example, the
connection of a parent node (`MESH_EVENT_PARENT_CONNECTED`) or of a child
(`MESH_EVENT_CHILD_CONNECTED`), indicating, respectively, that a node can start
emitting upward in the graph, or downward. Similarly, in a root node, the
reception of the events `IP_EVENT_STA_GOT_IP` and` IP_EVENT_STA_LOST_IP`
indicate that said root node may or may not send data to the external IP
network.

### Events

* `MESH_EVENT_STARTED`: mesh is started
* `MESH_EVENT_STOPPED`: mesh is stopped
* `MESH_EVENT_CHANNEL_SWITCH`: channel switch
* `MESH_EVENT_CHILD_CONNECTED`: a child is connected on softAP interface
* `MESH_EVENT_CHILD_DISCONNECTED`: a child is disconnected on softAP interface
* `MESH_EVENT_ROUTING_TABLE_ADD`: routing table is changed by adding newly joined children
* `MESH_EVENT_ROUTING_TABLE_REMOVE`: routing table is changed by removing leave children
* `MESH_EVENT_PARENT_CONNECTED`: parent is connected on station interface
* `MESH_EVENT_PARENT_DISCONNECTED`: parent is disconnected on station interface
* `MESH_EVENT_NO_PARENT_FOUND`: no parent found
* `MESH_EVENT_LAYER_CHANGE`: layer changes over the mesh network
* `MESH_EVENT_TODS_STATE`: state represents whether the root is able to access external IP network
* `MESH_EVENT_VOTE_STARTED`: the process of voting a new root is started either by children or by the root
* `MESH_EVENT_VOTE_STOPPED`: the process of voting a new root is stopped
* `MESH_EVENT_ROOT_ADDRESS`: the root address is obtained. It is posted by mesh stack automatically.
* `MESH_EVENT_ROOT_SWITCH_REQ`: root switch request sent from a new voted root candidate
* `MESH_EVENT_ROOT_SWITCH_ACK`: root switch acknowledgment responds the above request sent from current root
* `MESH_EVENT_ROOT_ASKED_YIELD`: the root is asked yield by a more powerful existing root. If self organized is disabled and this device is specified to be a root by users, users should set a new parent for this device. if self organized is enabled, this device will find a new parent by itself, users could ignore this event.
* `MESH_EVENT_ROOT_FIXED`: when devices join a network, if the setting of Fixed Root for one device is different from that of its parent, the device will update the setting the same as its parent’s. Fixed Root Setting of each device is variable as that setting changes of the root.
* `MESH_EVENT_SCAN_DONE`: if self-organized networking is disabled, user can call esp_wifi_scan_start() to trigger this event, and add the corresponding scan done handler in this event.
* `MESH_EVENT_NETWORK_STATE`: network state, such as whether current mesh network has a root.
* `MESH_EVENT_STOP_RECONNECTION`: the root stops reconnecting to the router and non-root devices stop reconnecting to their parents.
* `MESH_EVENT_FIND_NETWORK`: when the channel field in mesh configuration is set to zero, mesh stack will perform a full channel scan to find a mesh network that can join, and return the channel value after finding it.
* `MESH_EVENT_ROUTER_SWITCH`: if users specify BSSID of the router in mesh configuration, when the root connects to another router with the same SSID, this event will be posted and the new router information is attached.
* `MESH_EVENT_PS_PARENT_DUTY`: parent duty
* `MESH_EVENT_PS_CHILD_DUTY`: child duty
* `MESH_EVENT_PS_DEVICE_DUTY`: device duty


### LwIP and ESP-WIFI-MESH

The application can access the ESP-WIFI-MESH stack directly without having to go
through the LwIP stack. The LwIP stack is only required by the root node to
transmit/receive data to/from an external IP network. However, since every node
can potentially become the root node (due to automatic root node selection),
each node must still initialize the LwIP stack.

Each node is required to initialize LwIP by calling `tcpip_adapter_init()`. In
order to prevent non-root node access to LwIP, the application should stop the
following services after LwIP initialization:

- DHCP server service on the softAP interface.
- DHCP client service on the station interface.

The following code snippet demonstrates how to initialize LwIP for ESP-WIFI-MESH
applications.

```c
/*  tcpip initialization */
tcpip_adapter_init();
/*
 * for mesh
 * stop DHCP server on softAP interface by default
 * stop DHCP client on station interface by default
 */
ESP_ERROR_CHECK(tcpip_adapter_dhcps_stop(TCPIP_ADAPTER_IF_AP));
ESP_ERROR_CHECK(tcpip_adapter_dhcpc_stop(TCPIP_ADAPTER_IF_STA));
```

ESP-WIFI-MESH requires a root node to be connected with a router. Therefore, in
the event that a node becomes the root, the corresponding handler must start the
DHCP client service and immediately obtain an IP address. Doing so will allow
other nodes to begin transmitting/receiving packets to/from the external IP
network. However, this step is unnecessary if static IP settings are used.

### Writing an ESP-WIFI-MESH Application

The prerequisites for starting ESP-WIFI-MESH is to initialize LwIP and Wi-Fi,
The following code snippet demonstrates the necessary prerequisite steps before
ESP-WIFI-MESH itself can be initialized.

```c
tcpip_adapter_init();
/*
 * for mesh
 * stop DHCP server on softAP interface by default
 * stop DHCP client on station interface by default
 */
ESP_ERROR_CHECK(tcpip_adapter_dhcps_stop(TCPIP_ADAPTER_IF_AP));
ESP_ERROR_CHECK(tcpip_adapter_dhcpc_stop(TCPIP_ADAPTER_IF_STA));

/*  event initialization */
ESP_ERROR_CHECK(esp_event_loop_create_default());

/*  Wi-Fi initialization */
wifi_init_config_t config = WIFI_INIT_CONFIG_DEFAULT();
ESP_ERROR_CHECK(esp_wifi_init(&config));
/*  register IP events handler */
ESP_ERROR_CHECK(esp_event_handler_register(IP_EVENT, IP_EVENT_STA_GOT_IP, &ip_event_handler, NULL));
ESP_ERROR_CHECK(esp_wifi_set_storage(WIFI_STORAGE_FLASH));
ESP_ERROR_CHECK(esp_wifi_start());
```

After initializing LwIP and Wi-Fi, the process of getting an ESP-WIFI-MESH
network up and running can be summarized into the following three steps:

1. Initialize Mesh
2. Configuring an ESP-WIFI-MESH Network
3. Start Mesh


### 1. Initialize Mesh

The following code snippet demonstrates how to initialize ESP-WIFI-MESH:

```c
/*  mesh initialization */
ESP_ERROR_CHECK(esp_mesh_init());
/*  register mesh events handler */
ESP_ERROR_CHECK(esp_event_handler_register(MESH_EVENT, ESP_EVENT_ANY_ID, &mesh_event_handler, NULL));
```

### 2. Configuring an ESP-WIFI-MESH Network

ESP-WIFI-MESH is configured via `esp_mesh_set_config()` which receives its
arguments using the `mesh_cfg_t` structure. The structure contains the following
parameters used to configure ESP-WIFI-MESH:

| Parameter        | Description                                           |
|------------------|-------------------------------------------------------|
| Channel          | Range from 1 to 14                                    |
| Mesh ID          | ID of ESP-WIFI-MESH Network, see mesh_addr_t          |
| Router           | Router Configuration, see mesh_router_t               |
| Mesh AP          | Mesh AP Configuration, see mesh_ap_cfg_t              |
| Crypto Functions | Crypto Functions for Mesh IE, see mesh_crypto_funcs_t |


The following code snippet shows an example of how to configure ESP-WIFI-MESH:

```c
/* Mesh ID */
static const uint8_t MESH_ID = { 0x77, 0x77, 0x77, 0x77, 0x77, 0x77 };
/* Enable the Mesh IE encryption by default */
mesh_cfg_t cfg = MESH_INIT_CONFIG_DEFAULT();
/* mesh ID */
memcpy((uint8_t *) &cfg.mesh_id, MESH_ID, 6);
/* channel (must match the router's channel) */
cfg.channel = CONFIG_MESH_CHANNEL;
/* router */
cfg.router.ssid_len = strlen(CONFIG_MESH_ROUTER_SSID);
memcpy((uint8_t *) &cfg.router.ssid, CONFIG_MESH_ROUTER_SSID, cfg.router.ssid_len);
memcpy((uint8_t *) &cfg.router.password, CONFIG_MESH_ROUTER_PASSWD,
       strlen(CONFIG_MESH_ROUTER_PASSWD));
/* mesh softAP */
cfg.mesh_ap.max_connection = CONFIG_MESH_AP_CONNECTIONS;
memcpy((uint8_t *) &cfg.mesh_ap.password, CONFIG_MESH_AP_PASSWD,
       strlen(CONFIG_MESH_AP_PASSWD));
ESP_ERROR_CHECK(esp_mesh_set_config(&cfg));
```

### 3. Start Mesh

The following code snippet demonstrates how to start ESP-WIFI-MESH:

```c
/* mesh start */
ESP_ERROR_CHECK(esp_mesh_start());
```

After starting ESP-WIFI-MESH, the application should check for ESP-WIFI-MESH
events to determine when it has connected to the network. After connecting, the
application can start transmitting and receiving packets over the ESP-WIFI-MESH
network using `esp_mesh_send()` and `esp_mesh_recv()`.


!!! danger "Task 3.1"
	The most convenient way to observe the behavior of a WiFi network Mesh is to
	deploy an infrastructure with a sufficient number of nodes belonging to to
	the same network. Unfortunately, this requires would require to have a large
	amount of nodes in the same closed space, and given the conditions of this
	curse it wont be possible.

	In this lab experience, each of you will deploy a WiFi Mesh network with
	only two nodes, using the two ESP32 nodes that each student has. You will
	start by copying the example `examples/mesh/internal_communication` to
	another directory in your home folder. Then you can configure the project
	to:

	1. Connect to an access point generated with your own smartphone or the
	   wifi router at your place (*Router SSID and Router password*).
	2. Configure the ESP-MESH network to use WPA2_PSK and select as password
	   `password`.

	At this time, you will not make any changes to the code in the example.
	Compile your code. Flash the two ESP nodes you have and monitor the output
	of both nodes in two different terminals (use the command line toolset here
	for convenience).  If you have the possibility, try to physically arrange
	the nodes in a way that one has better connection with your
	smartphone/router than the other (play with distance or obstacles). Monitor
	the output of each node and annotate the following information:

	1. MAC addresses of the `STA` and` SoftAP` interfaces (you will see then in
	   the first outgoing messages).
	2. Layer of the topology in which your node is located (you will observe it
	   in `[L: XX]` format for sending and receiving data).
	3. If the root node has been chosen, also note this circumstance and the IP
	   assigned by the *router* (see the response to the corresponding event).

	Also, take note of the ID of the Mesh network that was used. Before
	collecting this information make sure that the topology has converged. Draw
	a graph of your small wifi mesh network.

	Next, turn off the root node and wait for the network to converge again.
	Verify that the other node became the new root node.

	Now reconnect the node you disconnected previously, and see how it
	reconnects to the mesh. Is it again the root node? Annotate it and discuss
	why you think it is or is not the root node again and if that is what you
	expected.

	Deliver a report in pdf format in which you explain your observations in
	english.

## Part 2. WiFi Provisioning

ESP-IDF provides a specific component that offers a WiFi provisioning service.
This component provides APIs that control Wi-Fi provisioning service for
receiving and configuring Wi-Fi credentials over SoftAP or BLE transport via
secure Protocol Communication (protocomm) sessions. The set of `wifi_prov_mgr_`
APIs help in quickly implementing a provisioning service having necessary
features with minimal amount of code and sufficient flexibility.

To complete this part of the lab assignment you will have to work with the
example `examples/provisioning/wifi-prov-mgr`.


### Initialization of the provisioning service

The `wifi_prov_mgr_init()` function must be called to configure and initialize
the provisioning manager before any other `wifi_prov_mgr_` API functions. Note
that the manager relies on other components of IDF, namely NVS, TCP/IP, Event
Loop and Wi-Fi (and optionally mDNS), hence these must be initialized
beforehand. The manager can be de-initialized at any moment by making a call to
`wifi_prov_mgr_deinit()`.

An initialization example could be:

```c
wifi_prov_mgr_config_t config = {
  .scheme = wifi_prov_scheme_ble,
  .scheme_event_handler = WIFI_PROV_SCHEME_BLE_EVENT_HANDLER_FREE_BTDM
};

ESP_ERR_CHECK( wifi_prov_mgr_init(config) );
```

The configuration structure `wifi_prov_mgr_config_t` has a few fields to specify
the behavior desired of the manager. The `scheme` field is used to specify the
provisioning scheme. Each scheme corresponds to one of the modes of transport
supported by protocomm:

- `wifi_prov_scheme_ble`: BLE transport and GATT Server for handling
  provisioning commands
- `wifi_prov_scheme_softap`: Wi-Fi SoftAP transport and HTTP Server for handling
  provisioning commands
- `wifi_prov_scheme_console`: Serial transport and console for handling
  provisioning commands

We refer you to [WiFi Provisioning
Initialization](https://docs.espressif.com/projects/esp-idf/en/latest/esp32/api-reference/provisioning/wifi_provisioning.html#initialization) 
for additional information on the fields of the `wifi_prov_mgr_config_t`
structure.

### Check Provisioning State

Whether the device is provisioned or not can be checked at runtime by calling
`wifi_prov_mgr_is_provisioned()`. This internally checks if the Wi-Fi
credentials are stored in NVS.

Although there are different methods to delete the provisioning information
stored in NVS, we will use the mechanism provided by `idf.py` to
delete its content. To do this, we will execute:

```sh
idf.py erase_flash
```

### Start Provisioning Service

At the time of starting provisioning we need to specify a service name and the
corresponding key. These translate to:

- Wi-Fi SoftAP SSID and passphrase, respectively, when scheme is
  `wifi_prov_scheme_softap`
- BLE Device name (service key is ignored) when scheme is `wifi_prov_scheme_ble`

Also, since internally the manager uses *protocomm*, we have the option of
choosing one of the security features provided by it :

- Security 1 is secure communication which consists of an initial handshake
  involving X25519 key exchange along with an authentication using a proof of
  possession (pop), followed by the encryption/decryption of subsequent
  messages with AES-CTR.
- Security 0 is simply a plain text communication. In this case the pop is simply
  ignored

See [Provisioning](https://docs.espressif.com/projects/esp-idf/en/latest/esp32/api-reference/provisioning/provisioning.html)
for details about the security features.

The following code snippet shows an example of Provisioning Service
initialization:

```c
const char *service_name = "my_device";
const char *service_key  = "password";

wifi_prov_security_t security = WIFI_PROV_SECURITY_1;
const char *pop = "abcd1234";

ESP_ERR_CHECK( wifi_prov_mgr_start_provisioning(security, pop, service_name, service_key) );
```

The provisioning service will automatically finish only if it receives valid
Wi-Fi AP credentials followed by a successful connection to the AP (IP
obtained). Nevertheless, the provisioning service can be stopped at any moment
by making a call to `wifi_prov_mgr_stop_provisioning()`.


### Waiting For Completion

Typically, the main application will wait for the provisioning to finish, then
de-initialize the manager to free up resources and finally start executing its
own logic.

There are two ways for making this possible: 

- The simpler way is to use a **blocking** call to `wifi_prov_mgr_wait()`.

```c
// Start provisioning service
ESP_ERROR_CHECK( wifi_prov_mgr_start_provisioning(security, pop, service_name, service_key) );

// Wait for service to complete
wifi_prov_mgr_wait();

// Finally de-initialize the manager
wifi_prov_mgr_deinit();

// From here, the usual application logic would starts
// ...
```


- The second mechanism is based on events (i.e., is asynchronous/non blocking).
  The default event loop handler to catch `WIFI_PROV_EVENT` and call
  `wifi_prov_mgr_deinit()` when event ID is `WIFI_PROV_END`:

```c
static void event_handler(void* arg, esp_event_base_t event_base,
                          int event_id, void* event_data)
{
    if (event_base == WIFI_PROV_EVENT && event_id == WIFI_PROV_END) {
        /* De-initialize manager once provisioning is finished */
        wifi_prov_mgr_deinit();
    }
}
```

### Provisioning tools for mobile devices

There are applications prepared by Espressif to carry out the process
provisioning over ESP32. These applications are available both for Android
and IOS devices, for BLE and/or SoftAP transports:

- Android:
    - [BLE Transport](https://play.google.com/store/apps/details?id=com.espressif.provble).
    - [SoftAP Transport](https://play.google.com/store/apps/details?id=com.espressif.provsoftap).

- IOS:
    - [BLE Transport](https://apps.apple.com/in/app/esp-ble-provisioning/id1473590141).
    - [SoftAP Transport](https://apps.apple.com/in/app/esp-softap-provisioning/id1474040630).

!!! danger "Task 3.2"
	Provision your ESP32 devices using the credentials that correspond to your
	WiFi network (home wifi or smartphone) using the applications corresponding
	to your mobile device, for both BLE and SoftAP transports.  Write down a
	small report in english (in pdf format) describing the process, including
	the screenshots corresponding to the ESP32 output that show that the
	provisioning was successful.  Remember, before each repetition of the
	experiment, use the command `idf.py erase_flash` to remove provisioning
	information from previous sessions. Check the operation of the different
	security levels.

These applications work by means of a very simple communication with the
unprovisioned ESP32, whose mechanisms depend on the transport being used.  In
the case of BLE, a GATT table is created with different characteristics used to
write (send) data to the device. We will see what a GATT table is in next lab
assignment. In the case of the `softAP` transport, a series of *endpoints* are
created (HTTP URIs) that allow, in a simple way, to read and write the data that
we want to communicate to the other end of the communication.

The following table summarizes the *endpoints* created by the standard versions
of the provisioning protocol (they can be adapted to include additional
information to exchange):

|                            | Endpoint (BLE + GATT Server) | URI (SoftAP + HTTP)       |
|----------------------------|------------------------------|---------------------------|
| Session establishment      | prov-session                 | http://IP:80/prov-session |
| Network scanning available | prov-scan                    | http://IP:80/prov-scan    |
| Provisioning configuration | prov-config                  | http://IP:80/prov-config  |
| Protocol version           | proto-ver                    | http://IP:80/proto-ver    |

The details of this type of provisioning protocol remain as additional exercise
to the student, and go beyond the goals of the assignment. However, it would be
advisable to have a mechanism that allows them to be observed, and determine,
for example in the case of SoftAP, if the exchange of credentials is done as
plain text (plaintext) or encrypted, which could pose serious security problems
for the user of a device mobile, since the credentials of connection to the WiFi
network would be exposed.

To analyze this security issue, we will use our laptop/pc as provisioning device.
We have to connect the laptop/pc to the provisioning SSID of the ESP32 node and
use a command line tool provided with the ESP-IDF toolset, called `esp_prov.py`,
which can be found in the directory `tools/esp_prov`.

!!! note "Note"
	Before using the program, you must install the respective dependencies
    using the commands (from the `tools/esp_prov` directory):

    ```
    pip install -r requirements.txt
    pip install -r requirements_linux_extra.txt
    ```

Its use is simple, and can be consulted by running `python esp_prov.py -h`.
Basically a provisioning session using `softAP` on a device with IP
`192.168.4.1`, without layer security (encryption) and providing the SSID and
key SSID_EXAMPLE/KEY_EXAMPLE would result in:

```sh
python esp_prov.py --transport softap --service_name "192.168.4.1:80" --sec_ver 0 --ssid SSID_EXAMPLE --passphrase KEY_EXAMPLE
```

!!! danger "Task 3.3"
	Perform the provisioning process from the command line using the above
	indications. Use the wireshark program to analyze the provisioning traffic
	and find evidences of the clear delivery of the network credentials between
	the provisioner and the device (text mode, without encryption) and the use
	of the *endpoints/URIs* previously mentioned. Create a small report in
	english (in pdf format) describing the process and showing the evidences you
	found.  Next, try with safe mode (option `--sec_ver 1`) and see how the keys
	exchanged are now encrypted. Add the corresponding comments to your report.

## Part 3. WiFi Power States

### Station mode

Currently, ESP32 Wi-Fi supports the Modem-sleep mode which refers to the legacy
power-saving mode in the IEEE 802.11 protocol. Modem-sleep mode works in
station-only mode and the station must connect to the AP first. If the
Modem-sleep mode is enabled, the station node will switch between active and
sleep state periodically. In sleep state, RF, PHY and BB are turned off in order
to reduce power consumption. The connection with the AP is nevertheless kept
alive.

`Modem-sleep` mode includes minimum and maximum power save modes. In minimum
power save mode, the station wakes up for every beacon with DTIM (Delivery
Traffic Indication Message) so that it can receive all the broadcast data.
However, it cannot save much more power if the DTIM interval is short, and this
interval is established by the AP.

In maximum power save mode, station wakes up every *listen* interval to receive
the AP beacon. The *listen* interval can be set longer than the AP DTIM
interval, leading extra power savings at the risk of loosing some broadcast
data, because station may be in sleep state during a DTIM beacon transmission.
The *listen* interval is configured with the `esp_wifi_set_config()` function,
which should be invoked before connecting to AP.

### AP mode

Currently ESP32 AP doesn’t support all of the power saving features defined in
the Wi-Fi specification. To be specific, in AP mode it only caches unicast data
for the stations connect to it, but does not cache the multicast data. If
stations connected to the ESP32 AP have enabled the power save mode, they may
experience multicast packet loss.

In the future, all power save features will be supported on ESP32 AP.

### Example

The example `examples/wifi/power_save` uses a simple code to illustrate
the configuration of a station in the `Modem-sleep` mode, and you can select
between the minimum and maximum submodes. These submodes can be configured
through the configuration menu. In addition, an option is offered to modify the
listening time in the case of the *maximum* submode.

!!! danger "Task 3.4"
	Compile, flash, and run the sample code using all the three configurations
	available: no savings, minimum savings and maximum savings. In the case of
	maximum savings, vary the listening time so that it takes different values.
	In all cases, connect your ESP32 to an access point and, from a laptop
	connected to the same AP, execute a series of `ping` commands towards the
	station. Analyze the relation between the mode, DTIM, listen times and the
	ping response time, showing graphical represntations when possible. Deliver
	a small report in english (in pdf format).

