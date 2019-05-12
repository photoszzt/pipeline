import json
from collections import OrderedDict
from spec import Encoder,Node,Stream,Config

video_filter=OrderedDict()
nodes=[]
nodes.append(Node(name="decode", stage="decode", delivery_function=None, config=Config(framesperchunk=None, chunklimit=None, duration=None, nworkers=None, nsockets=None, outdir=None, cmd=None), lambda_function=None))
nodes.append(Node(name="video_filter", stage="video_filter", delivery_function=None, config=Config(framesperchunk=None, chunklimit=None, duration=None, nworkers=None, nsockets=None, outdir=None, cmd=None), lambda_function=None))
nodes.append(Node(name="encode", stage="encode_to_dash", delivery_function=None, config=Config(framesperchunk=None, chunklimit=None, duration=None, nworkers=None, nsockets=None, outdir=None, cmd=None), lambda_function=None))
video_filter["nodes"]=nodes
streams=[]
streams.append(Stream(src="input_0:chunks", dst="decode:chunks"))
streams.append(Stream(src="decode:frames", dst="video_filter:frames"))
streams.append(Stream(src="video_filter:frames", dst="encode:frames"))
streams.append(Stream(src="encode:chunks", dst="output_0:chunks"))
video_filter["streams"]=streams
with open('video_filter.json', 'w') as f:
    json.dump(video_filter, f, indent=2, cls=Encoder)
