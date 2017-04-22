#!/usr/bin/env bash

$(pwd)/tools/helper/go.py --basepath $(pwd) --config $(pwd)/tools/helper/config.json --action link
$(pwd)/tools/helper/go.py --basepath $(pwd) --config $(pwd)/tools/helper/config.json --action patch
$(pwd)/tools/helper/go.py --basepath $(pwd) --config $(pwd)/tools/helper/config.json --action sass
