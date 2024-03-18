#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
VENV_PATH="$DIR/env/bin/activate"

for i in {1..250}
do

echo "Iteration $i"
osascript <<EOF
tell application "Terminal"
  do script "source '$VENV_PATH' && cd '$DIR' && python3 game/server.py; exit"
end tell
EOF

sleep 1

osascript <<EOF
tell application "Terminal"
  do script "source '$VENV_PATH' && cd '$DIR' && python3 ai/random_agent.py; exit"
end tell
EOF

osascript <<EOF
tell application "Terminal"
  do script "source '$VENV_PATH' && cd '$DIR' && python3 ai/random_agent.py; exit"
end tell
EOF

sleep 1

done
