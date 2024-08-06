#| code-fold: true
from micrograd2023.engine import Value
from micrograd2023.nn import MLP
import random
def test_unit_mlp():
    # random seed for reproducibility
    random.seed(4876)
    # input dimension
    Ninput = 3
    Nhid1, Nhid2 = 5, 4 
    Nout = 2
    # input vector
    xs = [Value(random.random()) for _ in range(Ninput)]
    # call a MLP
    nnw = MLP(nin=Ninput, nouts = [Nhid1, Nhid2, Nout])

    # test number of layer
    assert len(nnw.layers) == len([Nhid1, Nhid2, Nout])
    num_layers = len(nnw.layers)

    # # number of parameters should be (Ninput + 1 bias)*Nhid1 + (Nhid1+1 bias)*Nhid2 + (Nhid2 + 1bias)*Nout
    num_paras =  (Ninput + 1)*Nhid1 + (Nhid1+1)*Nhid2 + (Nhid2 + 1)*Nout
    assert len(nnw.parameters()) == num_paras

    ys = nnw(xs)
    # # test out put dimension
    assert len(ys) == Nout

    # # manual calculation of the outputs
    xh = xs
    for idx in range(num_layers):
        ym = nnw.layers[idx](xh)
        xh = ym
    # no Relu() for the output layer
    # ym = [y if y.data >0 else Value(0) for y in ym]

    # test ys (output of neuron) vs. ym (manual calculation)
    tol=1.e-6
    for ysi, ymi in zip(ys, ym):
        assert abs(ysi.data - ymi.data) < tol 
