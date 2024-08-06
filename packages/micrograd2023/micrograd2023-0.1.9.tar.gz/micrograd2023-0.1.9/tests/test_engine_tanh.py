#| code-fold: true
import torch
from micrograd2023.engine import Value
def test_unit_tanh():
    a = Value(1.15)
    b = Value(5.33)

    g = a * b.tanh()
    g.backward()
    amg, bmg, gmg = a, b, g
    print(amg.grad, bmg.grad, gmg.data)

    a = torch.Tensor([1.15]).double()
    b = torch.Tensor([5.33]).double()
    a.requires_grad = True
    b.requires_grad = True

    g = a * torch.tanh(b)
    g.backward()
    apt, bpt, gpt = a, b, g
    print(apt.grad.item(), bpt.grad.item(), gpt.data.item())

    tol = 1e-4
    # test forward pass
    assert abs(gmg.data - gpt.data.item()) < tol 
    # test backward pass i.e. derivatives of the output w.r.t. parameters a and b
    assert abs(amg.grad - apt.grad.item()) < tol 
    assert abs(bmg.grad - bpt.grad.item()) < tol
