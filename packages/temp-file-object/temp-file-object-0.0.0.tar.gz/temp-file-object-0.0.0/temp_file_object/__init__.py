
# 一時ファイルオブジェクト [temp-file-object]

import os
import sys
import shutil
import slim_id
from sout import sout

TEMP_FILE_DIR = "./__tfo_temp__/"

# with文脈で使われるとファイルハンドラーを返すオブジェクト
class FileHandlerGenerator:
	# 初期化処理
	def __init__(self, tfo_obj, mode):
		self.tfo_obj = tfo_obj
		self.mode = mode
	# with文脈での使用時
	def __enter__(self):
		path = self.tfo_obj.temp_file_path	# 操作対象のファイルパス
		self.handler = open(path, self.mode)
		return self.handler
	# with文脱出時の処理
	def __exit__(self, *exit_args):
		self.handler.__exit__(self, *exit_args)

# 「一時ファイルオブジェクト」クラス [temp-file-object]
class TempFileObject:
	# 初期化処理
	def __init__(self,
		ext,	# ファイル拡張子
		input_filepath = None,	# ファイルパス (ファイルからtfoオブジェクトを生成する場合)
	):
		self.ext = ext	# ファイルの拡張子
		self.data_id = slim_id.gen(lambda e: False, length = 22)	# データを識別するIDを生成 (暗号学的乱数)
		self.temp_file_path = os.path.join(TEMP_FILE_DIR, f"{self.data_id}.{self.ext}")	# 変な名前
		# ファイル設置 (ファイルからtfoオブジェクトを生成する場合)
		os.makedirs(os.path.dirname(self.temp_file_path), exist_ok = True)	# コピー先のディレクトリを作成
		if input_filepath is not None:
			shutil.copy(input_filepath, self.temp_file_path)
	# ファイルハンドラの取得 [tfo]
	def open(self, mode):
		# with文脈で使われるとファイルハンドラーを返すオブジェクト
		fhg = FileHandlerGenerator(self, mode)
		return fhg
	# tfoオブジェクトをファイルとして出力 [tfo]
	def save(self, output_filepath):
		shutil.copy(self.temp_file_path, output_filepath)
	# ガベージコレクタによるオブジェクト削除を拾う [tfo]
	def __del__(self):
		if os.path.exists(self.temp_file_path):
			os.remove(self.temp_file_path)
