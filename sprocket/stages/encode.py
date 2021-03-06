#!/usr/bin/python
import logging

from sprocket.controlling.tracker.machine_state import TerminalState, CommandListState, ForLoopState, OnePassState, ErrorState
from sprocket.config import settings
from sprocket.stages.util import default_trace_func
from sprocket.util.misc import rand_str


class FinalState(TerminalState):
    extra = "(finished)"


class EmitState(CommandListState):
    extra = "(emit output)"
    nextState = FinalState
    commandlist = [ (None, "quit:")
                  ]

    def __init__(self, prevState):
        super(EmitState, self).__init__(prevState, trace_func=default_trace_func)
        emit = prevState.emit
        out_key = prevState.out_key

        emit('chunks', {'metadata': self.in_events['frames']['metadata'], 'key': out_key})


class RunState(CommandListState):
    extra = "(run)"
    nextState = EmitState
    commandlist = [ (None, 'run:mkdir -p ##TMPDIR##/in_0/')
                  , ('OK:RETVAL(0)', 'collect:{in_key} ##TMPDIR##/in_0')
                  , ('OK:COLLECT', 'run:mkdir -p ##TMPDIR##/out_0/')
                  , ('OK:RETVAL(0)', 'run:time ./ffmpeg -framerate {fps} -start_number 1 -i ##TMPDIR##/in_0/%08d.png '
                                   '-c:v libx264 -pix_fmt yuv420p ##TMPDIR##/out_0/{segment}.mp4')
                  , ('OK:RETVAL(0)', 'emit:##TMPDIR##/out_0 {out_key}')
                  , ('OK:EMIT', None)
                    ]

    def __init__(self, prevState):
        super(RunState, self).__init__(prevState, trace_func=default_trace_func)
        self.emit = prevState.emit
        self.out_key = prevState.out_key

        params = {'in_key': self.in_events['frames']['key'], 'fps': self.in_events['frames']['metadata']['fps'],
                  'segment': '%08d'%int(self.in_events['metadata']['lineage']), 'out_key': self.out_key}
        logging.debug('params: '+str(params))
        self.commands = [ s.format(**params) if s is not None else None for s in self.commands ]


class InitState(CommandListState):
    extra = "(init)"
    nextState = RunState
    commandlist = [ ("OK:HELLO", "seti:nonblock:0")
                  , "run:rm -rf /tmp/*"
                  , "run:mkdir -p ##TMPDIR##"
                  , None
                  ]

    def __init__(self, prevState, in_events, emit):
        super(InitState, self).__init__(prevState, in_events=in_events, trace_func=default_trace_func)
        self.emit = emit
        self.out_key = settings['storage_base']+in_events['frames']['metadata']['pipe_id']+'/encode/'+rand_str(16)+'/'
        logging.debug('in_events: '+str(in_events)+', emit: '+str(emit))
