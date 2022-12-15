import subprocess

shards = 8
upper_bound = 16000

ps = [subprocess.Popen(["python", "puzzle_pt2.py", str(i), str(shards), str(upper_bound)]) for i in range(shards)]
exits = [p.wait() for p in ps]


