# isoadverse/tests/test_attacks.py
import unittest
from attacks.text_fgsm import text_fgsm_attack
from utils.model_loader import get_model_and_tokenizer

class TestTextFGSM(unittest.TestCase):
    def test_text_fgsm_attack(self):
        model, tokenizer = get_model_and_tokenizer()
        text = "This is a test sentence."
        target = torch.tensor([1])
        perturbed_text = text_fgsm_attack(model, tokenizer, text, target, epsilon=0.3)
        self.assertEqual(perturbed_text.shape, torch.Size([1, len(tokenizer.encode(text))]))

if __name__ == '__main__':
    unittest.main()
