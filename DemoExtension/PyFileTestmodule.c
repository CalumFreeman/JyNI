/*
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
 *
 *
 *
 * DemoExtensionmodule.c
 *
 *  Created on: 2018-07-30 13:35
 *	  Author: Calum Freeman
 */

#include <Python.h>

#ifndef MS_WINDOWS
#define _alloca alloca
#endif
PyMODINIT_FUNC initPyFileTest(void);
// make some macros to expand the stuff needed for python to understand this module
// Basically MakeTest(functionName) then in pyMethodDef MapTest(functionName) and that will expose test_functionName to python
#define MakeTest(X) static PyObject* testPyFile_ ## X (PyObject *self, PyObject *args);\
static char X ## _docs[] = "This tests the "#X" function"
#define MapTest(X) { "test_"#X, (PyCFunction)testPyFile_ ## X, METH_VARARGS, X ## _docs }

// SetBufSize SetEncoding SetEncodingAndErrors SoftSpace
// declare functions, doc strings and method def's
MakeTest(PyFile_WriteString);
MakeTest(PyFile_AsFile);
MakeTest(PyFile_Name);
MakeTest(PyFile_FromFile);
MakeTest(PyFile_FromString);
MakeTest(PyFile_GetLine);
MakeTest(PyFile_SetBufSize);
MakeTest(PyFile_SetEncoding);
MakeTest(PyFile_SetEncodingAndErrors);
MakeTest(PyFile_SoftSpace);
MakeTest(tp_repr);
MakeTest(tp_getattro);
MakeTest(tp_setattro);
MakeTest(tp_flags);
MakeTest(tp_doc);
MakeTest(tp_weaklistoffset);
MakeTest(tp_iter);
MakeTest(tp_iternext);
// declare doc strings
static char PyFile_docs[]= "this tests the PyFile API";

// declare module map
static PyMethodDef PyFileTestMethods[] = {
		MapTest(PyFile_WriteString),
		MapTest(PyFile_AsFile),
		MapTest(PyFile_Name),
		MapTest(PyFile_FromFile),
		MapTest(PyFile_FromString),
		MapTest(PyFile_GetLine),
		MapTest(PyFile_SetBufSize),
		MapTest(PyFile_SetEncoding),
		MapTest(PyFile_SetEncodingAndErrors),
		MapTest(PyFile_SoftSpace),
		MapTest(tp_repr),
		MapTest(tp_getattro),
		MapTest(tp_setattro),
		MapTest(tp_flags),
		MapTest(tp_doc),
		MapTest(tp_weaklistoffset),
		MapTest(tp_iter),
		MapTest(tp_iternext),
		{ NULL, NULL, 0, NULL }

};
//	PyObject_GenericGetAttr,                    // tp_getattro
//	PyObject_GenericSetAttr,                    // tp_setattro
//    Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE | Py_TPFLAGS_HAVE_WEAKREFS, // tp_flags
//    file_doc,                                   /* tp_doc */
//	0,//offsetof(PyFileObject, weakreflist),        // tp_weaklistoffset	This may cause trouble!
//	(getiterfunc)file_self,                     // tp_iter
//	(iternextfunc)file_iternext,                // tp_iternext
//	file_methods,                               // tp_methods
//	file_memberlist,                             // tp_members
//	file_getsetlist,                            // tp_getset


// define functions
static PyObject* testPyFile_PyFile_WriteString(PyObject *self, PyObject *args) {
	PyObject *f;
	char *myStr;
	if (!PyArg_ParseTuple(args, "Os", &f, &myStr)) {
		printf("PyArg_ParseTuple in testPyFile_PyFile_WriteString didn't work\n");
		return Py_BuildValue("i", -1);
	}

	// TODO check that the file actually wrote successfully check with empty and non-empty files
	int successReturn = PyFile_WriteString(myStr, f);
	if(successReturn==0) return Py_BuildValue("i", -1);

	int errorReturn = PyFile_WriteString(myStr, NULL);
	if(errorReturn!=-1) return Py_BuildValue("i", -1);

	// TODO find a way to throw a java IO exception that can be caught by JNI and trigger this block
	//int javaErrorReturn = PyFile_WriteString(myStr, NULL);
	//if(javaErrorReturn!=-2) return NULL;

	//free(myStr);
	return Py_BuildValue("i", 1);
}

