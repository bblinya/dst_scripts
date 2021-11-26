#!/bin/bash

source common.sh

cp ${TEMPLATE_DIR}/dedicated_server_mods_setup.lua "$DST_HOME/mods/"

# neccessary, to find relative files
cd "${DST_HOME}/bin"

./dontstarve_dedicated_server_nullrenderer \
	-cluster $CLUSTER_NAME \
	-only_update_server_mods
