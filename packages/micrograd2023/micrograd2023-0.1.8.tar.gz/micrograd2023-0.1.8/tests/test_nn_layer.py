#| code-fold: true
from micrograd2023.engine import Value
from micrograd2023.nn import Layer
import random
def test_unit_layer():
    
    # random seed for reproducibility
    random.seed(4899)
    # input dimension
    Ninput = 5
    Nout = 3
    # input vector
    xs = [Value(random.random()) for _ in range(Ninput)]
    # call a layer
    nl = Layer(nin=Ninput, nout=Nout)

    # number of parameters should be (Ninput + 1 bias)xNout = (5+1)x3 = 18
    num_paras =  (Ninput+1)*Nout
    assert len(nl.parameters()) == num_paras

    ys = nl(xs)
    # test out put dimension
    assert len(ys) == Nout

    # manual calculation of the outputs
    ym = [sum(xi*wi for xi, wi in zip(xs, nl.neurons[idx].parameters())) for idx in range(Nout)]
    # manual Relu()
    ym = [y if y.data >0 else Value(0) for y in ym]

    # test ys (output of neuron) vs. ym (manual calculation)
    tol = 1e-6
    for ysi, ymi in zip(ys, ym):
        assert abs(ysi.data - ymi.data) < tol
