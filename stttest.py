from pvleopard import create, LeopardActivationLimitError
from pvrecorder import PvRecorder
from threading import Thread
import time

vars = {}
with open('.env') as f:
	for line in f:
		line = line.strip()
		if line and '=' in line:
			key, value = line.split('=', 1)
			vars[key.strip()] = value.strip("'\'")
   
leopard = create(
    access_key = vars['ACCESS_KEY'],
    model_path = 'Arco-STT.pv'
)

class Recorder(Thread):
    def __init__(self, audio_device_index):
        super().__init__()
        self._pcm = list()
        self._is_recording = False
        self._stop = False
        self._audio_device_index = audio_device_index

    def is_recording(self):
        return self._is_recording

    def run(self):
        self._is_recording = True

        recorder = PvRecorder(frame_length=160, device_index=self._audio_device_index)
        recorder.start()

        while not self._stop:
            self._pcm.extend(recorder.read())
        recorder.stop()

        self._is_recording = False

    def stop(self):
        self._stop = True
        while self._is_recording:
            time.sleep(0.01)  # Avoid busy waiting
        return self._pcm

recorder = None

print('>>> Press `CTRL+C` to exit: ')

while True:
	if recorder is not None:
		input('>>> Recording ... Press `ENTER` to stop: ')
		try:
			transcript, words = leopard.process(recorder.stop())
			print(transcript)
		except LeopardActivationLimitError:
			print('AccessKey has reached its processing limit.')
		print()
		recorder = None
	else:
		input('>>> Press `ENTER` to start: ')
		recorder = Recorder(-1) # -1 means default device
		recorder.start()
		time.sleep(.25)