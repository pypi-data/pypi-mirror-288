# isoadverse/utils/data_loader.py
from torch.utils.data import DataLoader, Dataset

class TextDataset(Dataset):
    def __init__(self, texts, labels):
        self.texts = texts
        self.labels = labels

    def __len__(self):
        return len(self.texts)

    def __getitem__(self, idx):
        return self.texts[idx], self.labels[idx]

def get_data_loader(texts, labels, batch_size):
    dataset = TextDataset(texts, labels)
    return DataLoader(dataset, batch_size=batch_size, shuffle=True)
