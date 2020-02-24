#define PY_SSIZE_T_CLEAN
#include <Python.h>

int c_add(int a, int b) {
    return a + b;
}

static PyObject *add(PyObject *self, PyObject *args) {
    int a, b, c;

    if (!PyArg_ParseTuple(args, "ii", &a, &b)) {
        return NULL;
    }

    c = c_add(a, b);

    // pythonの値に変換
    return Py_BuildValue("i", c);
}

static PyMethodDef addMethods[] = {
    {"c_add", add, METH_VARARGS, "summate two int args"},
    {NULL}
};

static struct PyModuleDef add_module = {
    PyModuleDef_HEAD_INIT,
    "add_module",
    "Python3 C++ API Module",
    -1,
    addMethods
};

PyMODINIT_FUNC PyInit_add_module(void) {
    return PyModule_Create(&add_module);
}
