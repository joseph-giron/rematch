import idaplugin
import pytest


def recurse_subclasses(classes):
  if not classes:
    return set()

  subclasses = set()
  for cls in classes:
    subclasses |= set(cls.__subclasses__())

  return classes | recurse_subclasses(subclasses)


dialogs = recurse_subclasses({idaplugin.rematch.dialogs.base.BaseDialog})
dialogs = sorted(dialogs)


@pytest.mark.parametrize("dialog_entry", dialogs)
def test_dialog(dialog_entry, idapro_app):
  try:
    dialog = dialog_entry()
  except TypeError as ex:
    pytest.skip(str(ex))
