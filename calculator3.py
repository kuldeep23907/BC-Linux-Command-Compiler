#!/usr/bin/python3
import subprocess as sp

import sys
import ply.lex as lex
import ply.yacc as yacc


temp={}
sym=None
cnt=0
naam=0
naam2=0
live={}
live2={}
tokens = (
        'NUM', 'PLUS',  'MINUS', 'TIMES', 'DIVIDE','LB','RB','MOD','POW','EXIT','ID','EQT','CLEAR','IMG','I'
)

filename = "calc.dot"
filename2="calc2.dot"
file = open(filename, "w")
file2=open(filename2,"w")
str1="digraph G { ordering=out "
file.write(str1)
file.write("\n")
file2.write(str1)
file2.write("\n")

t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_LB=r'[(]'
t_RB=r'[)]'
t_MOD=r'[%]'
t_POW=r'\^'
t_EXIT=r'(quit)'
t_ID=r'[a-z]'
t_EQT=r'[=]'
t_CLEAR=r'(clear)'

t_ignore = " \t\n"


def t_IMG(t):
    r'[(]\w+[,]\w+[)]'
    s=str(t.value)
    lz=s.split(",")
    val=lz[0]
    val=val[1:]
    if val >= 'a' and val <= 'z':
        val=temp[val]
    ls=[]
    ls.append(val)
    val=lz[1]
    val=val[:-1]
    if val >= 'a' and val <= 'z':
        val=temp[val]
    ls.append(val)
    ss=str(ls[0])+","+str(ls[1])
    t.value=ss


    return t

def t_NUM(t):
    r'\d+'
    t.value = str(t.value)
    return t

#def t_COMPLEX(t):
#    r'\d+[+-]\d+[a-z]'
#    t.value = str(t.value)
#    return t

def t_error(t):
	print("Illegal character '%s'" % t.value[0])
	t.lexer.skip(1)




def p_statement_complex(p):
    "stt : IMG"
    print("complex no")
    print(p[1])

def p_statement_exp(p):
    '''stt : E
           | EXIT
           | CLEAR
           | ID EQT E

           '''

    if(p[1]=="quit"):

       str1="}"
       file.write(str1)
       file2.write(str1)
       sys.exit()
    elif (p[1]=="clear"):
       sp.call('clear',shell=True)
    elif (str(p[1])>='a' and str(p[1])<='z' and str(p[2])=='='):

        temp.update({p[1]:p[3]})
        #print(temp)



    else:
        print(p[1])


def p_statement_find(p):
    '''stt : ID'''
    if p[1] in temp:

      print(temp[p[1]])
    else:
        print("0")




def p_statement_plus(p):
    "E : E PLUS B"
    global sym
    global cnt
    global naam
    global naam2
    flag=1
    flag2=1
    save=[]
    save2=[]
    #if(p[1].count(',')>0):
    #    lz1=p[1].split(',')
    #    lz2=p[3].split(',')
    #    sumr=int(lz1[0])+int(lz2[0])
    #    sumi=int(lz1[1])+int(lz2[1])
    #    p[0]=str(sumr)+","+str(sumi)
    #else:


    p[0]= int(p[1]) + int(p[3])
    #print("into plus")


    s='''n'''+str(naam)+''' [ label = "+"]'''+";"
    #print(s)
    live.update({"n"+str(naam):0})
    #print(live)
    file.write(s)
    naam+=1
    file.write("\n")
    s='''n'''+str(naam2)+''' [ label = "+"]'''+";"
    #print(s)
    live2.update({"n"+str(naam2):0})
    #print(live2)
    file2.write(s)
    file2.write("\n")






    s='''n'''+str(naam)+''' [ label = "E"]'''+";"
    #print(s)
    live.update({"n"+str(naam):0})
    #print(live)

    file.write(s)
    file.write("\n")
    #s="n"+str(naam)+"->"+"n"+str(naam-1)+";"
    #print(s)
    #zz="n"+str(naam-1)
    #live[zz]=1
    #file.write(s)

    for i in range(naam-1,0,-1):

        if i % 2 == 1 and flag <=2 :

            zz="n"+str(i)
            if(live[zz]==0):
               s="n"+str(naam)+"->"+"n"+str(i)+";"
               save.append(s)
               #print(s)
               zz="n"+str(i)
               live[zz]=1
               #print(live)
               flag+=1
               #file.write(s)
            if(i==naam-2):
                s="n"+str(naam)+"->"+"n"+str(naam-1)+";"
                save.append(s)
                #print(s)
                zz="n"+str(naam-1)
                live[zz]=1
                #file.write(s)

    for i in range(len(save)-1,-1,-1):
        file.write(save[i])
        file.write("\n")


    for i in range(naam2-1,-1,-1):
         if  flag2 <=2 :

             zz="n"+str(i)
             if(live2[zz]==0):
                s="n"+str(naam2)+"->"+"n"+str(i)+";"
                save2.append(s)
                #print(s)
                zz="n"+str(i)
                live2[zz]=1
                #print(live2)
                flag2+=1
                #file2.write(s)

    for i in range(len(save2)-1,-1,-1):
        file2.write(save2[i])
        file2.write("\n")



    naam+=1
    naam2+=1






