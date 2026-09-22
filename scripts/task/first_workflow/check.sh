#!/bin/bash
set -uo pipefail

if [ ! -f /tmp/primary_output.txt ]; then
  exit 1
fi

if ! grep -q "primary" /tmp/primary_output.txt; then
  exit 1
fi

exit 0
