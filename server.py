"""Full-stack backend (stdlib only): serves index.html + JSON API.
Run: python3 server.py  ->  http://localhost:8000
API: /api/flux?e=0.8&T=800&Ts=300   /api/planck?T=5778   /api/materials"""
import json, os
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse, parse_qs
import numpy as np
from radiation import net_flux, wien_peak, planck

class Handler(SimpleHTTPRequestHandler):
    def _json(self, obj, code=200):
        b = json.dumps(obj).encode()
        self.send_response(code); self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(b))); self.end_headers(); self.wfile.write(b)

    def do_GET(self):
        u = urlparse(self.path); q = {k: v[0] for k, v in parse_qs(u.query).items()}
        try:
            if u.path == "/api/flux":
                e, T, Ts = float(q.get("e", .8)), float(q["T"]), float(q.get("Ts", 300))
                if not (0 <= e <= 1 and T > 0 and Ts > 0): return self._json({"error": "invalid input"}, 400)
                return self._json({"flux_Wm2": float(net_flux(e, T, Ts)), "wien_peak_nm": float(wien_peak(T) * 1e9),
                                   "note": "idealised grey-body estimate, not for safety-critical design"})
            if u.path == "/api/planck":
                T = float(q["T"]); wl = np.linspace(.1e-6, 20e-6, 100)
                return self._json({"wavelength_um": (wl * 1e6).tolist(), "radiance": planck(wl, T).tolist()})
            if u.path == "/api/materials":
                import pandas as pd
                return self._json(pd.read_csv("comparison_table.csv").to_dict("records"))
        except (KeyError, ValueError):
            return self._json({"error": "bad request"}, 400)
        return super().do_GET()

if __name__ == "__main__":
    print("http://localhost:8000"); ThreadingHTTPServer(("", 8000), Handler).serve_forever()
