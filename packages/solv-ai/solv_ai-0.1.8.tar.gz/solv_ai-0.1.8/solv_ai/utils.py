def profile_model(model, input_size, device):
    import time
    import torch

    model.eval()
    input_data = torch.randn(input_size).to(device)

    # Warm-up run
    with torch.no_grad():
        _ = model(input_data)

    # Measure inference time
    torch.cuda.synchronize()  # Ensure all CUDA operations are complete
    start_time = time.perf_counter()
    with torch.no_grad():
        output = model(input_data)
    torch.cuda.synchronize()  # Ensure all CUDA operations are complete
    end_time = time.perf_counter()

    inference_time = end_time - start_time
    print(f"Model output: {output}")
    print(f"Inference time: {inference_time:.10f} seconds")