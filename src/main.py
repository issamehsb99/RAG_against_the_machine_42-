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
        
    def chunking_py(self):
        file = "chunking.py"
        with open("chunking.py", "r")as f :
            data = f.read()
        if len(data) <= self.max_size :
            self.save_chunks(0, len(data), "chunking.py", data)
            return
        try :
            tree = parse(data)
        except Exception :
            pass
        start = None
        end = 0
        for node in tree.body:
            content = get_source_segment(data, node)
            if len(content) + end <= self.max_size:
                if start is not None :
                    self.save_chunks(start, end, file , data[start:end])
                start = data.find(content, end)
                end = len(content)
            else:
                if start is not None:
                    self.save_chunks(start, end, file , data[start:end])
                if isinstance(node, ast.ClassDef):
                    for i in node.body:
                        if len(get_source_segment(i )) + end < self.max_size: