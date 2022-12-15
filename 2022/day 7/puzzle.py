import json

data = """
$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k
""".strip()

with open("puzzle") as f:
    data = f.read()

def parse(lines):
    folder_stack = []
    folders = {}

    current = []
    for line in lines:
        if line.startswith("$"):
            if len(current) > 0:
                path = "/".join(folder_stack)
                folders[path] = [(size, f"{path}/{name}") for size, name in current]
                current = []

            command = line.split(" ")[1:]
            if command[0] == "cd":
                if command[1] == "..":
                    if len(folder_stack) > 1:
                        folder_stack.pop()
                else:
                    if command[1] == "/":
                        folder_stack = ["/"]
                    else:
                        folder_stack.append(command[1])
                        folders["/".join(folder_stack)] = []
        else:
            size, name = line.split(" ")
            size = int(size) if size != "dir" else size
            current.append((size, name))

    if len(current) > 0:
        path = "/".join(folder_stack)
        folders[path] = [(size, f"{path}/{name}") for size, name in current]

    return folders

def size_of(folders, folder):
    if folder not in folders:
        return 0
    
    total_size = 0
    for size, name in folders[folder]:
        if size == "dir":
            total_size += size_of(folders, name)
        else:
            total_size += size
    return total_size

folders = parse(data.split("\n"))
folder_sizes = []

print(json.dumps(folders, indent=4))

answer = 0
for folder in folders:
    size = size_of(folders, folder)
    folder_sizes.append((folder, size))
    if size <= 100_000:
        answer += size

print(answer)

total_size = size_of(folders, "/")
remaining_space = 70000000 - total_size
minimum_deleted = 30000000 - remaining_space
sorted_sizes = sorted([(folder, size) for folder, size in folder_sizes if size >= minimum_deleted], key=lambda d: d[1])
print(sorted_sizes[0])
