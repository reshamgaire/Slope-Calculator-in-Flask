from flask import Flask, request, render_template
import numpy as np
import base64
from io import BytesIO
import matplotlib.pyplot as plt
from sympy import *
from utils import funcin
from math import degrees, inf

app = Flask(__name__)

@app.route('/')
def homepage():
    return render_template('index.html')

@app.route('/points', methods=['POST'])
def line():
    x, y, z = symbols('x y z')
    xy1=request.form.get('xy1','')
    xy2=request.form.get('xy2','')
    uxy1=xy1
    uxy2=xy2
    if xy1=='' or xy2=='':
        return render_template('index.html',msg='Please enter all valid details and try again !',xy1=uxy1, xy2=uxy2)
    else:
        try:
            xy1s, xy2s= str(xy1).replace(' ','').split(','), str(xy2).replace(' ','').split(',')
            xy1=[]
            xy2=[]
            for i in xy1s:
                xy1.append(float(i))
            for j in xy2s:
                xy2.append(float(j))

            if len(xy1)==len(xy2)==3:
                x1,y1,z1=xy1[0],xy1[1],xy1[2]
                x2,y2,z2=xy2[0],xy2[1],xy2[2]
                rd=sqrt(((x1-x2)*(x1-x2)) + ((y1-y2)*(y1-y2)) + ((z1-z2)*(z1-z2)))
                l=(x2-x1)/rd
                m=(y2-y1)/rd
                n=(z2-z1)/rd
                anglx=acos(l)
                angly=acos(m)
                anglz=acos(n)
                params3d={
                    'xy1':uxy1,
                    'xy2':uxy2,
                    'sx':tan(anglx),
                    'sy':tan(angly),
                    'sz':tan(anglz),
                }
                return render_template('slopans.html',**params3d)

            elif len(xy1)==len(xy2)==2:
                x1,y1=xy1[0],xy1[1]
                x2,y2=xy2[0],xy2[1]
                a = y1-y2
                b = x2-x1
                if b==0:
                    slp=inf
                    func='x='+str(x1)
                else:
                    slp=-a/b
                    c = a*(x2) + b*(y2)
                    if b<0:
                        lhs=Eq(-b*y,a*x-c)
                        print(lhs)
                        rhs=Eq(a*x-c,-b*y)
                        flhs=solve(lhs,-b*y)
                        frhs=solve(rhs,a*x-c)
                        func= str(frhs[0])+'='+str(flhs[0])
                    else:
                        lhs=Eq(b*y,c-a*x)
                        rhs=Eq(c-a*x, b*y)
                        flhs=solve(lhs,b*y)
                        frhs=solve(rhs,c-a*x)
                        func= str(frhs[0])+'='+str(flhs[0])
                angl=degrees(atan(slp))
                params2d={
                    'xy1':uxy1,
                    'xy2':uxy2,
                    'slp':str(slp).replace('inf','∞'),
                    'func':func.replace('*','').replace(' ',''),
                    'angl':angl,
                }
                try:
                    highx=max([abs(x1),abs(x2)])
                    x=np.linspace(-highx-10,highx+10)
                    fig=plt.figure()
                    ax = fig.add_subplot(1, 1, 1)
                    ax.spines['left'].set_position('center')
                    ax.spines['bottom'].set_position('zero')
                    ax.spines['right'].set_color('none')
                    ax.spines['top'].set_color('none')
                    ax.xaxis.set_ticks_position('bottom')
                    ax.yaxis.set_ticks_position('left')
                    plt.scatter([x1,x2],[y1,y2],color='red')
                    if b==0:
                        plt.axvline(x = x1)
                    else:
                        fx=eval(str(solve(lhs,y)[0]))
                        if type(fx)==float:
                            plt.axhline(y = fx,xmin=-highx-10,xmax=highx+10)
                        else:
                            plt.plot(x,fx)
                    plt.text(x1,y1,f'({x1}, {y1})')
                    plt.text(x2,y2,f'({x2}, {y2})')
                    plt.grid()
                    buffer=BytesIO()
                    plt.savefig(buffer,format='png')
                    buffer.seek(0)
                    png_img=buffer.getvalue()
                    graph=base64.b64encode(png_img)
                    graph=graph.decode('utf-8')
                    buffer.close()
                    params2d['graph']=graph
                except Exception as e:
                    print(e)
                return render_template('slopans.html',**params2d)

            else:
                return render_template('index.html',msg='Please enter all valid details and try again !',xy1=uxy1, xy2=uxy2,)
        except:
            return render_template('index.html',msg='Something went wrong, Please enter all valid details and try again !',xy1=uxy1, xy2=uxy2,)


