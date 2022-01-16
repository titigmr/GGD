#!/bin/bash

if [ $* = "firefox" ];
    then
    wget https://github.com/mozilla/geckodriver/releases/download/v0.30.0/geckodriver-v0.30.0-linux64.tar.gz
    tar -zxvf geckodriver-v0.30.0-linux64.tar.gz
    rm geckodriver-v0.30.0-linux64.tar.gz
    mv geckodriver /usr/local/bin/

elif [ $* = 'chrome' ]
    then
    wget https://chromedriver.storage.googleapis.com/98.0.4758.48/chromedriver_linux64.zip
    unzip chromedriver_linux64.zip
    rm chromedriver_linux64.zip
    mv chromedriver /usr/local/bin/

else
    echo "Incorrect input value: $*"
    exit 1
fi
