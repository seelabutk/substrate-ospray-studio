#!/usr/bin/env bash

SCRIPT_DIR=$(dirname $(readlink -f "$0"))
SSH_DIR=$HOME/.ssh

docker pull seelab/substrate
if [ "$#" -ge 2 ]
then
	docker run ${@:1:$#-1} --rm -it \
		-v /var/run/docker.sock:/var/run/docker.sock \
		--mount type=bind,src=$SCRIPT_DIR/data,dst=/root/data \
		--mount type=bind,src=$SCRIPT_DIR/substrate.config.yaml,dst=/root/substrate.config.yaml \
		--mount type=bind,src=$SSH_DIR,dst=/root/.ssh \
		seelab/substrate:latest \
		substrate ospray-studio ${@: -1}
else
	docker run --rm -it \
		-v /var/run/docker.sock:/var/run/docker.sock \
		--mount type=bind,src=$SCRIPT_DIR/data,dst=/root/data \
		--mount type=bind,src=$SCRIPT_DIR/substrate.config.yaml,dst=/root/substrate.config.yaml \
		--mount type=bind,src=$SSH_DIR,dst=/root/.ssh \
		seelab/substrate:latest \
		substrate ospray-studio $1
fi
