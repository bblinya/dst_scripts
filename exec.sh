#!/bin/bash

source common.sh

function check_for_file()
{
	if [ ! -e "$1" ]; then
		fail "Missing file: $1"
	fi
}

cd "$steamcmd_dir" || fail "Missing $steamcmd_dir directory!"

check_for_file "$DST_KLEI/$CLUSTER_NAME/cluster.ini"
check_for_file "$DST_KLEI/$CLUSTER_NAME/cluster_token.txt"
check_for_file "$DST_KLEI/$CLUSTER_NAME/Master/server.ini"
check_for_file "$DST_KLEI/$CLUSTER_NAME/Caves/server.ini"

run_shared=("${DST_HOME}/bin/dontstarve_dedicated_server_nullrenderer")
# run_shared+=(-steam_authentication_port 12345 -steam_master_server_port 12346)
run_shared+=(-cluster "$CLUSTER_NAME")
run_shared+=(-monitor_parent_process $$)
run_shared+=(-shard)

cd ${DST_HOME}/bin

"${run_shared[@]}" Caves | sed 's/^/Caves: /' &
"${run_shared[@]}" Master | sed 's/^/Master: /'
