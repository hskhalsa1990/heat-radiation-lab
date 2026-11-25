"""Deep learning: small MLP written in pure numpy (no GPU/torch needed)."""
import numpy as np, pandas as pd
rng = np.random.default_rng(0)
d = pd.read_csv("emissivity_clean.csv")
X = d[["temp_K", "emissivity"]].values / np.array([1500., 1.])
y = (d["flux_Wm2"].values / 1e5)[:, None]
n = int(.8 * len(X)); Xt, Xv, yt, yv = X[:n], X[n:], y[:n], y[n:]
W1 = rng.normal(0, .3, (2, 32)); b1 = np.zeros(32)
W2 = rng.normal(0, .3, (32, 32)); b2 = np.zeros(32)
W3 = rng.normal(0, .3, (32, 1)); b3 = np.zeros(1)
def fwd(x):
    h1 = np.tanh(x @ W1 + b1); h2 = np.tanh(h1 @ W2 + b2); return h1, h2, h2 @ W3 + b3
lr = .01
for ep in range(6000):
    h1, h2, o = fwd(Xt); g = 2 * (o - yt) / len(Xt)
    gW3 = h2.T @ g; g2 = (g @ W3.T) * (1 - h2**2)
    gW2 = h1.T @ g2; g1 = (g2 @ W2.T) * (1 - h1**2); gW1 = Xt.T @ g1
    W3 -= lr * gW3; b3 -= lr * g.sum(0); W2 -= lr * gW2; b2 -= lr * g2.sum(0)
    W1 -= lr * gW1; b1 -= lr * g1.sum(0)
pv = fwd(Xv)[2]
r2 = 1 - ((pv - yv)**2).sum() / ((yv - yv.mean())**2).sum()
print("MLP validation R2 = %.4f" % r2)
