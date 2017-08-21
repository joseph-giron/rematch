import os
import functools

import idc
import ida_kernwin


def get_plugin_base(*path):
  return os.path.join(idc.GetIdaDirectory(), "plugins", *path)


def get_plugin_path(*path):
  return get_plugin_base("rematch", *path)


class ida_kernel_queue(object):
  def __init__(self, write=False, wait=False):
    self.wait = wait
    self.reqf = ida_kernwin.MFF_WRITE if write else ida_kernwin.MFF_READ
    if not self.wait:
      self.reqf |= ida_kernwin.MFF_NOWAIT

    self.__ret = None
    self.called = False

  def __call__(self, callback):
    if self.called:
      raise Exception("Can't be called twice!")
    self.called = True

    @functools.wraps(callback)
    def enqueue(*args, **kwargs):
      def partial_callback():
        self.__ret = callback(*args, **kwargs)
      ida_kernwin.execute_sync(partial_callback, self.reqf)
      return self.__ret

    return enqueue
