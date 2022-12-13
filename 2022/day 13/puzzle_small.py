import json
f=lambda x:isinstance(x,int)
g=lambda x:[x]if f(x)else x
c=lambda l,r:l-r if f(l)and f(r) else next((c(a,b)for a,b in zip(g(l),g(r))if c(a,b)!=0),len(g(l))-len(g(r)))
p=json.loads("[["+open("d").read().replace("\n\n","],[").replace("\n",",")+"]]")
print(sum(i+1for i,k in enumerate(p)if c(*k)<=0))
h=lambda a:sum(1 for x in p for k in x if c(k,a)<0)+1
print(h([[2]])*(h([[6]])+1))