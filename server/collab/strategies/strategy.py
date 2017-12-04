from django.db.models import Q

import json


class Strategy(object):
  def __init__(self, source_file, source_start, source_end,
               source_file_version, target_project, target_file, matchers):
    self.source_file = source_file
    self.source_start = source_start
    self.source_end = source_end
    self.source_file_version = source_file_version
    self.target_project = target_project
    self.target_file = target_file
    self.matchers = set(json.loads(matchers))

  def get_source_filters(self):
    # make sure vector belongs to the file_version (and therefore the file)
    # of the source
    source_filters = Q(file_version_id=self.source_file_version)

    # if provided with a source start and/or end, add additional limitations
    if self.source_start:
      source_filters &= Q(instance__offset__gte=self.source_start)
    if self.source_end:
      source_filters &= Q(instance__offset__lte=self.source_end)

    return source_filters

  def get_target_filters(self):
    # Exclude source file inputs from the target
    target_filter = ~Q(file_version__file=self.source_file)

    # if provided with a target file make sure to filter by it, else limit to
    # provided project or not at all
    if self.target_file:
      target_filter &= Q(file_version__file=self.target_file)
    elif self.target_project:
      target_filter &= Q(file_version__file__project_id=self.target_project)

    return target_filter

  def get_filters(self):
    return self.get_source_filters(), self.get_target_filters()

  @classmethod
  def is_abstract(cls):
    return not (hasattr(cls, 'strategy_type') and
                hasattr(cls, 'strategy_description') and
                hasattr(cls, 'strategy_name'))
