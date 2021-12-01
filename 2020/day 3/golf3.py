#(lambda m:eval("*".join(str([m[y][y*dx%len(m[y])]for y in range(0,len(m),dy)].count("#"))for dx,dy in [(1,1),(3,1),(5,1),(7,1),(1,2)])))(open("map.txt","r").read().split())

#print(eval("*".join(str(sum(1 if y%dy==0 and l[y*dx%len(l)]=="#"else 0 for y,l in enumerate(open("map.txt","r").read().split()))) for dx,dy in[(1,1),(3,1),(5,1),(7,1),(1,2)])))
r=1;print([r:=r*sum(l[y*dx%len(l)]=='#'for y,l in enumerate(open("m").read().split())if y%dy==0) for dx,dy in zip([1,3,5,7,1],[1]*4+[2])][::4])

r=1;print([r:=r*sum(l[x*i%len(l)]=='#'for i,l in enumerate([l.strip() for l in open('m')])if i%d==0) for x,d in zip([1,3,5,7,1],[1]*4+[2])][::4])

r=1;print([r:=r*sum(l[(x*i)%len(l)]=='#' for i,l in enumerate([l.strip() for l in open('m')][::d])) for x,d in zip([1,3,5,7,1],[1]*4+[2])][::4])
