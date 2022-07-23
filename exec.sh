#!/bin/bash

source common.sh

# init possible log files
mkdir -p ${DST_KLEI}/${CLUSTER_NAME}
ln -sf ${TEMPLATE_DIR}/init_worldgenoverride.lua ${DST_KLEI}/${CLUSTER_NAME}/worldgenoverride.lua

ln -sf ${TEMPLATE_DIR}/cluster.ini ${DST_KLEI}/${CLUSTER_NAME}/
ln -sf ${TEMPLATE_DIR}/cluster_token.txt ${DST_KLEI}/${CLUSTER_NAME}/

mkdir -p ${DST_KLEI}/${CLUSTER_NAME}/Master
cp -f ${TEMPLATE_DIR}/worldgenoverride.lua ${DST_KLEI}/${CLUSTER_NAME}/Master/
ln -sf ${TEMPLATE_DIR}/modoverrides.lua $DST_KLEI/$CLUSTER_NAME/Master/
ln -sf ${TEMPLATE_DIR}/master_server.ini ${DST_KLEI}/${CLUSTER_NAME}/Master/server.ini

mkdir -p ${DST_KLEI}/${CLUSTER_NAME}/Caves
cp -f ${TEMPLATE_DIR}/cave_worldgenoverride.lua ${DST_KLEI}/${CLUSTER_NAME}/Caves/worldgenoverride.lua
ln -sf ${TEMPLATE_DIR}/modoverrides.lua $DST_KLEI/$CLUSTER_NAME/Caves/
ln -sf ${TEMPLATE_DIR}/cave_server.ini ${DST_KLEI}/${CLUSTER_NAME}/Caves/server.ini

function check_for_file()
{
	if [ ! -e "$1" ]; then
		fail "Missing file: $1"
	fi
}

check_for_file "$DST_KLEI/$CLUSTER_NAME/cluster.ini"
check_for_file "$DST_KLEI/$CLUSTER_NAME/cluster_token.txt"
check_for_file "$DST_KLEI/$CLUSTER_NAME/Master/server.ini"
check_for_file "$DST_KLEI/$CLUSTER_NAME/Caves/server.ini"

cd "$steamcmd_dir" || fail "Missing $steamcmd_dir directory!"
run_shared=("${DST_HOME}/bin/dontstarve_dedicated_server_nullrenderer")
# run_shared+=(-steam_authentication_port 12345 -steam_master_server_port 12346)
run_shared+=(-cluster "$CLUSTER_NAME")
run_shared+=(-monitor_parent_process $$)
run_shared+=(-shard)

cd ${DST_HOME}/bin

"${run_shared[@]}" Caves | sed 's/^/Caves: /' &
"${run_shared[@]}" Master | sed 's/^/Master: /'
