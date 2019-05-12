import json
from collections import OrderedDict
from spec import Encoder,Node,Stream,Config

vidstab=OrderedDict()
nodes=[]
nodes.append(Node(name="parlink", stage="parallelize_link", delivery_function=None, config=Config(framesperchunk="{fps}", chunklimit=None, duration=None, nworkers=None, nsockets=None, outdir=None, cmd=None), lambda_function=None))
nodes.append(Node(name="decode", stage="decode_from_chunked_link", delivery_function=None, config=Config(framesperchunk=None, chunklimit=None, duration=None, nworkers=None, nsockets=None, outdir=None, cmd=None), lambda_function=None))
nodes.append(Node(name="vidstabdetect", stage="vidstabdetect", delivery_function=None, config=Config(framesperchunk=None, chunklimit=None, duration=None, nworkers=None, nsockets=None, outdir=None, cmd=None), lambda_function=None))
nodes.append(Node(name="vidstabaggregate", stage="vidstabaggregate", delivery_function=None, config=Config(framesperchunk=None, chunklimit=None, duration=None, nworkers=None, nsockets=None, outdir=None, cmd=None), lambda_function=None))
nodes.append(Node(name="vidstabtransform", stage="vidstabtransform", delivery_function=None, config=Config(framesperchunk=None, chunklimit=None, duration=None, nworkers=None, nsockets=None, outdir=None, cmd=None), lambda_function=None))
nodes.append(Node(name="encode", stage="encode_to_dash", delivery_function=None, config=Config(framesperchunk=None, chunklimit=None, duration=None, nworkers=None, nsockets=None, outdir=None, cmd=None), lambda_function=None))
vidstab["nodes"]=nodes
streams=[]
streams.append(Stream(src="input_0:video_link", dst="parlink:video_link"))
streams.append(Stream(src="parlink:chunked_link", dst="decode:chunked_link"))
streams.append(Stream(src="decode:frames", dst="grayscale:frames"))
streams.append(Stream(src="grayscale:frames", dst="encode:frames"))
streams.append(Stream(src="encode:chunks", dst="output_0:chunks"))
vidstab["streams"]=streams
with open('vidstab.json', 'w') as f:
    json.dump(vidstab, f, indent=2, cls=Encoder)
