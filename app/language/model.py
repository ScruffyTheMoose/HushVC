from transformers import BlenderbotForConditionalGeneration, BlenderbotTokenizer
import torch

# Reference:
# https://huggingface.co/docs/transformers/main/en/model_doc/blenderbot#transformers.BlenderbotForConditionalGeneration


class Blenderbot:

    def __init__(self, model, tokenizer, **kwargs) -> None:
        # model specific things
        self.model: BlenderbotForConditionalGeneration = model
        self.tokenizer: BlenderbotTokenizer = tokenizer
        self.kwargs = kwargs

        # dialogue management
        self.tokens = torch.empty(1, 1, dtype=torch.long)
        self.max_tokens = 128

    def generate(self, input: str) -> str:
        # generates a response from the model given a text input
        enc_input = self.tokenizer.encode(input, return_tensors="pt")
        # adding new tokens to context
        self.update_tokens([enc_input])

        # ensuring we don't exceed max len - would truncate most recent input
        self.freshen()

        # getting output based on newly built context
        enc_output = self.model.generate(
            self.tokens, max_new_tokens=1024, **self.kwargs)  # using default config
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
