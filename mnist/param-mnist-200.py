
import numpy as np

from learning.dataset import BarsData, FromModel, MNIST
from learning.preproc import Binarize
from learning.stbp_layers import  STBPStack, SigmoidBeliefLayer, FactoizedBernoulliTop, CNADE
from learning.training import Trainer
from learning.termination import LogLikelihoodIncrease, EarlyStopping
from learning.monitor import MonitorLL, DLogModelParams, SampleFromP

n_vis = 28*28

dataset  = MNIST(fname="mnist_salakhutdinov.pkl.gz", which_set='salakhutdinov_train', n_datapoints=59000)
smallset = MNIST(fname="mnist_salakhutdinov.pkl.gz", which_set='salakhutdinov_valid', n_datapoints=100)
valiset  = MNIST(fname="mnist_salakhutdinov.pkl.gz", which_set='salakhutdinov_valid', n_datapoints=1000)
testset  = MNIST(fname="mnist_salakhutdinov.pkl.gz", which_set='test', n_datapoints=10000)

p_layers=[
    SigmoidBeliefLayer( 
        n_X=n_vis,
        n_Y=200,
    ),
    FactoizedBernoulliTop(
        n_X=200,
    )
]

q_layers=[
    CNADE(
        unroll_scan=1,
        n_X=200,
        n_Y=n_vis,
        n_hid=200
    ),
]

model = STBPStack(
    p_layers=p_layers,
    q_layers=q_layers,
)

trainer = Trainer(
    n_samples=5,
    learning_rate_p=1e-3,
    learning_rate_q=1e-3,
    learning_rate_s=1e-3,
    layer_discount=1.0,
    batch_size=100,
    dataset=dataset, 
    model=model,
    termination=EarlyStopping(),
    #step_monitors=[MonitorLL(data=smallset, n_samples=[1, 5, 25, 100])],
    epoch_monitors=[MonitorLL(data=valiset, n_samples=[100]), DLogModelParams(), SampleFromP(n_samples=100)],
    final_monitors=[MonitorLL(data=testset, n_samples=[1, 5, 10, 25, 100, 500])],
    monitor_nth_step=100,
)
