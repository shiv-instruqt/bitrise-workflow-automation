#!/bin/bash
set -euxo pipefail

cd /root/mobile-app
bitrise run primary 2>&1 | tee /tmp/primary_output.txt
