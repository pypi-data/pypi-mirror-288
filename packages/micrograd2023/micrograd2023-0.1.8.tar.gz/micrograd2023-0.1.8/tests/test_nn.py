#| code-fold: true
import torch
from micrograd2023.engine import Value
from micrograd2023.nn import MLP
import random
import numpy as np
def test_integration_nn():
    """ TODO: to refactor this function and make it cleaner :) """
    # random seed for reproducibility
    random.seed(48198)
    # input dimension
    Ninput = 3
    Nhid1, Nhid2 = 5, 4 
    Nout = 2
    # input vector
    xs = [Value(random.random()) for _ in range(Ninput)]
    # call a MLP
    nnw = MLP(nin=Ninput, nouts = [Nhid1, Nhid2, Nout])
    ys = nnw(xs)
    loss = sum(ys).tanh()
    loss.backward()


    # let's have the same inputs for torch
    xst = torch.Tensor([xsi.data for xsi in xs])
    xst.requires_grad = True

    # let's use the same model for torch
    tmodel = torch.nn.Sequential(
        torch.nn.Linear(Ninput, Nhid1),
        torch.nn.ReLU(),
        torch.nn.Linear(Nhid1, Nhid2),
        torch.nn.ReLU(),
        torch.nn.Linear(Nhid2, Nout),
        # torch.nn.Tanh()
    )
    # let's fill the same parameters for the torch model
    ## 1st hidden layer
    tlayer_id = 0
    layer_id = 0
    Nrow = Nhid1
    Ncol = Ninput
    ws = []
    for idx in range(len(nnw.layers[layer_id].parameters())):
        ws.append(nnw.layers[layer_id].parameters()[idx].data)
    # reshape and remove the bias column
    wss = np.reshape(ws, (Nrow, Ncol+1))[:,:-1]
    # fill in the same weights for tmodel
    for i in range(Nrow):
            for j in range(Ncol):
                tmodel[tlayer_id].weight.data[i,j].fill_(wss[i,j])

    tmodel[tlayer_id].bias.data.fill_(0.0)

    # let's fill the same parameters for the torch model
    ## 2nd hidden layer
    tlayer_id = 2
    layer_id = 1
    Nrow = Nhid2
    Ncol = Nhid1
    ws = []
    for idx in range(len(nnw.layers[layer_id].parameters())):
        ws.append(nnw.layers[layer_id].parameters()[idx].data)
    # reshape and remove the bias column
    wss = np.reshape(ws, (Nrow, Ncol+1))[:,:-1]
    # fill in the same weights for tmodel
    for i in range(Nrow):
            for j in range(Ncol):
                tmodel[tlayer_id].weight.data[i,j].fill_(wss[i,j])

    tmodel[tlayer_id].bias.data.fill_(0.0)

    # let's fill the same parameters for the torch model
    ## 3rd hidden layer
    tlayer_id = 4
    layer_id = 2
    Nrow = Nout
    Ncol = Nhid2
    ws = []
    for idx in range(len(nnw.layers[layer_id].parameters())):
        ws.append(nnw.layers[layer_id].parameters()[idx].data)
    # reshape and remove the bias column
    wss = np.reshape(ws, (Nrow, Ncol+1))[:,:-1]
    # fill in the same weights for tmodel
    for i in range(Nrow):
            for j in range(Ncol):
                tmodel[tlayer_id].weight.data[i,j].fill_(wss[i,j])

    tmodel[tlayer_id].bias.data.fill_(0.0)

    # compute loss for torch
    yst = tmodel(xst)
    tloss = yst.sum().tanh()
    tloss.backward()

    # test forward pass
    tol = 1e-6
    assert abs(loss.data - tloss.data.item()) < tol

    # test backward pass
    for idx in range(Ninput):
        assert abs(xs[idx].grad - xst.grad[idx]) < tol
