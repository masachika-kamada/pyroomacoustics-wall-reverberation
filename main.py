import matplotlib.pyplot as plt
import numpy as np
import pyroomacoustics as pra

from src.file_io import load_signal_from_wav, write_signal_to_wav


def create_materials(m=None):
    return pra.Material(energy_absorption=1.0) if m is None else pra.Material(m)


def plot_reverberation_wall(room, filename):
    fig, ax = plt.subplots()
    walls = room.walls
    for wall in walls:
        xs, ys = wall.corners
        absorption = wall.absorption

        if np.array(absorption).mean() == 1:
            color = "black"
        else:
            color = "red"

        ax.plot(xs, ys, color=color)

    plt.savefig(filename)
    plt.close(fig)


def main():
    room_corners = np.array([[-4, -3], [-4, 1], [2, 1], [2, -3]]).T
    hard_material = create_materials("hard_surface")
    no_wall_material = create_materials()
    signal = load_signal_from_wav("data/impulse_response.wav", 16000)

    plt.figure(figsize=(12, 10))

    for i in range(4):
        materials = [no_wall_material] * 4
        materials[i] = hard_material
        room = pra.Room.from_corners(room_corners, fs=16000, max_order=17, materials=materials)

        plot_reverberation_wall(room, f"output/room_{i}.png")

        room.add_microphone([0.1, 0])
        room.add_source([-0.1, 0], signal=signal)
        room.simulate()
        audio = room.mic_array.signals
        write_signal_to_wav(audio[0], f"output/reverberation_{i}.wav", 16000)

        audio_clipped = audio[0][7500:9000]

        plt.subplot(4, 1, i + 1)
        plt.plot(range(7500, 9000), audio_clipped)
        plt.title(f"Clipped Audio Signal from {i}")
        plt.xlabel("Sample")
        plt.ylabel("Amplitude")

    plt.tight_layout()
    plt.savefig("output/clipped_audio.png")
    plt.close()


if __name__ == "__main__":
    main()
