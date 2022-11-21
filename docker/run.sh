docker run  -it \
            --gpus all \
            -d \
            -v /home/ubuntu/eric/DINO:$HOME/src/DINO \
            -v /data:$HOME/data \
            --env="DISPLAY" \
            --volume="/tmp/.X11-unix:/tmp/.X11-unix:rw" \
            --name $2 \
            --ipc=host \
            $1 \
            /bin/bash