# -*- coding: utf-8 -*-
from lxml import etree as et
import sys
import os
# for TTS(default system TTS)
import pyttsx
#coding: utf-8


#function that reads the xhtml file and returns the root of the document

def getData(fname):
  with open(fname) as f:
    parser = et.XMLParser(load_dtd=True, no_network=False,resolve_entities=False)
    data = f.read()
    data = data.replace('\t','')
    data = data.replace('\n','')
    doc = et.fromstring(data, parser=parser)
    return doc

#function to generate a basic sable root and append the version and other info at the end to a file "equation.sable"
def generateSable(node=None,flag=None):
  ##print 'in function generateSable'
  ##print flag
  documentInfo = '<?xml version="1.0"?><!DOCTYPE SABLE PUBLIC "-//SABLE//DTD SABLE speech mark up//EN" "Sable.v0_2.dtd" []>'
  if flag:
    sable = ''
    sable = documentInfo+et.tostring(node)
    ##print 'writing sable to file'
    f = open('equation.sable','w')
    f.write(sable)
    f.close()
    return
  return  et.Element('SABLE')

#function to parse the operators in the <mo> tagsunction that takes text and speaks it

def operatorParse(op):
  if op == '+':
    return 'plus'
  if op == '&plus;':
    return 'plus'
  if op == '&int;':
    return 'integral'
  if op == '&sum;':
    return ' summation'
  if op == '&prod;':
    return ' product '
  if op == '-':
    return 'minus'
  if op == '&minus;':
    return 'minus'
  if op == '&plusmn;':
    return 'plus or minus '
  if op == '...':
    return 'so on till,'
  if op == '=':
    return 'is equal to'
  if op == '&ne;':
    return 'is not equal to'
  if op == '&asymp;':
    return ' is almost equal to '
  if op == '&prop;':
    return 'is proportional to '
  if op == '&le;':
    return 'is less than or equal to'
  if op == '&ge;':
    return 'is greater than or equal to'
  if op == '&lt;':
    return ' is less than'
  if op == '&gt;':
    return 'is greater than '
  if op == '&lt;':
    return ' is less than'
  if op == '(':
    return 'the quantity ('
  if op == ')':
    return ')'
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
  if op == '&times;':
    return ' multiplied by'
  if op == '/':
    return 'divided by'
  if op == '&divide;':
    return 'divided by'
  if op == '%':
    return 'modulo divided by'
  if op == '&prime;':
    return 'first order derivative '
  if op == '&Prime;':
    return ' second derivative '
  if op == '&tprime;':
    return 'third derivative '
  if op == '&qprime;':
    return 'forth derivative '
  if op == '&part;':
    return ' parcial differential'
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
  if op == '&dd;':
    return 'D'
  if op == '&int;':
    return 'integral'
  if op == '.':
    return '.'
  if op == '&infin;':
    return 'infinity'
  if op == 'lim':
    return 'limit'
  if op == '&rarr;':
    return 'tends to'
  if op == ',':
    return ','
  return op
#fill in operators


# if op == the operator:
#return a text form of the operator

def getEntityValue(node):
  if node.tag.split('}')[1] == 'mi':
    if node[0].text == '&alpha;':
      node.text = 'alpha'
    if node[0].text == '&beta;':
      node.text = 'beta'
    if node[0].text == '&gama;':
      node. text = 'gama'
    if node[0].text == '&theta;':
      node.text = 'theta'
    if node[0].text == '&pi;':
      node.text='pi'
  else:
    node.text = node[0].text
  deleteElement = node[0]
  node.remove(deleteElement)
  return node
"""def speek(text):
  engine = pyttsx.init()
  engine.say(text)
  engine.runAndWait()
  return
  """

#function to parse the mathML
def mathparse(element,snode,exp = []):
  ###print 'testing element'
  ###print 'text:'
  ###print element.text
  ###print 'tag:',element.tag
  #mtag = ''
    #try:
  mtag = element.tag.split('}')[1]
    #except:
    #return []
  #mtag = element.tag
  ##print 'modified tag:',mtag
  ###print 'expression string:', exp
  # numbers and variables
  if mtag == 'mi' or mtag == 'mn':
    if len(element) > 0:
      element = getEntityValue(element)
    exp.append(element.text)
  # operators
  if mtag == 'mo':
    if len(element) > 0:
      element = getEntityValue(element)
      #print element.text
    ##print 'this is'
    ##print operatorParse(element.text)
    exp.append(operatorParse(element.text))
# fractions
  if mtag == 'mfrac':
    if len(snode) > 0:
      snode[-1].tail = ' '.join(exp)
    else:
      snode.text = ' '.join(exp)
    exp = []
