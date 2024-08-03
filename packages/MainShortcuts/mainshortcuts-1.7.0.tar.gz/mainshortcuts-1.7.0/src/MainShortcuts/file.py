import MainShortcuts.path as m_path
import os
import shutil
import builtins
_open = builtins.open


def read(path: str, encoding: str = "utf-8", force: bool = False, **kw) -> str:
  """Прочитать файл как текст
  encoding - кодировка
  force - если файла нет, возвращает пустую строку"""
  kw["encoding"] = encoding
  kw["file"] = path
  kw["mode"] = "r"
  if force:
    if os.path.isfile(path):
      with builtins.open(**kw) as f:
        return f.read()
    else:
      return ""
  else:
    with builtins.open(**kw) as f:
      return f.read()


def write(path: str, text: str = "", encoding: str = "utf-8", force=False, **kw) -> int:
  """Записать текст в файл
  text - текст для записи
  encoding - кодировка
  force - принудительно создать файл"""
  kw["encoding"] = encoding
  kw["file"] = path
  kw["mode"] = "w"
  if not "newline" in kw:
    kw["newline"] = "\n"
  if os.path.isdir(path) and force:
    m_path.rm(path)
  with builtins.open(**kw) as f:
    return f.write(text)


def open(path: str, force: bool = False, **kw) -> bytes:
  """Прочитать файл как байты
  force - если файла нет, возвращает пустые байты"""
  kw["file"] = path
  kw["mode"] = "rb"
  if force:
    if os.path.isfile(path):
      with builtins.open(path, "rb") as f:
        return f.read()
    else:
      return b""
  else:
    with builtins.open(path, "rb") as f:
      return f.read()


load = open


def save(path: str, content=b"", force=False, **kw) -> int:
  """Записать байты в файл
  content - байты для записи
  force - принудительно создать файл"""
  kw["file"] = path
  kw["mode"] = "wb"
  if os.path.isdir(path) and force:
    m_path.rm(path)
  with builtins.open(**kw) as f:
    return f.write(content)


def delete(path: str):
  """Удалить файл
  Если он не существует, ничего не изменится
  Если на месте папка, выдаст ошибку"""
  if os.path.isfile(path):
    return m_path.rm(path)
  if os.path.exists(path):
    raise Exception("This is not a file")


rm = delete


def copy(fr: str, to: str, force: bool = False):
  """Копировать файл
  force - если в месте назначения папка, удалить её"""
  if os.path.isfile(fr):
    if m_path.exists(to) and force:
      m_path.delete(to)
    return shutil.copy(fr, to)
  if os.path.exists(fr):
    raise Exception("This is not a file")
  raise FileNotFoundError("File not found")


cp = copy


def move(fr: str, to: str, force: bool = False):
  """Переместить файл
  force - если в месте назначения папка, удалить её"""
  if os.path.isfile(fr):
    if m_path.exists(to) and force:
      m_path.delete(to)
    return shutil.move(fr, to)
  if os.path.exists(fr):
    raise Exception("This is not a file")
  raise FileNotFoundError("File not found")


mv = move


def rename(fr: str, to: str, force: bool = False):
  """Переименовать файл
  force - если в месте назначения папка, удалить её"""
  if os.path.isfile(fr):
    if m_path.exists(to) and force:
      m_path.delete(to)
    return os.rename(fr, to)
  if os.path.exists(fr):
    raise Exception("This is not a file")
  raise FileNotFoundError("File not found")
