import os
import shutil
import MainShortcuts.path as m_path
from typing import Union


def create(path: str, force: bool = False) -> bool:
  """Создать папку
  Если путь существует, ничего не делает
  force - принудительно создать папку (удалит файл, который находится на её месте)"""
  if os.path.isdir(path):
    return True
  if force:
    if os.path.isfile(path):
      m_path.rm(path)
  os.makedirs(path)
  return True


mk = create


def delete(path: str):
  """Удалить папку с содержимым
  Если в назначении файл, выдаст ошибку"""
  if os.path.isdir(path):
    shutil.rmtree(path)
  if os.path.exists(path):
    raise Exception("This is not a dir")


rm = delete


def copy(fr: str, to: str, force: bool = False):
  """Копировать папку с содержимым
  force - принудительно копировать"""
  if os.path.isdir(fr):
    if force:
      if not os.path.isdir(to):
        m_path.rm(to)
    shutil.copytree(fr, to)
  else:
    raise Exception("This is not a dir")


cp = copy


def move(fr: str, to: str, force: bool = False):
  """Переместить папку с содержимым
  force - принудительно переместить"""
  if os.path.isdir(fr):
    if force:
      if not os.path.isdir(to):
        m_path.rm(to)
    shutil.move(fr, to)
  else:
    raise Exception("This is not a dir")


def rename(fr: str, to: str, force: bool = False):
  """Переименовать папку
  force - принудительно переименовать"""
  if os.path.isdir(fr):
    if force:
      if not os.path.isdir(to):
        m_path.rm(to)
    os.rename(fr, to)
  else:
    raise Exception("This is not a dir")


def list(path: str = ".", extensions: Union[str, list] = None, func=None, *, files: bool = True, dirs: bool = True, links: Union[bool, None] = None):
  """Получить список содержимого папки (пути)
  files      - True: включать файлы в список
               False: не показывать файлы в списке
  dirs       - True: включать папки в список
               False: не показывать папки в списке
  links      - None: показывать всё
               True: показывать только ссылки
               False: не показывать ссылки
  extensions - список допустимых расширений (для файлов)
  func       - функция для фильтрации
               принимает путь к файлу
               возвращает True или False"""
  r = []
  for i in os.listdir(path):
    i = f"{path}/{i}"
    if links == None:
      pass
    elif links == True:
      if not os.path.islink(i):
        continue
    elif links == False:
      if os.path.islink(i):
        continue
    else:
      raise Exception('"links" can only be True, False or None')
    if extensions != None and os.path.isfile(i):
      if type(extensions) == str:
        extensions = [extensions]
      for ext in extensions:
        ext = str(ext)
        if not ext.startswith("."):
          ext = "." + ext
        if not i.endswith(ext):
          continue
    if func != None:
      if not func(i):
        continue
    if files and dirs:
      r.append(i)
      continue
    if files:
      if os.path.isfile(i):
        r.append(i)
        continue
    if dirs:
      if os.path.isdir(i):
        r.append(i)
        continue
  return r
