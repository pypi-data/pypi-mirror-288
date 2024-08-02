# isoadverse/utils/model_loader.py
from transformers import BertForSequenceClassification, BertTokenizer

def get_model_and_tokenizer(model_name='bert-base-uncased'):
    model = BertForSequenceClassification.from_pretrained(model_name)
    tokenizer = BertTokenizer.from_pretrained(model_name)
    return model, tokenizer
