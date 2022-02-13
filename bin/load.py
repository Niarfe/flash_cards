import os
import shutil
SOURCE_DIR=os.environ.get('FC_SOURCE_DIR', None)
assert SOURCE_DIR, "Set the env var FC_SOURCE_DIR to pickup folder"
assert SOURCE_DIR.endswith('/'), "FC_SOURCE_DIR should end with a /, {}".format(SOURCE_DIR)

NOTEBOOK = os.environ.get('FC_NOTEBOOK', None)
assert NOTEBOOK, "Set FC_NOTEBOOK to name of googlesheet source"

STACKS = os.environ.get('FC_STACKS', None)
assert STACKS, "Set FC_STACKS to directory to store flashcard stacks"

PWD = os.getcwd()

stacks = [stack for stack in os.listdir(SOURCE_DIR) if stack.startswith(NOTEBOOK+' - ')]

print("Found", len(stacks))
#print(stacks)

def short_name(full_name):
    assert isinstance(full_name, str), "Expected string"
    assert ' - ' in full_name and full_name.endswith('.csv'), "expected blah - stuff.csv"
    return full_name.split(' - ')[1]

for stack in stacks:
    source = SOURCE_DIR+stack
    target = PWD+'/'+STACKS+short_name(stack)
    print("Moving", source, "to", target)
    shutil.move(source, target)
