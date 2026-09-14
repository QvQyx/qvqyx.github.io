import os
import random

import librosa
import numpy as np
import soundfile as sf


PIPA_DIR = "/Users/qvqyx/PipaSoloV2"
ACCOMPANIMENT_DIR = "/Users/qvqyx/PianoSoloV2"
OUTPUT_DIR = "/Users/qvqyx/PipaPianoData/test"

SAMPLE_RATE = 44100
MIXES_PER_PIPA = 6


def normalize(audio):
    peak = np.max(np.abs(audio))
    return audio / peak if peak > 0 else audio


def to_stereo(audio):
    return np.stack([audio, audio], axis=1)


os.makedirs(OUTPUT_DIR, exist_ok=True)

pipa_files = sorted(f for f in os.listdir(PIPA_DIR) if f.endswith(".wav"))
accompaniment_files = sorted(
    f for f in os.listdir(ACCOMPANIMENT_DIR) if f.endswith(".wav")
)

track_id = 1

for pipa_file in pipa_files:
    pipa_path = os.path.join(PIPA_DIR, pipa_file)
    pipa, sr = librosa.load(pipa_path, sr=SAMPLE_RATE, mono=True)
    pipa = normalize(pipa)

    for _ in range(MIXES_PER_PIPA):
        accompaniment_file = random.choice(accompaniment_files)
        accompaniment_path = os.path.join(ACCOMPANIMENT_DIR, accompaniment_file)
        accompaniment, _ = librosa.load(
            accompaniment_path,
            sr=SAMPLE_RATE,
            mono=True,
        )
        accompaniment = normalize(accompaniment)

        min_len = min(len(pipa), len(accompaniment))
        pipa_cut = pipa[:min_len]

        if len(accompaniment) > min_len:
            start = random.randint(0, len(accompaniment) - min_len)
            accompaniment = accompaniment[start : start + min_len]
        else:
            accompaniment = accompaniment[:min_len]

        pipa_gain = random.uniform(0.6, 1.0)
        accompaniment_gain = random.uniform(0.4, 1.0)

        pipa_stem = pipa_gain * pipa_cut
        other_stem = accompaniment_gain * accompaniment
        mixture = pipa_stem + other_stem

        peak = np.max(np.abs(mixture))
        if peak > 0:
            mixture = mixture / peak
            pipa_stem = pipa_stem / peak
            other_stem = other_stem / peak

        track_name = f"track_{track_id:04d}"
        track_dir = os.path.join(OUTPUT_DIR, track_name)
        os.makedirs(track_dir, exist_ok=True)

        sf.write(os.path.join(track_dir, "mixture.wav"), to_stereo(mixture), sr)
        sf.write(os.path.join(track_dir, "pipa.wav"), to_stereo(pipa_stem), sr)
        sf.write(os.path.join(track_dir, "other.wav"), to_stereo(other_stem), sr)

        track_id += 1


print(f"Produced {track_id - 1} tracks")
