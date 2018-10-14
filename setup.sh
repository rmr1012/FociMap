#1/usr/bin/env bash

sudo apt-get update
sudo apt-get install -y python3 python3-dev python3-setuptools
sudo apt-get update && sudo apt-get install python3-pip
sudo apt-get install -y libsm6 libxext6 libxrender-dev
sudo apt-get install -y nodejs npm nodejs-legacy
git clone https://github.com/rmr1012/FociMap
python3 --version
echo "Node.js" `node -v`
echo "npm" `npm -v`
