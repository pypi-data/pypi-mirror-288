def prime(n):
    c=0
    for i in range(1,n):
        if n%i==0:
            c+=1
    return c==1
def lprime(n):
    u=[]
    for i in range(1,n+1):
        c=0
        for j in range(1,i):
            if i%j==0:
                c+=1
        if c==1:
            u.append(i)
    return u



