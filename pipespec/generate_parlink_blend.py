import json
from collections import OrderedDict
from spec import Encoder,Node,Stream,Config

parlink_blend=OrderedDict()
nodes=[]
nodes.append(Node(name="parlink_0", stage="parallelize_link", delivery_function=None, config=Config(framesperchunk="{fps} * 2", chunklimit=None, duration=None, nworkers=None, nsockets=None, outdir=None, cmd=None), lambda_function=None))
nodes.append(Node(name="parlink_1", stage="parallelize_link", delivery_function=None, config=Config(framesperchunk="{fps} * 2", chunklimit=None, duration=None, nworkers=None, nsockets=None, outdir=None, cmd=None), lambda_function=None))
nodes.append(Node(name="decode_0", stage="decode_from_chunked_link", delivery_function=None, config=None, lambda_function=None))
nodes.append(Node(name="decode_1", stage="decode_from_chunked_link", delivery_function=None, config=None, lambda_function=None))
nodes.append(Node(name="blend", stage="blend", delivery_function="pair_delivery_func", config=None, lambda_function=None))
nodes.append(Node(name="encode", stage="encode_to_dash", delivery_function=None, config=None, lambda_function=None))
parlink_blend["nodes"]=nodes
streams=[]
streams.append(Stream(src="input_0:video_link", dst="parlink_0:video_link"))
streams.append(Stream(src="input_1:video_link", dst="parlink_1:video_link"))
streams.append(Stream(src="parlink_0:chunked_link", dst="decode_0:chunked_link"))
streams.append(Stream(src="parlink_1:chunked_link", dst="decode_1:chunked_link"))
streams.append(Stream(src="decode_0:frames", dst="blend:frames_0"))
streams.append(Stream(src="decode_1:frames", dst="blend:frames_1"))
streams.append(Stream(src="blend:frames", dst="encode:frames"))
streams.append(Stream(src="encode:chunks", dst="output_0:chunks"))
parlink_blend["streams"]=streams
with open('parlink_blend.json', 'w') as f:
    json.dump(parlink_blend, f, indent=2, cls=Encoder)
