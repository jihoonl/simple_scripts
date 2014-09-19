#!/usr/bin/env python

import os
import sys
import rospkg
import rosmsg
import genmsg

class ROSMsgException(Exception): pass

def get_search_path():
    rospack = rospkg.RosPack()
    search_path = {}
    for p in rospack.list():
        package_paths = rosmsg._get_package_paths(p, rospack)
        search_path[p] = [os.path.join(d, 'msg') for d in package_paths]
    return search_path


def get_spec(msg_type, search_path):
    context = genmsg.MsgContext.create_default()
    try:
        spec = genmsg.load_msg_by_type(context, msg_type, search_path)
        genmsg.load_depends(context, spec, search_path)
    except Exception as e:
        raise ROSMsgException("Unable to load msg [%s]: %s"%(msg_type, e))
    return spec

if __name__ == '__main__':

    if len(sys.argv) < 2:
        print 'Usage : get_msg_spec.py <MESSAGE TYPE>'
        sys.exit(0)

    msg_type = sys.argv[1]
    search_path = get_search_path()
    spec = get_spec(msg_type, search_path)    

    ## spec is genmsg.MsgSpec object. Look https://github.com/ros/genmsg/blob/indigo-devel/src/genmsg/msgs.py#L228 for the details.
    print(type(spec))

    # Check rosmsg.spec_to_str to print out full message spec with dependent mesasges. https://github.com/ros/ros_comm/blob/indigo-devel/tools/rosmsg/src/rosmsg/__init__.py#L365 
    print('Name  : ' + spec.full_name)

    print('== Variables ==')
    for type_, name in zip(spec.types, spec.names): 
        print('%s(%s)'%(name, type_))

    print('')

    # Constant is genmsg.Consant object. Look https://github.com/ros/genmsg/blob/indigo-devel/src/genmsg/msgs.py#L158
    print('== Constants ==')
    print(str(spec.constants))
