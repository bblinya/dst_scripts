#update of server

cd /home/admin/dst_scripts

screen -dr dst_server -X quit
./update_dst.sh
./restart.sh 
