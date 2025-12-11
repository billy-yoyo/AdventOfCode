import math

with open("data") as f:
    timestamp = int(f.readline().strip())
    buses = [
        (i, int(x.strip())) for i, x in enumerate(f.readline().strip().split(",")) if x != "x"
    ]

def euclidan(a, b):
    old_r, r = a, b
    old_s, s = 1, 0
    old_t, t = 0, 1

    while r != 0:
        quotient = old_r // r
        old_r, r = r, old_r - (quotient * r)
        old_s, s = s, old_s - (quotient * s)
        old_t, t = t, old_t - (quotient * t)
    
    return old_s, old_t 

def crt(bus1, bus2):
    a1, n1 = bus1
    a2, n2 = bus2

    m1, m2 = euclidan(n1, n2)

    return (a1 * m2 * n2) + (a2 * m1 * n1), n1 * n2

def check_solution(soln, buses):
    a = soln[0] % soln[1]
    for offset, interval in buses:
        if a % interval != offset % interval:
            print(f"solution fails after {len(buses)} steps, soln {a} doesn't match bus {(offset, interval)}")

for bus_a in buses:
    for bus_b in buses:
        if bus_a[1] != bus_b[1] and (bus_a[1] % bus_b[1] == 0 or bus_b[1] % bus_a[1] == 0):
            print(f"buses are not coprime: {bus_a}, {bus_b}")
print(buses) 

soln_buses = buses[:2]
soln = crt(buses[0], buses[1])
check_solution(soln, soln_buses)
for bus in buses[2:]:
    print(soln[0] % soln[1])
    soln = crt(soln, bus)
    soln_buses.append(bus)
    check_solution(soln, soln_buses)
    

print((-1 * soln[0]) % soln[1])
