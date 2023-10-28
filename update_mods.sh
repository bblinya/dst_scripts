#!/bin/bash

source common.sh

python ${TEMPLATE_DIR}/generator.py

# the setup config cannot be link, since it will override this file.
cp -f ${TEMPLATE_DIR}/dedicated_server_mods_setup.lua ${DST_HOME}/mods/

# neccessary, to find relative files
cd "${DST_HOME}/bin"

proxychains ./dontstarve_dedicated_server_nullrenderer \
  -cluster ${CLUSTER_NAME} \
  -only_update_server_mods
