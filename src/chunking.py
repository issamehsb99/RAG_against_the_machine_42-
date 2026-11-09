from pathlib import Path
from models import Source
from ast import get_source_segment ,  parse
import ast
class chunking():
    def __init__(self, max_size: int):
        self.max_size: int = max_size
        self.id: int = 1
        self.dic_chunks: dict = {"python":list(), "text":list()}


    def save_chunks(self, start, end, file, content, mode="python"):
        self.dic_chunks[mode].append(Source(file_path=file, first_character_index=start, last_character_index=end, content=content, chunk_id=self.id))
        self.id +=1


    def find_files(self):
        """
        this function separate files of code python and other docs that should 
        i chunk and make it in a dict 

        return value is dict of file with two keys "py" and "docs"
        """
        path_files= dict()
        path_files["py"] = []
        path_files["docs"] = []
        i = 1 
        repo = Path("../vllm-0.10.1")
        for file in repo.rglob("*"):
            if str(file).endswith(".py"):
                path_files["py"].append(str(file))
            elif str(file).endswith(".md"):
                path_files["docs"].append(str(file))
            elif str(file).endswith(".txt"):
                path_files["docs"].append(str(file))
        return path_files
    

    def chunk_docs(self, files:list[str]):
        """
        this function chunk docs files and should return first and last index
        and file path

        """
        overlap =int( self.max_size * 0.15)
        size = self.max_size
        start = 0
        for file in files:
            with open(file, 'r') as f:
                content = f.read()
            content_len = len(content)
            start = 0
            if content_len <= size:
                self.save_chunks(start=start, end=content_len,content=content,file= file, mode="text")
                continue
            step = size - overlap
            for s in range(0, max(len(content) - overlap, 1), step):
                self.save_chunks(s, min(s + size, len(content)), file, content[s:s+size], "text")

    
    def chunk_python(self, files:list[str]):
        max_size = self.max_size
        for file in files:
            with open(file, 'r') as f:
                code = f.read()
            if len(code) <= max_size :
                self.save_chunks(start= 0, end= len(code), content =code,file= file)
                continue
            try :
                tree =  parse(code)
            except:
                continue
            start = None
            end = 0
            for node in tree.body:
                content = get_source_segment(code, node)
import json
test = chunking(2000)
di = test.find_files()
# print("sssssssssssss")
test.chunk_docs(di["docs"])

all_chunks = [d.model_dump() for mode  in test.dic_chunks for d in test.dic_chunks[mode]]
with open("issam.json", 'w') as f:
    json.loads
    json.dump(all_chunks, f, indent=4)
