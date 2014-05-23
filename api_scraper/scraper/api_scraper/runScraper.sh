#!/bin/bash

export PYTHON=/Users/ampushkrush/Frameworks/Python.framework/Versions/2.7/bin/python
export PYTHONPATH=/Users/ampushkrush/eclipse/workspace/ApiSouper/api_scraper/scraper:/Users/ampushkrush/eclipse/workspace/ApiSouper/api_scraper
export DJANGO_SETTINGS_MODULE=scraper.settings
export SCRAPER=/Users/ampushkrush/eclipse/workspace/ApiSouper/api_scraper/scraper/api_scraper/prog_web_scraper.py

$PYTHON $SCRAPER $* 2>&1 | tee -a output.txt
