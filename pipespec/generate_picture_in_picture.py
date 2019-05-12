import json
from collections import OrderedDict
from spec import Encoder,Node,Stream,Config

picture_in_picture=OrderedDict()
nodes=[]
nodes.append(Node(name="decode_0", stage="decode_from_url", delivery_function=None, config=None, lambda_function=None))
nodes.append(Node(name="decode_1", stage="decode_from_url", delivery_function=None, config=None, lambda_function=None))
nodes.append(Node(name="resize", stage="resize", delivery_function=None, config=None, lambda_function=None))
nodes.append(Node(name="overlay", stage="overlay", delivery_function="pair_delivery_func", config=None, lambda_function=None))
nodes.append(Node(name="encode", stage="encode_to_dash", delivery_function=None, config=None, lambda_function=None))
picture_in_picture["nodes"]=nodes
streams=[]
streams.append(Stream(src="input_0:video_url", dst="decode_0:video_url"))
streams.append(Stream(src="input_1:video_url", dst="decode_1:video_url"))
streams.append(Stream(src="decode_0:frames", dst="overlay:frames_0"))
streams.append(Stream(src="decode_1:frames", dst="resize:frames"))
streams.append(Stream(src="resize:frames", dst="overlay:frames_1"))
streams.append(Stream(src="overlay:frames", dst="encode:frames"))
streams.append(Stream(src="encode:chunks", dst="output_0:chunks"))
picture_in_picture["streams"]=streams
with open('picture_in_picture.json', 'w') as f:
    json.dump(picture_in_picture, f, indent=2, cls=Encoder)
