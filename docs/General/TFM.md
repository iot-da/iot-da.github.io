# Final project proposals

## Important dates

- Deadline for topic selection: XX/XX.
- Deadline for advisor agreement for defense: XX/XX.
- Final defense: XX/XX.

## Description and rules

The Final Project is an individual work that aims at demonstrating
that the student has acquired the necessary knowledge and skills 
associated to the Master's Degree, and it will be developed 
**individually** under the supervision of one or more professors.

The content proposal of each project will depend on the specific
selected topic, and they will range from designing and developing
a specific IoT application/deployment, service or system within
the field of Internet of Things, specifically targeting in depth 
one or more of the topics studied in the subjects of the course.
The works will cover in detail topics related with hardware and
software integration for IoT, data analysis, or theoretical studies
of the state-of-the-art in the IoT field.

The project will allow the student to relate practical aspects
and professional issues with the topics covered within the development
of one or more of the subjects covered in the Master, adapted to the
interests of the student. 

The Advisor will define the topic and tasks to fulfill, and will guide
the student throughout the development of the work and the goals to
achieve. He/she will organize activities to control the correct
development of the work.

The evaluation of the Project will be carried out by a Committee that
will be composed by professors of the different subjects. In order
to defend the work, the student will need to pass all the subjects in
the Master, and he/she will need a signed agreement from the Advisor
stating his/her consent to proceed with the defense. This consent report
will include all the considerations necessary to help the Committee
evaluating the developed work. 

The students will present a report written in English, that will include,
at least, an Introduction, Goal description and Work Plan, together
with a critical discussion of the develped work and results, conclusions
and related bibliography. The defense of the work will be carried out
through an online presentation, and the Committee will evaluate the 
quality of the report and the defense to obtain the final grade of the
work.

In the following, we propose a number of topics proposed by professors
covering topics of interest. Even though several students can share 
a common proposal, the work need to be original and developed individually.
Plagiarism (from other students or third parties) will determine a fail
in the final grade of the work.

The dates and mechanisms to deliver the final report and to proceed with
the defense will be announced with enough time before the deadline.

Each student will contact the advisor stating his/her interest in a 
specific proposal with free student slots before the deadline stated
at the beginning of this page.

## Proposals

### Proposal 1

* Title: *Relation between air pollution, weather and traffic*
* Description:

The goal is to predict the pollution in a particular point of a city for the next few hours. The prediction will take as input from the data collected by sensors of air pollution and number of vehicles. We will train different models and evaluate the results to choose the best predictions in each case. The project includes:
    - Basic data management to prepare the data
    - Basic statistics to understand the data and detect outliers
    - Clustering for selecting days with similar pollution/traffic conditions
    - Feature selection
    - Hiperparameter tunning
    - Model Selection

* Requirements: good programming skills.
* Professor: Rafael Caballero Roldán.
* Available slots: 6

### Proposal 2

* Title: *Machine Learning Ensamble Methods*
* Description:

The ensemble Methods combine several "weak learners" to build a more efficient method. The main goal is to implement in Spark the three main Methods (bagging, stacking and Boosting). On particular the project will include:

    - A complete description of the tecniques
    - A Spark function implementing then
    - A benchmark using some datasets of the course to compare their efficiency

* Requirements: good programming skills.
* Professor: Rafael Caballero Roldán.
* Available slots: 6

### Proposal 3

* Title: *IoT devices or services for well-being*

* Description:

Well-being is usually desired by most people, and smart watches and smart bands are growing in
popularity for such purpose. However, other IoT devices and services can help users to provide
accurate perspectives of certain well-being aspects in order to provide personalized advices for
increasing the well-being. For example, smart beds can help you in tracking you sleeping, door
sensors could measure the time spent in outdoor activities or the times you eat meals at home. All
this information related with emotional information could feed an intelligent system to output the
right advices for increasing the well-being. This work could be conducted from either (1) a research
perspective being relevant the analysis of existing works in this topic and the proposal of novel ideas,
or (2) from a technical perspective addressing to program some intelligent system for providing well-
being advices based on information from IoT devices.

* Professor: Iván García-Magariño García 

* Available slots: 6

### Proposal 4

