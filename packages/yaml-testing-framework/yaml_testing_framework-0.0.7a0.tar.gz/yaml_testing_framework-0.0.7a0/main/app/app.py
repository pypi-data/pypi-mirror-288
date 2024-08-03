#!.venv/bin/python3
# -*- coding: utf-8 -*-

import os
from types import ModuleType
from types import SimpleNamespace as sns
from typing import Callable, List

from main.process import (
  casts,
  checks,
  environment,
  locations,
  nodes,
  patches,
  setup as SETUP,
  spies,
)
from main.utils import (
  get_config,
  get_module,
  independent,
  logger,
  methods,
  objects,
)


ROOT_DIR = os.getcwd()
LOCALS = locals()

CONFIG = get_config.main()
LOGGING_ENABLED = True
TEST_IDS = {}
FLAGS = {}


def main(
  project_path: str | None = None,
  exclude_files: str | list | None = None,
  include_files: str | list | None = None,
  exclude_methods: str | list | None = None,
  include_methods: str | list | None = None,
  yaml_suffix: str | None = None,
  logging_flag: bool | None = None,
  setup: list = [],
) -> list:
  logger.create_logger(
    logging_flag=logging_flag,
    project_path=project_path,
  )
  data = independent.get_model(schema=CONFIG.schema.App, data=locals())
  data = independent.process_operations(
    operations=CONFIG.operations.main,
    functions=LOCALS,
    data=data,
  )
  return objects.get(
    parent=data,
    route='tests',
  ) or []


def add_entrypoint(
  entrypoint: str = '',
  root: str = '',
) -> sns:
  entrypoint = entrypoint or CONFIG.entrypoint
  root = root or ROOT_DIR
  path = os.path.join(root, entrypoint)
  message = 'entrypoint exists'

  if not os.path.isfile(path):
    FLAGS.update(dict(entrypoint=1))
    message = 'entrypoint added'
    with open(
        file=path,
        mode='w',
        encoding='utf-8',
    ) as file:
      file.write(CONFIG.entrypoint_source_code)

  logger.main(message=message, level='info')
  return sns(entrypoint=path, _=message)


def remove_added_entrypoint(
  entrypoint: str = '',
  flags: dict = {},
) -> sns:
  flags = flags or FLAGS
  message = 'nothing to do'

  flag = False not in [
    os.path.isfile(str(entrypoint)),
    objects.get(
      parent=flags,
      route='entrypoint',
    ) == 1,
  ]
  if flag and os.path.isfile(entrypoint):
    os.remove(path=entrypoint)
    message = 'entrypoint removed'

  logger.main(level='info', message=message)
  return sns(entrypoint=entrypoint, _=message)


def handle_id(
  module_route: str | None = None,
  function: str | None = None,
  description: str | List[str] | None = None,
  key: str | None = None,
) -> sns:
  id_short = f'{module_route}.{function}'
  id_ = f' {id_short} - {key} '

  description = locations.format_as_list(value=description)
  if len(description) > 0:
    id_ = id_ + f'- {description[-1]} '

  logger.main(
    message=f'Generated test id for {id_short}',
    level='info',
  )
  return sns(id=id_, id_short=id_short)


def get_function(
  function: str | None = None,
  module: ModuleType | None = None,
) -> sns:
  function_ = objects.get(parent=module, route=function)

  if not isinstance(function_, Callable):
    logger.main(
      message='Method `{}` does not exist in {}'.format(
        function, module.__file__
      ),
      level='warning',
    )

  return sns(function=function_, function_name=function)


def run_test_for_function(test: sns | None = None) -> sns:
  test = independent.process_operations(
    operations=CONFIG.operations.run_test_for_functions,
    functions=LOCALS,
    data=test,
  )
  return test.checks


def run_test_handler(tests: list | None = None) -> sns:
  tests = tests or []
  results = []

  for test in reversed(tests):
    target = ''
    for test_kind in CONFIG.test_kinds:
      if test_kind in test.__dict__:
        target = f'run_test_for_{test_kind}'
        break
    target = LOCALS.get(target)
    result = target(test)
    results.extend(result)

  return sns(tests=results)


def run_tests(locations: List[sns] | None = None) -> sns:
  tests = []

  for i, item in enumerate(locations):
    result = independent.process_operations(
      operations=CONFIG.operations.run_tests,
      functions=LOCALS,
      data=item,
    )
    tests.extend(result.tests)

  flag = len(tests or []) > 0
  logger.do_nothing() if flag else logger.main(
    message='No tests collected',
    level='warning',
    standard_output=True,
  )
  return sns(tests=tests)


def examples() -> None:
  from main.utils import invoke_testing_method

  invoke_testing_method.main('.main/app')


if __name__ == '__main__':
  examples()
