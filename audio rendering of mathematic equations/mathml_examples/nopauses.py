# -*- coding: utf-8 -*-
from lxml import etree as et
import sys
import os
# for TTS(default system TTS)
import pyttsx
#coding: utf-8


#function that reads the xhtml file and returns the root of the document
def getData(fname):
  f=open(fname)
  d=f.read()
  data = d.replace('\n','')
  root = et.fromstring(data)
  return root

#function to parse the operators in the <mo> tags
def operatorParse(op):
  if op == '+':
    return 'plus'
  if op == '-':
    return 'minus'
  if op == '...':
    return 'so on till,'
  if op == '=':
    return 'is equal to,'
  if op == '(':
    return 'the quantity, ('
  if op == ')':
    return '),'
  if op == 'sin':
    return 'sine'
  if op == 'cos':
    return 'cos'
  if op == 'tan':
    return 'tan'
  if op == 'log':
    return 'log'
  if op == '*':
    return 'times'
  if op == '/':
    return 'divided by'
  if op == '%':
    return 'modulo divided by'
  if op == '∫∫':
    return 'double integral of'
  if op == '∫':
    return 'integral of'
  if op == '∮':
    return ' contour integral of'
  if op == '∯':
    return ' surface integral of'
  if op == '∰':
    return ' volume integral of'
  if op == '∱':
    return ' clockwise integral of'
  if op == '∂':
    return 'partial derivative of'
  if op == '∠':
    return ' angle of'
  # alternative way for an integral, using the direct symbol should also work
  if op == '&integral':
    return 'integral'

#fill in operators
# if op == the operator:
#return a text form of the operator

#function that takes text and speaks it
"""def speek(text):
  engine = pyttsx.init()
  engine.say(text)
  engine.runAndWait()
  return
  """

#function to parse the mathML
def mathparse(element,exp = []):
  print 'testing element'
  print 'text:'
  print element.text
  print 'tag:',element.tag
  mtag = element.tag.split('}')[1]
  print 'modified tag:',mtag
  print 'expression string:', exp
  # numbers and variables
  if mtag == 'mi' or mtag == 'mn':
    exp.append(element.text)
  # operators
  if mtag == 'mo':
    exp.append(operatorParse(element.text))
  # fractions
  if mtag == 'mfrac':
    exp.append('fraction')
    mathparse(element[0],exp)
    exp.append('devided by')
    mathparse(element[1],exp)
          #if len(exp) > 0:
      #exp[-1]=exp[-1]+','
    return exp
  # superscript
  if mtag == 'msup':
    #if len(exp) > 0:
      #exp[-1] = exp[-1]+','
    mathparse(element[0],exp)
    exp.append('superscript')
    mathparse(element[1],exp)
    return exp
  #subscript
  if mtag == 'msub':
    #if len(exp) > 0:
      #exp[-1] = exp[-1]+','
    mathparse(element[0],exp)
    exp.append('subscript')
    mathparse(element[1],exp)
    return exp
  #subscript-superscript pairs
  if mtag == 'msubsup':
    mathparse(element[0],exp)
    #if len(exp) > 0:
      #exp[-1] = exp[-1]+','
    exp.append('subscript')
    mathparse(element[1],exp)
    exp.append('superscript')
    mathparse(element[2],exp)
    #if len(exp) > 0:
      #exp[-1] = exp[-1] + ','
    return exp
  #fence
  if mtag == 'mfence':
    exp.append('the quantity')
    for c in element:
      mathparse(c,exp)
    #if len(exp) > 0:
      #exp[-1] = exp[-1]+','
    return exp
  # over script
  if mtag == 'mover':
    mathparse(element[0],exp)
    exp.append('overscript')
    mathparse(element[1])
    #if len(exp) > 0:
      #exp[-1] = exp[-1]+','
    return exp
  #underscript
  if mtag == 'munder':
    mathparse(element[0],exp)
    exp.append('underscript')
    mathparse(element[1])
    #if len(exp) > 0:
      #exp[-1] = exp[-1] + ','
    return exp
  # underscript-overscript pair
  if mtag == 'munderover':
    mathparse(element[0],exp)
    exp.append('from')
    mathparse(element[1],exp)
    exp.append('to')
    mathparse(element[2],exp)
    return exp
  # square root
  if mtag == 'msqrt':
    exp.append('square root')
    if len(element) == 1 and len(element[0]) > 1:
      exp.append('of')
      for c in element:
        mathparse(c,exp)
      #if len(exp) > 0:
        #exp[-1] = exp[-1]+','
      return exp
  # general root
  if mtag == 'mroot':
    mathparse(element[-1],exp)
    exp.append('root of')
    for c in element[:-1]:
      mathparse(c,exp)
    #if len(exp) > 0:
      #exp[-1] = exp[-1]+','
    return exp
  print 'list:',len(exp)
  for e in element:
    mathparse(e,exp)
  return exp
def main():
  args = sys.argv
  if len(args) < 2:
    print 'usage:\ndemo.py inputFile.xhtml'
    exit(1)
  fileName = str(sys.argv[1])
  xmlroot = getData(fileName)  #'example1.xhtml' contains the xhtml code given above
  expList = mathparse(xmlroot)
  print 'list in the main function:\n',expList
  print len(expList)
  expression = ' '.join(expList)
  #print the resulting string
  print 'result:',expression
  #speak the expression
  #speek(expression)
  #speak the expression using festival
  cmd = 'echo "'+expression+'" | festival --tts'
  os.system(cmd)

if __name__ == '__main__':
  main()