#!/usr/bin/python
import logging
from sprocket.controlling.tracker.machine_state import TerminalState, CommandListState, ForLoopState, OnePassState, ErrorState
from sprocket.config import settings
from sprocket.stages import InitStateTemplate
from sprocket.stages.util import default_trace_func
from sprocket.util.misc import rand_str
import boto3


class FinalState(TerminalState):
    extra = "(finished)"


class EmitState(CommandListState):
    extra = "(emit output)"
    nextState = FinalState
    commandlist = [ (None, "quit:")
                  ]

    def __init__(self, prevState):
        super(EmitState, self).__init__(prevState)
        self.emit_event('frames', {'metadata': self.in_events['frames_0']['metadata'], 'key': self.local['out_key']})


class RunState(CommandListState):
    extra = "(run)"
    nextState = EmitState
    commandlist = [ (None, 'run:mkdir -p ##TMPDIR##/in_0/ ##TMPDIR##/in_1/ ##TMPDIR##/out_0/')
                  , ('OK:RETVAL(0)', 'collect:{in_key_0} ##TMPDIR##/in_0')
                  , ('OK:COLLECT', 'collect:{in_key_1} ##TMPDIR##/in_1')
                  , ('OK:COLLECT', 'run:time ./ffmpeg -y -i ##TMPDIR##/in_0/%08d.png -i ##TMPDIR##/in_1/%08d.png -filter_complex '
                                   '\'scale2ref[1:v][0:v]; [0:v][1:v]blend=all_mode=average\' ##TMPDIR##/out_0/%08d.png')
                  , ('OK:RETVAL(0)', 'emit:##TMPDIR##/out_0 {out_key}')
                  , ('OK:EMIT', None)
                    ]

    def __init__(self, prevState):
        super(RunState, self).__init__(prevState)
        s3_client = boto3.client('s3')
        bucket_name = ''
        if settings.get('hash_bucket'):
            bucket_name = settings['temp_storage_base'] + rand_str(1)
            self.local['out_key'] = 's3://' + bucket_name + '/' + rand_str(16) + '/'
        else:
            bucket_name = settings['storage_base'] + rand_str(16)
            self.local['out_key'] = 's3://' + bucket_name + '/'
        s3_client.create_bucket(Bucket=bucket_name)

        params = {'in_key_0': self.in_events['frames_0']['key'], 'in_key_1': self.in_events['frames_1']['key'],
                  'out_key': self.local['out_key']}
        logging.debug('params: '+str(params))
        self.commands = [ s.format(**params) if s is not None else None for s in self.commands ]


class InitState(InitStateTemplate):
    nextState = RunState

    def __init__(self, prevState, **kwargs):
        super(InitState, self).__init__(prevState, **kwargs)
        self.trace_func = lambda ev, msg, op: default_trace_func(ev, msg, op, stage='blend')
