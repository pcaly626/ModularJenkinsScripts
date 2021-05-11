import sys, importlib, os
'''
Main requires the Module and an any arguments that is required
Call the Run method on the module

Attributes
================
    moduleName : str
        First argument that is the exact name of the Module

    otherArgs : list
        *args of all arguments passed after the Module name

Example Call
================
    python Main.py ModuleName Arg1 Arg2 ArgN

'''
moduleDirectory = "Tasks"

try:
    moduleName = sys.argv[ 1 ]
    otherArgs = sys.argv[ 2: ]
    module = importlib.import_module( f"{moduleDirectory}.{moduleName}" )
    moduleClass = getattr( module, moduleName )

    if  "help" in otherArgs:
        moduleClass().Help()
    else:
        moduleClass().Run( otherArgs )
except Exception as e:
    print( str(e) )
    print( "Avaliable Options are: ")
    files = os.listdir(moduleDirectory)
    files.remove("__pycache__")
    files.append("help")
    for item in files:
        print( f"\t {item.split('.')[0]}")
    print("Example: python Main.py ModuleName arg1 arg2 argN")

