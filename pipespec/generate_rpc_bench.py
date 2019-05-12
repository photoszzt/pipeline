import json
from collections import OrderedDict
from spec import Encoder,Node,Stream,Config

rpc_bench=OrderedDict()
nodes=[]
nodes.append(Node(name="rpc_bench", stage="rpc_bench", delivery_function=None, config=Config(framesperchunk=None, chunklimit=None, duration=None, nworkers=None, nsockets=None, outdir=None, cmd=None), lambda_function=None))
rpc_bench["nodes"]=nodes
streams=[]
streams.append(Stream(src="input_0:chunks", dst="rpc_bench:chunks"))
streams.append(Stream(src="rpc_bench:chunks", dst="output_0:chunks"))
rpc_bench["streams"]=streams
with open('rpc_bench.json', 'w') as f:
    json.dump(rpc_bench, f, indent=2, cls=Encoder)
