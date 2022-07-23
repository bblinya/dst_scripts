if [[ true ]]; then
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