* Title: *IoT devices or services for healthcare*
* Description:

Healthcare is benefiting from the growing of IoT. For instance, smart homes could track the progress
of certain symptoms. Smart IoT dispensers can help patients in reminding their medication to avoid
both missing it and forgetting whether certain medication has been taken. This work could be
conducted from either (1) a research perspective being relevant the analysis of existing works in this
topic and the proposal of novel ideas, or (2) from a technical perspective addressing to prototype a
certain IoT device or service and program the necessary software for providing a system that could
help in some aspect of healthcare.

* Professor: Iván García-Magariño García 

* Available slots: 6

### Proposal 5

* Title: *OpenData iniciatives in China: situation, perspectives and use cases*
* Description:

OpenData initiatives pursue offering data sources in an open, royalty-free and accessible manner. It follows a similar philosophy as that of Open Source or Open Hardware, and aims at facilitating data analysis to the community taken from official channels, both from Local or National Goverments, or from companies.

The goal of the project is two-fold: first, to provide a global, in-depth study and discussion of the OpenData initiatives in China, both from the Government and from Private Companies; second, to select a set of realistic use cases to perform specific data analysis oriented to real-world applications, mainly based on or with application to the IoT paradigm. 

* Professors: Francisco Igual and J. Ignacio Gómez

* Available slots: 6

### Proposal 6

* Title: *SmartCities: requirements, infrastructure and use cases*
* Description:

We have been using the term *Smart Cities* for many years now, but it still looks like a *to be defined* concept. There are many flavours in Smart Cities initiatives and many actors that play different roles in the process of implementing them.  Focusing on IoT, there is always a need to deploy an infrastructure that may represent a huge economical investment with some return expected (economic, social...).

The goal of this project is to deep into the idea of Smart Cities, starting with a general description of its typical topics: smart mobility, smart buildings, smart grid (energy distribution and savings), smart health, water supply, waste disposal facilities...  The students will choose two of those topic and provide an in-depth study of the requirements (sensors, nodes, edge computing, servers...) including the deployment and maintenance process.  The study must include at least two examples of existing cities implementing initiatives in the topics chosen (one Chinese and one European city, if possible). There are many questions this study may answer: how is a given project improving the quality of life of the citizens? Who is paying the cost of the infrastructure? What is the expected "Return Of Investment" (ROI)? Will there be shared infrastructures? (i.e. companies that deploy a sensor network and rent it to other companies/public organisations as a "service")

* Professors: Francisco Igual and J. Ignacio Gómez

* Available slots: 6


### Proposal 7

* Title: *Building meshes with WiFi*
* Description:

ESP-IDF provides a proprietary protocol, called *ESP-WIFI-MESH*, that allows  numerous devices spread over a large physical area (both indoors and outdoors) to be interconnected under a single WLAN (Wireless Local-Area Network). ESP-WIFI-MESH is self-organizing and self-healing meaning the network can be built and maintained autonomously. [You can find information about ESP-WIFI-MESH in this link](https://docs.espressif.com/projects/esp-idf/en/latest/esp32/api-guides/esp-wifi-mesh.html).

Some of those nodes (but not necessarily all of them) may have access to a router (border router) that provides access to the internet. The far-away nodes (those outside the range of the router) may still connect to the internet asking the intermediate nodes to relay their transmissions.

ESP-IDF also provides an API to access *Thread*, an IPv6-based mesh networking technology for IoT. Once again, it allows a mesh of nodes to gain access to the internet even if they are not close to a border router. [More information about Thread can be found in this link](https://openthread.io/).

The goal of this project is to build a mesh of ESP32 nodes using both technologies to comparte their APIs, capabilities and performance. The nodes will run simple applications (sensing temperature, for example) and will try to send the information to an external server using MQTT. Some of the nodes will be close to a router providing access to the internet (and thus, to the external server), while some others will be out of the range of the router signal.

The study should compare both implementations, trying to figure out the overheads of each implementation, relative performance, ease of use...

**IMPORTANT**: to perform this project, you will need more than 2 ESP32 boards, so the team partners should live close enough to physically meet to make tests.

 
* Professors: Francisco Igual and J. Ignacio Gómez

* Available slots: 6



