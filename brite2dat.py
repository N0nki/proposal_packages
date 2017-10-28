#!/usr/bin/env python

import argparse
from brite_utils import *

parser = argparse.ArgumentParser(description=".briteファイルからdatファイルまたはmatplotlibで描画する際に必要なノードの位置座標を書き込んだCSVファイルを生成します")
parser.add_argument("mode", type=str, help="生成するファイルの種類を指定します．値は必ずdatまたはcsvとしてください")
parser.add_argument("brite", type=str, help="対象とする.briteファイルを指定してください")
parser.add_argument("output", type=str, help="出力するdatまたはcsvファイルを指定してください")
args = parser.parse_args()

if args.mode == "dat":
    to_dat(args.brite, args.output)
elif args.mode == "csv":
    to_coordinate_csv(args.brite, args.output)
else:
    raise parser.error("不正な値です．第1引数は必ずdatまたはcsvとしてください")
