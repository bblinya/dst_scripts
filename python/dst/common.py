import os
import sys
import logging
from os import path

CODE_ROOT = path.dirname(path.dirname(
    path.dirname(path.realpath(__file__))))
TEMP_ROOT = path.join(CODE_ROOT, "templates")

STEAM_CMD_HOME = path.expandvars("$HOME/steamcmd")
STEAM_CMD = path.join(STEAM_CMD_HOME, "steamcmd.sh")

DST_HOME=path.expandvars("$HOME/dst")
DST_BIN_HOME = path.join(DST_HOME, "bin")
DST_KLEI=path.expandvars("$HOME/.klei/DoNotStarveTogether")

CLUSTER = os.environ.get("CLUSTER", "")

ALL_CLUSTERS = os.listdir(DST_KLEI)
ALL_CLUSTERS = [c for c in ALL_CLUSTERS \
        if path.isdir(path.join(DST_KLEI, c))]
ALL_CLUSTERS = [c for c in ALL_CLUSTERS \
        if path.exists(path.join(DST_KLEI, c, "cluster.ini"))]

def env_check():
    if not CLUSTER:
        logging.error("env CLUSTER is not set.")
        logging.info("Add CLUSTER=? before command.")
        logging.info("Existing Clusters: %s" % ", ".join(ALL_CLUSTERS))
        logging.info("Or execute: export CLUSTER=?")
        sys.exit(-1)

    # logging.info("Init Cluster: %s" % CLUSTER)

CLUSTER_PATH = path.join(DST_KLEI, CLUSTER)

def get_screen_name(cluster_name):
    return "dst_server_" + cluster_name
SCREEN_NAME = get_screen_name(CLUSTER)

LOG_DIR = path.join(CODE_ROOT, "logs_" + CLUSTER)
os.makedirs(LOG_DIR, exist_ok=True)
