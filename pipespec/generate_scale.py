import json
from collections import OrderedDict
from spec import Encoder,Node,Stream,Config

scale=OrderedDict()
nodes=[]
nodes.append(Node(name="parlink", stage="parallelize_link", delivery_function=None, config=Config(framesperchunk="{fps}", chunklimit=None, duration=None, nworkers=None, nsockets=None, outdir=None, cmd=None), lambda_function=None))
nodes.append(Node(name="decode", stage="decode_from_chunked_link", delivery_function=None, config=Config(framesperchunk=None, chunklimit=None, duration=None, nworkers=None, nsockets=None, outdir=None, cmd=None), lambda_function=None))
nodes.append(Node(name="scale", stage="scale", delivery_function=None, config=Config(framesperchunk=None, chunklimit=None, duration=None, nworkers=None, nsockets=None, outdir=None, cmd=None), lambda_function=None))
nodes.append(Node(name="encode", stage="encode_frame_list", delivery_function="serialized_frame_delivery_func", config=Config(framesperchunk=None, chunklimit=None, duration=None, nworkers=None, nsockets=None, outdir=None, cmd=None), lambda_function=None))
scale["nodes"]=nodes
streams=[]
streams.append(Stream(src="input_0:video_link", dst="parlink:video_link"))
streams.append(Stream(src="parlink:chunked_link", dst="decode:chunked_link"))
streams.append(Stream(src="decode:frames", dst="scale:frames"))
streams.append(Stream(src="scale:frame", dst="encode:frame_list"))
streams.append(Stream(src="encode:chunks", dst="output_0:chunks"))
scale["streams"]=streams
with open('scale.json', 'w') as f:
    json.dump(scale, f, indent=2, cls=Encoder)
