import pvporcupine
from pvrecorder import PvRecorder
from datetime import datetime

vars = {}
with open('.env') as f:
	for line in f:
		line = line.strip()
		if line and '=' in line:
			key, value = line.split('=', 1)
			vars[key.strip()] = value.strip("'\'")


porcupine = pvporcupine.create(
	access_key=vars['ACCESS_KEY'],
	keyword_paths=['Arco-Wake.ppn']
)

recorder = PvRecorder(frame_length=porcupine.frame_length)
recorder.start()

print('Listening ... (press Ctrl+C to exit)')

try:
	while True:
		pcm = recorder.read()
		result = porcupine.process(pcm)

		if result >= 0:
			print(f'[{str(datetime.now())}] Detected "Hey Arco"')
except KeyboardInterrupt:
	print('Stopping ...')
finally:
	recorder.delete()
	porcupine.delete()
