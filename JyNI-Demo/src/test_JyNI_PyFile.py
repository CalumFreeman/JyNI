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

    def test_PyFile_WriteString(self):
        print "running"
        file = open("/tmp/fred", 'w+')
        char = 'a'
        print pf.test_PyFile_WriteString(file, char)
        
        print file.read()
        print "hi?"






if __name__ == '__main__':
    unittest.main()