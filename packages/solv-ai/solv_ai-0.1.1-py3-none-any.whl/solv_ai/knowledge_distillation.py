import torch
import torch.nn as nn
import torch.nn.functional as F

class DistillationLoss(nn.Module):
    def __init__(self, teacher_model, student_model, temperature=2.0, alpha=0.5):
        if not isinstance(teacher_model, nn.Module):
            raise TypeError("Teacher model must be an instance of nn.Module")
        if not isinstance(student_model, nn.Module):
            raise TypeError("Student model must be an instance of nn.Module")
        if not isinstance(temperature, (int, float)) or temperature <= 0:
            raise ValueError("Temperature must be a positive number")
        if not isinstance(alpha, (int, float)) or not (0 <= alpha <= 1):
            raise ValueError("Alpha must be between 0 and 1")
        super(DistillationLoss, self).__init__()
        self.teacher_model = teacher_model
        self.student_model = student_model
        self.temperature = temperature
        self.alpha = alpha

    def forward(self, x, target):
        if not isinstance(x, torch.Tensor):
            raise TypeError("Input must be a torch.Tensor")
        if not isinstance(target, torch.Tensor):
            raise TypeError("Target must be a torch.Tensor")
        teacher_output = self.teacher_model(x)
        student_output = self.student_model(x)
        soft_loss = F.kl_div(F.log_softmax(student_output / self.temperature, dim=1),
                             F.softmax(teacher_output / self.temperature, dim=1),
                             reduction='batchmean') * (self.temperature ** 2)
        hard_loss = F.cross_entropy(student_output, target)
        return self.alpha * soft_loss + (1 - self.alpha) * hard_loss