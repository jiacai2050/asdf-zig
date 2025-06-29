#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" &>/dev/null && pwd -P)
GH_REPO="https://github.com/jiacai2050/asdf-zig"
TOOL_NAME="zig"
TOOL_TEST="$TOOL_NAME"

fail() {
	echo -e "asdf-$TOOL_NAME: $*"
	exit 1
}
