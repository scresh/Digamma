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

