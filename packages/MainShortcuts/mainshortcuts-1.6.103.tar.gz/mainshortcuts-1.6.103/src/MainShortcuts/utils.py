import os
import sys
import inspect
from typing import *
if hasattr(sys, "MainShortcuts_imports"):
  for i in sys.MainShortcuts_imports:
    exec(f"import {i}")
else:
  setattr(sys, "MainShortcuts_imports", [])


def riot(**t_kw):
  """Run In Another Thread (threading)"""
  import threading
  if not "daemon" in t_kw:
    t_kw["daemon"] = False

  def decorator(func):
    t_kw["target"] = func

    def wrapper(*args, **kwargs) -> threading.Thread:
      t_kw["args"] = args
      t_kw["kwargs"] = kwargs
      t = threading.Thread(**t_kw)
      t.start()
      return t
    return wrapper
  return decorator


def riop(**p_kw):
  """Run In Another Process (multiprocessing)"""
  import multiprocessing
  if not "daemon" in p_kw:
    p_kw["daemon"] = False

  def decorator(func):
    p_kw["target"] = func

    def wrapper(*args, **kwargs) -> multiprocessing.Process:
      p_kw["args"] = args
      p_kw["kwargs"] = kwargs
      p = multiprocessing.Process(**p_kw)
      p.start()
      return p
    return wrapper
  return decorator
# class PingStats:pass
# def ping(host:str,*,count:int=1,size:int=64,timeout:Union[int,float,timedelta]=10)->PingStats:
#   import socket
#   with socket.socket(socket.AF_INET,socket.SOCK_RAW,socket.IPPROTO_ICMP) as sock:
#     ip=socket.gethostbyname(host)
#     sock.connect((host))


async def async_request(method: str, url: str, *, ignore_status: bool = False, **kw):
  """aiohttp request"""
  import aiohttp
  kw["method"] = method
  kw["url"] = url
  resp = aiohttp.request(**kw)
  if not ignore_status:
    resp.raise_for_status()
  return resp


def sync_request(method: str, url: str, *, ignore_status: bool = False, **kw):
  """requests request"""
  import requests
  kw["method"] = method
  kw["url"] = url
  resp = requests.request(**kw)
  if not ignore_status:
    resp.raise_for_status()
  return resp


request = sync_request


async def async_download_file(url: str, path: str, *, delete_on_error: bool = True, chunk_size: int = 1024, **kw) -> int:
  kw["url"] = url
  if not "method" in kw:
    kw["method"] = "GET"
  async with async_request(**kw) as resp:
    with open(path, "wb") as fd:
      size = 0
      try:
        async for chunk in resp.content.iter_chunked(chunk_size):
          fd.write(chunk)
          size += len(chunk)
      except:
        if delete_on_error:
          if os.path.isfile(path):
            os.remove(path)
        raise
  return size


def sync_download_file(url: str, path: str, *, delete_on_error: bool = True, chunk_size: int = 1024, **kw) -> int:
  kw["stream"] = True
  kw["url"] = url
  if not "method" in kw:
    kw["method"] = "GET"
  with sync_request(**kw) as resp:
    with open(path, "wb") as fd:
      size = 0
      try:
        for chunk in resp.iter_content(chunk_size):
          fd.write(chunk)
          size += len(chunk)
      except:
        if delete_on_error:
          if os.path.isfile(path):
            os.remove(path)
        raise
  return size


download_file = sync_download_file


def args2kwargs(func: Callable, args: Iterable = (), kwargs: dict[str, Any] = {}) -> dict[str, Any]:
  kw = kwargs.copy()
  args = list(args)
  for i in inspect.signature(func).parameters:
    if not i in kw:
      kw[i] = args.pop(0)
  if len(args) > 0:
    raise TypeError("Too many arguments")
  return kw
