import json
from collections import OrderedDict
from spec import Encoder,Node,Stream,Config

roundtrip=OrderedDict()
nodes=[]
nodes.append(Node(name="decode", stage="decode", delivery_function=None, config=Config(framesperchunk=None, chunklimit=None, duration=None, nworkers=None, nsockets=None, outdir=None, cmd=None), lambda_function=None))
nodes.append(Node(name="encode", stage="encode_to_dash", delivery_function=None, config=Config(framesperchunk=None, chunklimit=None, duration=None, nworkers=None, nsockets=None, outdir=None, cmd=None), lambda_function=None))
roundtrip["nodes"]=nodes
streams=[]
streams.append(Stream(src="input_0:chunks", dst="decode:chunks"))
streams.append(Stream(src="decode:frames", dst="encode:frames"))
streams.append(Stream(src="encode:chunks", dst="output_0:chunks"))
roundtrip["streams"]=streams
with open('roundtrip.json', 'w') as f:
    json.dump(roundtrip, f, indent=2, cls=Encoder)