static PyObject* testPyFile_PyFile_AsFile(PyObject *self, PyObject *args){
	// takes in a file containing a character and that character then gets a file pointer and uses it to see if the char is there, if it is then this is probably pointing to the right file
	PyObject *Obj;
	char myCh;
	if (!PyArg_ParseTuple(args, "Oc", &Obj, &myCh)) {
		printf("PyArg_ParseTuple in testPyFile_PyFile_AsFile didn't work\n");
	    return NULL;
	}
	FILE *f = PyFile_AsFile(Obj);
	if(f == NULL){
		return Py_BuildValue("s", "file is closed");
	}
	char ch = fgetc(f);
	return Py_BuildValue("c", ch);
}

static PyObject* testPyFile_PyFile_Name(PyObject *self, PyObject *args){
	PyObject *Obj;
	if (!PyArg_ParseTuple(args, "O", &Obj)) {
		printf("PyArg_ParseTuple in testPyFile_PyObject_AsFileDescriptor didn't work\n");
		return NULL;
	}
	return PyFile_Name(Obj);
}

static PyObject* testPyFile_PyFile_FromFile(PyObject *self, PyObject *args){
	PyObject *Obj;
	char* Cname;
	char* Cmode;
	if (!PyArg_ParseTuple(args, "Oss", &Obj, &Cname, &Cmode)) {
		printf("PyArg_ParseTuple in testPyFile_PyObject_AsFileDescriptor didn't work\n");
		return NULL;
	}
	FILE* file = PyFile_AsFile(Obj);
	PyObject *o = PyFile_FromFile(file, Cname, Cmode, (int (*)(FILE *))NULL);
	// TODO check the PyFile works/is what we expect
	return Py_BuildValue("O", o);
}

static PyObject* testPyFile_PyFile_FromString(PyObject *self, PyObject *args){
	char* Cname;
	char* Cmode;
	if (!PyArg_ParseTuple(args, "ss", &Cname, &Cmode)) {
		printf("PyArg_ParseTuple in testPyFile_PyObject_AsFileDescriptor didn't work\n");
		return NULL;
	}
	PyObject *o = PyFile_FromString(Cname, Cmode);
	// TODO check the PyFile works/is what we expect
	return Py_BuildValue("O", o);
}

static PyObject* testPyFile_PyFile_GetLine(PyObject *self, PyObject *args){
	PyObject *Obj;
	int n;
	if (!PyArg_ParseTuple(args, "Oi", &Obj, &n)) {
		printf("PyArg_ParseTuple in testPyFile_PyObject_AsFileDescriptor didn't work\n");
		return NULL;
	}
	return PyFile_GetLine(Obj, n);
}

static PyObject* testPyFile_PyFile_SetBufSize(PyObject *self, PyObject *args){
	PyObject *Obj;
	int n;
	if (!PyArg_ParseTuple(args, "Oi", &Obj, &n)) {
		printf("PyArg_ParseTuple in testPyFile_PyObject_AsFileDescriptor didn't work\n");
		return NULL;
	}
	PyFile_SetBufSize(Obj, n);
	Py_RETURN_NONE; // This is just making sure it doesn't throw an error
}
static PyObject* testPyFile_PyFile_SetEncoding(PyObject *self, PyObject *args){
	PyObject *Obj;
	char *enc;
	if (!PyArg_ParseTuple(args, "Os", &Obj, &enc)) {
		printf("PyArg_ParseTuple in testPyFile_PyObject_AsFileDescriptor didn't work\n");
		return NULL;
	}
	return Py_BuildValue("i", PyFile_SetEncoding(Obj, enc));
}
static PyObject* testPyFile_PyFile_SetEncodingAndErrors(PyObject *self, PyObject *args){
	PyObject *Obj;
	char *enc;
	char *err;
	if (!PyArg_ParseTuple(args, "Oss", &Obj, &enc, &err)) {
		printf("PyArg_ParseTuple in testPyFile_PyObject_AsFileDescriptor didn't work\n");
		return NULL;
	}
	;
	return Py_BuildValue("i", PyFile_SetEncodingAndErrors(Obj, enc, err));
}
static PyObject* testPyFile_PyFile_SoftSpace(PyObject *self, PyObject *args){
	PyObject *Obj;
	int newflag;
	if (!PyArg_ParseTuple(args, "Oi", &Obj, &newflag)) {
		printf("PyArg_ParseTuple in testPyFile_PyObject_AsFileDescriptor didn't work\n");
		return NULL;
	}
	return Py_BuildValue("i", PyFile_SoftSpace(Obj, newflag));
}

