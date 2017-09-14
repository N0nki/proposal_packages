import sys, os

def expand_load_path(filename):
    """
    ロードパスにファイルの１つ上のディレクトリを追加する
    """
    sys.path.append(os.path.dirname(os.path.abspath(filename)) + "/..")
