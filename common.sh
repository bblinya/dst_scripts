STEAM_CMD_HOME="$HOME/steamcmd"

export DST_HOME="$HOME/dst"

export DST_KLEI="$HOME/.klei/DoNotStarveTogether"

TEMPLATE_DIR="$(pwd)/templates"

# export CLUSTER_NAME=${CLUSTER_NAME:-"Myth"}
# export CLUSTER_NAME="Myth"
# CLUSTER_NAME="BBWM"
if [ -z ${CLUSTER_NAME+x} ]; then 
  echo "CLUSTER NAME is unset"; 
  echo "Add CLUSTER_NAME=name before command.";
  echo "Or execute cmd: export CLUSTER_NAME=?"
  exit -1;
fi

echo "Init Cluster Name: $CLUSTER_NAME"

export CLUSTER_PATH="$DST_KLEI/$CLUSTER_NAME"

SC_NAME="dst_server_${CLUSTER_NAME}"

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
LOG_DIR="${SCRIPT_DIR}/logs"

function fail()
{
	echo Error: "$@" >&2
	exit 1
}

function check_for_file()
{
	if [ ! -e "$1" ]; then
		fail "Missing file: $1"
	fi
}

