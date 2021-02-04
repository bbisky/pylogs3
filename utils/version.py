import django
import os.path
import re
from platform import python_version
def get_runtime_revision(path=None):
    """
    Returns the SVN revision in the form SVN-XXXX,
    where XXXX is the revision number.

    Returns SVN-unknown if anything goes wrong, such as an unexpected
    format of internal SVN files.

    If path is provided, it should be a directory whose SVN info you want to
    inspect. If it's not provided, this will use the root django/ package
    directory.
    """
    return u'Python: v%s Django: v%s' % (python_version(), django.get_version())
    
