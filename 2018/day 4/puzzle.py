from collections import defaultdict

with open("input") as f:
    data = f.read().strip().split("\n")

START = "start"
SLEEP = "sleep"
WAKE = "wake"

events = []

for line in data:
    date, log = line.split("]")
    date, time = date[1:].split(" ")
    hour, minute = [int(x) for x in time.split(":")]
    log = log.strip()
    if log.startswith("Guard"):
        current_guard_id = int(log.split(" ")[1][1:])
        events.append(((date, hour, minute), START, current_guard_id))
    elif log.startswith("falls") and current_guard_id is not None:
        events.append(((date, hour, minute), SLEEP, None))
    elif log.startswith("wakes") and current_guard_id is not None:
        events.append(((date, hour, minute), WAKE, None))

guard_sleep_times = defaultdict(lambda: defaultdict(int))
guard_total_asleep = defaultdict(int)

events = sorted(events, key=lambda x: x[0])
current_guard_id = None
sleep_start = None
for event_time, action, guard_id in events:
    if action == START:
        current_guard_id = guard_id
        sleep_start = None
    elif action == SLEEP and current_guard_id is not None:
        sleep_start = event_time
    elif action == WAKE and current_guard_id is not None and sleep_start is not None:
        sleep_end = event_time
        
        for x in range(sleep_start[2], sleep_end[2]):
            guard_sleep_times[current_guard_id][x] += 1
            guard_total_asleep[current_guard_id] += 1

        sleep_start = None
        
sleepy_guard = max(guard_total_asleep.keys(), key=lambda x: guard_total_asleep[x])
sleepy_guard_minute = max(guard_sleep_times[sleepy_guard].keys(), key=lambda x: guard_sleep_times[sleepy_guard][x])

print(sleepy_guard * sleepy_guard_minute)

most_sleepy_minute_guard = max(guard_sleep_times.keys(), key=lambda g: max(guard_sleep_times[g][x] for x in range(60)))
most_sleepy_minute = max(guard_sleep_times[most_sleepy_minute_guard].keys(), key=lambda x: guard_sleep_times[most_sleepy_minute_guard][x])
print(most_sleepy_minute_guard * most_sleepy_minute)