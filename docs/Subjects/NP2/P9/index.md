# Laboratory 5. Node-RED

## Introduction and goals

Node-RED is an open-source tool initially developed by IBM and, being oriented
to data flow construction, offers mechanisms to associate hardware devices, APIs
and online services within an IoT ecosystem.
Node-RED is a graphical tool, usable from within any web browser, that allows
for the creation and edition of data flows that take input data (via input nodes)
process them (via processing nodes) and provide outputs (via output nodes).
All elements, including complex flows defined by the user, can be stored
in JSON format and can be imported in other setups. Node-RED allows the interconnection
of software and hardware elements virtually via any known network protocol, 
accelerating the deployment of IoT infrastructures.

The development of the laboratory differs from that used in previous labs. 
In this case, this handout includes only information and instructions for the
installation of the Node-RED tool in the Virtual Machine (you can install it 
in any physical machine), and an exercise proposal that you need to design and
implement.

During the first laboratoriy session, the professor will demonstrate the main
features of Node-RED and a guide for basic use of the tool.

## Installation and setup

To install Node-RED in the Virtual Machine, you can use the `npm` package
manager:

```sh
sudo npm install -g --unsafe-perm node-red
```

If everything is fine, you should see an output similar to this:

```sh
+ node-red@1.1.0
added 332 packages from 341 contributors in 18.494s
found 0 vulnerabilities
```

In order to execute Node-RED, once installed, it is possible to use
the order `node-red` from any terminal. To stop the process, just use
`Ctrl-C`:

```sh
$ node-red

Welcome to Node-RED
===================

30 Jun 23:43:39 - [info] Node-RED version: v1.1.0
30 Jun 23:43:39 - [info] Node.js  version: v10.21.0
30 Jun 23:43:39 - [info] Darwin 18.7.0 x64 LE
30 Jun 23:43:39 - [info] Loading palette nodes
30 Jun 23:43:44 - [warn] rpi-gpio : Raspberry Pi specific node set inactive
30 Jun 23:43:44 - [info] Settings file  : /Users/nol/.node-red/settings.js
30 Jun 23:43:44 - [info] HTTP Static    : /Users/nol/node-red/web
30 Jun 23:43:44 - [info] Context store  : 'default' [module=localfilesystem]
30 Jun 23:43:44 - [info] User directory : /Users/nol/.node-red
30 Jun 23:43:44 - [warn] Projects disabled : set editorTheme.projects.enabled=true to enable
30 Jun 23:43:44 - [info] Creating new flows file : flows_noltop.json
30 Jun 23:43:44 - [info] Starting flows
30 Jun 23:43:44 - [info] Started flows
30 Jun 23:43:44 - [info] Server now running at http://127.0.0.1:1880/red/
```

With the software started, it is possible to access to the Node-RED editor
via the address `http://localhost:1880` from any browser.

Upon boot, you will observe four areas in the editor:

1. **Main bar**, in the upper part, with buttons *Deploy* and *Main Menu*.

2. **Node panel**, on the left side, that gives direct access to all nodes available
in Node-RED. It is possible to install new nodes via the Node Palette, 
available via the Main Menu (*Manage Palette*). 
These nodes can be dragged to the editor to conform new data flows.

3. **Edit panel or workspace**, on the middle of the screen, where you will be able
to drag and drop new nodes. It is possible to create new flows in independent
tabs.

4. **Information panel**, on the right part of the screen, where the most
useful button is *Debug*, with which you will see the output of the 
*Debug* in our flows.

## Example 1

In the following, we show a basic use example for the Node-RED editor, including the
use of nodes *Inject*, *Debug* and *Function*.

### Node *Inject*

The *Inject* node can inject messages in a flow, pushing on the button
associated to the node, or establishing an interval of time between injections.
Look in the left panel for a node of type *Inject* and drag it to the
workspace. In the information panel, you can check the data associated to the 
node, and help information to use it.

### Node *Debug*

