python3 -m lerobot.replay \
    --robot.type=so101_follower \
    --robot.port=/dev/ttyACM1 \
    --robot.id=follower \
    --dataset.repo_id=frk2/pickyellowdropblue5 \
    --dataset.episode=3 # choose the episode you want to replay
