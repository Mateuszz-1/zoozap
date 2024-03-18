#!/bin/bash

# This script is designed for GNOME Terminal, it may not run on other terminals or operating systems.

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
VENV_PATH="$DIR/env/bin/activate"

for i in {1..200}; do

  echo "Iteration $i"
  
  gnome-terminal -- bash -c "cd '$DIR'; source '$VENV_PATH'; python3 game/server.py; exec bash"
  
  sleep 1
  
  gnome-terminal -- bash -c "cd '$DIR'; source '$VENV_PATH'; python3 ai/random_agent.py; exec bash"
  gnome-terminal -- bash -c "cd '$DIR'; source '$VENV_PATH'; python3 ai/random_agent.py; exec bash"
  
  sleep 1

done
