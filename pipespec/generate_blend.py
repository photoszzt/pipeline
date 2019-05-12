import json
from collections import OrderedDict
from spec import Encoder,Node,Stream

blend=OrderedDict()
nodes=[]
nodes.append(Node(name="decode_0", stage="decode", delivery_function=None, config=None, lambda_function=None))
nodes.append(Node(name="decode_1", stage="decode", delivery_function=None, config=None, lambda_function=None))
nodes.append(Node(name="blend", stage="blend", delivery_function="pair_delivery_func", config=None, lambda_function=None))
nodes.append(Node(name="encode", stage="encode_to_dash", delivery_function=None, config=None, lambda_function=None))
blend["nodes"]=nodes
streams=[]
streams.append(Stream(src="input_0:chunks", dst="decode_0:chunks"))
streams.append(Stream(src="input_1:chunks", dst="decode_1:chunks"))
streams.append(Stream(src="decode_0:frames", dst="blend:frames_0"))
streams.append(Stream(src="decode_1:frames", dst="blend:frames_1"))
streams.append(Stream(src="blend:frames", dst="encode:frames"))
streams.append(Stream(src="encode:chunks", dst="output_0:chunks"))
blend["streams"]=streams
with open('blend.json', 'w') as f:
    json.dump(blend, f, indent=2, cls=Encoder)
