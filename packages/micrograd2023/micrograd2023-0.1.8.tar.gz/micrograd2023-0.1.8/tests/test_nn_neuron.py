#| code-fold: true
from micrograd2023.engine import Value
from micrograd2023.nn import Neuron
import random
def test_unit_neuron():
    
    # random seed for reproducibility
    random.seed(41)
    # input dimension
    Ninput = 5

    # input vector
    xs = [Value(random.random()) for _ in range(Ninput)]

    # call a neuron
    nron = Neuron(nin=Ninput)

    # number of parameters should be 6 (5 + 1 bias)
    assert len(nron.parameters()) == (Ninput+1)

    # neuron output    
    ys = nron(xs)
    # manual calculation of the output
    ym = sum(xi*wi for xi, wi in zip(xs, nron.parameters()))
    # manual Relu()
    ym = ym if ym.data >0 else Value(0)
    print(ys, ym)

    # test ys (output of neuron) vs. ym (manual calculation)
    tol = 1e-6
    assert abs(ys.data - ym.data) < tol
