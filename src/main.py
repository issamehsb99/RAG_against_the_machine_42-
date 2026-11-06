from pathlib import Path
from chunking import chunking
from ast import get_source_segment, parse

with open("chunking.py", 'r')as f:
    data = f.read()
try :
    tree = parse(data)
except:
    pass
for i in tree.body:
    # print(data.find(str(get_source_segment(data, i))), get_source_segment(data, i), len(get_source_segment(data, i)))
    try:
        print(i._fields,"-=--=-=-=-=-",i.body, "=-==", i.name)
        for k in i.body:
            if "body" in k._fields:
                # print("ddddddddddddddddd")
                # print("name ---------- ", k.name)
                # print(k._fields, "====" ,get_source_segment(data, k))
                pass
    except :
        pass 
