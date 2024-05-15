

def funcin(f):
    f=f.replace(" ",'').replace("^",'**').replace("inf",'oo').replace("π",'pi').replace("∞",'oo').replace('cosec','csc').replace('{','(').replace('[','(').replace('}',')').replace(']',')')

    lst=['log','cos','sin','cot','tan','sec','csc']
    punc="""!"#$%&'()*+, -./:;<=>?@[\]^_`{|}~"""
    for g in lst:
        ya=[a for a in range(len(f)) if f.startswith(g,a)]
        for k in ya:
            if k!=0:
               if f[k-1].isalpha() or f[k-1].isdigit() or f[k-1]==")":
                   f=f[:k]+'*'+f[k:]
        ys=[a for a in range(len(f)) if f.startswith(g,a) and f[a+3]!='(']
        s=0
        for t in ys:
            t=t+s
            i=t+3
            while True:
                if i>=len(f):
                    break
                if f[i] in punc:
                    break
                i=i+1
            f= f[:t+3] + '(' + f[t+3:i] + ')' + f[i:]
            s=s+2
    md=[a for a in range(len(f)) if f.startswith('|',a)]
    if len(md)%2==0:
        id1=0
        id2=0
        for x in md:
            id=id1+id2
            x+=id
            f=f[:x]+'abs('+f[x+1:md[md.index(x-id)+1]+id]+')'+f[int(md[md.index(x-id)+1])+id+1:]
            if x!=0:
                if f[x-1].isalpha() or f[x-1].isdigit() or f[x-1]==")":
                    f=f[:x]+'*'+f[x:]
                    id2+=1
            md.pop(md.index(x-id)+1)
            id1+=3

    er=[a for a in range(len(f)) if f.startswith('e',a)]
    cvt=[]
    for x in er:
        if x==0:
            if not f[x+1].isalpha():
                cvt.append(x)
        elif x==len(f)-1:
            if not f[x-1].isalpha():
                cvt.append(x)
        else:
            if not (f[x+1].isalpha() or f[x-1].isalpha()):
                cvt.append(x)
    i=0
    for t in cvt:
        f = f[:t+i] + 'exp' + f[t+1+i:]
        i+=2
    exp=[a for a in range(len(f)) if f.startswith('exp',a) if not f.startswith('exp(',a)]
    i=0
    for a in exp:
        f = f[:a+i] + 'exp(1)' + f[a+3+i:]
        i+=3

    g=0
    while True:
        if g<len(f)-1:
            if (f[g]==')' and (f[g+1].isdigit() or f[g+1].isalpha())) or (f[g].isdigit() and f[g+1].isalpha()) or (f[g].isalpha() and f[g+1].isdigit()):
                f=f[:g+1]+'*'+f[g+1:]
            g+=1
        else:
            break
    return f