def profile_model(model, input_size):
    import time
    import torch

    model.eval()
    input_data = torch.randn(input_size)
    start_time = time.time()
    with torch.no_grad():
        _ = model(input_data)
    end_time = time.time()
    print(f"Inference time: {end_time - start_time:.6f} seconds")