from transformers import WhisperProcessor, WhisperForConditionalGeneration
import torch
import numpy as np

# Reference:
# https://huggingface.co/docs/transformers/main/en/model_doc/whisper#overview

# load model and processor
processor = WhisperProcessor.from_pretrained("openai/whisper-tiny")
model = WhisperForConditionalGeneration.from_pretrained("openai/whisper-tiny")
model.config.forced_decoder_ids = None


input_features = processor(
    sample["array"], sampling_rate=sample["sampling_rate"], return_tensors="pt").input_features

# generate token ids
predicted_ids = model.generate(input_features)
# decode token ids to text
transcription = processor.batch_decode(
    predicted_ids, skip_special_tokens=False)

transcription = processor.batch_decode(predicted_ids, skip_special_tokens=True)


class Whisper:
    def __init__(self, **kwargs) -> None:
        self.model = WhisperForConditionalGeneration.from_pretrained(
            "openai/whisper-tiny")
        self.processor = WhisperProcessor.from_pretrained(
            "openai/whisper-tiny")

        # temporary explicit definition
        self.sample_width = 2
        self.channels = 2
        self.sample_rate = 48000

    def generate(self, audio_array: np.ndarray) -> None:
        input_features = self.processor(
            audio_array, sampling_rate=self.sample_rate, return_tensors="pt", padding=True).input_features

        pred_ids = self.model.generate(input_features)

        transcription = processor.batch_decode(
            pred_ids, skip_special_tokens=False)

        return transcription