static PyObject* testPyFile_tp_repr(PyObject *self, PyObject *args){
	PyObject *Obj;
	if (!PyArg_ParseTuple(args, "O", &Obj)) {
		printf("PyArg_ParseTuple in testPyFile_file_repr didn't work\n");
		return NULL;
	}
	PyObject* pstr = Obj->ob_type->tp_repr(Obj);
	char* str = PyString_AsString(pstr);
	return Py_BuildValue("s", str);
}

static PyObject* testPyFile_tp_getattro(PyObject *self, PyObject *args){
	PyObject *Obj;
	char *Cname;
	if (!PyArg_ParseTuple(args, "Os", &Obj, &Cname)) {
		printf("PyArg_ParseTuple in testPyFile_file_repr didn't work\n");
		return NULL;
	}
	PyObject *name = PyString_FromString(Cname);
	return Obj->ob_type->tp_getattro(Obj, name);
}

static PyObject* testPyFile_tp_setattro(PyObject *self, PyObject *args){
	PyObject *Obj;
	char *Cname;
	PyObject *value;
	if (!PyArg_ParseTuple(args, "OsO", &Obj, &Cname, &value)) {
		printf("PyArg_ParseTuple in testPyFile_file_repr didn't work\n");
		return NULL;
	}
	PyObject *name = PyString_FromString(Cname);
	int res = Obj->ob_type->tp_setattro(Obj, name, value);
	return Py_BuildValue("i", res);
}

static PyObject* testPyFile_tp_flags(PyObject *self, PyObject *args){
	PyObject *Obj;
	if (!PyArg_ParseTuple(args, "O", &Obj)) {
		printf("PyArg_ParseTuple in testPyFile_file_repr didn't work\n");
		return NULL;
	}
	return Py_BuildValue("i", Obj->ob_type->tp_flags);
}

static PyObject* testPyFile_tp_doc(PyObject *self, PyObject *args){
	PyObject *Obj;
	if (!PyArg_ParseTuple(args, "O", &Obj)) {
		printf("PyArg_ParseTuple in testPyFile_file_repr didn't work\n");
		return NULL;
	}
	return Py_BuildValue("s", Obj->ob_type->tp_doc);
}

static PyObject* testPyFile_tp_weaklistoffset(PyObject *self, PyObject *args){
	PyObject *Obj;
	if (!PyArg_ParseTuple(args, "O", &Obj)) {
		printf("PyArg_ParseTuple in testPyFile_file_repr didn't work\n");
		return NULL;
	}
	return Py_BuildValue("s", "Nope");
}

static PyObject* testPyFile_tp_iter(PyObject *self, PyObject *args){
	PyObject *Obj;
	if (!PyArg_ParseTuple(args, "O", &Obj)) {
		printf("PyArg_ParseTuple in testPyFile_file_repr didn't work\n");
		return NULL;
	}
	return Py_BuildValue("s", Obj->ob_type->tp_iter(Obj));
}

static PyObject* testPyFile_tp_iternext(PyObject *self, PyObject *args){
	PyObject *Obj;
	if (!PyArg_ParseTuple(args, "O", &Obj)) {
		printf("PyArg_ParseTuple in testPyFile_file_repr didn't work\n");
		return NULL;
	}
	return Py_BuildValue("s", Obj->ob_type->tp_iternext(Obj));
}

//initialise module
PyMODINIT_FUNC
initPyFileTest(void)
{
	(void)Py_InitModule3("PyFileTest", PyFileTestMethods, PyFile_docs);
}
