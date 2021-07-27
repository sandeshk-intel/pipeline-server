'''
* Copyright (C) 2019-2021 Intel Corporation.
*
* SPDX-License-Identifier: BSD-3-Clause
'''

import json
import spatial_analytics_events
from vaserving.common.utils import logging

logger = logging.get_logger('gva_event_convert', is_static=True)

def process_frame(frame):
    try:
        add_events_message(frame)
    except Exception as error:
            logger.error(error)
            return False
    return True

def add_events_message(frame):
    events = spatial_analytics_events.events(frame)
    if not events:
        return
    spatial_analytics_events.remove_events(frame)
    for message in frame.messages():
        message_obj = json.loads(message)
        if "objects" in message_obj:
            frame.remove_message(message)
            message_obj['events'] = events
            frame.add_message(json.dumps(message_obj, separators=(',', ':')))
            break