#et.SubElement(snode,'AUDIO',SRC='http://localhost/test/testsound.wav')
    et.SubElement(snode,'EMPH').text = 'fraction'
    #tnode = et.SubElement(snode,'RATE',SPEED = '+25%')
    t2node = et.SubElement(snode,'PITCH',BASE = '+25%')
    #tnode.tail = 'over'
    snode.tail = 'over'
    exp=mathparse(element[0],t2node,exp)
    if len(t2node) > 0:
      t2node[-1].tail = ' '.join(exp)
    else:
      t2node.text = ' '.join(exp)
    exp = []
    #dnode = et.SubElement(snode,'RATE',SPEED = '+25%')
    d2node = et.SubElement(snode,'PITCH',BASE = '-25%')
    exp=mathparse(element[1],d2node,exp)
    if len(d2node) > 0:
      d2node[-1].tail = ' '.join(exp)
    else:
      d2node.text = ' '.join(exp)
    exp = []
    return []
# superscript
  if mtag == 'msup':
    ###print 'expression before superscript manipulation:\n',exp
    ###print 'mathML before superscript manipulation:\n',et.tostring(snode)
    if len(snode) > 0:
      snode[-1].tail = ' '.join(exp)
    ###print '##printing tail of node\n',snode.tail
    else:
      snode.text = ' '.join(exp)
###print '##printing text of node\n',snode.text
    exp = []
    #et.SubElement(snode,'AUDIO',SRC='http://localhost/test/superscript.wav')
    et.SubElement(snode,'BREAK',LEVEL = 'Large')
    exp=mathparse(element[0],snode,exp)
###print '##printing exp after parsing base of superscript\n',exp
###print '##printing node after parsing base of superscript\n',et.tostring(snode)
    if len(snode) > 0:
      snode[-1].tail = ' '.join(exp)
###print '##printing tail after parsing base of superscript\n',snode.tail
    else:
      snode.text = ' '.join(exp)
###print '##printing text of node after parsing the base of superscript\n',snode.text
    exp = []
    enode =et.SubElement(snode,'PITCH',BASE = '+50%')
    et.SubElement(enode,'EMPH').text = 'superscript'
###print 'exp list before calling function on the exponent node:\n',exp
    exp=mathparse(element[1],enode,exp)
###print 'exp after passing it to the function for the exponent node:\n',exp
    if len(enode) > 0:
      enode[-1].tail = ' '.join(exp)
###print '##printing tail after parsing the superscript text\n',enode.tail
    else:
      enode.text = ' '.join(exp)
###print '##printing text after parsing superscript\n',enode.text
    exp = []
    return []
#subscript
  if mtag == 'msub':
    if len(snode) > 0:
      snode[-1].tail = ' '.join(exp)
    else:
      snode.text = ' '.join(exp)
    exp = []
    #et.SubElement(snode,'AUDIO',SRC='http://localhost/test/subscript.wav')
    et.SubElement(snode,'BREAK',LEVEL = 'Medium')
    exp=mathparse(element[0],snode,exp)
    if len(snode) > 0:
      snode[-1].tail = ' '.join(exp)
    else:
      snode.text = ' '.join(exp)
    exp = []
    subNode =et.SubElement(snode,'PITCH',BASE = '-50%')
    et.SubElement(subNode,'EMPH').text = 'subscript'
    exp=mathparse(element[1],subNode,exp)
    if len(subNode) > 0:
      subNode[-1].tail = ' '.join(exp)
    else:
      subNode.text = ' '.join(exp)
    exp = []
    return []
