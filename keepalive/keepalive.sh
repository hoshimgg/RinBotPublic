rm -rf /home/ubuntu/mcl/bots/12345/cache
tmux send -t mcl "stop" ENTER
sleep 10
tmux send -t mcl "./mcl" ENTER
sleep 30
tmux send -t qq "python3 qq.py" ENTER
tmux send -t schedule "python3 schedule.py" ENTER
