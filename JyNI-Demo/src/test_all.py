print "Hello! This file will run all the tests eventually"

import test_JyNI as te

te.TestJyNI('test_DemoExtension_doc')()

import test_JyNI_PyFile as t
t.Test_PyFile('test_PyFile_WriteString')()