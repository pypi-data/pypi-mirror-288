# isoadverse/attacks/deepwordbug.py
import random

def deepwordbug_attack(text, num_bugs=5):
    words = text.split()
    perturbed_text = words.copy()
    for _ in range(num_bugs):
        idx = random.randint(0, len(words) - 1)
        perturbed_text[idx] = perturbed_text[idx][:-1]  # Simple bug: remove last character
    return ' '.join(perturbed_text)
