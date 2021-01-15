---
page_type: sample
languages:
  - python
products:
  - azure
  - azure-media-services
  - azure-live-video-analytics
description: "The samples in this repo show how to use the Live Video Analytics on IoT Edge that enables you to capture, record, and analyze videos using AI."  
---

# Live Video Analytics on IoT Edge samples

This repo provides Python samples for Live Video Analytics on IoT Edge

## Contents

| File/folder          | Description                                |
|----------------------|--------------------------------------------|
| `src`                | Sample source code.                        |
| `.gitignore`         | Defines what to ignore at commit time.     |
| `README.md`          | This README file.                          |
| `LICENSE`            | The license for the sample.                |
| `SECURITY`           | Guidelines for reporting security issues   |
| `CODE_OF_CONDUCT.md` | Open source code of conduct                |

The 'src' folder contains three sub-folders

* **cloud-to-device-console-app** - This folder contains a Python app that enables you to invoke direct methods of Live Video Analytics on IoT Edge module, with parameters defined by you in a JSON file (operations.json).
* **edge** - This folder has a few IoT Edge deployment manifest templates, along with sample code for an IoT Edge module (under 'modules' folder) that can be used in conjunction with the Live Video Analytics on IoT Edge module.
* **ams-asset-player** - This folder contains a Python app that showcases how you can playback assets recorded by Live Video Analytics on IoT Edge (in the Azure Media Services account referenced in the module twin properties).

## Prerequisites

1. An active Azure subscription
2. Azure resources deployed in the Azure subscription

    a. IoT Hub

    b. Storage Account

    c. Media Services

    d. Azure container registry

3. A Linux edge device with [IoT Edge runtime](https://docs.microsoft.com/en-us/azure/iot-edge/how-to-install-iot-edge-linux)

4. [Visual Studio Code](https://code.visualstudio.com/) on your development machine with following extensions

    a. [Azure IoT Tools](https://marketplace.visualstudio.com/items?itemName=vsciot-vscode.azure-iot-tools)

    b. [Python](https://marketplace.visualstudio.com/items?itemName=ms-python.python)

5. [Docker](https://docs.docker.com/engine/install/) on your development machine

> [!TIP]
> You can use the [LVA resources setup script](https://github.com/Azure/live-video-analytics/tree/master/edge/setup) to deploy the Azure resources mentioned above, along with an Azure Linux VM to serve as your IoT Edge device.

## Setup

After cloning the repository, follow instructions outlined in **src/cloud-to-device-console-app/readme.md** to setup the console app and instructions in **src/ams-asset-player/readme.md** to setup the player app.

## Running the sample

Follow instructions outlined in **src/cloud-to-device-console-app/readme.md** to run the console app and instructions in **src/ams-asset-player/readme.md** to run the player app.

## Key concepts

Read [Live Video Analytics on IoT Edge concepts](https://docs.microsoft.com/en-us/azure/media-services/live-video-analytics-edge/overview)

## Code of conduct

This project has adopted the [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/). For more information see the [Code of Conduct FAQ](https://opensource.microsoft.com/codeofconduct/faq/) or
contact [opencode@microsoft.com](mailto:opencode@microsoft.com) with any additional questions or comments.
