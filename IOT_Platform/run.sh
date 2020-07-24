# sudo docker run --rm --network=host -v $PWD/../../:/opt scheduler_image
# sudo docker run --rm --network=host -v $PWD/../../:/opt monitoring_image
# sudo docker run --rm --network=host -v $PWD/../../:/opt load_balancer_image
# sudo docker run --rm --network=host -v $PWD/../../:/opt deployer_image
# sudo docker run --rm --network=host -v $PWD/../../:/opt logging_image
# sudo docker run --rm --network=host -v $PWD/../../:/opt notification_manager_image


gnome-terminal --geometry=65x16+0+0 --  bash -c "sudo docker run --rm --network=host -v $PWD/../../:/opt scheduler_image; exec bash"
# gnome-terminal --geometry=65x16+1000+0 --  bash -c "sudo docker run --rm --network=host -v $PWD/../../:/opt monitoring_image; exec bash"
# gnome-terminal --geometry=65x16+0+1000 --  bash -c "sudo docker run --rm --network=host -v $PWD/../../:/opt load_balancer_image; exec bash"
# gnome-terminal --geometry=65x16+1000+1000 --  bash -c "sudo docker run --rm --network=host -v $PWD/../../:/opt deployer_image; exec bash"


# gnome-terminal --geometry=65x16+0+0 --  bash -c "sudo docker run --rm --network=host -v $PWD/../../:/opt logging_image; exec bash"
# gnome-terminal --geometry=65x16+1000+0 --  bash -c "sudo docker run --rm --network=host -v $PWD/../../:/opt notification_manager_image; exec bash"