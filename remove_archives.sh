#!/bin/bash

source common.sh


if [ -d "$CLUSTER_PATH/Master" ]; then
	echo "Remove DST forest archieve"
	rm -rf "$CLUSTER_PATH/Master/save/session"
	rm -rf "$CLUSTER_PATH/Master/save/server_temp"
fi

if [ -d "$CLUSTER_PATH/Caves" ]; then
	echo "Remove DST cave archieve"
	rm -rf "$CLUSTER_PATH/Caves/save/session"
	rm -rf "$CLUSTER_PATH/Caves/save/server_temp"
fi
