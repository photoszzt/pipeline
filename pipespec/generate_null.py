import json
from collections import OrderedDict
from spec import Encoder,Node,Stream,Config

null=OrderedDict()
nodes=[]
nodes.append(Node(name="parlink", stage="parallelize_link", delivery_function=None, config=Config(framesperchunk="{fps}", chunklimit=None, duration=None, nworkers=None, nsockets=None, outdir=None, cmd=None), lambda_function=None))
nodes.append(Node(name="null", stage="null", delivery_function=None, config=Config(framesperchunk=None, chunklimit=None, duration=None, nworkers=None, nsockets=None, outdir=None, cmd=None), lambda_function=None))
null["nodes"]=nodes
streams=[]
streams.append(Stream(src="input_0:video_link", dst="parlink:video_link"))
streams.append(Stream(src="parlink:chunked_link", dst="null:chunked_link"))
streams.append(Stream(src="null:chunked_link", dst="output_0:chunked_link"))
null["streams"]=streams
with open('null.json', 'w') as f:
    json.dump(null, f, indent=2, cls=Encoder)
