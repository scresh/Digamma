#!/usr/bin/env bash

# Stop running script when error occurs
set -o errexit
set -o nounset


service tor stop
#pkill -9 tor
mkdir -p tmp
rm -rf tmp/*


SocksPort=9050
ControlPort=9051

# Default values
TorInstances=32
InstanceID=0

if [ ${#} -ne 0 ]; then
	TorInstances=${1}
fi


while [ ${InstanceID} -lt ${TorInstances} ]; do
    tor --SocksPort ${SocksPort} --ControlPort ${ControlPort} --DataDirectory "./tmp/${SocksPort}"  --quiet &

    while ! nc -z localhost ${SocksPort}; do
        sleep 0.2
    done


    let InstanceID=InstanceID+1
    let SocksPort=SocksPort+2
    let ControlPort=ControlPort+2
done

#./main.py ${TorInstances} test
