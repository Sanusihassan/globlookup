import os
from bs4 import BeautifulSoup
from transformers import GPT2LMHeadModel, GPT2Tokenizer, TextDataset, DataCollatorForLanguageModeling
from transformers import Trainer, TrainingArguments

# Step  1: Data Collection
html_folder = "/workspace/globlookup/backend/store/html"
data = []

for filename in os.listdir(html_folder):
    if filename.endswith('.html'):
        with open(os.path.join(html_folder, filename), 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f, 'html.parser')
            text = soup.get_text()
            data.append(text)

# Save the collected data to a text file for training
with open('collected_data.txt', 'w', encoding='utf-8') as f:
    for item in data:
        f.write("%s\n" % item)

# Step  2: Preprocessing (if needed)
# This step depends on the model requirements and may involve tokenization, etc.

# Step  3: Model Training
tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
model = GPT2LMHeadModel.from_pretrained('gpt2')

def load_dataset(train_path, test_path, tokenizer):
    train_dataset = TextDataset(
        tokenizer=tokenizer,
        file_path=train_path,
        block_size=128)
    
    test_dataset = TextDataset(
        tokenizer=tokenizer,
        file_path=test_path,
        block_size=128)
    
    data_collator = DataCollatorForLanguageModeling(
        tokenizer=tokenizer, mlm=False,
    )
    
    return train_dataset, test_dataset, data_collator

train_dataset, test_dataset, data_collator = load_dataset('collected_data.txt', 'collected_data.txt', tokenizer)

training_args = TrainingArguments(
    output_dir="/workspace/globlookup/backend/store/data",
    overwrite_output_dir=True,
    num_train_epochs=1,
    per_device_train_batch_size=1,
    save_steps=10_000,
    save_total_limit=2,
)

trainer = Trainer(
    model=model,
    args=training_args,
    data_collator=data_collator,
    train_dataset=train_dataset,
    eval_dataset=test_dataset,
)

trainer.train()

# Step  4: Prompting
prompt = "What are the telephone numbers in"
generated_text = model.generate(tokenizer.encode(prompt, return_tensors="pt"), max_length=100)
print(tokenizer.decode(generated_text[0], skip_special_tokens=True))
