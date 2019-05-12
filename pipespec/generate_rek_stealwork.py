import json
from collections import OrderedDict
from spec import Encoder,Node,Stream,Config

rek_stealwork=OrderedDict()
nodes=[]
nodes.append(Node(name="matchFace", stage="matchFace", delivery_function=None, config=Config(framesperchunk=None, chunklimit=None, duration=None, nworkers=None, nsockets=None, outdir=None, cmd=None), lambda_function=None))
nodes.append(Node(name="decode", stage="C_F_stealwork_decode", delivery_function=None, config=Config(framesperchunk=None, chunklimit=None, duration=None, nworkers=None, nsockets=None, outdir=None, cmd=None), lambda_function=None))
nodes.append(Node(name="scenechange", stage="scenechange", delivery_function=None, config=Config(framesperchunk=None, chunklimit=None, duration=None, nworkers=None, nsockets=None, outdir=None, cmd=None), lambda_function=None))
nodes.append(Node(name="rek", stage="rek", delivery_function="serialized_scene_delivery_func", config=Config(framesperchunk=None, chunklimit=None, duration=None, nworkers=None, nsockets=None, outdir=None, cmd=None), lambda_function=None))
nodes.append(Node(name="draw", stage="draw", delivery_function="serialized_scene_delivery_func", config=Config(framesperchunk=None, chunklimit=None, duration=None, nworkers=None, nsockets=None, outdir=None, cmd=None), lambda_function=None))
nodes.append(Node(name="encode", stage="encode_frame_list", delivery_function="serialized_frame_delivery_func", config=Config(framesperchunk=None, chunklimit=None, duration=None, nworkers=None, nsockets=None, outdir=None, cmd=None), lambda_function=None))
rek_stealwork["nodes"]=nodes
streams=[]
streams.append(Stream(src="input_0:chunks", dst="decode:chunks"))
streams.append(Stream(src="input_1:person", dst="matchFace:person"))
streams.append(Stream(src="decode:frames", dst="scenechange:frames"))
streams.append(Stream(src="scenechange:scene_list", dst="rek:scene_list"))
streams.append(Stream(src="rek:frame", dst="draw:frame"))
streams.append(Stream(src="draw:frame", dst="encode:frame_list"))
streams.append(Stream(src="encode:chunks", dst="output_0:chunks"))
rek_stealwork["streams"]=streams
with open('rek_stealwork.json', 'w') as f:
    json.dump(rek_stealwork, f, indent=2, cls=Encoder)
