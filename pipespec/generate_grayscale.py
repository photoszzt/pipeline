import json
from collections import OrderedDict
from spec import Encoder,Node,Stream,Config

grayscale=OrderedDict()
nodes=[]
nodes.append(Node(name="decode", stage="decode", delivery_function=None, config=Config(framesperchunk=None, chunklimit=None, duration=None, nworkers=None, nsockets=None, outdir=None, cmd=None), lambda_function=None))
nodes.append(Node(name="grayscale", stage="grayscale", delivery_function=None, config=Config(framesperchunk=None, chunklimit=None, duration=None, nworkers=None, nsockets=None, outdir=None, cmd=None), lambda_function=None))
nodes.append(Node(name="encode", stage="encode_to_dash", delivery_function=None, config=Config(framesperchunk=None, chunklimit=None, duration=None, nworkers=None, nsockets=None, outdir=None, cmd=None), lambda_function=None))
grayscale["nodes"]=nodes
streams=[]
streams.append(Stream(src="input_0:chunks", dst="decode:chunks"))
streams.append(Stream(src="decode:frames", dst="grayscale:frames"))
streams.append(Stream(src="grayscale:frames", dst="encode:frames"))
streams.append(Stream(src="encode:chunks", dst="output_0:chunks"))
grayscale["streams"]=streams
with open('grayscale.json', 'w') as f:
    json.dump(grayscale, f, indent=2, cls=Encoder)
