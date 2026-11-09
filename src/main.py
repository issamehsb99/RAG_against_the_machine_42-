from pathlib import Path
from models import Source
from ast import get_source_segment ,  parse
import ast

class chunk :
    def __init__(self, max_size: int):
        self.max_size: int = max_size
        self.id: int = 1
        self.dic_chunks: dict = {"python":list(), "text":list()}

    def save_chunks(self, start, end, file, content, mode="python"):
        self.dic_chunks[mode].append(Source(file_path=file, first_character_index=start, last_character_index=end, content=content, chunk_id=self.id))
        self.id +=1

    def chunking_long_node(self, node, code, ofset, file):
        start = None
        end = 0 
        for child in node.body:
            content = get_source_segment(code, child)
            print(end)
            s = code.find(content, min(ofset, end))
            print(s, content)
            # s =  child.lineno
            # print(s)
            e = s + len(content)
            print(s, "->",e)
            if len(content) >= self.max_size:
                if start is not None:
                    self.save_chunks(start , end, "file", code[start:end])
                    start = None
                for i in range(s, e , self.max_size):
                    k = min(e, i+self.max_size)
                    self.save_chunks(i,k, file, code[i:k])
            elif start is None:
                start = s
            elif e - start  >= self.max_size:
                self.save_chunks(start, end , "file", code[start:end])
                start = s
            end = e
        if start is not None:
            self.save_chunks(start, end , file, code[start:end])   

        # self.save_chunks(s, e , "sss", code[s:e])


    def chunking_py(self):
        file = "chunking.py"
        with open("chunking.py", "r")as f :
            code = f.read()
        if len(code) <= self.max_size :
            self.save_chunks(0, len(code), "chunking.py", code)
            return
        try :
            tree = parse(code)
        except Exception :
            pass
        start = None
        end = 0
        for node in tree.body:
            content = get_source_segment(code, node)
            s_n = code.find(content, end)
            e_n = len(content) + s_n
            # print(e_n, "kkk")
            if len(content) >= self.max_size:
                if start is not None:
                    # print(start, end)
                    self.save_chunks(start, end , "file" , code[start : end])
                    start = None
                self.chunking_long_node(node, code, end, file)
            elif start is None:
                start = s_n
            elif e_n - start >= self.max_size :
                print("ss")
                self.save_chunks(start, end , file , code[start: end])
                start = s_n
            end = e_n
        if start is not None :
            self.save_chunks(start, end , file , code[start: end])
c = chunk(2000)
import json 
c.chunking_py()
all_chunks = [d.model_dump() for mode  in c.dic_chunks for d in c.dic_chunks[mode]]
with open("python.json", 'w') as f:
    json.loads
    json.dump(all_chunks, f, indent=4)