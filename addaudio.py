#!/usr/bin/env python3

import os
import subprocess
import tempfile

class AudioClipParams:
	def __init__(self, startTime, fadeOutTime, fadeOutLength, volume):
		self.startTime = startTime
		self.fadeOutTime = fadeOutTime
		self.fadeOutLength = fadeOutLength
		self.volume = volume

ffmpeg = "/usr/bin/ffmpeg"

srcAudioFn = "srcAudio.aac"
extraAudioEditedFn = "extraAudioEdited.aac"
srcAudioEditedFn = "srcAudioEdited.aac"

def FadeOutAudio(srcAudioFn, audioClipParams, destAudioFn):
	startTimeMs = int(audioClipParams.startTime * 1000)
	cmd = [
		ffmpeg,
		"-i", srcAudioFn,
		"-t", "%.3f" % (audioClipParams.fadeOutTime + audioClipParams.fadeOutLength),
		"-filter:a", "volume=%.3f, afade=t=out:st=%.3f:d=%.3f, adelay=%i:all=1" % (audioClipParams.volume, audioClipParams.fadeOutTime - audioClipParams.startTime, audioClipParams.fadeOutLength, startTimeMs),
		destAudioFn,
	]
	print(" ".join('"%s"' % s for s in cmd))
	subprocess.run(cmd)

def AddAudio(srcVideoFn, extraAudioFn, extraAudioClipParams, destVideoFn):
	with tempfile.TemporaryDirectory() as d:
		try:
			srcAudioAbsFn = os.path.join(d, srcAudioFn)
			srcAudioEditedAbsFn = os.path.join(d, srcAudioEditedFn)
			extraAudioEditedAbsFn = os.path.join(d, extraAudioEditedFn)

			FadeOutAudio(extraAudioFn, extraAudioClipParams, extraAudioEditedAbsFn)
			subprocess.run([ffmpeg, "-i", srcVideoFn, "-vn", "-acodec", "copy", srcAudioAbsFn])
			subprocess.run([ffmpeg, "-i", srcAudioAbsFn, "-i", extraAudioEditedAbsFn, "-filter_complex", "amix=inputs=2:duration=longest", srcAudioEditedAbsFn])
			subprocess.run([ffmpeg, "-i", srcVideoFn, "-i", srcAudioEditedAbsFn, "-c:v", "copy", "-c:a", "aac", "-map", "0:v:0", "-map", "1:a:0", "-shortest", destVideoFn])

		except subprocess.CalledProcessError as e:
			print(e)
