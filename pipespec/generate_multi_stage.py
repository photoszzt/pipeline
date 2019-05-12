import json
from collections import OrderedDict
from spec import Encoder,Node,Stream,Config

multi_stage=OrderedDict()
nodes=[]
nodes.append(Node(name="decode", stage="decode", delivery_function=None, config=Config(framesperchunk=None, chunklimit=None, duration=None, nworkers=None, nsockets=None, outdir=None, cmd=None), lambda_function=None))
nodes.append(Node(name="grayscale", stage="grayscale", delivery_function=None, config=Config(framesperchunk=None, chunklimit=None, duration=None, nworkers=None, nsockets=None, outdir=None, cmd=None), lambda_function=None))
nodes.append(Node(name="rotate", stage="rotate", delivery_function=None, config=Config(framesperchunk=None, chunklimit=None, duration=None, nworkers=None, nsockets=None, outdir=None, cmd=None), lambda_function=None))
nodes.append(Node(name="pixscale", stage="pixscale", delivery_function=None, config=Config(framesperchunk=None, chunklimit=None, duration=None, nworkers=None, nsockets=None, outdir=None, cmd=None), lambda_function=None))
nodes.append(Node(name="encode", stage="encode_to_dash", delivery_function=None, config=Config(framesperchunk=None, chunklimit=None, duration=None, nworkers=None, nsockets=None, outdir=None, cmd=None), lambda_function=None))
multi_stage["nodes"]=nodes
streams=[]
streams.append(Stream(src="input_0:chunks", dst="decode:chunks"))
streams.append(Stream(src="decode:frames", dst="grayscale:frames"))
streams.append(Stream(src="grayscale:frames", dst="rotate:frames"))
streams.append(Stream(src="rotate:frames", dst="pixscale:frames"))
streams.append(Stream(src="pixscale:frames", dst="encode:frames"))
streams.append(Stream(src="encode:chunks", dst="output_0:chunks"))
multi_stage["streams"]=streams
with open('multi_stage.json', 'w') as f:
    json.dump(multi_stage, f, indent=2, cls=Encoder)
