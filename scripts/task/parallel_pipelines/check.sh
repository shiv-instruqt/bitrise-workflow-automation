#!/bin/bash
set -uo pipefail

if [ ! -f /tmp/deploy_output.txt ]; then
  exit 1
fi

if ! grep -q "deploy" /tmp/deploy_output.txt; then
  exit 1
fi

exit 0
