import unittest
import os
# get the list of files in this folder
mypath=os.path.dirname(os.path.realpath(__file__))
listOfFiles = os.listdir(mypath)

excludedFiles = ["test_all.py"]
# work out which of them are tests and add the tests to the module list (without their .py file ending)
modulesList = []
for f in listOfFiles:
    # check it starts with "test_", ends with ".py" and isn't one of the excluded files
    if((f[:5] == "test_") and (f.split(".")[1] == "py") and (not excludedFiles.__contains__(f))):
        modulesList.append(f.split(".")[0])
print "running "+str(len(modulesList))+" tests: "+str(modulesList)
for m in modulesList:
    exec "import "+str(m)+"\nsuite = unittest.TestLoader().loadTestsFromModule("+str(m)+")\nunittest.TextTestRunner(verbosity=2).run(suite)"