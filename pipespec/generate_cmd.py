import json
from collections import OrderedDict
from spec import Encoder,Node,Stream,Config

cmd=OrderedDict()
nodes=[]
nodes.append(Node(name="cmd", stage="cmd", delivery_function=None, config=Config(framesperchunk=None, chunklimit=None, duration=None, nworkers=None, nsockets=None, outdir=None, cmd="sleep 5"), lambda_function=None))
cmd["nodes"]=nodes
streams=[]
streams.append(Stream(src="input_0:chunked_link", dst="cmd:chunked_link"))
streams.append(Stream(src="cmd:chunked_link", dst="output_0:chunked_link"))
cmd["streams"]=streams
with open('cmd.json', 'w') as f:
    json.dump(cmd, f, indent=2, cls=Encoder)
