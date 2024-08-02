# isoadverse/attacks/text_fgsm.py
import torch

def text_fgsm_attack(model, tokenizer, text, target, epsilon):
    # Tokenize the input text
    inputs = tokenizer(text, return_tensors='pt')
    
    # Ensure inputs are on the same device as the model
    inputs = {key: value.to(model.device) for key, value in inputs.items()}
    
    # Get embeddings from input IDs
    embedding_layer = model.get_input_embeddings()
    inputs_embeds = embedding_layer(inputs['input_ids'])
    
    # Set requires_grad on embeddings
    inputs_embeds = inputs_embeds.clone().detach().requires_grad_(True)
    
    # Forward pass using embeddings
    outputs = model(inputs_embeds=inputs_embeds, attention_mask=inputs['attention_mask'])
    
    # Ensure the output has 'logits' for compatibility
    logits = outputs.logits if hasattr(outputs, 'logits') else outputs
    
    # Ensure target is a tensor and on the correct device
    target = torch.tensor(target).to(model.device)

    # Calculate loss
    loss = torch.nn.CrossEntropyLoss()(logits, target)
    
    # Zero all existing gradients
    model.zero_grad()
    
    # Backward pass
    loss.backward()
    
    # Collect the gradients of the embeddings
    data_grad = inputs_embeds.grad.data
    
    # Create the perturbed embeddings
    sign_data_grad = data_grad.sign()
    perturbed_data = inputs_embeds + epsilon * sign_data_grad

    # Convert perturbed embeddings back to input IDs
    with torch.no_grad():
        logits = model(inputs_embeds=perturbed_data, attention_mask=inputs['attention_mask']).logits
        perturbed_ids = torch.argmax(logits, dim=-1)

    return perturbed_ids


