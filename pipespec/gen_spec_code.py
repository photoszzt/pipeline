import json
import os
from spec import decode,val_str,config_str

for file_name in os.listdir("."):
    if file_name.endswith(".pipe"):
        with open(file_name) as f:
            print(file_name)
            data = f.read()
            z = json.loads(data, object_hook=decode)
            base = os.path.basename(file_name)
            name_arr = os.path.splitext(base)
            with open("generate_"+name_arr[0]+".py", 'w') as cg:
                cg.write("import json\n")
                cg.write("from collections import OrderedDict\n")
                cg.write("from spec import Encoder,Node,Stream\n")
                cg.write("\n")
                cg.write(name_arr[0]+"=OrderedDict()\n")
                cg.write("nodes=[]\n")
                for i in z["nodes"]:
                    cg.write("nodes.append(Node(name="+val_str(i.name) +
                             ", stage="+val_str(i.stage)+", delivery_function="+val_str(i.delivery_function) +
                             ", config="+config_str(i.config) + ", lambda_function="+val_str(i.lambda_function)+"))\n")
                cg.write(name_arr[0]+"[\"nodes\"]=nodes\n")
                cg.write("streams=[]\n")
                for i in z["streams"]:
                    cg.write(
                        "streams.append(Stream(src="+val_str(i.src)+", dst="+val_str(i.dst)+"))\n")
                cg.write(name_arr[0]+"[\"streams\"]=streams\n")
                cg.write("with open(\'"+name_arr[0]+".json\', \'w\') as f:\n")
                cg.write("    json.dump("+name_arr[0]+", f, indent=2, cls=Encoder)\n")
