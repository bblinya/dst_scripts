source common.sh

working_dir="$(pwd)"

mkdir -p ~/steamcmd
cd ~/steamcmd
if [[ ! -f "steamcmd_linux.tar.gz" ]]; then
  sudo dpkg --add-architecture i386 # If running a 64bit OS
  sudo apt-get update
  sudo apt-get install -y lib32gcc1    # If running a 64bit OS

  sudo apt-get install -y lib32stdc++6 # If running a 64bit OS
  # sudo apt-get install -y libgcc1      # If running a 32bit OS
  sudo apt-get install -y libcurl4-gnutls-dev:i386

  wget https://steamcdn-a.akamaihd.net/client/installer/steamcmd_linux.tar.gz
  tar -xvzf steamcmd_linux.tar.gz
fi

cd ${working_dir}

# init possible log files
mkdir -p ${DST_KLEI}/${CLUSTER_NAME}
# ln -sf ${TEMPLATE_DIR}/worldgenoverride_init.lua ${DST_KLEI}/${CLUSTER_NAME}/worldgenoverride.lua

# ln -sf ${TEMPLATE_DIR}/cluster.ini ${DST_KLEI}/${CLUSTER_NAME}/
rm -rf ${DST_KLEI}/${CLUSTER_NAME}/cluster.ini
rm -rf ${DST_KLEI}/${CLUSTER_NAME}/cluster_token.txt
ln -sf ${TEMPLATE_DIR}/adminlist.txt ${DST_KLEI}/${CLUSTER_NAME}/
# ln -sf ${TEMPLATE_DIR}/cluster_token.txt ${DST_KLEI}/${CLUSTER_NAME}/

mkdir -p ${DST_KLEI}/${CLUSTER_NAME}/Master
rm -rf ${DST_KLEI}/${CLUSTER_NAME}/Master/modoverrides.lua
rm -rf ${DST_KLEI}/${CLUSTER_NAME}/Master/server.ini
cp -f ${TEMPLATE_DIR}/worldgenoverride_much.lua ${DST_KLEI}/${CLUSTER_NAME}/Master/worldgenoverride.lua
# ln -sf ${TEMPLATE_DIR}/modoverrides.lua $DST_KLEI/$CLUSTER_NAME/Master/
# ln -sf ${TEMPLATE_DIR}/server_master.ini ${DST_KLEI}/${CLUSTER_NAME}/Master/server.ini

mkdir -p ${DST_KLEI}/${CLUSTER_NAME}/Caves
rm -rf ${DST_KLEI}/${CLUSTER_NAME}/Caves/modoverrides.lua
rm -rf ${DST_KLEI}/${CLUSTER_NAME}/Caves/server.ini
cp -f ${TEMPLATE_DIR}/worldgenoverride_much_cave.lua ${DST_KLEI}/${CLUSTER_NAME}/Caves/worldgenoverride.lua
# ln -sf ${TEMPLATE_DIR}/modoverrides.lua $DST_KLEI/$CLUSTER_NAME/Caves/
# ln -sf ${TEMPLATE_DIR}/server_cave.ini ${DST_KLEI}/${CLUSTER_NAME}/Caves/server.ini

python templates/setup.py

