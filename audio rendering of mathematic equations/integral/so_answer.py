
import lxml.etree as ET
# function that reads the xhtml file and returns the root of the document


def getData(fname):
  with open(fname) as f:
    parser = ET.XMLParser(load_dtd=True, no_network=False,resolve_entities=True)
    doc = ET.parse(f, parser=parser)
    return doc.getroot()

def printTags(root):
  for child in root:
    child
    try:
      mtag= child.tag.split('}')
      print child.text
    except:
      print 'exeption'
  #print child.tag
    print '\n'
    printTags(child)
  return

def main():
  r = getData('integral_example.xhtml')
  printTags(r)
#print ET.tostring(r)

if __name__ == '__main__':
  main()