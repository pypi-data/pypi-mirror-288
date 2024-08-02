# isoadverse/attacks/text_pgd.py
import torch

def text_pgd_attack(model, tokenizer, text, target, epsilon, alpha, num_steps):
    # Tokenize the input text
    inputs = tokenizer(text, return_tensors='pt')
    
    # Ensure inputs are on the same device as the model
    inputs = {key: value.to(model.device) for key, value in inputs.items()}
    
    # Get embeddings from input IDs
    embedding_layer = model.get_input_embeddings()
    inputs_embeds = embedding_layer(inputs['input_ids'])
    
    # Initialize perturbed embeddings
    perturbed_embeds = inputs_embeds.clone().detach().requires_grad_(True)
    
    for _ in range(num_steps):
        # Forward pass using embeddings
        outputs = model(inputs_embeds=perturbed_embeds, attention_mask=inputs['attention_mask'])
        
        # Ensure the output has 'logits' for compatibility
        logits = outputs.logits if hasattr(outputs, 'logits') else outputs
        
        # Calculate loss
        loss = torch.nn.CrossEntropyLoss()(logits, target.to(model.device))
        
        # Zero all existing gradients
        model.zero_grad()
        
        # Backward pass
        loss.backward()
        
        # Collect the gradients of the embeddings
        data_grad = perturbed_embeds.grad.data
        
        # Create the perturbed embeddings
        perturbed_embeds = perturbed_embeds + alpha * data_grad.sign()
        
        # Ensure perturbed embeddings are within epsilon of the original embeddings
        delta = torch.clamp(perturbed_embeds - inputs_embeds, min=-epsilon, max=epsilon)
        perturbed_embeds = torch.clamp(inputs_embeds + delta, min=0, max=1).detach()
        perturbed_embeds.requires_grad_()
    
    return perturbed_embeds


