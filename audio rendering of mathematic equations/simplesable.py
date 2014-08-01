import os
import sys
from lxml import etree as et

def getData(fname):
  f=open(fname)
  d=f.read()
  data = d.replace('\n','')
  root = et.fromstring(data)
  return root

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



def operatorParse(op):
  if op =='+':
    return 'plus'
  if op =='-':
    return 'minus'
  if op =='/':
    return 'divided by'
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
  



def mathparse(element,snode,exp):#xmlroot, sableroot
  print 'testing element'
  print 'text:'
  print element.text
  #mtag=element.tag
  mtag = element.tag.split('}')[1]
  print mtag
  
  print 'expression string:', exp
  # numbers and variables
  if mtag =='mi' or mtag =='mn':
    exp.append(element.text)
  # operators
  if mtag =='mo':
    exp.append(operatorParse(element.text))


  if mtag == 'mfrac':
    if len(snode) > 0:
      snode[-1].tail = ' '.join(exp)
    else:
      snode.text = ' '.join(exp)
    # exp = []
    exp.append('fraction')

    t2node = et.SubElement(snode,'PITCH')
    
    mathparse(element[0],t2node,exp)
    if len(t2node) > 0:
      t2node[-1].tail = ' '.join(exp)
    else:
      t2node.text = ' '.join(exp)
    exp.append('divided by')
    # exp = []
    tnode = et.SubElement(snode,'RATE',SPEED = '+25%')
    t2node = et.SubElement(tnode,'PITCH',BASE = '-25%')
    et.SubElement(tnode,'BREAK',LEVEL = 'Large')
    mathparse(element[1],t2node,exp)
    if len(t2node) > 0:
      t2node[-1].tail = ' '.join(exp)
    else:
      t2node.text = ' '.join(exp)
    # exp = []
    et.SubElement(snode,'BREAK',LEVEL = 'Medium')
    return exp



  if mtag == 'msup':     
      if len(snode) > 0:
        snode[-1].tail = ' '.join(exp)
      else:
        snode.text = ' '.join(exp)  
      tnode=et.SubElement(snode,'BREAK')
      mathparse(element[0],tnode,exp)
      if len(tnode) > 0:
        tnode[-1].tail = ' '.join(exp)
      else:
        tnode.text = ' '.join(exp) 
      exp.append('superscript')


      t2node =et.SubElement(snode,'PITCH',BASE = '+25%')
      mathparse(element[1],t2node,exp)
      if len(t2node) > 0:
       t2node[-1].tail = ' '.join(exp)
      else:
       t2node.text =' '.join(exp)
   
      return exp


  if mtag == 'msub':
    
    if snode.text:
      snode[-1].tail = ' '.join(exp)
    else:
      snode.text = ' '.join(exp)
      
    tnode=et.SubElement(snode,'BREAK')
    mathparse(element[0],snode,exp)
    exp.append('subscript')
    tnode =et.SubElement(snode,'PITCH',BASE = '-25%')
    mathparse(element[1],tnode,exp)
    return exp
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


  for e in element:
    mathparse(e,snode,exp)
  return exp



def main():
  args = sys.argv
  if len(args) < 2:
    print 'usage:\ndemo.py inputFile.xhtml'
    exit(1)
  fileName = str(sys.argv[1])
  xmlroot = getData(fileName)  #'example1.xhtml' contains the xhtml code given above
  sableroot=generateSable()
  expList =mathparse(xmlroot,sableroot,exp=[])
  if len(sableroot) > 0:
    sableroot[-1].tail = ' '.join(expList)
  else:
    sableroot.text = ' '.join(expList)
  generateSable(sableroot,1)
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