#subscript-superscript pairs
  if mtag == 'msubsup':
    exp=mathparse(element[0],snode,exp)
    if len(snode) > 0:
      snode[-1].tail = ' '.join(exp)
    else:
      snode.text = ' '.join(exp)
    exp = []
    #et.SubElement(snode,'AUDIO',SRC='http://localhost/test/subsuper.wav')
    et.SubElement(snode,'BREAK',LEVEL='Large')
    ssSub = et.SubElement(snode,'PITCH',BASE='-50%')
    et.SubElement(ssSub,'EMPH').text = 'subscript'
    exp=mathparse(element[1],ssSub,exp)
    if len(ssSub) > 0:
      ssSub[-1].tail = ' '.join(exp)
    else:
      ssSub.text = ' '.join(exp)
    exp = []
    ssSup = et.SubElement(snode,'PITCH',BASE = '+50%')
    et.SubElement(ssSup,'EMPH').text = 'superscript'
    exp=mathparse(element[2],ssSup,exp)
    if len(ssSup) > 0:
      ssSup[-1].tail = ' '.join(exp)
    else:
      ssSup.text = ' '.join(exp)
    exp = []
    return []
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
#et.SubElement(snode,'AUDIO',SRC='http://localhost/test/superscript.wav')
    et.SubElement(snode,'BREAK',LEVEL = 'Medium')
    exp=mathparse(element[0],snode,exp)
    if len(snode) > 0:
      snode[-1].tail = ' '.join(exp)
    else:
      snode.text = ' '.join(exp)
    exp = []
    overNode =et.SubElement(snode,'PITCH',BASE = '+60%')
    et.SubElement(overNode,'EMPH').text = 'overscript'
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
    #et.SubElement(snode,'AUDIO',SRC='http://localhost/test/subscript.wav')
    et.SubElement(snode,'BREAK',LEVEL = 'Medium')
    exp=mathparse(element[0],snode,exp)
    if len(snode) > 0:
      snode[-1].tail = ' '.join(exp)
    else:
      snode.text = ' '.join(exp)
    exp = []
    underNode =et.SubElement(snode,'PITCH',BASE = '-60%')
    et.SubElement(underNode,'EMPH').text = 'underscript'
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
    #et.SubElement(snode,'AUDIO',SRC='http://localhost/test/subsuper.wav')
    et.SubElement(snode,'BREAK',LEVEL = 'Medium')

#et.SubElement(snode,'BREAK',LEVEL='medium')
    underOverBase=et.SubElement(snode,'EMPH')
    underOverBase.text = ' '.join(mathparse(element[0],snode,exp))
    underOverBase.tail = 'from'
    exp = []
    underOverSub =et.SubElement(snode,'PITCH',BASE = '-60%')
    underOverSub.tail = 'to'
    exp=mathparse(element[1],underOverSub,exp)
    if len(underOverSub) > 0:
      underOverSub[-1].tail = ' '.join(exp)
    else:
      underOverSub.text = ' '.join(exp)
    exp = []
    underOverSup =et.SubElement(snode,'PITCH',BASE = '+60%')
    exp=mathparse(element[2],underOverSup,exp)
    if len(underOverSup) > 0:
      underOverSup[-1].tail = ' '.join(exp)
    else:
      underOverSup.text = ' '.join(exp)
    exp = []
    return []

# square root
  if mtag == 'msqrt':
    if len(snode) > 0:
      snode[-1].tail = ' '.join(exp)
    else:
      snode.text = ' '.join(exp)
    exp = []
    #et.SubElement(snode,'AUDIO',SRC='http://localhost/test/squareroot.wav')
    et.SubElement(snode,'BREAK',LEVEL='Medium')
    et.SubElement(snode,'EMPH').text = 'square root of'
    sqrtNode = et.SubElement(snode,'RATE',SPEED='+30%')
    for c in element:
      exp=mathparse(c,sqrtNode,exp)
    if len(sqrtNode)>0:
      sqrtNode[-1].tail = ' '.join(exp)
    else:
      sqrtNode.text = ' '.join(exp)
    exp = []
    return []
# general root
  if mtag == 'mroot':
    exp=mathparse(element[-1],snode,exp)
    mathparse(element[-1],snode,exp)
    exp.append('root of')
    for c in element[:-1]:
      mathparse(c,snode,exp)
    if len(exp) > 0:
      exp[-1] = exp[-1]+','
    return exp
###print 'list:',len(exp)
###print 'items in the list:\n',exp
  ##print 'sable markup:\n',et.tostring(snode)
  for e in element:
    exp=mathparse(e,snode,exp)
  #print exp
  if len(snode) > 0:
    if snode[-1].tail != None:
      
      snode[-1].tail = snode[-1].tail+' '.join(exp)
    else:
      snode[-1].tail = ' '.join(exp)
#exp = []
  else:
    if snode.text:
      snode.text = snode.text + ' '.join(exp)
    else:
      snode.text = ' '.join(exp)

  ##print 'sable just before exiting:\n',et.tostring(snode)
  return exp
def main():
  args = sys.argv
  if len(args) < 2:
    ##print 'usage:\nbasicSable.py inputFile.xhtml'
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
###print 'list in the main function:\n',expList
###print len(expList)
  expression = ' '.join(expList)
  ###print the resulting string
  ##print 'result:',expression
#speak the expression
#speek(expression)
#speak the expression using festival
  cmd = 'echo "'+expression+'" | festival --tts'
  festCmd = 'festival --tts equation.sable'
#os.system(festCmd)

if __name__ == '__main__':
  main()
