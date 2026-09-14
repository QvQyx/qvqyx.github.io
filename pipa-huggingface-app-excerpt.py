from pathlib import Path
import tempfile

import gradio as gr
import torch
import torchaudio
from demucs.apply import apply_model
from demucs.audio import save_audio
from huggingface_hub import hf_hub_download


MODEL_REPO = "QvQyx/pipa-separator"


def load_model():
    model_path = hf_hub_download(repo_id=MODEL_REPO, filename="best.th")
    checkpoint = torch.load(model_path, map_location="cpu")
    model = checkpoint["klass"](**checkpoint["kwargs"])
    model.load_state_dict(checkpoint["state"])
    model.eval()
    return model


model = load_model()


def separate(audio_path):
    wav, sample_rate = torchaudio.load(audio_path)
    wav = wav.unsqueeze(0)

    with torch.no_grad():
        sources = apply_model(model, wav)

    output_dir = Path(tempfile.mkdtemp())
    output_paths = []

    for index, name in enumerate(model.sources):
        output_path = output_dir / f"{name}.wav"
        save_audio(sources[0, index], output_path, sample_rate)
        output_paths.append(str(output_path))

    return output_paths


with gr.Blocks(title="Pipa Separator") as demo:
    gr.Markdown("# Pipa Separator")
    gr.Markdown(
        "Upload an audio file containing pipa and other instruments. "
        "The model will separate them into individual stems."
    )

    audio_input = gr.Audio(label="Input audio", type="filepath")
    separate_button = gr.Button("Separate", variant="primary")

    with gr.Row():
        pipa_output = gr.Audio(label="Pipa")
        other_output = gr.Audio(label="Other")

    separate_button.click(
        fn=separate,
        inputs=audio_input,
        outputs=[pipa_output, other_output],
    )


if __name__ == "__main__":
    demo.launch()
