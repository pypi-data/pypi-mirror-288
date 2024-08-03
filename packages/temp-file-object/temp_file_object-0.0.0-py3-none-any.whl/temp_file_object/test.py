
# 一時ファイルオブジェクト [temp-file-object]
# 【動作確認 / 使用例】

import sys
import wave
from sout import sout
from ezpip import load_develop
# 一時ファイルオブジェクト [temp-file-object]
tfo = load_develop("temp_file_object", "../", develop_flag = True)

# 音声ファイルの中身を取り出す
def read_sound_tfo(arg_tfo):
	with arg_tfo.open("rb") as f:	# ファイルハンドラの取得 [tfo]
		with wave.open(f, "rb") as wav_obj:
			frames = wav_obj.readframes(wav_obj.getnframes())	# フレームデータを取得
			params = wav_obj.getparams()	# パラメータを取得
	return frames, params

# 2つの音声を結合
def concat_sounds(sound_1_tfo, sound_2_tfo):
	frames_1, params_1 = read_sound_tfo(sound_1_tfo)	# 音声ファイルの中身を取り出す
	frames_2, params_2 = read_sound_tfo(sound_2_tfo)	# 音声ファイルの中身を取り出す
	# 出力のtfoを作る
	res_tfo = tfo.TempFileObject("wav")	# 無名のtfoオブジェクトを作る [tfo]
	with res_tfo.open("wb") as f:	# ファイルハンドラの取得 [tfo]
		with wave.open(f, "wb") as wav_obj:
			wav_obj.setparams(params_1)
			wav_obj.writeframes(frames_1)	# 1つ目のフレームデータを書き込む
			wav_obj.writeframes(frames_2)	# 2つ目のフレームデータを書き込む
	return res_tfo

# 入力ファイルをtfoオブジェクトに変換
sound_1_tfo = tfo.TempFileObject("wav", "./test_file/test_1.wav")	# ファイルからtfoオブジェクトを生成 [tfo]
sound_2_tfo = tfo.TempFileObject("wav", "./test_file/test_2.wav")	# ファイルからtfoオブジェクトを生成 [tfo]
# 処理を実行
res_tfo = concat_sounds(sound_1_tfo, sound_2_tfo)	# 2つの音声を結合
# 結果をファイルとして保存
res_tfo.save("output.wav")	# tfoオブジェクトをファイルとして出力 [tfo]
