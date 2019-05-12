import json
from collections import OrderedDict
from spec import Encoder,Node,Stream,Config

rek=OrderedDict()
nodes=[]
nodes.append(Node(name="parallelize_link", stage="parallelize_link", delivery_function=None, config=Config(framesperchunk=None, chunklimit=None, duration=None, nworkers=None, nsockets=None, outdir=None, cmd=None), lambda_function=None))
nodes.append(Node(name="matchFace", stage="matchFace", delivery_function=None, config=Config(framesperchunk=None, chunklimit=None, duration=None, nworkers=None, nsockets=None, outdir=None, cmd=None), lambda_function=None))
nodes.append(Node(name="decode", stage="rek_decode", delivery_function=None, config=Config(framesperchunk=None, chunklimit=None, duration=None, nworkers=None, nsockets=None, outdir=None, cmd=None), lambda_function=None))
nodes.append(Node(name="scenechange", stage="scenechange", delivery_function=None, config=Config(framesperchunk=None, chunklimit=None, duration=None, nworkers=None, nsockets=None, outdir=None, cmd=None), lambda_function=None))
nodes.append(Node(name="rek", stage="rek", delivery_function="serialized_scene_delivery_func", config=Config(framesperchunk=None, chunklimit=None, duration=None, nworkers=None, nsockets=None, outdir=None, cmd=None), lambda_function=None))
nodes.append(Node(name="draw", stage="draw", delivery_function="serialized_scene_delivery_func", config=Config(framesperchunk=None, chunklimit=None, duration=None, nworkers=None, nsockets=None, outdir=None, cmd=None), lambda_function=None))
nodes.append(Node(name="encode", stage="encode_frame_list", delivery_function="serialized_frame_delivery_func", config=Config(framesperchunk=None, chunklimit=None, duration=None, nworkers=None, nsockets=None, outdir=None, cmd=None), lambda_function=None))
rek["nodes"]=nodes
streams=[]
streams.append(Stream(src="input_0:video_link", dst="parallelize_link:video_link"))
streams.append(Stream(src="input_1:person", dst="matchFace:person"))
streams.append(Stream(src="parallelize_link:chunked_link", dst="decode:chunked_link"))
streams.append(Stream(src="decode:frames", dst="scenechange:frames"))
streams.append(Stream(src="scenechange:scene_list", dst="rek:scene_list"))
streams.append(Stream(src="rek:frame", dst="draw:frame"))
streams.append(Stream(src="draw:frame", dst="encode:frame_list"))
streams.append(Stream(src="encode:chunks", dst="output_0:chunks"))
rek["streams"]=streams
with open('rek.json', 'w') as f:
    json.dump(rek, f, indent=2, cls=Encoder)
