def profile_model(model, input_size, device):
    import time
    import torch

    model.eval()
    input_data = torch.randn(input_size).to(device)

    # Warm-up run
    with torch.no_grad():
        _ = model(input_data)

    # Measure inference time
    start_time = time.time()
    with torch.no_grad():
        output = model(input_data)
    end_time = time.time()

    print(f"Model output: {output}")
    print(f"Inference time: {end_time - start_time:.10f} seconds")