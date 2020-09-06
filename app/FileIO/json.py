import json
from json import JSONEncoder
import numpy


class NumpyArrayEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, numpy.ndarray):
            return obj.tolist()
        return JSONEncoder.default(self, obj)


def read(fileName):
    with open(fileName, 'r', encoding="utf-8") as reader:
        jf = json.loads(reader.read())
    return jf


def write(jsonData, jsonf):
    with open(jsonf, 'w+') as f:
        f.seek(0)
        # ascii for chinese
        json.dump(jsonData, f, ensure_ascii=False, cls=NumpyArrayEncoder)
        f.truncate()
