sleep 2
python3 ./scheduler/scheduler.py &
echo $! >> process_id
sleep 2
python3 ./load_balancer/load_balancer.py &
echo $! >> process_id
sleep 2
python3 ./monitoring/monitoring.py &
echo $! >> process_id
sleep 2
python3 ./deployer/deployer.py &
echo $! >> process_id
sleep 2
python3 ./logging/logging.py &
echo $! >> process_id
sleep 2
python3 ./notification_manager/notification_manager.py &
echo $! >> process_id
sleep 2
python3 ./servers/server1/server.py &
echo $! >> process_id
python3 ./servers/server2/server.py &
echo $! >> process_id
python3 ./servers/server3/server.py &
echo $! >> process_id
python3 ./sensors/binary.py &
echo $! >> process_id
python3 ./sensors/numeric.py &
echo $! >> process_id
python3 ./sensors/temperature_ac.py &
echo $! >> process_id
python3 ./sensors/temperature_env.py &
echo $! >> process_id

python3 manage.py runserver


# gnome-terminal --geometry=65x16+0+0 --working-directory=$PWD/scheduler/ --  bash -c  "python3 scheduler.py; exec bash"
# gnome-terminal --geometry=65x16+1000+0 --working-directory=$PWD/load_balancer/ --  bash -c "python3 load_balancer.py ; exec bash " 
# gnome-terminal --geometry=65x16+0+1000 --working-directory=$PWD/monitoring/ --  bash -c "python3 monitoring.py ; exec bash " 
# gnome-terminal --geometry=65x16+1000+1000 --working-directory=$PWD/deployer/ --  bash -c "python3 deployer.py ; exec bash " 

# gnome-terminal --geometry=65x16+0+0 --working-directory=$PWD/logging/ --  bash -c "python3 logging.py; exec bash "
# gnome-terminal --geometry=65x16+1000+0 --working-directory=$PWD/notification_manager/ --  bash -c "python3 notification_manager.py ; exec bash "
# gnome-terminal --geometry=65x16+0+1000 --working-directory=$PWD/servers/server1/ --  bash -c "python3 server.py ; exec bash "
# gnome-terminal --geometry=65x16+1000+1000 --working-directory=$PWD/servers/server2/ --  bash -c "python3 server.py ; exec bash "

# gnome-terminal --geometry=65x16+0+0 --working-directory=$PWD/servers/server3/ --  bash -c "python3 server.py; exec bash "
# # gnome-terminal --geometry=65x16+1000+0 --working-directory=$PWD/sensors/ --  bash -c "python3 binary.py ; exec bash &"
# # gnome-terminal --geometry=65x16+0+1000 --working-directory=$PWD/sensors/ --  bash -c "python3 numeric.py ; exec bash &"
# gnome-terminal --geometry=65x16+1000+1000 --working-directory=$PWD/sensors/ --  bash -c "python3 temperature_ac.py ; exec bash &"

# # gnome-terminal --geometry=65x16+0+0 --working-directory=$PWD/sensors/ --  bash -c "python3 temperature_env.py; exec bash "
