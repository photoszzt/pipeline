import json
from collections import OrderedDict
from spec import Encoder,Node,Stream,Config

stream_grayscale=OrderedDict()
nodes=[]
nodes.append(Node(name="streamlink", stage="stream_link", delivery_function=None, config=Config(framesperchunk="{fps}", chunklimit=None, duration=None, nworkers=None, nsockets=None, outdir=None, cmd=None), lambda_function=None))
nodes.append(Node(name="decode", stage="decode_from_chunked_link", delivery_function=None, config=Config(framesperchunk=None, chunklimit=None, duration=None, nworkers=None, nsockets=None, outdir=None, cmd=None), lambda_function=None))
nodes.append(Node(name="grayscale", stage="grayscale_flat", delivery_function=None, config=Config(framesperchunk=None, chunklimit=None, duration=None, nworkers=None, nsockets=None, outdir=None, cmd=None), lambda_function=None))
nodes.append(Node(name="encode", stage="encode_frame_list", delivery_function="serialized_frame_delivery_func", config=Config(framesperchunk=None, chunklimit=None, duration=None, nworkers=None, nsockets=None, outdir=None, cmd=None), lambda_function=None))
stream_grayscale["nodes"]=nodes
streams=[]
streams.append(Stream(src="input_0:video_link", dst="streamlink:video_link"))
streams.append(Stream(src="streamlink:chunked_link", dst="decode:chunked_link"))
streams.append(Stream(src="decode:frames", dst="grayscale:frames"))
streams.append(Stream(src="grayscale:frame", dst="encode:frame_list"))
streams.append(Stream(src="encode:chunks", dst="output_0:chunks"))
stream_grayscale["streams"]=streams
with open('stream_grayscale.json', 'w') as f:
    json.dump(stream_grayscale, f, indent=2, cls=Encoder)
