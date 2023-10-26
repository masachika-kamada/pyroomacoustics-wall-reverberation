import os
import wave

import numpy as np
from scipy.io import wavfile
from scipy.signal import resample_poly


def ensure_dir(file_path: str) -> None:
    directory = os.path.dirname(file_path)
    if directory and not os.path.exists(directory):
        os.makedirs(directory)


def scale_signal(signal: np.ndarray) -> np.ndarray:
    # スケーリングファクターを信号の最大絶対値に設定
    scaling_factor = np.max(np.abs(signal))
    # 音声データをスケーリングして int16 に変換
    return (signal * np.iinfo(np.int16).max / scaling_factor).astype(np.int16)


def write_signal_to_wav(signal: np.ndarray, wav_file_path: str, sample_rate: int) -> None:
    ensure_dir(wav_file_path)
    signal = scale_signal(signal)
    if len(signal.shape) == 1:
        channels = 1
    else:
        channels = signal.shape[0]
        signal = signal.T.flatten()

    with wave.open(wav_file_path, "w") as wave_out:
        wave_out.setnchannels(channels)
        wave_out.setsampwidth(2)
        wave_out.setframerate(sample_rate)
        wave_out.writeframes(signal.tobytes())


def load_signal_from_wav(wav_file_path: str, expected_fs: int) -> np.ndarray:
    fs, signal = wavfile.read(wav_file_path)
    if fs != expected_fs:
        signal = signal.astype(float)
        signal = resample_poly(signal, expected_fs, fs)
    return signal
