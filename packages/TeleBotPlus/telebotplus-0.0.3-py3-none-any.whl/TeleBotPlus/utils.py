import os
import requests
import MainShortcuts as ms
from threading import Thread
_import_errors = {}
try:
  import aiohttp
except Exception as error:
  _import_errors["aiohttp"] = error
try:
  import asyncio
  import concurrent.futures
  pool = concurrent.futures.ThreadPoolExecutor()
except Exception as error:
  _import_errors["async2sync"] = error


def id_bot2client(id: int):
  id = str(id)
  if id.startswith("-100"):
    return int(id[4:])
  elif id.startswith("-"):
    return int(id[1:])
  else:
    return int(id)


def async2sync(coroutine):
  if "async2sync" in _import_errors:
    raise _import_errors["async2sync"]
  return pool.submit(asyncio.run, coroutine).result()


def sync2async(func):
  async def wrapper(*args, **kwargs):
    return func(*args, **kwargs)
  return wrapper


try:
  riot = ms.utils.riot
except Exception:
  def riot(**t_kw):
    """Run In Another Thread"""
    def decorator(func):
      t_kw["target"] = func

      def wrapper(*args, **kwargs) -> Thread:
        t_kw["args"] = args
        t_kw["kwargs"] = kwargs
        t = Thread(**t_kw)
        t.start()
        return t
      return wrapper
    return decorator

try:
  async_download_file = ms.utils.async_download_file
except Exception:
  async def async_download_file(url: str, path: str, *, ignore_status: bool = False, delete_on_error: bool = True, chunk_size: int = 1024, **kw) -> int:
    if "aiohttp" in _import_errors:
      raise _import_errors["aiohttp"]
    kw["url"] = url
    if not "method" in kw:
      kw["method"] = "GET"
    async with aiohttp.request(**kw) as resp:
      if not ignore_status:
        resp.raise_for_status()
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

try:
  sync_download_file = ms.utils.sync_download_file
except Exception:
  def sync_download_file(url: str, path: str, *, ignore_status: bool = False, delete_on_error: bool = True, chunk_size: int = 1024, **kw) -> int:
    kw["stream"] = True
    kw["url"] = url
    if not "method" in kw:
      kw["method"] = "GET"
    with requests.request(**kw) as resp:
      if not ignore_status:
        resp.raise_for_status()
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
