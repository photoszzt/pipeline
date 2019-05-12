import json
from collections import OrderedDict
from pprint import pprint
import os


def iterable(cls):
    def iterfn(self):
        iters = dict((x, y) for x, y in cls.__dict__.items() if x[:2] != '__')
        iters.update(self.__dict__)

        for x, y in iters.items():
            if y != None:
                yield x, y

    cls.__iter__ = iterfn
    return cls


@iterable
class Node(object):
    def __init__(self, name=None, stage=None, delivery_function=None, config=None, lambda_function=None):
        self.name = name
        self.stage = stage
        self.delivery_function = delivery_function
        self.config = config
        self.lambda_function = lambda_function


@iterable
class Stream(object):
    def __init__(self, src=None, dst=None):
        self.src = src
        self.dst = dst


@iterable
class Config(object):
    def __init__(self, framesperchunk=None, chunklimit=None, duration=None, nworkers=None, nsockets=None, outdir=None, cmd=None):
        self.framesperchunk = framesperchunk
        self.chunklimit = chunklimit
        self.duration = duration
        self.nworkers = nworkers
        self.nsockets = nsockets
        self.outdir = outdir
        self.cmd = cmd


class Encoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, Config) or isinstance(obj, Stream) or isinstance(obj, Node):
            return OrderedDict(obj)
        else:
            return super().default(obj)


def decode_config(dct):
    if dct != None:
        return Config(framesperchunk=dct.get("framesperchunk"),
                      chunklimit=dct.get("chunklimit"),
                      duration=dct.get("duration"),
                      nworkers=dct.get("nworkers"),
                      nsockets=dct.get("nsockets"),
                      outdir=dct.get("outdir"),
                      cmd=dct.get("cmd")
                      )
    return dct


def decode(dct):
    if "name" in dct and "stage" in dct:
        return Node(name=dct.get("name"), stage=dct.get("stage"),
                    delivery_function=dct.get("delivery_function"),
                    config=decode_config(dct.get("config")),
                    lambda_function=dct.get("lambda_function"))
    elif "src" in dct and "dst" in dct:
        return Stream(src=dct["src"], dst=dct["dst"])
    else:
        return dct


def val_str(val):
    if val != None:
        return "\""+str(val)+"\""
    else:
        return "None"


def config_str(config):
    if config != None:
        return "Config(framesperchunk=" + val_str(config.framesperchunk) + \
            ", chunklimit=" + val_str(config.chunklimit) + \
            ", duration=" + val_str(config.duration) + \
            ", nworkers=" + val_str(config.nworkers) + \
            ", nsockets=" + val_str(config.nsockets) + \
            ", outdir=" + val_str(config.outdir) + \
            ", cmd=" + val_str(config.cmd) + ")"
    else:
        return "None"
