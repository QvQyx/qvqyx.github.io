from pathlib import Path

import torch
import torchaudio
from demucs.apply import apply_model
from demucs.audio import save_audio


CHECKPOINT_PATH = "/Users/qvqyx/demucs/outputs/xps/50e985af/best.th"
TEST_AUDIO_PATH = "/Users/qvqyx/Desktop/6b/Spliter/tests/testPipaPiano.WAV"
OUTPUT_DIR = Path("/Users/qvqyx/Desktop/6b/Spliter/output")


def load_trained_model(checkpoint_path):
    checkpoint = torch.load(checkpoint_path, map_location="cpu")
    model = checkpoint["klass"](**checkpoint["kwargs"])
    model.load_state_dict(checkpoint["state"])
    model.eval()
    return model


model = load_trained_model(CHECKPOINT_PATH)
wav, sample_rate = torchaudio.load(TEST_AUDIO_PATH)
wav = wav.unsqueeze(0)

with torch.no_grad():
    sources = apply_model(model, wav)

OUTPUT_DIR.mkdir(exist_ok=True)

for index, name in enumerate(model.sources):
    output_path = OUTPUT_DIR / f"{name}.wav"
    save_audio(sources[0, index], output_path, sample_rate)
    print(f"Saved {output_path}")


print("Separation complete")
