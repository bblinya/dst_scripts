#!/bin/bash

source common.sh

source setup.sh

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

mkdir -p ${LOG_DIR}
find ${LOG_DIR} -mtime +3 -name "dst.log.*" -exec rm -rf {} \;

LOG_FILE="${LOG_DIR}/dst.log.$(date +%m-%d,%H.%M.%S)"
ln -sf ${LOG_FILE} "${LOG_DIR}/dst.log"

# unbuffer echo "log file: ${LOG_FILE}" | tee ${LOG_FILE}
# exit

cd ${DST_HOME}/bin

stdbuf -oL "${run_shared[@]}" Caves  2>&1 | sed -u 's/^/ Caves: /' | tee -a ${LOG_FILE} & 
stdbuf -oL "${run_shared[@]}" Master 2>&1 | sed -u 's/^/Master: /' | tee -a ${LOG_FILE}
