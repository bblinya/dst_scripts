#!/bin/bash

source common.sh

$STEAM_CMD_HOME/steamcmd.sh \
	+@ShutdownOnFailedCommand 1 \
	+@NoPromptForPassword 1 \
	+login anonymous \
	+force_install_dir ${DST_HOME} \
	+app_update 343050 validate +quit

cd ${DST_HOME}/bin
./dontstarve_dedicated_server_nullrenderer \
	-cluster $CLUSTER_NAME \
	-only_update_server_mods
