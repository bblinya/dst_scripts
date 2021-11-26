#!/bin/bash

source common.sh

run_shared=("${DST_HOME}/bin/dontstarve_dedicated_server_nullrenderer")
run_shared+=(-console)
run_shared+=(-cluster "$CLUSTER_NAME")
run_shared+=(-monitor_parent_process $$)
run_shared+=(-shard)

cd ${DST_HOME}/bin

"${run_shared[@]}" Caves | sed 's/^/Caves: /' &
"${run_shared[@]}" Master | sed 's/^/Master: /'
