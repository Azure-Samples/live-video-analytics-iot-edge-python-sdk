# Python app for playing Media Services Assets

This directory contains a Python sample app that showcases how to playback assets recorded by Live Video Analytics on IoT Edge.

## Contents

Most of the files in the folder are automatically generated when you create a Flask project. Some notable files include the following.

* **amsHelper.py** - Contains code for invoking calls to Azure Media Services.
* **app/routes.py** - Contains the backend code which translate requests into HTML responses.
* **app/templates** - Contains the HTML for the frontend.

This sample uses [Azure Media Player](https://aka.ms/azuremediaplayer) to host an embedded player in the browser.

## Setup

Create the file `.env` in `src/ams-asset-player` and add the following text to it. Read [How to access Media Services API](https://docs.microsoft.com/en-us/azure/media-services/latest/access-api-howto) to understand how to get the values for these parameters.

```env
SUBSCRIPTION_ID=""
RESOURCE_GROUP=""
AMS_ACCOUNT=""
AAD_TENANT_ID=""
AAD_CLIENT_ID=""
AAD_SECRET=""
SECRET_KEY=""
```

- `SECRET_KEY` can be any randomly generated secret.

## Running the sample

* Install the python packages from `requirements.txt`. Do do this, run `pip install -r src/ams-asset-player/requirements.txt`.
* From Visual Studio Code menu, select **View --> Run** and then click on the drop-down at the top of the "Run" pane and select **"AMS Asset Player - Python/Flask"**.
* Hit F5 to start debugging. This will result in your browser getting launched, or you can navigate to [http://localhost:8000]().
* Enter the name of the Media Services asset that you would like to play and hit the Submit button.

## Next steps

Review [this](https://docs.microsoft.com/azure/media-services/live-video-analytics-edge/playback-multi-day-recordings-tutorial) tutorial on how to create a multi-day recording, and try the other features of this application.