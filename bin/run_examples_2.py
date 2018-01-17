import nbformat
from nbconvert.preprocessors import ExecutePreprocessor
import os

DIR = "../examples/"
# DIR = "../tutorial/"

nb_list = os.listdir(DIR)
nb_list = [n for n in nb_list if n.endswith(".ipynb")]

print(nb_list)

for nb_file in nb_list:

    nb_path = DIR + nb_file

    print("Executing {}".format(nb_path))

    with open(nb_path) as f:
        nb = nbformat.read(f, as_version=4)

    ep = ExecutePreprocessor(timeout=36000, kernel_name='python3')

    try:
        out = ep.preprocess(nb, {'metadata': {'path': DIR}})
    except CellExecutionError:
        out = None
        msg = 'Error executing the notebook "%s".\n\n' % nb_path
        # msg += 'See notebook "%s" for the traceback.' % notebook_filename_out
        print(msg)
        raise
    # finally:
        # with open(notebook_filename_out, mode='wt') as f:
        # nbformat.write(nb, f)
