import cx_Freeze 
import sys 
import os
import os.path

base = None
if sys.platform == 'win32':
    base = 'Win32GUI'

PYTHON_INSTALL_DIR = os.path.dirname(os.path.dirname(os.__file__))
os.environ['TCL_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tcl8.6')
os.environ['TK_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tk8.6')

executables = [cx_Freeze.Executable('Diapo_infV1.py',base=base)]

cx_Freeze.setup(
        name = "Programme de Diaporama Infini",
        version='0.1',
        executables= executables,
        options = {"build_exe":{"packages":["tkinter","time","os","pickle","tkinter.messagebox","random"],
        'include_files':[
            os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tcl8.6'),
            os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tk8.6'),
        ]
    }}
    )