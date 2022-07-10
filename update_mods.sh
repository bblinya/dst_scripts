#!/bin/bash

source common.sh

# neccessary, to find relative files
cd "${DST_HOME}/bin"

./dontstarve_dedicated_server_nullrenderer -only_update_server_mods
