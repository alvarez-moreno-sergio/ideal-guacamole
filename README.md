# ideal-guacamole

## Overview
This project aims to be fed with your own Binance API and to give you useful metrics. It is intended to be run each 24h or so, to save daily data and be able to generate metrics.

## Features
Some examples of already implemented metrics:
  - Your Spot balance shown in Euros
  - Your Earn balance shown in Euros
  - Your Global balance shown in Euros
  - Information about tokens:
    - Current price
    - Owning quantity in Spot market
    - Owning quantity in Earn market
    - Global balance for this token

When finished running, this script will serialize your updated token collection with all attributes (for future uses).

## Incoming features
- Deserialize saved file to obtain metrics 
- Show some useful information like:
  - Percentage of change for spot balance
  - Percentage of change for earn balance
  - Percentage of change for global balance
  - Percentage of change for global balance for each token

## Configuration
Your `./secrets.ini` file should look like this:
````
{"binance_api_uri": "https://api.binance.com", "api_key": "Your API KEY here", "api_secret": "Your SECRET key here"}
````

Please change the following variables:
- api_key
- api_secret

You can get your own key at: https://www.binance.com/en/my/settings/api-management
