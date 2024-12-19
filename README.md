<a href="https://www.buymeacoffee.com/qG6DdXgzah" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-blue.png" alt="Buy Me A Coffee" style="height: 60px !important;width: 217px !important;" ></a>
# homeassistant-solax-http
This is Home Assistant integration for SolaX local API.
Work is based on https://github.com/wills106/homeassistant-solax-modbus and all credits for initial conception work go there.

There are some Modbus registers which I skipped because I think it is not interesting. If you see something useful in EVC Modbus document what is not here, let me know.
HTTP API is not 1:1 to Modbus but there is high chance that I can add required sensor.

This has to be taken as only other mean of communication where Modbus is not possible.

Please write only issues specific to Http API here.
All other stuff is common and should be discussed in https://github.com/wills106/homeassistant-solax-modbus

# Supported devices
G1 SolaX EV Charger X3 is supported.
G2 SolaX Smart EV Charger support is under development and testing.
Let me know if you have other device and you are interested in integrating it. Physical device is required as there is no documentation available.

# Installation
This repository is compatible with HACS. You can use this link to install the integration.
[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=PatrikTrestik&repository=homeassistant-solax-http&category=integration)

# Available entities
![image](https://github.com/PatrikTrestik/homeassistant-solax-http/assets/17616747/e7faad55-d647-4736-93a3-8fc22917d20c)
![image](https://github.com/PatrikTrestik/homeassistant-solax-http/assets/17616747/299655fc-cb52-41d0-97d4-0ff0c9a103af)
![image](https://github.com/PatrikTrestik/homeassistant-solax-http/assets/17616747/2bad6d88-91ca-4656-aea1-4bf53a12fa38)
![image](https://github.com/PatrikTrestik/homeassistant-solax-http/assets/17616747/659b9fff-2898-4cb8-a911-38eaa7261fe0)


