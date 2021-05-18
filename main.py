

import xml.etree.ElementTree as ET

xmlcode = '''
<note date="20180510">
  	<to>WORLD</to>
    	<from>IML <hi>asd</hi> </from>
    	<from>IML</from>
    	<heading>Reminder</heading>
    	<body>Hello, WORLD!</body>
</note>
	'''
tree = ET.ElementTree(ET.fromstring(xmlcode))
note = tree.getroot()

childs = note.getiterator("from")   # from 태그만 반환
children = note.getchildren()       # 모든 자식 태그 반환

for i in childs:
	print(ET.tostring(i))
print()
for i in children:
	print(ET.tostring(i))