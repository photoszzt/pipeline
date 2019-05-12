import json
from collections import OrderedDict
from spec import Encoder,Node,Stream,Config

singlestage_transform=OrderedDict()
nodes=[]
nodes.append(Node(name="transform", stage="C_C_stealwork_transform", delivery_function=None, config=Config(framesperchunk=None, chunklimit=None, duration=None, nworkers=None, nsockets=None, outdir=None, cmd=None), lambda_function=None))
singlestage_transform["nodes"]=nodes
streams=[]
streams.append(Stream(src="input_0:chunks", dst="transform:chunks"))
streams.append(Stream(src="transform:chunks", dst="output_0:chunks"))
singlestage_transform["streams"]=streams
with open('singlestage_transform.json', 'w') as f:
    json.dump(singlestage_transform, f, indent=2, cls=Encoder)