def p_statement_plus2(p):
    "E : B"
    p[0]=p[1]

def p_statement_mult(p):

    "B : B TIMES D"
    global sym
    global cnt
    global naam
    global naam2
    flag2=1
    flag=1
    save=[]
    save2=[]
    #if(p[1].count(',')>0):
    #    lz1=p[1].split(',')
    #    lz2=p[3].split(',')
    #    sumr=int(lz1[0])*int(lz2[0])-int(lz1[1])*int(lz2[1])
    #    sumi=int(lz1[1])*int(lz2[0])+int(lz2[1])*int(lz1[0])
    #    p[0]=str(sumr)+","+str(sumi)
    #else:
    p[0]= int(p[1]) * int(p[3])
    print("into mul")


    s='''n'''+str(naam)+''' [ label = "*"]'''+";"
    #print(s)
    live.update({"n"+str(naam):0})
    #print(live)
    file.write(s)
    file.write("\n")
    naam+=1


    s='''n'''+str(naam2)+''' [ label = "*"]'''+";"
    #print(s)
    live2.update({"n"+str(naam2):0})
    #print(live2)
    file2.write(s)
    file2.write("\n")


    s='''n'''+str(naam)+''' [ label = "E"]'''+";"
    #print(s)
    live.update({"n"+str(naam):0})
    #print(live)

    file.write(s)
    file.write("\n")
    #s="n"+str(naam)+"->"+"n"+str(naam-1)+";"
    #print(s)
    #zz="n"+str(naam-1)
    #live[zz]=1
    #file.write(s)

    for i in range(naam-1,0,-1):
        if i % 2 == 1  and flag<=2:

            zz="n"+str(i)
            if(live[zz]==0):
               s="n"+str(naam)+"->"+"n"+str(i)+";"
               save.append(s)
               #print(s)
               zz="n"+str(i)
               live[zz]=1
               flag+=1
               #print(live)
               #file.write(s)
            if(i==naam-2):
                s="n"+str(naam)+"->"+"n"+str(naam-1)+";"
                save.append(s)
                #print(s)
                zz="n"+str(naam-1)
                live[zz]=1
                #file.write(s)

    for i in range(len(save)-1,-1,-1):
        file.write(save[i])
        file.write("\n")

    for i in range(naam2-1,-1,-1):
         if  flag2 <=2 :

             zz="n"+str(i)
             if(live2[zz]==0):
                s="n"+str(naam2)+"->"+"n"+str(i)+";"
                save2.append(s)
                #print(s)
                zz="n"+str(i)
                live2[zz]=1
                #print(live2)
                flag2+=1
                #file2.write(s)

    for i in range(len(save2)-1,-1,-1):
        file2.write(save2[i])
        file2.write("\n")




    naam+=1
    naam2+=1



def p_statement_mult2(p):
    "B : D"
    p[0]=p[1]



def p_statement_number(p):
    "D : NUM"
    global naam
    global live
    global naam2
    global live2

    p[0]=p[1]

    s='''n'''+str(naam)+''' [ label = "name:'''+str(p[1])+'''"]'''+";"
    #print(s)



    live.update({"n"+str(naam):0})
    #print(live)
    file.write(s)
    file.write("\n")
    naam+=1

    s='''n'''+str(naam2)+''' [ label = "'''+str(p[1])+'''"]'''+";"
    #print(s)
    live2.update({"n"+str(naam2):0})
    #print(live2)
    file2.write(s)
    file2.write("\n")
    naam2+=1


    s='''n'''+str(naam)+''' [ label = "E"]'''+";"
    #print(s)
    live.update({"n"+str(naam):0})
    #print(live)
    file.write(s)
    file.write("\n")
    s="n"+str(naam)+"->"+"n"+str(naam-1)+";"
    zz="n"+str(naam-1)
    live[zz]=1
    #print(s)

    file.write(s)
    file.write("\n")
    naam+=1

def p_statement_number1(p):
    "E : ID "
    if p[1] in temp:
        p[0]=temp[p[1]]
    else:
        p[0]=0



def p_statement_number2(p):
    "E : IMG "
    p[0]=p[1]



def p_error(p):
	if p:
		print("syntax error at {0}".format(p.value))
	else:
		print("syntax error at EOF")
def process(data):

	lex.lex()
	yacc.yacc()
	return str(yacc.parse(data))



if __name__ == "__main__" :
    print("XCALC version 1.01 \nCopyright 2018-2020 \nDesigned and Developed by BETA (Born for Enduring Technological Advancement)\n")
    while True :
            data = sys.stdin.readline()
            process(data)
