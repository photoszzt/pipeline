import json
from collections import OrderedDict
from spec import Encoder,Node,Stream,Config

random_cut=OrderedDict()
nodes=[]
nodes.append(Node(name="parlink", stage="parallelize_link", delivery_function=None, config=Config(framesperchunk="{fps}", chunklimit=None, duration=None, nworkers=None, nsockets=None, outdir=None, cmd=None), lambda_function=None))
nodes.append(Node(name="decode", stage="decode_from_chunked_link", delivery_function=None, config=Config(framesperchunk=None, chunklimit=None, duration=None, nworkers=None, nsockets=None, outdir=None, cmd=None), lambda_function=None))
nodes.append(Node(name="random_cut", stage="random_cut", delivery_function=None, config=Config(framesperchunk=None, chunklimit=None, duration=None, nworkers=None, nsockets=None, outdir=None, cmd=None), lambda_function=None))
nodes.append(Node(name="encode", stage="encode_frame_list", delivery_function="serialized_frame_delivery_func", config=Config(framesperchunk=None, chunklimit=None, duration=None, nworkers=None, nsockets=None, outdir=None, cmd=None), lambda_function=None))
random_cut["nodes"]=nodes
streams=[]
streams.append(Stream(src="input_0:video_link", dst="parlink:video_link"))
streams.append(Stream(src="parlink:chunked_link", dst="decode:chunked_link"))
streams.append(Stream(src="decode:frames", dst="random_cut:frames"))
streams.append(Stream(src="random_cut:frame", dst="encode:frame_list"))
streams.append(Stream(src="encode:chunks", dst="output_0:chunks"))
random_cut["streams"]=streams
with open('random_cut.json', 'w') as f:
    json.dump(random_cut, f, indent=2, cls=Encoder)
