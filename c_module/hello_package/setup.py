from distutils.core import setup, Extension

setup(name = "hello_package", 
    version = "1.0.0",
    packages=['hello_package'], # hello_package/__init__.py も読み込むため
    ext_package='hello_package', # Extension("hello_package.hello_module", ~　とするのと同じ
    ext_modules = [Extension("hello_module", ["hello_package/hello_module.cpp"]),
        Extension("copy.hello_module_copy", ["hello_package/hello_module_copy.cpp"])]
        # 下の書き方だと site-packages/hello_module/copy/以下に hello_module_copy が作成される
        # Extension("copy.hello_module_copy", ["hello_package/hello_module_copy.cpp"])]
        # 下の書き方はhello_module_copyがうまくインストールされない
        # ext_modules = [Extension("hello_module", ["hello_package/hello_module.cpp", "hello_package/hello_module_copy.cpp"])]
    )

### python setup.py build_ext -i -> ビルドのみ
### python setup.py install -> パッケージとしてインストール
### setup.pyを行う場合は都度 buildディレクトリを削除する必要がある