The *Debug* node permits that any incoming message is shown in the debug panel, 
on the right of the screen. By default, it just shows the message *payload*
even thout it can be configured to show the complete message. Drag a
node *Debug* the workspace and keep it prepared.

### Link and deployment (*Deploy*)

Connect the nodes *Inject* and *Debug* establishing a link (*Wire*) between both.
Deploy the flow using the button *Deploy* from the main bar. This will deploy the
flow on the server.

Select the option *Debug* on the information panel, and press the button *Inject*.
You should see numbers appearing on the panel. By default, the *Inject* node emits
the numbre of milliseconds from 1/1/1970 as the *payload*.

Modify (temporarily) the node *Debug* so that it just shows all the message
instead of only the *payload*. Deploy the flow again and observe the differences.

Configure again the *Debug* node as was when you inserted it.

### Node *Function*

The *Function* node can process the input message via a JavaScript function. 
Delete the *Wire* you created, and add a *Function* node between nodes *Inject* and
*Debug*.

Double-click on the new node to open the edition dialog. Copy the following code in
the *Function* field:

```javascript
// Create a Date object from the payload
var date = new Date(msg.payload);
// Change the payload to be a formatted Date string
msg.payload = date.toString();
// Return the message so it can be sent on
return msg;
```

Click on *Done* and deploy the flow. Observe that, now, the debug messages show
timestamps in a visible format. Take into account that a node always receives a 
message (*msg*) as an input, and returns a message (*msg*) as an output. Both objects
contain a field *payload*.

For more information about the use of functions and work with messages,
inluding multiple return values, and work with global values for the flow, 
the student is requested to study the following documentation:

