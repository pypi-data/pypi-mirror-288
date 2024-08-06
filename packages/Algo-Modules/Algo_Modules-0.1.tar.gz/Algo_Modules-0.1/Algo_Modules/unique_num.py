def unique(l):
    x=[]
    for i in l:
        if i not in x:
            x.append(i)
    print(x,end=' ')