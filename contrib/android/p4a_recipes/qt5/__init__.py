import os

from pythonforandroid.recipes.qt5 import Qt5Recipe

from pythonforandroid.util import load_source

util = load_source('util', os.path.join(os.path.dirname(os.path.dirname(__file__)), 'util.py'))

assert Qt5Recipe._version == "9b43a43ee96198674060c6b9591e515e2d27c28f"
assert Qt5Recipe.depends == ['python3']
assert Qt5Recipe.python_depends == []

class Qt5RecipePinned(util.InheritedRecipeMixin, Qt5Recipe):
    pass

recipe = Qt5RecipePinned()