* **Working with messages**: [link to documentation](https://nodered.org/docs/user-guide/messages).
* **Working with functions**: [link to documentation](https://nodered.org/docs/user-guide/writing-functions).

## Example 2

### Node *Inject*

In the last example, we showed how to create an *Inject* node to activate the
flow when the associated button was pressed. In this example, we will configure the
*Inject* node to activate the flow at regular intervals.

Drag a new *Inject* node in the workspace. Double-click on it and, on the edit
dialog, use the option *Repeat interval*, fixing a regular interval. Close the
edition dialog.

### Node *HTTP Request*

The node of type *HTTP Request* can be used to download a webpage or HTTP resource.
Add une to the workspace and edit it so that its *URL* property targets to
`https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/significant_month.csv`.

This URL is a repository of earthquakes in the last month, published by the official
entity in charge, returned in a CSV format.

### Node *CSV*

Add a new *CSV* node and edit its properties. Activate the option 
*First row contains column names* and finish the edition.

### Node *Debug* and wiring

Add a *Debug* node and link the nodes:

* Connect the output of the *Inject* node to the input of the *HTTP Request* node.
* Connect the output of the *HTTP Request* node to the input to the node *CSV*.
* Connect the output of the *CSV* node to the input of the node *Debug*.

### Node *Switch*

Add a *Switch* node to the workspace. Edit its properties and configure it 
to check the property `msg.payload.mag`, using the operation `>=` on a numeric value and
the value `6.2`, for example.

Add a second *Wire* between the node *CSV* and the node *Switch*.

### Node *Change*

Add a node *Change*, connected to the output of the *Switch* node. Configure it to establish
a value of `msg.payload` to `ALARM`.

### Node *Debug*

Add a *Debug* node and deploy the flow. On the *Debug* panel you should
observe, for eac activatio of the *Inject* node, an output similar to this:

```sh
msg.payload : Object
{"time":"2017-11-19T15:09:03.120Z","latitude":-21.5167,"longitude":168.5426,"depth":14.19,"mag":6.6,"magType":"mww","gap":21,"dmin":0.478,"rms":0.86,"net":"us","id":"us2000brgk","updated":"2017-11-19T17:10:58.449Z","place":"68km E of Tadine, New Caledonia","type":"earthquake","horizontalError":6.2,"depthError":2.8,"magError":0.037,"magNst":72,"status":"reviewed","locationSource":"us","magSource":"us"}
```

You can click on the small arrow on the left of each property to expand it and
to examine the contents.

If there is any earthquake with a magnitude higher than `6.2`, you will observe
an additional output:

```sh
msg.payload : string(6)
"ALARM"
```

For more information on the basic nodes in Node-RED, you can check:

* **The Core Nodes**: [link to documentation](https://nodered.org/docs/user-guide/nodes).

## MQTT client and deployment of a control panel (dashboard)

The node *MQTT in* can perform subscriptions to *topics* on MQTT brokers.

Drag a new *MQTT in* node in your workspace and configure the associated
broker to *localhost*, using the default port. Establish a *topic* 
of interest. Connect a *Debug* node and deploy the flow.

From your console, publish messages via *mosquitto_pub* and see how, effectively,
they can be viewed from Node-RED.

Next, we will create a small control panel to graphically represent the
published value. First, install the node 
`node-red-dashboard` from the main many, option      
*Manage palette*. Upon a successful installation, you will see that new nodes
appear in the control panel; these nodes will let us design and implement a basic
control based on widgets.

Drag a node of type *Gauge* to the workspace, and configure its default values. Connect
the output of your *MQTT in* node to the input of the new *Gauge* node. 

Deploy the flow, and navigate to `http://localhost:1880/ui`, where you will 
observe the control panel with the *widget* you just created. Interat with it 
publishin messages via MQTT.

For more information on the deployment of control panels, you can check:

* **Node-Red-Dashboard**: [link to documentation](https://flows.nodered.org/node/node-red-dashboard).

## Additional documentation

The official user guides from Node-RED are a good starting point to further
study on the use of the infrastructures. Between them, the most important
part to commence is that that introduces the basic concepts of Node-RED, including
the work with nodes, flows, contexts (important to work with global and shared values
across nodes in a flow, for example), messages, *wires*, etc:

* **Node-RED Concepts**: [link to documentation](https://nodered.org/docs/user-guide/concepts).

The guide *Node-RED Guide* contains interesting documentation (additional and advanced)
for the deployment of flows and for the use of control panels (local or using remote
services (e.g. *Freeboard*)):

* **Node-RED Guide**: [link to documentation](http://noderedguide.com).

## Ejercicio entregable

Study the documentation associatd to Node-RED, both in its webpage
and on the programming guide *Node-RED Guide* (specifically on the first
four parts). Together with the demos offered by the professor and previous
examples, this study will help you on the development of the exercise.

!!! danger "Deliverable task"
    The exercise consists on the design and development of a system based on
    data flows built on top of Node-RED, that implements a mechanism to monitor
    ambient parameters (e.g. temperature) and notify (alarm) on given circumstances (e.g.
    if the sensed temperature is higher than a threshold).

    The students will design the system and implement it, meeting the following conditions:

    * **(2/10 points)**. The system will use, *at least* one external device (e.g. ESP32, mobile phone, ...)
    for data gathering. We will evaluate positively the use of more than one device or type of device.

    * **(2/10 points)**. The system will store or interact with, *at least*, 
    one external system (mail server, Twitter, WeChat, Telegram, IBM Bluemix, ...).

    * **(2/10 points)**. The system will store observed data on a persisten media (e.g. NoSQL database, files, ...)
    to allow further analysis of them.

    * ** (2/10 points)**. The system will act as an alarm system only upon certain 
    input conditions (E.g. when receiving a value from a sensor higher than a pre-established
    threshold; that value could, for example, be configured via MQTT or via a control panel).

    * **(2/10 points)**. The system will use, at least, one node type not installed by default
    with the basic Node-RED installation.

    The studenst will deliver the JSON file or files that describe the nodes, and a short report
    describing the designed system and the developed work, highlighting the difficulties found and 
    those additional aspects considered of interest by the students.
