#!/bin/bash

source common.sh

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
LOG_DIR="${SCRIPT_DIR}/logs"

find ${LOG_DIR} -mtime +3 -name ".*dst.log" -exec rm -rf {} \;

# init possible log files
mkdir -p ${DST_KLEI}/${CLUSTER_NAME}
# ln -sf ${TEMPLATE_DIR}/worldgenoverride_init.lua ${DST_KLEI}/${CLUSTER_NAME}/worldgenoverride.lua

ln -sf ${TEMPLATE_DIR}/cluster.ini ${DST_KLEI}/${CLUSTER_NAME}/
ln -sf ${TEMPLATE_DIR}/cluster_token.txt ${DST_KLEI}/${CLUSTER_NAME}/

mkdir -p ${DST_KLEI}/${CLUSTER_NAME}/Master
cp -f ${TEMPLATE_DIR}/worldgenoverride_much.lua ${DST_KLEI}/${CLUSTER_NAME}/Master/worldgenoverride.lua
ln -sf ${TEMPLATE_DIR}/modoverrides.lua $DST_KLEI/$CLUSTER_NAME/Master/
ln -sf ${TEMPLATE_DIR}/server_master.ini ${DST_KLEI}/${CLUSTER_NAME}/Master/server.ini

mkdir -p ${DST_KLEI}/${CLUSTER_NAME}/Caves
cp -f ${TEMPLATE_DIR}/worldgenoverride_much_cave.lua ${DST_KLEI}/${CLUSTER_NAME}/Caves/worldgenoverride.lua
ln -sf ${TEMPLATE_DIR}/modoverrides.lua $DST_KLEI/$CLUSTER_NAME/Caves/
ln -sf ${TEMPLATE_DIR}/server_cave.ini ${DST_KLEI}/${CLUSTER_NAME}/Caves/server.ini

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

LOG_FILE="${LOG_DIR}/dst.log.$(date +%Y-%m-%d.%H:%M:%S)"
ln -sf ${LOG_FILE} "${LOG_DIR}/dst.log"

# unbuffer echo "log file: ${LOG_FILE}" | tee ${LOG_FILE}
# exit

cd ${DST_HOME}/bin

stdbuf -oL "${run_shared[@]}" Caves  2>&1 | sed -u 's/^/ Caves: /' | tee -a ${LOG_FILE} & 
stdbuf -oL "${run_shared[@]}" Master 2>&1 | sed -u 's/^/Master: /' | tee -a ${LOG_FILE}
