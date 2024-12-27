
DST_BIN_HOME=$1

run_shared=("$1/dontstarve_dedicated_server_nullrenderer")
run_shared+=(-cluster "$2")
run_shared+=(-monitor_parent_process $$)
run_shared+=(-shard)

LOG_FILE=$3

# unbuffer echo "log file: ${LOG_FILE}" | tee ${LOG_FILE}
# exit

cd ${DST_BIN_HOME}

stdbuf -oL "${run_shared[@]}" Caves  2>&1 | sed -u 's/^/ Caves: /' | tee -a ${LOG_FILE} & 
stdbuf -oL "${run_shared[@]}" Master 2>&1 | sed -u 's/^/Master: /' | tee -a ${LOG_FILE}
