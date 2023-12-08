#!/usr/bin/env python3

import os
import subprocess
import tempfile

class AudioClipParams:
	def __init__(self, fadeOutTime, fadeOutLength, volume):
		self.fadeOutTime = fadeOutTime
		self.fadeOutLength = fadeOutLength
		self.volume = volume

ffmpeg = "/usr/bin/ffmpeg"

srcAudioFn = "srcAudio.aac"
extraAudioEditedFn = "extraAudioEdited.aac"

def FadeOutAudio(srcAudioFn, audioClipParams, destAudioFn):
	cmd = [
		ffmpeg,
		"-i", srcAudioFn,
		"-t", "%.3f" % (audioClipParams.fadeOutTime + audioClipParams.fadeOutLength),
		"-filter:a", "volume=%.3f, afade=t=out:st=%.3f:d=%.3f" % (audioClipParams.volume, audioClipParams.fadeOutTime, audioClipParams.fadeOutLength),
		destAudioFn,
	]
	subprocess.run(cmd)

def AddAudio(srcVideoFn, extraAudioFn, audioClipParams, destVideoFn):
	extraAudioClipParams = AudioClipParams(4, 1, 0.2)
	with tempfile.TemporaryDirectory() as d:
		try:
			FadeOutAudio(extraAudioFn, extraAudioClipParams, os.path.join(d, extraAudioEditedFn))
			# subprocess.run([ffmpeg, "-i", srcVideoFn, "-vn", "-acodec", "copy", os.path.join(d, srcAudioFn))
			# subprocess.run([ffmpeg, 
			print(d)
			input("heehee done!")

		except subprocess.CalledProcessError as e:
			print(e)
