'''
 * Copyright of JyNI:
 * Copyright (c) 2013, 2014, 2015, 2016, 2017 Stefan Richthofer.
 * All rights reserved.
 *
 *
 * Copyright of Python and Jython:
 * Copyright (c) 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008,
 * 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017
 * Python Software Foundation.
 * All rights reserved.
 *
 *
 * This file is part of JyNI.
 *
 * JyNI is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Lesser General Public License as
 * published by the Free Software Foundation, either version 3 of
 * the License, or (at your option) any later version.
 *
 * JyNI is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU Lesser General Public License for more details.
 *
 * You should have received a copy of the GNU Lesser General Public
 * License along with JyNI.  If not, see <http://www.gnu.org/licenses/>.


Created on: 2018-07-30 13:35

@author: Calum Freeman
'''

import sys
import os
import platform

if os.name == 'java':
    systm = platform.java_ver()[-1][0].lower().replace(' ', '')
    if systm == 'macosx':
        ver = platform.java_ver()[-1][1]
        ver = ver[:5] # e.g."10.12.4" => "10.12"
        buildf = '-'.join((systm, ver, 'intel'))
    else:
        if systm.startswith('win'):
            systm = 'win'
        buildf = '-'.join((systm, os.uname()[-1]))
else:
    systm = os.uname()[0].lower()
    if systm == 'darwin':
        ver = platform.mac_ver()[0]
        ver = ver[:5] # e.g."10.12.4" => "10.12"
        buildf = '-'.join(('macosx', ver, 'intel'))
    else:
        buildf = '-'.join((systm, os.uname()[-1]))


#Since invalid paths do no harm, we add several possible paths here, where
#PyFileTest.so could be located in various build scenarios. If you use different
#scenarios in parallel, select the one to be used by setting some of the paths as comments.

#built with an IDE in debug mode:
sys.path.append('../../DemoExtension/Debug') #in case you run it from src dir
sys.path.append('./DemoExtension/Debug') #in case you run it from base dir
#built with an IDE in release mode:
sys.path.append('../../DemoExtension/Release') #in case you run it from src dir
sys.path.append('./DemoExtension/Release') #in case you run it from base dir
sys.path.append('../../DemoExtension/build/Release') #in case you run it from src dir
sys.path.append('./DemoExtension/build/Release') #in case you run it from base dir
#built with setup.py:
sys.path.append('../../DemoExtension/build/lib.'+buildf+'-2.7') #in case you run it from src dir
sys.path.append('./DemoExtension/build/lib.'+buildf+'-2.7') #in case you run it from base dir
sys.path.append('./DemoExtension/build')
import datetime
import unittest
import PyFileTest as pf

class Test_PyFile(unittest.TestCase):

    def test_PyFile_WriteString(self): # TODO assertRaises() would allow testing exceptions if we add an exception for null file
        name = "/tmp/fred"
        file = open(name, 'w+')
        string = "Hello World!"
        self.assertEqual(pf.test_PyFile_WriteString(file, string), 1)
        file.close()
        file = open(name, 'r+')
        res = file.read()
        self.assertEqual(res, string, "failed to write: \""+str(string)+"\" to file, got: \""+res+"\" instead");
        import os
        os.remove(name)


    def test_PyFile_AsFile(self): # TODO assertRaises() would allow testing exceptions if we add an exception for null file
        name = "/tmp/fred"
        file = open(name, 'w+')
        string = 'a'
        file.write(string)
        file.close()
        file = open(name, 'r+') 
        self.assertEqual(pf.test_PyFile_AsFile(file, string), string)
        file.close()
        self.assertEqual(pf.test_PyFile_AsFile(file, string), "file is closed")
        import os
        os.remove(name)
    
    def test_PyFile_Name(self): # TODO assertRaises() would allow testing exceptions if we add an exception for null file
        name = "/tmp/fred"
        file = open(name, 'w+')
        self.assertEqual(pf.test_PyFile_Name(file), name)
        file.close()
        import os
        os.remove(name)
    
    def test_file_repr(self): # TODO assertRaises() would allow testing exceptions if we add an exception for null file
        name = "/tmp/fred"
        file = open(name, 'w+')
        self.assertEqual(str(file), pf.test_file_repr(file))
        file.close()
        import os
        os.remove(name)
    
    def test_PyFile_FromFile(self): # Note: this assumes that PyFile_AsFile works!
        name = "/tmp/fred"
        file = open(name, 'w+')
        # TODO find a better way to test this
        file2 = pf.test_PyFile_FromFile(file, name, "w+")
        self.assertEqual(file.mode, file2.mode, "PyFile_FromFile gave file with different mode")
        self.assertEqual(file.name, file2.name, "PyFile_FromFile gave file with different name")
        file.close()
        import os
        os.remove(name)


if __name__ == '__main__':
    #suite = unittest.TestLoader().loadTestsFromName("test_PyFile_AsFile", Test_PyFile)
    #unittest.TextTestRunner(verbosity=2).run(suite)
    unittest.main()