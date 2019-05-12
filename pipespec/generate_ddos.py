import json
from collections import OrderedDict
from spec import Encoder,Node,Stream,Config

ddos=OrderedDict()
nodes=[]
nodes.append(Node(name="parlink", stage="parallelize_link", delivery_function=None, config=Config(framesperchunk="{fps}/4", chunklimit="1000", duration=None, nworkers=None, nsockets=None, outdir=None, cmd=None), lambda_function="lambda_test_JS2aw5Hx"))
nodes.append(Node(name="ddos", stage="ddos", delivery_function=None, config=Config(framesperchunk=None, chunklimit=None, duration="10", nworkers="4", nsockets="4", outdir="/tmp/out", cmd=None), lambda_function=None))
ddos["nodes"]=nodes
streams=[]
streams.append(Stream(src="input_0:video_link", dst="parlink:video_link"))
streams.append(Stream(src="parlink:chunked_link", dst="ddos:chunked_link"))
streams.append(Stream(src="ddos:chunked_link", dst="output_0:chunked_link"))
ddos["streams"]=streams
with open('ddos.json', 'w') as f:
    json.dump(ddos, f, indent=2, cls=Encoder)
