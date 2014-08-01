
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
    mtag = child.tag.split('}')[1]
    if mtag == 'mo':
      print mtag
      print ' text is\n',child.text
      print 'length is',len(child)
      if len(child) == 1:
        print 'element'
        print child
        print 'child of mo is'
        print child[0]
        print ' text of child is',child[0].text
        print 'length of the child is',len(child[0])
    printTags(child)
  return

def main():
  r = getData('integral_example.xhtml')
  printTags(r)
#print ET.tostring(r)

if __name__ == '__main__':
  main()