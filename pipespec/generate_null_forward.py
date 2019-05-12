import json
from collections import OrderedDict
from spec import Encoder,Node,Stream,Config

null_forward=OrderedDict()
nodes=[]
nodes.append(Node(name="parlink", stage="parallelize_link", delivery_function=None, config=Config(framesperchunk="{fps}", chunklimit="1400", duration=None, nworkers=None, nsockets=None, outdir=None, cmd=None), lambda_function=None))
nodes.append(Node(name="null", stage="null", delivery_function=None, config=Config(framesperchunk=None, chunklimit=None, duration=None, nworkers=None, nsockets=None, outdir=None, cmd=None), lambda_function=None))
nodes.append(Node(name="null1", stage="null", delivery_function=None, config=Config(framesperchunk=None, chunklimit=None, duration=None, nworkers=None, nsockets=None, outdir=None, cmd=None), lambda_function=None))
nodes.append(Node(name="null2", stage="null", delivery_function=None, config=Config(framesperchunk=None, chunklimit=None, duration=None, nworkers=None, nsockets=None, outdir=None, cmd=None), lambda_function=None))
nodes.append(Node(name="null3", stage="null", delivery_function=None, config=Config(framesperchunk=None, chunklimit=None, duration=None, nworkers=None, nsockets=None, outdir=None, cmd=None), lambda_function=None))
nodes.append(Node(name="null4", stage="null", delivery_function=None, config=Config(framesperchunk=None, chunklimit=None, duration=None, nworkers=None, nsockets=None, outdir=None, cmd=None), lambda_function=None))
null_forward["nodes"]=nodes
streams=[]
streams.append(Stream(src="input_0:video_link", dst="parlink:video_link"))
streams.append(Stream(src="parlink:chunked_link", dst="null:chunked_link"))
streams.append(Stream(src="null:chunked_link", dst="null1:chunked_link"))
streams.append(Stream(src="null1:chunked_link", dst="null2:chunked_link"))
streams.append(Stream(src="null2:chunked_link", dst="null3:chunked_link"))
streams.append(Stream(src="null3:chunked_link", dst="null4:chunked_link"))
streams.append(Stream(src="null4:chunked_link", dst="output_0:chunked_link"))
null_forward["streams"]=streams
with open('null_forward.json', 'w') as f:
    json.dump(null_forward, f, indent=2, cls=Encoder)
