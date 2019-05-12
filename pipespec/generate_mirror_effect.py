import json
from collections import OrderedDict
from spec import Encoder,Node,Stream,Config

mirror_effect=OrderedDict()
nodes=[]
nodes.append(Node(name="decode", stage="decode", delivery_function=None, config=None, lambda_function=None))
nodes.append(Node(name="crop", stage="duplicate_filter", delivery_function=None, config=Config(framesperchunk=None, chunklimit=None, duration=None, nworkers=None, nsockets=None, outdir=None, cmd=None), lambda_function=None))
nodes.append(Node(name="hflip", stage="video_filter", delivery_function=None, config=Config(framesperchunk=None, chunklimit=None, duration=None, nworkers=None, nsockets=None, outdir=None, cmd=None), lambda_function=None))
nodes.append(Node(name="hstack", stage="merge_filter", delivery_function="pair_delivery_func", config=Config(framesperchunk=None, chunklimit=None, duration=None, nworkers=None, nsockets=None, outdir=None, cmd=None), lambda_function=None))
nodes.append(Node(name="encode", stage="encode_to_dash", delivery_function=None, config=None, lambda_function=None))
mirror_effect["nodes"]=nodes
streams=[]
streams.append(Stream(src="input_0:chunks", dst="decode:chunks"))
streams.append(Stream(src="decode:frames", dst="crop:frames"))
streams.append(Stream(src="crop:frames_0", dst="hflip:frames"))
streams.append(Stream(src="hflip:frames", dst="hstack:frames_0"))
streams.append(Stream(src="crop:frames_1", dst="hstack:frames_1"))
streams.append(Stream(src="hstack:frames", dst="encode:frames"))
streams.append(Stream(src="encode:chunks", dst="output_0:chunks"))
mirror_effect["streams"]=streams
with open('mirror_effect.json', 'w') as f:
    json.dump(mirror_effect, f, indent=2, cls=Encoder)
