#pip install transformers
from transformers import GPT2LMHeadModel, GPT2Tokenizer

# Load pre-trained GPT-2 model and tokenizer
model = GPT2LMHeadModel.from_pretrained("gpt2")
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")

def generate_text(prompt, max_length=50):
    input_ids = tokenizer.encode(prompt, return_tensors="pt")

    # Generate text using the model
    output = model.generate(input_ids, max_length=max_length, num_return_sequences=1)

    # Decode the output to get the generated text
    generated_text = tokenizer.decode(output[0], skip_special_tokens=True)
    return generated_text


# Example usage
prompt_text = "Once upon a time"
predicted_text = generate_text(prompt_text, max_length=20)
print(predicted_text)

