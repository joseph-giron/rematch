import os
import functools

import logger

import idc
import ida_kernwin


def get_plugin_base(*path):
  return os.path.join(idc.GetIdaDirectory(), "plugins", *path)


def get_plugin_path(*path):
  return get_plugin_base("rematch", *path)


def ida_kernel_queue(callback, write=False, wait=False):
  reqf = ida_kernwin.MFF_WRITE if write else ida_kernwin.MFF_READ
  if not wait:
    reqf |= ida_kernwin.MFF_NOWAIT

  @functools.wraps(callback)
  def enqueue(*args, **kwargs):
    partial_callback = functools.partial(callback, *args, **kwargs)
    r = ida_kernwin.execute_sync(partial_callback, reqf)
    if r == -1:
      logger.log('ida_main').warn("Possible failure in queueing for main "
                                  "thread with callback: {}, reqf: {}, args: "
                                  "{}, kwargs: {}".format(callback, reqf,
                                                          args, kwargs))
    elif wait:
      return r

  return enqueue
