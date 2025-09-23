from datasets import load_dataset
from transformers import AutoTokenizer, AutoModelForSequenceClassification, Trainer, TrainingArguments
import torch

dataset = load_dataset('csv', data_files='review_dataset_clean.csv')
tokenizer = AutoTokenizer.from_pretrained('distilbert-base-uncased')
model = AutoModelForSequenceClassification.from_pretrained('distilbert-base-uncased', num_labels=3)

def preprocess(examples):
    return tokenizer(examples['text'], truncation=True, padding='max_length', max_length=128)

dataset = dataset.map(preprocess, batched=True)
label_map = {'positive': 0, 'neutral': 1, 'negative': 2}
dataset = dataset.class_encode_column('sentiment', label_map)

training_args = TrainingArguments(
    output_dir='./results',
    num_train_epochs=2,
    per_device_train_batch_size=16,
    per_device_eval_batch_size=16,
    evaluation_strategy='epoch',
    save_strategy='epoch',
    logging_dir='./logs',
    logging_steps=10,
    fp16=torch.cuda.is_available()
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=dataset['train'],
    eval_dataset=dataset['test']
)

trainer.train()
model.save_pretrained('transformer_sentiment_model')
tokenizer.save_pretrained('transformer_sentiment_model')
