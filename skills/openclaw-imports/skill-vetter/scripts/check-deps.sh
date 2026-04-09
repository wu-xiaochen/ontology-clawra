#!/bin/bash
# check-deps.sh — verify required tools are available

set -euo pipefail

# Ensure Go binaries are in PATH
export PATH="$HOME/go/bin:$PATH"

MISSING=()

check() {
    command -v "$1" &>/dev/null || MISSING+=("$1")
}

check aguara
check skill-scanner
check python3
check curl
check jq
check git

if [ ${#MISSING[@]} -eq 0 ]; then
    echo "✅ All dependencies present"
    echo ""
    echo "Scanners available:"
    echo "  • aguara (prompt injection detection)"
    echo "  • skill-scanner (Cisco AI vulnerability scanner)"
    echo "  • python3 (additional checks)"
    exit 0
else
    echo "❌ Missing dependencies: ${MISSING[*]}"
    echo ""
    echo "Install instructions:"
    for dep in "${MISSING[@]}"; do
        case $dep in
            aguara)
                echo "  aguara: go install github.com/garagon/aguara/cmd/aguara@latest"
                ;;
            skill-scanner)
                echo "  skill-scanner: pip install cisco-ai-skill-scanner"
                ;;
            jq)
                echo "  jq: brew install jq (macOS) or apt install jq (Linux)"
                ;;
            git)
                echo "  git: brew install git (macOS) or apt install git (Linux)"
                ;;
            *)
                echo "  $dep: install manually"
                ;;
        esac
    done
    exit 1
fi
