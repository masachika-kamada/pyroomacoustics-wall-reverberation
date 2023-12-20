import pyroomacoustics as pra
import numpy as np
import matplotlib.pyplot as plt

from src.file_io import load_signal_from_wav, write_signal_to_wav


corners = np.array([
    [0, 0],
    [0, 3],
    [3, 3],
    [3, 1],
    [5, 1],
    [5, 3],
    [8, 3],
    [8, 0],
]).T

material = pra.Material("hard_surface")
room = pra.Room.from_corners(corners, fs=16000, materials=material, max_order=0)
# max_orderを増やして音源からマイクまでのパスを作るとエラーが消える
# room = pra.Room.from_corners(corners, fs=16000, materials=material, max_order=6)

signal = load_signal_from_wav("data/arctic_a0001.wav", 16000)
room.add_source([1, 2], signal=signal)

room.add_microphone_array(pra.MicrophoneArray(np.array([[6, 2.5]]).T, fs=16000))

room.plot()
plt.savefig("room.png")
plt.close()

room.simulate()
write_signal_to_wav(room.mic_array.signals, "room.wav", 16000)
