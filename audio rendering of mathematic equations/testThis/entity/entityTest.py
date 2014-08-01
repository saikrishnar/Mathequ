#! usr/bin/python
import lxml.etree as ET
# function that reads the xhtml file and returns the root of the document


def getData(fname):
  with open(fname) as f:
    parser = ET.XMLParser(load_dtd=True, no_network=False,resolve_entities=False)
    data=f.read()
    data = data.replace('\t','')
    data = data.replace('\n','')
    doc = ET.fromstring(data, parser=parser)  
    return doc

def printTags(root):
  for child in root:
    temp = str(child.tag)
    #print 'temp is'
    #print temp,'\n'
    if temp[-1] == '>':
      print 'child is'
      print child
      print 'length of child is\n', len(child)
      print 'childs tag is'
      print child.tag
      print 'childs text is'
      print child.text
      print 'temp is\n',child.text
      #if child.text == '&int;':
      #print 'found integral\n'
      #else:
      #print 'not an integral\n'
    print '\n\n\n'
    printTags(child)
  return

def main():
  r = getData('integral_example.xhtml')
  printTags(r)
#print ET.tostring(r)

if __name__ == '__main__':
  main()