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

#function to generate a basic sable root and append the version and other info at the end to a file "equation.sable"
def generateSable(node=None,flag=None):
  print 'in function generateSable'
  print flag
  documentInfo = '<?xml version="1.0"?><!DOCTYPE SABLE PUBLIC "-//SABLE//DTD SABLE speech mark up//EN" "Sable.v0_2.dtd" []>'
  if flag:
    sable = ''
    sable = documentInfo+et.tostring(node)
    print 'writing sable to file'
    f = open('equation.sable','w')
    f.write(sable)
    f.close()
    return
  return  et.Element('SABLE')

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
def mathparse(element,snode,exp = []):
  #print 'testing element'
  #print 'text:'
  #print element.text
  #print 'tag:',element.tag
  mtag = element.tag.split('}')[1]
  #print 'modified tag:',mtag
  #print 'expression string:', exp
  # numbers and variables
  if mtag == 'mi' or mtag == 'mn':
    exp.append(element.text)
  # operators
  if mtag == 'mo':
    exp.append(operatorParse(element.text))
# fractions
  if mtag == 'mfrac':
    if len(snode) > 0:
      snode[-1].tail = ' '.join(exp)
    else:
      snode.text = ' '.join(exp)
    exp = []
    et.SubElement(snode,'EMPH').text = 'fraction'
    et.SubElement(snode,'BREAK',LEVEL = 'Medium')
    tnode = et.SubElement(snode,'RATE',SPEED = '+25%')
    t2node = et.SubElement(tnode,'PITCH',BASE = '+25%')
    tnode.tail = 'divided by'
    exp=mathparse(element[0],t2node,exp)
    if len(t2node) > 0:
      t2node[-1].tail = ' '.join(exp)
    else:
      t2node.text = ' '.join(exp)
    exp = []
    dnode = et.SubElement(snode,'RATE',SPEED = '+25%')
    d2node = et.SubElement(dnode,'PITCH',BASE = '-25%')
    et.SubElement(dnode,'BREAK',LEVEL = 'Large')
    exp=mathparse(element[1],d2node,exp)
    if len(d2node) > 0:
      d2node[-1].tail = ' '.join(exp)
    else:
      d2node.text = ' '.join(exp)
    exp = []
    et.SubElement(snode,'BREAK',LEVEL = 'Medium')
    return []
# superscript
  if mtag == 'msup':
    print 'expression before superscript manipulation:\n',exp
    print 'mathML before superscript manipulation:\n',et.tostring(snode)
    if len(snode) > 0:
      snode[-1].tail = ' '.join(exp)
      print 'printing tail of node\n',snode.tail
    else:
      snode.text = ' '.join(exp)
      print 'printing text of node\n',snode.text
    exp = []
    et.SubElement(snode,'BREAK',LEVEL = 'Large')
    exp=mathparse(element[0],snode,exp)
    print 'printing exp after parsing base of superscript\n',exp
    print 'printing node after parsing base of superscript\n',et.tostring(snode)
    if len(snode) > 0:
      snode[-1].tail = ' '.join(exp)
      print 'printing tail after parsing base of superscript\n',snode.tail
    else:
      snode.text = ' '.join(exp)
      print 'printing text of node after parsing the base of superscript\n',snode.text
    exp = []
    et.SubElement(snode,'EMPH').text = 'superscript'
    enode =et.SubElement(snode,'PITCH',BASE = '+50%')
    print 'exp list before calling function on the exponent node:\n',exp
    exp=mathparse(element[1],enode,exp)
    print 'exp after passing it to the function for the exponent node:\n',exp
    if len(enode) > 0:
      enode[-1].tail = ' '.join(exp)
      print 'printing tail after parsing the superscript text\n',enode.tail
    else:
      enode.text = ' '.join(exp)
      print 'printing text after parsing superscript\n',enode.text
    exp = []
    return []
#subscript
  if mtag == 'msub':
    if len(snode) > 0:
      snode[-1].tail = ' '.join(exp)
    else:
      snode.text = ' '.join(exp)
    exp = []
    et.SubElement(snode,'BREAK',LEVEL = 'Medium')
    exp=mathparse(element[0],snode,exp)
    if len(snode) > 0:
      snode[-1].tail = ' '.join(exp)
    else:
      snode.text = ' '.join(exp)
    exp = []
    et.SubElement(snode,'EMPH').text = 'subscript'
    subNode =et.SubElement(snode,'PITCH',BASE = '-50%')
    exp=mathparse(element[1],subNode,exp)
    if len(subNode) > 0:
      subNode[-1].tail = ' '.join(exp)
    else:
      subNode.text = ' '.join(exp)
    exp = []
    return []
#subscript-superscript pairs
  if mtag == 'msubsup':
    mathparse(element[0],snode,exp)
    if len(exp) > 0:
      et.SubElement(snode,'BREAK',LEVEL='Large')
    et.SubElement(snode,'EMPH').text = 'subscript'
    mathparse(element[1],snode,exp)
    et.SubElement(snode,'EMPH').text = 'superscript'
    mathparse(element[2],snode,exp)
    et.SubElement(snode,'BREAK')
    return exp
