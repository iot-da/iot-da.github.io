# Lab 4. Bluetooth Low Energy (BLE)

# Goals

* Dissect in detail a GATT table construction *firmware* (GATT server) using the
  ESP-IDF API.
* Learn to use `gatttool` to interact with the GATT server.
* Modify the GATT server to accept notification requests from the client,
  and to publish updated values for a certain characteristic on demand.

# GATT Sever Implementation

## Introduction

In this lab assignmet, we will deploy a GATT server using the ESP-IDF API. This
API exposes the functionalities of Bluedroid, the Bluetooth stack (including
BLE) that provides ESP-IDF for the development of Bluetooth applications.

We will use the example from `examples/bluetooth/bluedroid/ble/gatt_server_service_table`,
which example implements a Bluetooth Low Energy (BLE) Generic
Attribute (GATT) Server using a table-like data structure to define the server
services and characteristics such as the one shown in the figure below
Therefore, it demonstrates a practical way to define the server functionality in
one place instead of adding services and characteristics one by one.

This example implements the *Heart Rate Profile* as defined by the [Traditional
Profile Specifications](https://www.bluetooth.com/specifications/profiles-overview).

<div align="center"><img src="image/Heart_Rate_Service.png" width = "450" alt="Table-like data structure representing the Heart Rate Service" align=center /> </div>

We will therefore display three characteristics. Of them, the most important for
us will be the heart rate measurement value, with its value (*Heart Rate
Measurement Value*) and its notification settings (*Heart Rate Measurement
Notification Configuration*).

Due to the complexity of the code (at least in its initial part), this document
follows the program workflow and breaks down the code in order to make sense of
every section and reasoning behind the implementation.

## Includes

Let’s start by taking a look at the included headers:

```c
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "freertos/event_groups.h"
#include "esp_system.h"
#include "esp_log.h"
#include "nvs_flash.h"
#include "esp_bt.h"
#include "esp_gap_ble_api.h"
#include "esp_gatts_api.h"
#include "esp_bt_main.h"
#include "gatts_table_creat_demo.h"
#include "esp_gatt_common_api.h"
```

These includes are required for the *FreeRTOS* and underlaying system components
to run, including logging functionality and a library to store data in
non-volatile flash memory. We are interested in ``bt.h``, ``esp_bt_main.h``,
``esp_gap_ble_api.h`` and ``esp_gatts_api.h`` which expose the BLE APIs required
to implement this example.

* `esp_bt.h`: implements BT controller and VHCI configuration procedures from the host side.
* `esp_bt_main.h`: implements initialization and enabling of the Bluedroid stack.
* `esp_gap_ble_api.h`: implements GAP configuration such as advertising and connection parameters.
* `esp_gatts_api.h`: implements GATT Server configuration such as creating services and characteristics.


## Service Table

The header file `gatts_table_creat_demo.h` is where an enumeration of the
services and characteristics is created:


```c
enum
{
    IDX_SVC,
    IDX_CHAR_A,
    IDX_CHAR_VAL_A,
    IDX_CHAR_CFG_A,

    IDX_CHAR_B,
    IDX_CHAR_VAL_B,

    IDX_CHAR_C,
    IDX_CHAR_VAL_C,

    HRS_IDX_NB,
};
```

The enumeration elements are set up in the same order as the Heart Rate Profile
attributes, starting with the service followed by the characteristics of that
service. In addition, the Heart Rate Measurement characteristic has a Client
Characteristic Configuration (CCC) descriptor which is an additional attribute
that describes if the characteristic has notifications enabled. The enumeration
index can be used to identify each element later when creating the actual
attributes table. In summary, the elements are described as follows:

* ``IDX_SVC``: Heart Rate Service index
* ``IDX_CHAR_A``: Heart Rate Measurement characteristic index
* ``IDX_CHAR_VAL_A``: Heart Rate Measurement characteristic value index
* ``IDX_CHAR_CFG_A``: Heart Rate Measurement notifications configuration (CCC) index
* ``IDX_CHAR_B``: Heart Rate Body Sensor Location characteristic index
* ``IDX_CHAR_VAL_B``: Heart Rate Body Sensor Location characteristic value index
* ``IDX_CHAR_C``: Heart Rate Control Point characteristic index
* ``IDX_CHAR_VAL_C``: Heart Rate Control Point characteristic value index
* ``IDX_NB``: Number of table elements.


## Main Entry Point

The entry point to this example is the ``app_main()`` function:

```c
void app_main(void)
{
    esp_err_t ret;

    /* Initialize NVS. */
    ret = nvs_flash_init();
    if (ret == ESP_ERR_NVS_NO_FREE_PAGES || ret == ESP_ERR_NVS_NEW_VERSION_FOUND) {
        ESP_ERROR_CHECK(nvs_flash_erase());
        ret = nvs_flash_init();
    }
    ESP_ERROR_CHECK( ret );

    ESP_ERROR_CHECK(esp_bt_controller_mem_release(ESP_BT_MODE_CLASSIC_BT));

    esp_bt_controller_config_t bt_cfg = BT_CONTROLLER_INIT_CONFIG_DEFAULT();
    ret = esp_bt_controller_init(&bt_cfg);
    if (ret) {
        ESP_LOGE(GATTS_TABLE_TAG, "%s enable controller failed: %s", __func__, esp_err_to_name(ret));
        return;
    }

    ret = esp_bt_controller_enable(ESP_BT_MODE_BLE);
    if (ret) {
        ESP_LOGE(GATTS_TABLE_TAG, "%s enable controller failed: %s", __func__, esp_err_to_name(ret));
        return;
    }

    ret = esp_bluedroid_init();
    if (ret) {
        ESP_LOGE(GATTS_TABLE_TAG, "%s init bluetooth failed: %s", __func__, esp_err_to_name(ret));
        return;
    }

    ret = esp_bluedroid_enable();
    if (ret) {
        ESP_LOGE(GATTS_TABLE_TAG, "%s enable bluetooth failed: %s", __func__, esp_err_to_name(ret));
        return;
    }

    ret = esp_ble_gatts_register_callback(gatts_event_handler);
    if (ret){
        ESP_LOGE(GATTS_TABLE_TAG, "gatts register error, error code = %x", ret);
        return;
    }

    ret = esp_ble_gap_register_callback(gap_event_handler);
    if (ret){
        ESP_LOGE(GATTS_TABLE_TAG, "gap register error, error code = %x", ret);
        return;
    }

    ret = esp_ble_gatts_app_register(ESP_APP_ID);
    if (ret){
        ESP_LOGE(GATTS_TABLE_TAG, "gatts app register error, error code = %x", ret);
        return;
    }

    esp_err_t local_mtu_ret = esp_ble_gatt_set_local_mtu(500);
    if (local_mtu_ret){
        ESP_LOGE(GATTS_TABLE_TAG, "set local  MTU failed, error code = %x", local_mtu_ret);
    }
}
```

The main function starts by initializing the non-volatile storage library in
order to be able to save parameters in flash memory.

```c
ret = nvs_flash_init();
```


## BT Controller and Stack Initialization

The main function also initializes the BT controller by first creating a BT
controller configuration structure named `esp_bt_controller_config_t` with
default settings generated by the `BT_CONTROLLER_INIT_CONFIG_DEFAULT()` macro.

The BT controller implements the Host Controller Interface (HCI) on the
controller side, the Link Layer (LL) and the Physical Layer (PHY). The BT
Controller is invisible to the user applications and deals with the lower layers
of the BLE stack. The controller configuration includes setting the BT
controller stack size, priority and HCI baud rate. With the settings created,
the BT controller is initialized and enabled with the `esp_bt_controller_init()`
function:

```c
esp_bt_controller_config_t bt_cfg = BT_CONTROLLER_INIT_CONFIG_DEFAULT();
ret = esp_bt_controller_init(&bt_cfg);
```

Next, the controller is enabled in BLE Mode.

```c
ret = esp_bt_controller_enable(ESP_BT_MODE_BLE);
```

There are four Bluetooth modes supported:

1. `ESP_BT_MODE_IDLE`: Bluetooth not running
2. `ESP_BT_MODE_BLE`: BLE mode
3. `ESP_BT_MODE_CLASSIC_BT`: BT Classic mode
4. `ESP_BT_MODE_BTDM`: Dual mode (BLE + BT Classic)

After the initialization of the BT controller, the Bluedroid stack, which
includes the common definitions and APIs for both BT Classic and BLE, is
initialized and enabled by using:

```c
ret = esp_bluedroid_init();
ret = esp_bluedroid_enable();
```
The Bluetooth stack is up and running at this point in the program flow, however
the functionality of the application has not been defined yet. The functionality
is defined by reacting to events such as what happens when another device tries
to read or write parameters and establish a connection.

The two main managers of events are the GAP and GATT event handlers. The
application needs to register a callback function for each event handler in
order to let the application know which functions are going to handle the GAP
and GATT events:

```c
esp_ble_gatts_register_callback(gatts_event_handler);
esp_ble_gap_register_callback(gap_event_handler);
```

The functions `gatts_event_handler()` and `gap_event_handler()` handle all the
events that are pushed to the application from the BLE stack.

## Application Profiles

This example implements one Application Profile for the Heart Rate Service. An
Application Profile is a way to group functionality which is designed to be used
by one client application, for example one smartphone mobile app. In this way,
different types of profiles can be accommodated in one server.

The Application Profile ID, which is an user-assigned number to identify each
profile, is used to register the profile in the stack, in this example the ID is
0x55.

```c
#define PROFILE_NUM                 1
#define PROFILE_APP_IDX             0
#define ESP_APP_ID                  0x55
```

The profiles are stored in the ``heart_rate_profile_tab`` array. Since there is
only one profile in this example, one element is stored in the array with index
zero as defined by the ``PROFILE_APP_IDX``. Additionally, the profile event
handler callback function is initialized. Each application on the GATT server
uses a different interface, represented by the ``gatts_if`` parameter. For
initialization, this parameter is set to ``ESP_GATT_IF_NONE``, later when the
application is registered, the ``gatts_if`` parameter is updated with the
corresponding interface generated by the stack.

```c
/* One gatt-based profile one app_id and one gatts_if, this array will store the gatts_if returned by ESP_GATTS_REG_EVT */
static struct gatts_profile_inst heart_rate_profile_tab[PROFILE_NUM] = {
    [PROFILE_APP_IDX] = {
        .gatts_cb = gatts_profile_event_handler,
        .gatts_if = ESP_GATT_IF_NONE,       /* Not get the gatt_if, so initial is ESP_GATT_IF_NONE */
    },
};
```

The application registration takes place inside ``app_main()`` using the
``esp_ble_gatts_app_register()`` function:

```c
esp_ble_gatts_app_register(ESP_HEART_RATE_APP_ID);
```

## Setting GAP Parameters

The register application event is the first one that is triggered during the lifetime of the program. This example uses this event to configure advertising parameters upon registration in the profile event handler. The functions used to achieve this are:

* ``esp_ble_gap_set_device_name()``: used to set the advertised device name.
* ``esp_ble_gap_config_adv_data()``: used to configure standard advertising data.

The function used to configure standard Bluetooth Specification advertisement parameters is ``esp_ble_gap_config_adv_data()`` which takes a pointer to an ``esp_ble_adv_data_t`` structure. The ``esp_ble_adv_data_t`` data structure for advertising data has the following definition:

```c
typedef struct {
    bool set_scan_rsp;    /*!< Set this advertising data as scan response or not*/
    bool include_name;    /*!< Advertising data include device name or not */
    bool include_txpower; /*!< Advertising data include TX power */
    int min_interval;     /*!< Advertising data show slave preferred connection min interval */
    int max_interval;     /*!< Advertising data show slave preferred connection max interval */
    int appearance;       /*!< External appearance of device */
    uint16_t manufacturer_len; /*!< Manufacturer data length */
    uint8_t *p_manufacturer_data; /*!< Manufacturer data point */
    uint16_t service_data_len;    /*!< Service data length */
    uint8_t *p_service_data;      /*!< Service data point */
    uint16_t service_uuid_len;    /*!< Service uuid length */
    uint8_t *p_service_uuid;      /*!< Service uuid array point */
    uint8_t flag;         /*!< Advertising flag of discovery mode, see BLE_ADV_DATA_FLAG detail */
} esp_ble_adv_data_t;
```

In this example, the structure is initialized as follows:

```c
static esp_ble_adv_data_t heart_rate_adv_config = {
    .set_scan_rsp = false,
    .include_name = true,
    .include_txpower = true,
    .min_interval = 0x0006,
    .max_interval = 0x0010,
    .appearance = 0x00,
    .manufacturer_len = 0, //TEST_MANUFACTURER_DATA_LEN,
    .p_manufacturer_data =  NULL, //&test_manufacturer[0],
    .service_data_len = 0,
    .p_service_data = NULL,
    .service_uuid_len = sizeof(heart_rate_service_uuid),
    .p_service_uuid = heart_rate_service_uuid,
    .flag = (ESP_BLE_ADV_FLAG_GEN_DISC | ESP_BLE_ADV_FLAG_BREDR_NOT_SPT),
};
```

The minimum and maximum slave preferred connection intervals are set in units of
1.25 ms. In this example, the minimum slave preferred connection interval is
defined as 0x0006 * 1.25 ms = 7.5 ms and the maximum slave preferred connection
interval is initialized as 0x0010 * 1.25 ms = 20 ms.

An advertising payload can be up to 31 bytes of data. It is possible that some
of the parameters surpass the 31-byte advertisement packet limit which causes
the stack to cut the message and leave some of the parameters out. To solve
this, usually the longer parameters are stored in the scan response, which can
be configured using the same ``esp_ble_gap_config_adv_data()`` function and an
additional esp_ble_adv_data_t type structure with the .set_scan_rsp parameter is
set to true. Finally, to set the device name the
``esp_ble_gap_set_device_name()`` function is used. The registering event
handler is shown as follows:

```c
static void gatts_profile_event_handler(esp_gatts_cb_event_t event,
esp_gatt_if_t gatts_if, esp_ble_gatts_cb_param_t *param)
{
    ESP_LOGE(GATTS_TABLE_TAG, "event = %x\n",event);
    switch (event) {
        case ESP_GATTS_REG_EVT:
            ESP_LOGI(GATTS_TABLE_TAG, "%s %d\n", __func__, __LINE__);
            esp_ble_gap_set_device_name(SAMPLE_DEVICE_NAME);
            ESP_LOGI(GATTS_TABLE_TAG, "%s %d\n", __func__, __LINE__);
            esp_ble_gap_config_adv_data(&heart_rate_adv_config);
            ESP_LOGI(GATTS_TABLE_TAG, "%s %d\n", __func__, __LINE__);
...
```

## GAP Event Handler

Once the advertising data have been set, the
``ESP_GAP_BLE_ADV_DATA_SET_COMPLETE_EVT`` is triggered and managed by the GAP
event handler. Moreover, an ``ESP_GAP_BLE_SCAN_RSP_DATA_SET_COMPLETE_EVT`` is
triggered as well if the scan response is also set. Once the configuration of
the advertising and scan response data has been set, the handler can use any of
these events to start advertising, which is done using the
``esp_ble_gap_start_advertising()`` function:

```c
static void gap_event_handler(esp_gap_ble_cb_event_t event, esp_ble_gap_cb_param_t *param)
{
    ESP_LOGE(GATTS_TABLE_TAG, "GAP_EVT, event %d\n", event);

    switch (event) {
    case ESP_GAP_BLE_ADV_DATA_SET_COMPLETE_EVT:
        esp_ble_gap_start_advertising(&heart_rate_adv_params);
        break;
    case ESP_GAP_BLE_ADV_START_COMPLETE_EVT:
        //advertising start complete event to indicate advertising start successfully or failed
        if (param->adv_start_cmpl.status != ESP_BT_STATUS_SUCCESS) {
            ESP_LOGE(GATTS_TABLE_TAG, "Advertising start failed\n");
        }
        break;
    default:
        break;
    }
}
```

The function to start advertising takes a structure of type
``esp_ble_adv_params_t`` with the advertising parameters required.

```c
/// Advertising parameters
typedef struct {
    uint16_t adv_int_min; /*!< Minimum advertising interval for undirected and low duty cycle directed advertising.
    Range: 0x0020 to 0x4000
    Default: N = 0x0800 (1.28 second)
    Time = N * 0.625 msec
    Time Range: 20 ms to 10.24 sec */
    uint16_t adv_int_max; /*!< Maximum advertising interval for undirected and low duty cycle directed advertising.
    Range: 0x0020 to 0x4000
    Default: N = 0x0800 (1.28 second)
    Time = N * 0.625 msec
    Time Range: 20 ms to 10.24 sec */
    esp_ble_adv_type_t adv_type;            /*!< Advertising type */
    esp_ble_addr_type_t own_addr_type;      /*!< Owner bluetooth device address type */
    esp_bd_addr_t peer_addr;                /*!< Peer device bluetooth device address */
    esp_ble_addr_type_t peer_addr_type;     /*!< Peer device bluetooth device address type */
    esp_ble_adv_channel_t channel_map;      /*!< Advertising channel map */
    esp_ble_adv_filter_t adv_filter_policy; /*!< Advertising filter policy */
} esp_ble_adv_params_t;
```

Note that ``esp_ble_gap_config_adv_data()`` configures the data that is
advertised to the client and takes an ``esp_ble_adv_data_t structure``, while
``esp_ble_gap_start_advertising()`` makes the server to actually start
advertising and takes an ``esp_ble_adv_params_t`` structure. The advertising
data is the information that is shown to the client, while the advertising
parameters are the configuration required by the BLE stack to execute.

For this example, the advertisement parameters are initialized as follows:

```c
static esp_ble_adv_params_t heart_rate_adv_params = {
    .adv_int_min        = 0x20,
    .adv_int_max        = 0x40,
    .adv_type           = ADV_TYPE_IND,
    .own_addr_type      = BLE_ADDR_TYPE_PUBLIC,
    //.peer_addr            =
    //.peer_addr_type       =
    .channel_map        = ADV_CHNL_ALL,
    .adv_filter_policy = ADV_FILTER_ALLOW_SCAN_ANY_CON_ANY,
};
```

These parameters configure the advertising interval between 20 ms to 40 ms. The
advertisement is of type ADV_IND, which is generic, not directed to a particular
central device and advertises the server as connectable. The address type is
public, uses all channels and allows both scan and connection requests from any
central.

If the advertising started successfully, an
``ESP_GAP_BLE_ADV_START_COMPLETE_EVT`` event is generated which in this example
is used to check if the advertising status is indeed advertising or otherwise
print an error message.

```c
...
    case ESP_GAP_BLE_ADV_START_COMPLETE_EVT:
        //advertising start complete event to indicate advertising start successfully or failed
        if (param->adv_start_cmpl.status != ESP_BT_STATUS_SUCCESS) {
            ESP_LOGE(GATTS_TABLE_TAG, "Advertising start failed\n");
        }
        break;
...
```

## GATT Event Handlers

When an Application Profile is registered, an ``ESP_GATTS_REG_EVT`` event is
triggered. The parameters of the ``ESP_GATTS_REG_EVT`` are:

```c
esp_gatt_status_t status;    /*!< Operation status */
uint16_t app_id;             /*!< Application id which input in register API */
```

In addition to the previous parameters, the event also contains the GATT
interface assigned by the BLE stack. The event is captured by the
``gatts_event_handler()`` which stores the generated interface in the profile
table and then forwards it to the corresponding profile event handler.

```c
static void gatts_event_handler(esp_gatts_cb_event_t event, esp_gatt_if_t gatts_if, esp_ble_gatts_cb_param_t *param)
{
    ESP_LOGI(GATTS_TABLE_TAG, "EVT %d, gatts if %d\n", event, gatts_if);

    /* If event is register event, store the gatts_if for each profile */
    if (event == ESP_GATTS_REG_EVT) {
        if (param->reg.status == ESP_GATT_OK) {
            heart_rate_profile_tab[HEART_PROFILE_APP_IDX].gatts_if = gatts_if;
        } else {
            ESP_LOGI(GATTS_TABLE_TAG, "Reg app failed, app_id %04x, status %d\n",
                    param->reg.app_id,
                    param->reg.status);
            return;
        }
    }

    do {
        int idx;
        for (idx = 0; idx < HEART_PROFILE_NUM; idx++) {
            if (gatts_if == ESP_GATT_IF_NONE || /* ESP_GATT_IF_NONE, not specify a certain gatt_if, need to call every profile cb function */
            gatts_if == heart_rate_profile_tab[idx].gatts_if) {
                if (heart_rate_profile_tab[idx].gatts_cb) {
                    heart_rate_profile_tab[idx].gatts_cb(event, gatts_if, param);
                }
            }
        }
    } while (0);
}
```

## Creating Services and Characteristics with the Attribute Table

The register event is used to create a table of profile attributes by employing
the ``esp_ble_gatts_create_attr_tab()`` function. This function takes an
argument of type ``esp_gatts_attr_db_t`` which corresponds to a look up table
keyed by the enumeration values defined in the header file.

The ``esp_gatts_attr_db_t`` structure has two members:

```c
esp_attr_control_t    attr_control;       /*!< The attribute control type*/
esp_attr_desc_t       att_desc;           /*!< The attribute type*/
```

The attr_control is the auto-respond parameter which can be set as
``ESP_GATT_AUTO_RSP`` to allow the BLE stack to take care of responding messages
when read or write events arrive. The other option is ``ESP_GATT_RSP_BY_APP``
which allows to manually respond to messages using the
``esp_ble_gatts_send_response()`` function.

The ``att_desc`` is the attribute description which is made of:

```c
uint16_t uuid_length;      /*!< UUID length */
uint8_t  *uuid_p;          /*!< UUID value */
uint16_t perm;             /*!< Attribute permission */
uint16_t max_length;       /*!< Maximum length of the element*/
uint16_t length;           /*!< Current length of the element*/
uint8_t  *value;           /*!< Element value array*/
```

For example, the first element of the table in this example is the service
attribute:

```c
[HRS_IDX_SVC]                       =
    {{ESP_GATT_AUTO_RSP}, {ESP_UUID_LEN_16, (uint8_t *)&primary_service_uuid, ESP_GATT_PERM_READ,
      sizeof(uint16_t), sizeof(heart_rate_svc), (uint8_t *)&heart_rate_svc}},
```

The initialization values are:

* ``[HRS_IDX_SVC]``: Named or designated initializer in the enum table.
* ``ESP_GATT_AUTO_RSP``: Auto respond configuration, set to respond automatically by the stack.
* ``ESP_UUID_LEN_16``: UUID length set to 16 bits.
* ``(uint8_t *)&primary_service_uuid``: UUID to identify the service as a primary one (0x2800).
* ``ESP_GATT_PERM_READ``: Read Permission for the service.
* ``sizeof(uint16_t)``: Maximum length of the service UUID (16 bits).
* ``sizeof(heart_rate_svc)``: Current service length set to the size of the variable *heart_rate_svc*, which is 16 bits.
* ``(uint8_t *)&heart_rate_svc``: Service attribute value set to the variable *heart_rate_svc* which contains the Heart Rate Service UUID (0x180D).

The rest of the attributes is initialized in the same way. Some attributes also
have the *NOTIFY* property which is set by ``&char_prop_notify``. The complete
table structure is initialized as follows:

```c
/// Full HRS Database Description - Used to add attributes into the database
static const esp_gatts_attr_db_t heart_rate_gatt_db[HRS_IDX_NB] =
{
    // Heart Rate Service Declaration
    [HRS_IDX_SVC]                       =
    {{ESP_GATT_AUTO_RSP}, {ESP_UUID_LEN_16, (uint8_t *)&primary_service_uuid, ESP_GATT_PERM_READ,
      sizeof(uint16_t), sizeof(heart_rate_svc), (uint8_t *)&heart_rate_svc}},

    // Heart Rate Measurement Characteristic Declaration
    [HRS_IDX_HR_MEAS_CHAR]            =
    {{ESP_GATT_AUTO_RSP}, {ESP_UUID_LEN_16, (uint8_t *)&character_declaration_uuid, ESP_GATT_PERM_READ,
      CHAR_DECLARATION_SIZE,CHAR_DECLARATION_SIZE, (uint8_t *)&char_prop_notify}},

    // Heart Rate Measurement Characteristic Value
    [HRS_IDX_HR_MEAS_VAL]               =
    {{ESP_GATT_AUTO_RSP}, {ESP_UUID_LEN_16, (uint8_t *)&heart_rate_meas_uuid, ESP_GATT_PERM_READ,
      HRPS_HT_MEAS_MAX_LEN,0, NULL}},

    // Heart Rate Measurement Characteristic - Client Characteristic Configuration Descriptor
    [HRS_IDX_HR_MEAS_NTF_CFG]           =
    {{ESP_GATT_AUTO_RSP}, {ESP_UUID_LEN_16, (uint8_t *)&character_client_config_uuid, ESP_GATT_PERM_READ|ESP_GATT_PERM_WRITE,
      sizeof(uint16_t),sizeof(heart_measurement_ccc), (uint8_t *)heart_measurement_ccc}},

    // Body Sensor Location Characteristic Declaration
    [HRS_IDX_BOBY_SENSOR_LOC_CHAR]  =
    {{ESP_GATT_AUTO_RSP}, {ESP_UUID_LEN_16, (uint8_t *)&character_declaration_uuid, ESP_GATT_PERM_READ,
      CHAR_DECLARATION_SIZE,CHAR_DECLARATION_SIZE, (uint8_t *)&char_prop_read}},

    // Body Sensor Location Characteristic Value
    [HRS_IDX_BOBY_SENSOR_LOC_VAL]   =
    {{ESP_GATT_AUTO_RSP}, {ESP_UUID_LEN_16, (uint8_t *)&body_sensor_location_uuid, ESP_GATT_PERM_READ,
      sizeof(uint8_t), sizeof(body_sensor_loc_val), (uint8_t *)body_sensor_loc_val}},

    // Heart Rate Control Point Characteristic Declaration
    [HRS_IDX_HR_CTNL_PT_CHAR]          =
    {{ESP_GATT_AUTO_RSP}, {ESP_UUID_LEN_16, (uint8_t *)&character_declaration_uuid, ESP_GATT_PERM_READ,
      CHAR_DECLARATION_SIZE,CHAR_DECLARATION_SIZE, (uint8_t *)&char_prop_read_write}},

    // Heart Rate Control Point Characteristic Value
    [HRS_IDX_HR_CTNL_PT_VAL]             =
    {{ESP_GATT_AUTO_RSP}, {ESP_UUID_LEN_16, (uint8_t *)&heart_rate_ctrl_point, ESP_GATT_PERM_WRITE|ESP_GATT_PERM_READ,
      sizeof(uint8_t), sizeof(heart_ctrl_point), (uint8_t *)heart_ctrl_point}},
};
```

## Starting the Service
When the attribute table is created, an ``ESP_GATTS_CREAT_ATTR_TAB_EVT`` event is triggered. This event has the following parameters:

```c
esp_gatt_status_t status;    /*!< Operation status */
esp_bt_uuid_t svc_uuid;      /*!< Service uuid type */
uint16_t num_handle;         /*!< The number of the attribute handle to be added to the gatts database */
uint16_t *handles;           /*!< The number to the handles */
```

This example uses this event to print information and to check that the size of the created table equals the number of elements in the enumeration HRS_IDX_NB. If the table is correctly created, the attribute handles are copied into the handle table heart_rate_handle_table and the service is started using the ``esp_ble_gatts_start_service()`` function:

```c
case ESP_GATTS_CREAT_ATTR_TAB_EVT:{
        ESP_LOGI(GATTS_TABLE_TAG, "The number handle =%x\n",param->add_attr_tab.num_handle);
        if (param->add_attr_tab.status != ESP_GATT_OK){
            ESP_LOGE(GATTS_TABLE_TAG, "Create attribute table failed, error code=0x%x", param->add_attr_tab.status);
        }
        else if (param->add_attr_tab.num_handle != HRS_IDX_NB){
            ESP_LOGE(GATTS_TABLE_TAG, "Create attribute table abnormally, num_handle (%d) \
                    doesn't equal to HRS_IDX_NB(%d)", param->add_attr_tab.num_handle, HRS_IDX_NB);
        }
        else {
            memcpy(heart_rate_handle_table, param->add_attr_tab.handles, sizeof(heart_rate_handle_table));
            esp_ble_gatts_start_service(heart_rate_handle_table[HRS_IDX_SVC]);
        }
        break;
```
The handles stored in the handles pointer of the event parameters are numbers
that identify each attribute. The handles can be used to know which
characteristic is being read or written to, therefore they can be passed around
and to upper layers of the application to handle different actions.

Finally, the heart_rate_handle_table contains the Application Profile in the
form of a structure with information about the attribute parameters as well as
GATT interface, connection ID, permissions and application ID. The profile
structure is shown as follows, note that not all members are used in this
example:

```c
struct gatts_profile_inst {
    esp_gatts_cb_t gatts_cb;
    uint16_t gatts_if;
    uint16_t app_id;
    uint16_t conn_id;
    uint16_t service_handle;
    esp_gatt_srvc_id_t service_id;
    uint16_t char_handle;
    esp_bt_uuid_t char_uuid;
    esp_gatt_perm_t perm;
    esp_gatt_char_prop_t property;
    uint16_t descr_handle;
    esp_bt_uuid_t descr_uuid;
};
```

# Interaction with the GATT Server

There are many tools that allow you to manage the connection to the GATT server.
On Linux, we will use `hcitool` and` gatttool`. In Windows, you can use a tool
called `Bluetooth LE Explorer`, that implements, albeit graphically, the same
functionality.

For this part of the lab assignment, you have to make visible the bluetooth
controller of your host machine (laptop/pc) to the virtual machine used for the
course.

## Using `hcitool` and `gatttool` in client mode

### Scanning available devices: `hcitool`

`hcitool` is a command line tool that allows you to manage the Bluetooth
interface of the computer on which it is running. In our case, We will need to
determine the Bluetooth MAC address of our server.  To do this, first of all, we
will perform a scan of the devices BLE available in the environment using the
command:

```sh
sudo hcitool lescan
```

!!! danger "Note"
	This command will not work if you did not make the bluetooth controller
	available to the virtual machine.

If all went well, one line per available BLE device in the announcement phase
will be displayed. Among them, we must find our device, and annotate its MAC
address.

!!! note "Task"
	Edit the file `main/gatts_table_creat_demo.c` and modify the name of your
	device, which will be announced in each emmited advertisment packet in the
	`advertising` phase. You can achieve this by modifying the corresponding
	field of the structure `raw_adv_data`. Next, compile and flash the example,
	and start a session of scanning of BLE devices using the command:

	```
	sudo hcitool lescan
	```

	You should see your device on one of the output lines. Write down or
	remember its MAC address.

### Interacting with the GATT server: `gatttool`.

!!! danger "Task 4.1"
	Write a small pdf report documenting all the steps and Tasks in this
	section.

Once the Bluetooth MAC address of the device is obtained, we must proceed in two
phases. The first one is to pair it to the ESP device. The second, the
interaction with the GATT table. In both cases, you will use the `gatttool` tool
from the command line.

To start a `gatttool` session, we'll invoke the tool in interactive mode, using
the command:

```sh
gatttool -b MAC -I
```

This will open an interactive console, waiting for the corresponding commands.

To perform the pairing, and considering that the Bluetooth MAC is already known,
we will use the `connect` command. If everything went well, we should observe a
change in the color of the prompt, and the *Connection successful* message. At
this point, see how the debugging output of ESP32 shows the messages
corresponding to the pairing process.

From the `gatttool` terminal, you can run the command `help` to get help (in the
form of a list of available commands):

```sh
gatttool -b 24:6F:28:36:60:B2 -I
[24:6F:28:36:60:B2][LE]> connect
Attempting to connect to 24:6F:28:36:60:B2
Connection successful
[24:6F:28:36:60:B2][LE]> help
help                                           Show this help
exit                                           Exit interactive mode
quit                                           Exit interactive mode
connect         [address [address type]]       Connect to a remote device
disconnect                                     Disconnect from a remote device
primary         [UUID]                         Primary Service Discovery
included        [start hnd [end hnd]]          Find Included Services
characteristics [start hnd [end hnd [UUID]]]   Characteristics Discovery
char-desc       [start hnd] [end hnd]          Characteristics Descriptor Discovery
char-read-hnd   <handle>                       Characteristics Value/Descriptor Read by handle
char-read-uuid  <UUID> [start hnd] [end hnd]   Characteristics Value/Descriptor Read by UUID
char-write-req  <handle> <new value>           Characteristic Value Write (Write Request)
char-write-cmd  <handle> <new value>           Characteristic Value Write (No response)
sec-level       [low | medium | high]          Set security level. Default: low
mtu             <value>                        Exchange MTU for GATT/ATT
```

We'll start by looking at the list of GATT server features.

!!! note "Task"
	Using the corresponding command (`characteristics`), consult and write down
	the features available on your GATT server.

One of these characteristics will be of crucial interest, since it will allow us
access, through its UUID, the instant heart rate measurement value, as well as
as well as the notification settings on that value. To determine which of the
lines is the one that interests us, look at the returned UUID value for each of
them, and determine, based on the macro `GATTS_CHAR_UUID_TEST_A` which one is
it.

To interact with this feature, we will need to know its handler, to use it as a
parameter in the `gatttool` commands. This handler is shown, for each line,
after the string *char value handle*.

!!! note "Task"
	The handler that allows reading the *Heart Rate Value* has associated a
	handler of type character. Write its value down.

To read the value of the characteristic we can use the read command, using the
annotated handler as argument (`char-read-hnd handler`).

!!! note "Task"
	Read the heart rate monitoring value characteristic. What do you obtain? You
	should observe a four-byte return value with value 0x00. These values
	correspond to those of the `char_value` variable in your code. Modify them,
	rebuild the project and *flash* it on the ESP32. Repeat the read. Did you
	read the new value?

!!! note "Task"
	Now try to write to the characteristic. Use the command `char-write-cmd
	handler value`, where value is, for example, `11223344`. It's possible?
	Why?


We will now write to its client configuration characteristic descriptor. Its hancler
is the handler of the characteristic's value plus one. For instance, if the
handle for the value is `0x0001`, its cliente configuration characteristic
would have the handle `0x0002`.

!!! note "Task"
	Try now to write to the client configuration characteristic. Use the command
	`char-write-cmd handler value`, where value is, for example, `0100`. It's
	possible? Why?

### Task 4.2

As you may have noticed, it is possible to read from the monitoring value,
and write to config value. We will use this last feature to configure
notifications about the monitoring value. This way, each time the value
changes, the clients that have activated the notifications will receive the
new value.

To achieve this we need to modify some parts of our code. Specifically, we
will need:

1. Create a new task that periodically modifies the heart rate value (in our
   case generating a new random value). This task will consist of an
   infinite loop that, generates a new value for the characteristic and
   correctly updates the gatt table. Then, if notifications have been
   activated, it sends the new value to the clients:

```c
static void publish_data_task(void *pvParameters)
{
	while (1) {
		ESP_LOGI("APP", "Sending data...");

		// Paso 1: Actualizo valor...

		// Paso 2: Si notificación activa...

		// Paso 3: Envío datos...

		// Paso 4: Duermo un segundo...
		vTaskDelay( 1000. / portTICK_PERIOD_MS);
	}
}
```

This routine should be created in response to the connection event by a
client, using, for example, the invocation to:

```c
xTaskCreate(&publish_data_task, "publish_data_task", 4096, NULL, 5, NULL);
```

2. The update of the value, carried out periodically and randomly, will modify
byte 1 of the heart rate value, taking a random value between 0 and 255 (as an
additional note, current heart rate monitors support values higher for heart
rate, although the configuration of this functionality is outside the scope of
practice), and then update the internal gatt table using the
[`esp_ble_gatts_set_attr_value`](https://docs.espressif.com/projects/esp-idf/en/latest/esp32/api-reference/bluetooth/esp_gatts.html?highlight=esp_ble_gatts_set_attr_value#_CPPv428esp_ble_gatts_set_attr_value8uint16_t8uint16_tPK7uint8_t)
function.

3. The verification of the activation or not of the notification is done by
consulting the two bytes of the corresponding client configuration
characteristic. If these values are `0x01` and` 0x00` (positions 0 and 1,
respectively), the notifications are active, and therefore, the notification
shall be sent. You will need to use the function
[`esp_ble_gatts_get_attr_value`](https://docs.espressif.com/projects/esp-idf/en/latest/esp32/api-reference/bluetooth/esp_gatts.html?highlight=esp_ble_gatts_get_attr_value#_CPPv428esp_ble_gatts_get_attr_value8uint16_tP8uint16_tPPK7uint8_t)
to read this descriptor.

4. To send the notification, we will use the following function:

```c
esp_ble_gatts_send_indicate(heart_rate_profile_tab[0].gatts_if,
									  heart_rate_profile_tab[0].conn_id,
									  heart_rate_handle_table[IDX_CHAR_VAL_A],
									  sizeof(char_value), char_value, false);
```

The activation of notifications from `gatttool` will be done by writing the
value `0x0100` in the client configuration characteristic, this is:

```sh
char-write-cmd HANDLER 0100
```

If you also modify the UUIDs by those provided in the specification of Bluetooth
for the *Heart Rate Service*, and everything has been configured correctly, your
ESP32 should be able to interface with any heart rate monitor to, for example,
Android. To do this, use the following UUIDs:

* static const uint16_t GATTS_SERVICE_UUID_TEST      = 0x180D; //0x00FF;
* static const uint16_t GATTS_CHAR_UUID_TEST_A       = 0x2A37; //0xFF01;
* static const uint16_t GATTS_CHAR_UUID_TEST_B       = 0x2A38; //0xFF02;
* static const uint16_t GATTS_CHAR_UUID_TEST_C       = 0x2A39; //0xFF03;

Deliver the modified code with a small pdf report showing how you activate the
notifications with gatttool, and how the node then sends a new value every
second.