@app.route('/equation', methods=['POST'])
def curve():
    x, y = symbols('x y')
    usr_eq=request.form.get('equation', '')
    uslpplc=request.form.get('slplc','')
    uusr_eq=usr_eq
    if usr_eq=='' or uslpplc=='':
        return render_template('index.html', msg='Please enter all valid details and try again !',cerr='error',eq=uusr_eq, point=uslpplc)

    else:
        usr_eq=funcin(usr_eq)
        eq2=str(usr_eq).split('=')

        sympeq=Eq(parse_expr(eq2[0]),parse_expr(eq2[1]))
        slpplcs=str(funcin(uslpplc)).replace(' ','').replace('(','').replace(')','').replace('i','I').split(',')
        slpplc=[]
        for a in slpplcs:
            if 'I' in str(a):
                slpplc.append(parse_expr(a))
            else:
                slpplc.append(float(a))
        ok=solve(sympeq,y)
        if len(slpplc)>1:
            yf=''
            for t in ok:
                if round(t.subs(x,slpplc[0]),3)==round(slpplc[1],3):
                    yf=t
                    break
            if yf=='':
                return render_template('index.html',msg=f"The curve {usr_eq} doesn't pass with point ({uslpplc}).",cerr='error', eq=uusr_eq, point=uslpplc)
            slpeq=diff(yf,x)
            slope=slpeq.subs(x,slpplc[0])
            try:
                if (str(str(slope).split('.')[1]).startswith('0000')) and ('I' not in str(slope)):
                    slope=int(slope)
                else:
                    slope=round(slope, 4)
            except:
                pass
            slop={
                'eq':uusr_eq,
                'point':f'{slpplcs[0]},{slpplcs[1]}'.replace('*','').replace(' ','').replace(',',', '),
                'slope':str(slope).replace('*','')
            }
            if 'I' in str(slope):
                slop['dmsg']='I'
            
            x1,y1 = slpplc[0],slpplc[1]
            xlist=np.linspace(-13*x1/10,13*x1/10)
            slpx=np.linspace(x1-3*x1/10,13*x1/10)
            line=slope*(slpx - x1) + y1
            ylist=eval(str(yf).replace('x','xlist'))
            fig=plt.figure()
            ax = fig.add_subplot(1, 1, 1)
            ax.spines['left'].set_position('center')
            ax.spines['bottom'].set_position('zero')
            ax.spines['right'].set_color('none')
            ax.spines['top'].set_color('none')
            ax.xaxis.set_ticks_position('bottom')
            ax.yaxis.set_ticks_position('left')
            plt.scatter([x1],[y1],color='red')
            plt.plot(slpx,line,linewidth=2)
            if type(ylist)==float or type(ylist)==int:
                plt.axhline(y = ylist)
            else:    
                plt.plot(xlist,ylist)
            plt.text(x1,y1,f'({x1}, {y1})')
            plt.grid()
            buffer=BytesIO()
            plt.savefig(buffer,format='png')
            buffer.seek(0)
            png_img=buffer.getvalue()
            graph=base64.b64encode(png_img)
            graph=graph.decode('utf-8')
            buffer.close()
            slop['graph']=graph
            return render_template('slopans.html',**slop)

        elif len(slpplc)==1:
            yax=ok[0].subs(x,slpplc[0])
            try:
                if str(str(yax).split('.')[1]).startswith('000'):
                    yax=int(yax)
                elif len(slpplcs[0].split('.'))>=2:
                    fnum=len(slpplcs[0].split('.')[1])
                    if fnum>2:
                        yax=round(yax, fnum)
                    else:
                        yax=round(yax, 3)
                else:
                    yax=round(yax, 3)
            except:
                pass
            slpeq=diff(ok[0],x)
            slope=slpeq.subs(x,slpplc[0])
            try:
                if (str(str(slope).split('.')[1]).startswith('0000')) and ('I' not in str(slope)):
                    slope=int(slope)
                else:
                    slope=round(slope, 4)
            except:
                pass
            slop={
                'eq':uusr_eq,
                'point':f'{slpplcs[0]},{yax}'.replace('*','').replace(' ','').replace(',',', '),
                'slope':str(slope).replace('*','')
            }
            if ('I' in str(yax)) or ('I' in str(slope)):
                slop['dmsg']='I'

            x1,y1 = slpplc[0],yax
            xlist=np.linspace(-13*x1/10,13*x1/10)
            slpx=np.linspace(x1-3*x1/10,13*x1/10)
            line=slope*(slpx - x1) + y1
            ylist=eval(str(ok[0]).replace('x','xlist'))
            fig=plt.figure()
            ax = fig.add_subplot(1, 1, 1)
            ax.spines['left'].set_position('center')
            ax.spines['bottom'].set_position('zero')
            ax.spines['right'].set_color('none')
            ax.spines['top'].set_color('none')
            ax.xaxis.set_ticks_position('bottom')
            ax.yaxis.set_ticks_position('left')
            plt.scatter([x1],[y1],color='red')
            plt.plot(slpx,line,linewidth=2)
            if type(ylist)==float or type(ylist)==int:
                plt.axhline(y = ylist)
            else:    
                plt.plot(xlist,ylist)
            plt.text(x1,y1,f'({x1}, {y1})')
            plt.grid()
            buffer=BytesIO()
            plt.savefig(buffer,format='png')
            buffer.seek(0)
            png_img=buffer.getvalue()
            graph=base64.b64encode(png_img)
            graph=graph.decode('utf-8')
            buffer.close()
            slop['graph']=graph
            return render_template('slopans.html',**slop)
        else:
            return render_template('index.html',msg='Please enter all valid details and try again !',cerr='error', eq=uusr_eq, point=uslpplc)

if __name__ == '__main__':
    app.run(debug=True)