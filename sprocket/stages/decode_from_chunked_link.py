#!/usr/bin/python
# coding=utf-8
import logging

from sprocket.controlling.tracker.machine_state import TerminalState, CommandListState, ForLoopState, OnePassState, ErrorState, IfElseState
from sprocket.config import settings
from sprocket.stages import InitStateTemplate
from sprocket.stages.util import default_trace_func, get_output_from_message
from sprocket.util.misc import rand_str
import boto3


class FinalState(OnePassState):
    extra = "(sending quit)"
    expect = None
    command = "quit:"
    nextState = TerminalState

    def __init__(self, prevState):
        super(FinalState, self).__init__(prevState)


class ConfirmEmitState(OnePassState):
    extra = "(confirm emit)"
    expect = 'OK:EMIT'
    command = None
    nextState = FinalState

    def __init__(self, prevState):
        super(ConfirmEmitState, self).__init__(prevState)

    def post_transition(self):
        self.emit_event('frames', {'metadata': self.in_events['chunked_link']['metadata'], 'key': self.local['out_key']
            , 'nframes': self.local['output_count']})

        #for smart serialization 
        lineage = self.in_events['chunked_link']['metadata']['lineage']
        return self.nextState(self)  # don't forget this


class TryEmitState(OnePassState):
    extra = "(emit output)"
    expect = None
    command = 'emit:##TMPDIR##/out_0 {out_key}'
    nextState = ConfirmEmitState

    def __init__(self, prevState):
        super(TryEmitState, self).__init__(prevState)
        params = {'out_key': self.local['out_key']}
        self.command = self.command.format(**params)


class CheckOutputState(IfElseState):
    extra = "(check output)"
    expect = 'OK:RETVAL('
    consequentState = TryEmitState
    alternativeState = FinalState

    def testfn(self):
        self.local['output_count'] = int(get_output_from_message(self.messages[-1]))
        return self.local['output_count'] > 0

    def __init__(self, prevState):
        super(CheckOutputState, self).__init__(prevState)


class RunState(CommandListState):
    extra = "(run)"
    nextState = CheckOutputState
    commandlist = [(None, 'run:mkdir -p ##TMPDIR##/out_0/')
        , ('OK:RETVAL(0)',
           'run:./youtube-dl --get-url {URL} -f "{selector}" 2>/dev/null | head -n1 | xargs -IPLACEHOLDER '
           './ffmpeg -y -ss {starttime} -i PLACEHOLDER -frames {frames} -f image2 -c:v png '
           '-start_number 1 ##TMPDIR##/out_0/%08d.png')
        , ('OK:RETVAL(0)', 'run:find ##TMPDIR##/out_0/ -name "*png" | wc -l')
                   # result will be used in next state
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

        params = {'starttime': self.in_events['chunked_link']['starttime'],
                  'frames': self.in_events['chunked_link']['frames'],
                  'URL': self.in_events['chunked_link']['key'],
                  'selector': self.in_events['chunked_link']['selector'],
                  'out_key': self.local['out_key']}
        logging.debug('params: ' + str(params))
        self.commands = [s.format(**params) if s is not None else None for s in self.commands]


class InitState(InitStateTemplate):
    nextState = RunState

    def __init__(self, prevState, **kwargs):
        super(InitState, self).__init__(prevState, **kwargs)
        self.trace_func = lambda ev, msg, op: default_trace_func(ev, msg, op, stage='decode')
