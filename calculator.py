#!/usr/bin/python3
import subprocess as sp

import sys
import ply.lex as lex
import ply.yacc as yacc


temp={}
sym=None
cnt=0
tokens = (
        'NUM', 'PLUS',  'MINUS', 'TIMES', 'DIVIDE','LB','RB','MOD','POW','EXIT','ID','EQT','CLEAR','IMG','I'
)

filename = "calc.dot"
file = open(filename, "w")
str1="digraph G {"
file.write(str1)

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
    r'[(]\w+[,][-+]?\w+[)]'
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
    r'[-]?\d+'
    t.value = str(t.value)

    return t

#def t_COMPLEX(t):
#    r'\d+[+-]\d+[a-z]'
#    t.value = str(t.value)
#    return t

def t_error(t):
	print("Illegal character '%s'" % t.value[0])
	t.lexer.skip(1)


precedence = (

	('left', 'PLUS', 'MINUS'),
        ('left', 'TIMES', 'DIVIDE','MOD'),
        ('right','POW')
)


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
    "E : E PLUS E"
    global sym
    global cnt
    if(p[1].count(',')>0):
        lz1=p[1].split(',')
        lz2=p[3].split(',')
        sumr=int(lz1[0])+int(lz2[0])
        sumi=int(lz1[1])+int(lz2[1])
        p[0]=str(sumr)+","+str(sumi)
    else:
        p[0]= int(p[1]) + int(p[3])

    if(cnt==0):
       str1=str(p[1])+"->"+'''"+"'''+";"
       file.write(str1)
       cnt=1
    if(sym=='"*"' or sym=='"/"' or sym=='"%"'):
        str1=str(p[1])+"->"+'''"+"'''+";"
        file.write(str1)
    else:
        str1=str(p[3])+"->"+'''"+"'''+";"
        file.write(str1)

    if(sym!=None):
      str1=sym+"->"+'"+"'+";"
      file.write(str1)
    sym='"+"'


def p_statement_minus(p):

    "E : E MINUS E"
    global sym
    global cnt
    if(p[1].count(',')>0):
        lz1=p[1].split(',')
        lz2=p[3].split(',')
        sumr=int(lz1[0])-int(lz2[0])
        sumi=int(lz1[1])-int(lz2[1])
        p[0]=str(sumr)+","+str(sumi)
    else:
        p[0]= int(p[1]) - int(p[3])

    if(cnt==0):
        str1=str(p[1])+"->"+'''"-"'''+";"
        file.write(str1)
        cnt=1
    if(sym=='"*"' or sym=='"/"' or sym=='"%"'):
        str1=str(p[1])+"->"+'''"-"'''+";"
        file.write(str1)
    else:
        str1=str(p[3])+"->"+'''"-"'''+";"
        file.write(str1)

    bb=sym
    if(bb!=None):
       str1=bb+"->"+'"-"'+";"
       file.write(str1)
    sym='"-"'


def p_statement_mult(p):

    "E : E TIMES E"
    global sym
    global cnt
    if(p[1].count(',')>0):
        lz1=p[1].split(',')
        lz2=p[3].split(',')
        sumr=int(lz1[0])*int(lz2[0])-int(lz1[1])*int(lz2[1])
        sumi=int(lz1[1])*int(lz2[0])+int(lz2[1])*int(lz1[0])
        p[0]=str(sumr)+","+str(sumi)
    else:
        p[0]= int(p[1]) * int(p[3])

    if(cnt==0):
         str1=str(p[1])+"->"+'''"*"'''+";"
         file.write(str1)
         cnt=1
    if(sym=='"^"'):
        str1=str(p[1])+"->"+'''"*"'''+";"
        file.write(str1)
    else:
        str1=str(p[3])+"->"+'''"*"'''+";"
        file.write(str1)

    bb=sym
    if(bb!=None):
       str1=bb+"->"+'"*"'+";"
       file.write(str1)
    sym='"*"'


def p_statement_divide(p):

    "E : E DIVIDE E"
    global sym
    global cnt
    p[0]=float(p[1]) /float(p[3])
    if(cnt==0):
        str1=str(p[1])+"->"+'''"/"'''+";"
        file.write(str1)
        cnt=1
    if(sym=='"^"'):
        str1=str(p[1])+"->"+'''"/"'''+";"
        file.write(str1)
    else:
        str1=str(p[3])+"->"+'''"/"'''+";"
        file.write(str1)
    bb=sym
    if(bb!=None):
      str1=bb+"->"+'"/"'+";"
      file.write(str1)
    sym='"/"'


def p_statement_mod(p):

    "E : E MOD E"
    global sym
    global cnt

    p[0]=int(p[1]) % int(p[3])
    if(cnt==0):
        str1=str(p[1])+"->"+'''"%"'''+";"
        file.write(str1)
        cnt=1
    if(sym=='"^"'):
        str1=str(p[1])+"->"+'''"%"'''+";"
        file.write(str1)
    else:
        str1=str(p[3])+"->"+'''"%"'''+";"
        file.write(str1)
    bb=sym
    if(bb!=None):
      str1=bb+"->"+'"%"'+";"
      file.write(str1)
    sym='"%"'



def p_statement_pow(p):

    "E : E POW E"
    global sym
    global cnt
    p[0]=int(p[1]) ** int(p[3])
    if(cnt==0):
        str1=str(p[1])+"->"+'''"^"'''+";"
        file.write(str1)
        cnt=1
    str1=str(p[3])+"->"+'''"^"'''+";"
    file.write(str1)
    bb=sym
    if(bb!=None):
      str1=bb+"->"+'"^"'+";"
      file.write(str1)
    sym='"^"'

def p_statement_bckt(p):
    "E : LB E RB "
    p[0]=p[2]

def p_statement_number(p):
    "E : NUM"
    p[0]=p[1]



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
