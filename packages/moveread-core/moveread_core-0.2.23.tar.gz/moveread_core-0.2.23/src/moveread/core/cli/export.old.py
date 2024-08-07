from typing import Literal, Iterable
import sys
import os
import fs
import pure_cv as vc
import files_dataset as fds
import ocr_dataset as ods
from moveread.core import Core, cli

async def export_pgn(core: Core, verbose: bool):
  games = await cli.read_games(core, verbose)
  if games.tag == 'left':
    return
  for id, game in sorted(games.value):
    if game.meta.pgn:
      for player in game.players:
        labs = player.labels(game.meta.pgn)
        if labs.tag == 'left':
          if verbose:
            print(f'Error exporting "{id}":', labs.value, file=sys.stderr)
          continue
        pgn = game.meta.pgn[:player.meta.end_correct]
        line = ' '.join(pgn)
        print(line)
    elif verbose:
      print(f'Game "{id}" has no PGN', file=sys.stderr)

async def export_boxes(
  core: Core, output: str, *, 
  num_boxes: int | None | Literal['auto'] = 'auto',
  verbose: bool,
):
  """
  - `num_boxes`:
    - `'auto'`: Export boxes up to the number of PGN moves
    - `None`: Export all boxes
    - `int`: Export at most `num_boxes` boxes
  """
  games = await cli.read_games(core, True)
  if games.tag == 'left':
    return
  
  total_boxes = i = 0
  for i, (id, game) in enumerate(sorted(games.value)):
    base = os.path.join(output, id.replace('/', '-'))
    if not (pgn := game.meta.pgn):
      if verbose:
        print(f'WARNING: No/empty PGN found in "{id}"', file=sys.stderr)
      continue

    if num_boxes == 'auto':
      max_boxes = len(pgn) if pgn is not None else None
    else:
      max_boxes = num_boxes

    for j, player in enumerate(game.players):
      labs = player.labels(pgn)
      if labs.tag == 'left':
        if verbose:
          print(f'Error in "{id}", player {j}:', labs.value, file=sys.stderr)
        continue
      elif labs.value == []:
        if verbose:
          print(f'WARNING: Empty labels found in "{id}", player {j}', file=sys.stderr)
        continue
      
      either = await player.boxes(core.blobs)
      if either.tag == 'left':
        if verbose:
          print(f'Error in "{id}", player {j}', either.value, file=sys.stderr)
        continue
      elif either.value == []:
        if verbose:
          print(f'WARNING: No boxes found in "{id}", player {j}', file=sys.stderr)
        continue

      boxes = either.value[:max_boxes]
      total_boxes += len(boxes)
      path = f'{base}-{j}'
      os.makedirs(path, exist_ok=True)
      tarfile = f'boxes{j}.tar'
      files = [(f'box_{i}.jpg', vc.encode(box, '.jpg')) for i, box in enumerate(boxes)]
      fs.create_tarfile(files, os.path.join(path, tarfile))
      archive = fds.Archive(archive=tarfile, format='tar', num_files=len(boxes))
      meta = fds.MetaJson(files_dataset={'boxes': archive})
      with open(os.path.join(path, 'meta.json'), 'w') as f:
        f.write(meta.model_dump_json(indent=2, exclude_defaults=True))

    print(f'\r{i+1}/{len(games.value)} - {total_boxes:06} boxes', end='', file=sys.stderr)

async def export_ocr(core: Core, output: str, verbose: bool):
  games = await cli.read_games(core, True)
  if games.tag == 'left':
    return
  
  total_samples = i = 0
  for i, (id, game) in enumerate(sorted(games.value)):
    base = os.path.join(output, id.replace('/', '-'))
    if (pgn := game.meta.pgn) is None:
      continue
    for j, player in enumerate(game.players):
      either = await player.ocr_samples(pgn, core.blobs)
      if either.tag == 'left':
        if verbose:
          print(f'Error in "{id}", player {j}', either.value, file=sys.stderr)
        continue
      elif either.value == []:
        if verbose:
          print(f'WARNING: No samples found in "{id}", player {j}', file=sys.stderr)
        continue

      samples = [(vc.encode(s.img, '.jpg'), s.lab) for s in either.value]
      ods.create_tar(f'{base}-{j}', samples, images_name='boxes')
      total_samples += len(samples)

    print(f'\r{i+1}/{len(games.value)} - {total_samples:05} boxes', end='', file=sys.stderr)