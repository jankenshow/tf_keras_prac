#define PY_SSIZE_T_CLEAN // 書くといいことがあるらしい
#include <Python.h> // 他のヘッダファイルをインクルードする前に必ず行う


// 関数本体
static PyObject *helloworld(PyObject *self, PyObject *args) {
    fprintf(stderr, "Hello, world\n");
    return Py_None;
}


// 関数の定義体 ・・・　モジュールとして使用する関数群を定義
/* 
定義の内容は {（関数名）,（関数へのポインタ）,（引数受け渡し方法）,（説明文）} の順に記述
引数がない関数の場合は（引数受け渡し方法）に METH_NOARGS 
引数を利用する場合には METH_VARARGS　を指定する
*/
static PyMethodDef helloMethods[] = {
    {"helloworld", helloworld, METH_NOARGS, "print hello world"},
    {NULL}
};


// モジュール定義の構造体　・・・　モジュール名や説明、関数の定義体を定義
/*
*/
static struct PyModuleDef hello_module = {
    PyModuleDef_HEAD_INIT,
    "hello_module",
    "Python3 C++ API Module",
    -1,
    helloMethods
};


// モジュールを初期化する関数
PyMODINIT_FUNC PyInit_hello_module(void) {
    // import_array(); 配列を扱う場合に必要
    return PyModule_Create(&hello_module);
}