#fence
  if mtag == 'mfence':
    exp.append('the quantity')
    if snode.text:
      snode[-1].tail = '' .join(exp)
    else:
      snode.text = ' '.join(exp)
    exp = []
    et.SubElement(snode,'BREAK',LEVEL = 'Large')
    for c in element:
      exp=mathparse(c,snode,exp)
    et.SubElement(snode,'BREAK',LEVEL='Medium')
    exp = []
    return exp
# over script
  if mtag == 'mover':
    if len(snode) > 0:
      snode[-1].tail = ' '.join(exp)
    else:
      snode.text = ' '.join(exp)
    exp = []
    et.SubElement(snode,'BREAK',LEVEL = 'Medium')
    exp=mathparse(element[0],snode,exp)
    if len(snode) > 0:
      snode[-1].tail = ' '.join(exp)
    else:
      snode.text = ' '.join(exp)
    exp = []
    et.SubElement(snode,'EMPH').text = 'overscript'
    overNode =et.SubElement(snode,'PITCH',BASE = '+30%')
    exp=mathparse(element[1],overNode,exp)
    if len(overNode) > 0:
      overNode[-1].tail = ' '.join(exp)
    else:
      overNode.text = ' '.join(exp)
    exp = []
    return []
#underscript
  if mtag == 'munder':
    if len(snode) > 0:
      snode[-1].tail = ' '.join(exp)
    else:
      snode.text = ' '.join(exp)
    exp = []
    et.SubElement(snode,'BREAK',LEVEL = 'Medium')
    exp=mathparse(element[0],snode,exp)
    if len(snode) > 0:
      snode[-1].tail = ' '.join(exp)
    else:
      snode.text = ' '.join(exp)
    exp = []
    et.SubElement(snode,'EMPH').text = 'underscript'
    underNode =et.SubElement(snode,'PITCH',BASE = '-30%')
    exp=mathparse(element[1],underNode,exp)
    if len(underNode) > 0:
      underNode[-1].tail = ' '.join(exp)
    else:
      underNode.text = ' '.join(exp)
    exp = []
    return []
# underscript-overscript pair
  if mtag == 'munderover':
    if len(snode) > 0:
      snode[-1].tail = ' '.join(exp)
    else:
      snode.text = ' '.join(exp)
    exp = []
    et.SubElement(snode,'BREAK',LEVEL = 'Medium')
    exp=mathparse(element[0],snode,exp)
    et.SubElement(snode,'BREAK',LEVEL='medium')
    underOverBase=et.SubElement(snode,'EMPH').text = ' '.join(exp)
    underOverBase.tail = 'from'
    exp = []
    underOverSub =et.SubElement(snode,'PITCH',BASE = '-50%')
    exp=mathparse(element[1],underOverSub,exp)
    if len(underOverSub) > 0:
      underOverSub[-1].tail = ' '.join(exp)
    else:
      underOverSub.text = ' '.join(exp)
    exp = []
    underOverSup =et.SubElement(snode,'PITCH',BASE = '+50%')
    exp=mathparse(element[2],underOversup,exp)
    if len(underOverSup) > 0:
      underOverSup[-1].tail = ' '.join(exp)
    else:
      underOverSup.text = ' '.join(exp)
    exp = []
    return []

# square root
  if mtag == 'msqrt':
    exp.append('square root')
    if len(element) == 1 and len(element[0]) > 1:
      exp.append('of')
      for c in element:
        mathparse(c,snode,exp)
      if len(exp) > 0:
        exp[-1] = exp[-1]+','
      return exp
# general root
  if mtag == 'mroot':
    mathparse(element[-1],snode,exp)
    exp.append('root of')
    for c in element[:-1]:
      mathparse(c,snode,exp)
    if len(exp) > 0:
      exp[-1] = exp[-1]+','
    return exp
  print 'list:',len(exp)
  print 'items in the list:\n',exp
  print 'sable markup:\n',et.tostring(snode)
  for e in element:
    exp=mathparse(e,snode,exp)
  if len(snode) > 0:
    if snode[-1].tail:
      snode[-1].tail = snode[-1].tail+' '.join(exp)
    else:
      snode[-1].tail = ' '.join(exp)
#exp = []
  else:
    if snode.text:
      snode.text = snode.text + ' '.join(exp)
    else:
      snode.text = ' '.join(exp)

  print 'sable just before exiting:\n',et.tostring(snode)
  return exp
def main():
  args = sys.argv
  if len(args) < 2:
    print 'usage:\ndemo.py inputFile.xhtml'
    exit(1)
  fileName = str(sys.argv[1])
  xmlroot = getData(fileName)  #'example1.xhtml' contains the xhtml code given above
  sableroot=generateSable()
  expList = mathparse(xmlroot,sableroot)
  if len(sableroot) > 0:
    sableroot[-1].tail = ' '.join(expList)
  else:
    sableroot.text = ' '.join(expList)
  generateSable(sableroot,1)
#print 'list in the main function:\n',expList
#print len(expList)
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