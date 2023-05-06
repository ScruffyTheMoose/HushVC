from transformers import BlenderbotForConditionalGeneration, BlenderbotTokenizer
import torch

# Reference:
# https://huggingface.co/docs/transformers/main/en/model_doc/blenderbot#transformers.BlenderbotForConditionalGeneration

# just an initial test of the model to validate it will work for our use case
# will build out the rest shortly

model_name = "facebook/blenderbot-400M-distill"

tokenizer = BlenderbotTokenizer.from_pretrained(model_name)
model = BlenderbotForConditionalGeneration.from_pretrained(model_name)

UTTERANCE = " "
print("Human: ", UTTERANCE)

inputs = tokenizer.encode(UTTERANCE, return_tensors="pt")
reply_ids = model.generate(inputs, max_new_tokens=1024)
print("Bot: ", tokenizer.batch_decode(reply_ids, skip_special_tokens=False)[0])

# this class will use the pretrained model with default configs/weights
print(inputs)
print(tokenizer.batch_decode(inputs))


class Blenderbot:
    # static delimiters
    st = "<s>"  # token id 1
    en = "</s>"  # token id 2

    def __init__(self, model, tokenizer, **kwargs) -> None:
        # model specific things
        self.model: BlenderbotForConditionalGeneration = model
        self.tokenizer: BlenderbotTokenizer = tokenizer
        self.kwargs = kwargs

        # dialogue management
        self.tokens = torch.empty(1, 1)
        self.max_tokens = 128

    def generate(self, input: str) -> str:
        # generates a response from the model given a text input
        enc_input = self.tokenizer.encode(input, return_tensors="pt")
        # adding new tokens to context
        self.update_tokens([enc_input])

        # ensuring we don't exceed max len - would truncate most recent input
        self.freshen()

        # getting output based on newly built context
        enc_output = self.model.generate(self.tokens)  # using default config
        # concatenate tokens
        self.update_tokens([enc_output])

        output = self.tokenizer.batch_decode(
            enc_output, skip_special_tokens=True)[0]

        return output

    def update_tokens(self, new_tokens: list[torch.Tensor]) -> None:
        tks = tuple([self.tokens] + new_tokens)

        self.tokens = torch.cat(tks, dim=1)

    def freshen(self) -> None:
        # clears old responses to ensure we are passing <= max sequence length to the model
        # we don't want our newest input to be truncated
        # tokenizer.model_max_length == 128 for 400M distill

        num_tokens = len(self.tokens[0])  # token count
        idx = num_tokens - self.max_tokens  # num tokens over max

        if idx > 0:
            self.tokens = self.tokens[:, idx:]  # slicing out excess tokens
