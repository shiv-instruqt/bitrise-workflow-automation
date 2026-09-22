#!/bin/bash
set -uo pipefail

if [ ! -f /tmp/step_count.txt ]; then
  exit 1
fi

count="$(tr -d '[:space:]' < /tmp/step_count.txt)"

if [ "${count}" != "4" ]; then
  exit 1
fi

exit 0
