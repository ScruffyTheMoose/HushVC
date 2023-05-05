from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
import torch

# Reference:
# https://huggingface.co/docs/transformers/main/en/model_doc/blenderbot#transformers.BlenderbotForConditionalGeneration

# just an initial test of the model to validate it will work for our use case
# will build out the rest shortly

model_name = "facebook/blenderbot-400M-distill"

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

UTTERANCE = "My dog is having a blast running outside today!"
print("Human: ", UTTERANCE)

inputs = tokenizer([UTTERANCE], return_tensors="pt")
reply_ids = model.generate(**inputs)
print("Bot: ", tokenizer.batch_decode(reply_ids, skip_special_tokens=True)[0])
