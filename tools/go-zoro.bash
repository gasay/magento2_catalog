#!/usr/bin/env bash

$(pwd)/tools/helper/go.py --basepath $(pwd) --config $(pwd)/tools/helper/config.json --action system
$(pwd)/tools/helper/go.py --basepath $(pwd) --config $(pwd)/tools/helper/config.json --action composer
