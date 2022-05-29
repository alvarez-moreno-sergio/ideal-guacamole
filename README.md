# ideal-guacamole

## Overview
This project aims to be fed with your own Binance API and to give you useful metrics. It is intended to be run each 24h or so, to save daily data and be able to generate metrics.
The information will be saved in your own MongoDB instance.

## Features
Some examples of already implemented metrics:
  - Your Spot balance shown in Euros
  - Your Earn balance shown in Euros
  - Your Global balance shown in Euros
  - Information about tokens:
    - Current price
    - Owning quantity in Spot market
    - Owning quantity in Earn market
    - :sparkles: Global balance for this token, including earn products and spot assets

When finished running, this script will save your updated token collection with all attributes in Mongo database.

## Incoming features
- Run queries against db to obtain metrics 
- Show some useful information like:
  - Percentage of change for spot balance
  - Percentage of change for earn balance
  - Percentage of change for global balance
  - Percentage of change for each token's global balance

## Required Modules
The following python modules are required. You can install them with `pip install module_name`:
- python-binance
- pymongo

## Configuration
Your `./secrets.ini` file should look like this:
````
{"binance_api_uri": "https://api.binance.com", "api_key": "Your API KEY here", "api_secret": "Your SECRET key here"}
````

Please change the following variables:
- api_key
- api_secret

You can get your own key at: https://www.binance.com/en/my/settings/api-management

## Running
To exec this script, use the following command:
`````
python3 app.py
