#!/bin/sh
tmux set-option -g mouse on
tmux new-session -d 'uvicorn --port 9200 --reload --workers 4 main:app'
sleep 1
tmux set-option -g mouse on
tmux split-window -h 'python turn.py'
#tmux swap-pane -U
#tmux swap-pane -D
tmux attach-session -d