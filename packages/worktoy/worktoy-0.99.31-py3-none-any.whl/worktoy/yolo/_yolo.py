"""The 'yolo' function receives any number of callables and runs them."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

import os
import sys
import time
from math import log
from typing import Callable

from worktoy.text import stringList


def yolo(*args: Callable) -> None:
  """The 'yolo' function receives any number of callables and runs them."""
  tic = time.perf_counter_ns()
  print('Running python script located at: \n%s' % sys.argv[0])
  print('Started at: %s' % time.ctime())
  print(77 * '-')
  retCode = 0
  for callMeMaybe in args:
    print('\nRunning: %s\n' % callMeMaybe.__name__)
    try:
      retCode = callMeMaybe()
    except BaseException as exception:
      exceptionTypeName = exception.__class__.__name__
      exceptionMessage = str(exception)
      print('ENCOUNTERED!\n  %s: %s' % (exceptionTypeName, exceptionMessage))
      tb = exception.__traceback__
      while True:
        fileName = tb.tb_frame.f_code.co_filename
        if fileName == __file__:
          tb = tb.tb_next
          if tb is None:
            break
          continue
        lineNumber = tb.tb_lineno
        print("""In file: '%s', at line: %d""" % (fileName, lineNumber))
        with open(fileName, 'r') as file:
          data = file.readlines()
        for i in range(lineNumber - 3, lineNumber + 3):
          if 0 < i < len(data):
            line = data[i].replace(os.linesep, '')
            if i - lineNumber + 1:
              print('  %03d:    %s   ' % (i, line))
            else:
              print('  %03d: >> %s << ' % (i, line))
        if getattr(tb, 'tb_next', None):
          tb = tb.tb_next
        else:
          break

      retCode = -1
  retCode = 0 if retCode is None else retCode
  print(77 * '-')
  print('Return Code: %s' % retCode)
  toc = int(time.perf_counter_ns() - tic)
  n = 0
  n = int(log(toc) / log(1e03))
  prefixes = stringList("""nano, micro, milli""")
  if n < 3:
    prefix = prefixes[n]
    msg = """Runtime: %d %s-seconds"""
    print(msg % (int(toc * 1e-03 ** n), prefix))
    sys.exit(0)
  toc *= 1e-09
  seconds = int(toc) % 60
  toc = int(toc - seconds)
  minutes = toc % 60
  toc = int(toc - minutes)
  hours = toc % 24
  toc = int(toc - hours)
  if hours:
    msg = """Runtime: %d hours, %d minutes, %d seconds - Completed on %s"""
    print(msg % (hours, minutes, seconds, time.ctime()))
  elif minutes:
    msg = """Runtime: %d minutes, %d seconds - Completed on %s"""
    print(msg % (minutes, seconds, time.ctime()))
  else:
    msg = """Runtime: %d seconds - Completed on %s"""
    print(msg % (seconds, time.ctime()))
