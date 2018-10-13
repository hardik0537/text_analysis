#!/bin/sh

echo 'Extrating and cleaning the data'

python EC.py

echo 'Done with data extraction and cleaning'

python sentiment_analysis.py

echo 'Processing the data Done'

python load_elasticsearch.py

echo 'Loaded the data in the Elastic Search'
