#!/bin/bash

source common.sh

if [ -d "$CLUSTER_PATH/Master" ]; then
	echo "Copy mod config into DST Forest"
	cp ${TEMPLATE_DIR}/modoverrides.lua "$DST_KLEI/$CLUSTER_NAME/Master"
else
	echo "DST forest not exits"
fi

if [ -d "$CLUSTER_PATH/Caves" ]; then
	echo "Copy mod config into DST Cave"
	cp ${TEMPLATE_DIR}/modoverrides.lua "$DST_KLEI/$CLUSTER_NAME/Caves"
else
	echo "DST cave not exits"
fi

