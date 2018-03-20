#!/usr/bin/env bash

# Stop running script when error occurs
set -o errexit
set -o nounset

#
service tor stop
pkill -9 tor
rm -rf tmp/*


SocksPort=9050
ControlPort=9051

# Default values
TorInstances=10
InstanceID=0

if [ ${#} -ne 0 ]; then
	TorInstances=${1}
fi

while [ ${InstanceID} -lt ${TorInstances} ]; do
    mkdir -p "tmp/${InstanceID}"
    tor --SocksPort ${SocksPort} --ControlPort ${ControlPort} --DataDirectory "tmp/${SocksPort}" --quiet &

    let InstanceID=InstanceID+1
    let SocksPort=SocksPort+2
    let ControlPort=ControlPort+2
done

./main.py