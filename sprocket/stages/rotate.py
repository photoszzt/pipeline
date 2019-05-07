#!/usr/bin/python
import logging

from sprocket.controlling.tracker.machine_state import TerminalState, CommandListState, ForLoopState, OnePassState, ErrorState
from sprocket.config import settings
from sprocket.stages import InitStateTemplate, ExtractTarStateTemplate, CreateTarStateTemplate, FinalStateTemplate
from sprocket.stages.util import default_trace_func
from sprocket.util.misc import rand_str
import boto3


class FinalState(FinalStateTemplate):
    pass


class ConfirmEmitState(OnePassState):
    extra = "(confirm emit)"
    expect = 'OK:EMIT'
    command = None
    nextState = FinalState

    def __init__(self, prevState):
        super(ConfirmEmitState, self).__init__(prevState)

    def post_transition(self):
        self.emit_event('frames', {'metadata': self.in_events['frames']['metadata'], 'key': self.local['out_key']})
        return self.nextState(self)  # don't forget this


class TryEmitState(CommandListState):
    extra = "(emit output)"
    commandlist = [  (None, 'emit:##TMPDIR##/out_0 {out_key}')
    ]
    nextState = ConfirmEmitState

    def __init__(self, prevState):
        super(TryEmitState, self).__init__(prevState)
        s3_client = boto3.client('s3')
        bucket_name = ''
        if settings.get('hash_bucket'):
            bucket_name = settings['temp_storage_base'] + rand_str(1)
            self.local['out_key'] = 's3://' + bucket_name + '/' + rand_str(16) + '/'
        else:
            bucket_name = settings['storage_base'] + rand_str(16)
            self.local['out_key'] = 's3://' + bucket_name + '/'
        s3_client.create_bucket(Bucket=bucket_name)
        params = {'out_key': self.local['out_key']}
        self.commands = [ s.format(**params) if s is not None else None for s in self.commands ]


class CreateTarState(CreateTarStateTemplate):
    nextState = TryEmitState
    tar_dir = '##TMPDIR##/out_0'


class RunState(CommandListState):
    extra = "(run)"
    nextState = CreateTarState if settings.get('use_tar') else TryEmitState
    commandlist = [ (None, 'run:mkdir -p ##TMPDIR##/out_0/')
                  , ('OK:RETVAL(0)', 'run:./ffmpeg -start_number 1 -i ##TMPDIR##/in_0/%08d.png '
                                     '-vf "transpose=2,transpose=2" -c:a copy -safe 0 -start_number 1 ##TMPDIR##/out_0/%08d.png')
                  , ('OK:RETVAL(0)', None)
                    ]

    def __init__(self, prevState):
        super(RunState, self).__init__(prevState)

        params = {'in_key': self.in_events['frames']['key']}
        logging.debug('params: '+str(params))
        self.commands = [ s.format(**params) if s is not None else None for s in self.commands ]


class ExtractTarState(ExtractTarStateTemplate):
    tar_dir = '##TMPDIR##/in_0/'
    nextState = RunState


class CollectState(CommandListState):
    nextState = ExtractTarState if settings.get('use_tar') else RunState
    commandlist = [
        (None, 'run:mkdir -p ##TMPDIR##/in_0/')
        , ('OK:RETVAL(0)', 'collect:{in_key} ##TMPDIR##/in_0')
        , ('OK:COLLECT', None)
    ]

    def __init__(self, prevState):
        super(CollectState, self).__init__(prevState)
        params = {'in_key': self.in_events['frames']['key']}
        self.commands = [s.format(**params) if s is not None else None for s in self.commands]


class InitState(InitStateTemplate):
    nextState = CollectState

    def __init__(self, prevState, **kwargs):
        super(InitState, self).__init__(prevState, **kwargs)
        self.trace_func = lambda ev, msg, op: default_trace_func(ev, msg, op, stage='rotate')
