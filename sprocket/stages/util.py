#!/usr/bin/python
import time

from sprocket.config import settings
from sprocket.util import lightlog
from sprocket.util.misc import rand_str
import boto3


def default_trace_func(in_events, msg, op, **kwargs):
    """Log every command message sent/recv by the state machine.
    op includes send/recv/undo_recv/kick
    """
    # logger = logging.getLogger(in_events.values()[0]['metadata']['pipe_id'])
    # logger.debug('%s, %s, %s', in_events.values()[0]['metadata']['lineage'], op, escape_for_csv(msg))
    logger = lightlog.getLogger(in_events.values()[0]['metadata']['pipe_id'])
    logger.debug(ts=time.time(), lineage=in_events.values()[0]['metadata']['lineage'], op=op, msg=msg, **kwargs)


def staged_trace_func(stage, num_frames, worker_called, in_events, msg, op):
    """Log every command message sent/recv by the state machine.
    op includes send/recv/undo_recv/kick
    """
    logger = lightlog.getLogger(in_events.values()[0]['metadata']['pipe_id'])
    logger.debug(stage=stage, num_frames=num_frames, worker_called=worker_called, lineage=in_events.values()[0]['metadata']['lineage'], op=op, msg=msg)


def get_output_from_message(msg):
    o_marker = '):OUTPUT('
    c_marker = '):COMMAND('
    if msg.count(o_marker) != 1 or msg.count(c_marker) != 1:
        raise Exception('incorrect message format: ' + msg)
    return msg[msg.find(o_marker) + len(o_marker):msg.find(c_marker)]


def preprocess_config(config, existing):
    new_config = {}
    for k, v in config.iteritems():
        try:
            new_value = v.format(**existing)
            new_value = eval(new_value)
            new_config[k] = new_value
        except:
            new_config[k] = v
    return new_config

def get_output_key():
    s3_client = boto3.client('s3')
    if settings.get('hash_bucket'):
        bucket_name = settings['temp_storage_base'] + rand_str(1)
        s3_client.create_client(Bucket=bucket_name)
        return 's3://' + bucket_name + '/' + rand_str(16) + '/'
    else:
        bucket_name = settings['storage_base'] + rand_str(16)
        s3_client.create_client(Bucket=bucket_name)
        return 's3://' + bucket_name + '/'
