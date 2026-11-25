"""PyTorch models: physics-informed NN (PINN) and a small CNN for thermal images.
Needs: pip install torch.  Run: python3 torch_models.py
NOTE: written to run on a normal PyTorch install; not executed in the authoring sandbox (no torch there)."""
import numpy as np, pandas as pd, torch, torch.nn as nn
from radiation import SIGMA

torch.manual_seed(0)
d = pd.read_csv("emissivity_clean.csv")
Tn, En = 1500.0, 1.0
X = torch.tensor(d[["temp_K", "emissivity"]].values / [Tn, En], dtype=torch.float32)
Ts = torch.tensor(d.surr_K.values, dtype=torch.float32)[:, None]
y = torch.tensor(d.flux_Wm2.values / 1e5, dtype=torch.float32)[:, None]

class PINN(nn.Module):
    def __init__(s):
        super().__init__(); s.net = nn.Sequential(nn.Linear(2, 64), nn.Tanh(), nn.Linear(64, 64), nn.Tanh(), nn.Linear(64, 1))
    def forward(s, x): return s.net(x)

m = PINN(); opt = torch.optim.Adam(m.parameters(), 1e-3)
for ep in range(3000):
    x = X.clone().requires_grad_(True); out = m(x)
    dT = torch.autograd.grad(out.sum(), x, create_graph=True)[0][:, :1]          # d flux / d (T/Tn)
    phys = 4 * x[:, 1:2] * SIGMA * (x[:, :1] * Tn) ** 3 * Tn / 1e5               # theory: 4 e sigma T^3
    loss = nn.functional.mse_loss(out, y) + 0.1 * nn.functional.mse_loss(dT, phys)
    opt.zero_grad(); loss.backward(); opt.step()
print("PINN final loss: %.5f" % loss.item())

class ThermalCNN(nn.Module):
    """Classifies a 64x64 thermal patch as hot-spot / normal."""
    def __init__(s):
        super().__init__()
        s.f = nn.Sequential(nn.Conv2d(1, 8, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2),
                            nn.Conv2d(8, 16, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2), nn.Flatten(), nn.Linear(16 * 16 * 16, 2))
    def forward(s, x): return s.f(x)

def synth(n):
    g = np.random.default_rng(0); xs, ys = [], []
    yy, xx = np.mgrid[0:64, 0:64]
    for i in range(n):
        im = 300 + g.normal(0, 2, (64, 64)); hot = i % 2
        if hot: cx, cy = g.integers(10, 54, 2); im += g.uniform(80, 200) * np.exp(-((xx - cx)**2 + (yy - cy)**2) / 40)
        xs.append((im - 300) / 200); ys.append(hot)
    return torch.tensor(np.array(xs), dtype=torch.float32)[:, None], torch.tensor(ys)

xi, yi = synth(600); cnn = ThermalCNN(); o = torch.optim.Adam(cnn.parameters(), 1e-3)
for ep in range(15):
    l = nn.functional.cross_entropy(cnn(xi[:480]), yi[:480]); o.zero_grad(); l.backward(); o.step()
acc = (cnn(xi[480:]).argmax(1) == yi[480:]).float().mean().item()
print("CNN hot-spot accuracy on synthetic validation: %.2f" % acc)
