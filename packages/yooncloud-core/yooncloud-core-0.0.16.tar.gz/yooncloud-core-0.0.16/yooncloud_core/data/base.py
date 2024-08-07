from typing import Optional
from datetime import datetime, date
from pydantic import BaseModel, create_model
from pydash import _

class Base:
    def __init__(self, schema=None, name="", transforms=[]):
        self.transforms = transforms
        self.model = self.create_model(schema, name) if schema else None
        

    def __iter__(self):
        gen = self.gen()
        if self.model:
            gen = map(lambda x: self.model(**x), gen)
        gen = self._transform(gen)
        yield from gen


    def _transform(self, gen):
        for t in self.transforms:
            match t["type"]:
                case "map":
                    func = make_function_with_scripts(t["scripts"])
                    gen = map(func, gen)
                case "filter":
                    func = make_function_with_scripts(t["scripts"])
                    gen = filter(func, gen)
                case "tap":
                    func = make_function_with_scripts(t["scripts"], args="rows")
                    gen = [a for a in gen]
                    gen = func(gen)
                case "histogram":
                    pass
                case "unit_cut":
                    pass
                case "moving_function":
                    pass
        return gen

    
    def create_model(self, schema:Optional[dict], name:str) -> BaseModel:
        for key, value in schema.items():
            if value == "string":
                schema[key] = (str, None)
            elif value == "int" or value == "integer":
                schema[key] = (int, None)
            elif value == "float":
                schema[key] = (float, None)
            elif value == "date":
                schema[key] = (date, None)
            elif value == "datetime":
                schema[key] = (datetime, None)
            elif value == "bool" or value == "boolean":
                schema[key] = (bool, None)
        return create_model(name, **schema, __config__={"extra": "allow"})


    def gen(self):
        raise NotImplementedError()
    

def make_function_with_scripts(scripts: list[str], args="row"):
    exec(f"def func({args}):\n\t" + "\n\t".join(scripts))
    return locals()["func"]