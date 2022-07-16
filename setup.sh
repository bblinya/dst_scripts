if [[ ! true ]]; then
  sudo dpkg --add-architecture i386 # If running a 64bit OS
  sudo apt-get update
  sudo apt-get install -y lib32gcc1    # If running a 64bit OS

  sudo apt-get install -y lib32stdc++6 # If running a 64bit OS
  # sudo apt-get install -y libgcc1      # If running a 32bit OS
  sudo apt-get install -y libcurl4-gnutls-dev:i386
fi

working_dir="$(pwd)"

mkdir -p ~/steamcmd
cd ~/steamcmd
if [[ ! -f "steamcmd_linux.tar.gz" ]]; then
  wget https://steamcdn-a.akamaihd.net/client/installer/steamcmd_linux.tar.gz
  tar -xvzf steamcmd_linux.tar.gz
fi

cd ${working_dir}
source common.sh

mkdir -p ${DST_KLEI}/${CLUSTER_NAME}
ln -sf ${TEMPLATE_DIR}/init_worldgenoverride.lua ${DST_KLEI}/${CLUSTER_NAME}/worldgenoverride.lua

ln -sf ${TEMPLATE_DIR}/cluster.ini ${DST_KLEI}/${CLUSTER_NAME}/
ln -sf ${TEMPLATE_DIR}/cluster_token.txt ${DST_KLEI}/${CLUSTER_NAME}/

mkdir -p ${DST_KLEI}/${CLUSTER_NAME}/Master
cp -f ${TEMPLATE_DIR}/worldgenoverride.lua ${DST_KLEI}/${CLUSTER_NAME}/Master/
ln -sf ${TEMPLATE_DIR}/modoverrides.lua $DST_KLEI/$CLUSTER_NAME/Master/
ln -sf ${TEMPLATE_DIR}/master_server.ini ${DST_KLEI}/${CLUSTER_NAME}/Master/server.ini

mkdir -p ${DST_KLEI}/${CLUSTER_NAME}/Caves
cp -f ${TEMPLATE_DIR}/cave_worldgenoverride.lua ${DST_KLEI}/${CLUSTER_NAME}/Caves/worldgenoverride.lua
ln -sf ${TEMPLATE_DIR}/modoverrides.lua $DST_KLEI/$CLUSTER_NAME/Caves/
ln -sf ${TEMPLATE_DIR}/cave_server.ini ${DST_KLEI}/${CLUSTER_NAME}/Caves/server.ini
