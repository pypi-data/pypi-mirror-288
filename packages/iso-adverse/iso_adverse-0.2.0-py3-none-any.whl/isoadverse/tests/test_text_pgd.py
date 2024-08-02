# isoadverse/tests/test_attacks.py
import unittest
from attacks.text_pgd import text_pgd_attack
from utils.model_loader import get_model_and_tokenizer

class TestTextPGD(unittest.TestCase):
    def test_text_pgd_attack(self):
        model, tokenizer = get_model_and_tokenizer()
        text = "This is a test sentence."
        target = torch.tensor([1])
        perturbed_text = text_pgd_attack(model, tokenizer, text, target, epsilon=0.3, alpha=0.1, num_steps=10)
        self.assertEqual(perturbed_text.shape, torch.Size([1, len(tokenizer.encode(text))]))

if __name__ == '__main__':
    unittest.main()
