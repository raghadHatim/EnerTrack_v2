"""
Check one finished dishwasher cycle with the trained EnerTrack model.

Needs only numpy (no scikit-learn / scipy / pandas).
Place next to: enertrack_model.json   (e.g. analysis/ml/)
"""
import json
from pathlib import Path

import numpy as np

STEP = 10  # seconds between samples
_MODEL = None


def _load():
    """Load the model once, on first use."""
    global _MODEL
    if _MODEL is None:
        with open(Path(__file__).parent / "enertrack_model.json") as f:
            _MODEL = json.load(f)
    return _MODEL


def readings_to_cycle(times, powers):
    """Raw readings (datetimes or seconds + watts) -> power array on a 10 s grid."""
    t = np.array([x.timestamp() if hasattr(x, "timestamp") else float(x) for x in times])
    p = np.asarray(powers, dtype=float)
    order = np.argsort(t)
    t, p = t[order], p[order]
    t = t - t[0]
    grid = np.arange(0, t[-1] + 1, STEP)
    return p[np.searchsorted(t, grid, side="right") - 1]   # hold last value


def cycle_features(power):
    """power: array of watts, one value every 10 s, for one whole cycle."""
    p = np.asarray(power, dtype=float)
    heat = p > 400                     # heating element
    mid = (p > 9) & ~heat              # pumps / drain
    return {
        "duration_s": (len(p) - 1) * STEP,
        "energy_kwh": round(float(p.sum() * STEP / 3.6e6), 4),
        "peak_w": float(p.max()),
        "heat_seconds": int(heat.sum() * STEP),
        "n_heat_blocks": int((heat[1:] & ~heat[:-1]).sum() + heat[0]),
        "mean_pump_w": round(float(p[mid].mean()), 2) if mid.any() else 0.0,
        "final_idle_w": round(float(p[-6:].mean()), 2),
    }


def check_cycle(power):
    """Returns {'is_fault', 'fault_type', 'reason', 'energy_kwh'}."""
    m = _load()
    f = cycle_features(power)
    x = np.array([f[c] for c in m["cols"]], dtype=float)

    # 1) is it far from a normal cycle? (Mahalanobis distance)
    xs = (x - np.array(m["scaler_mean"])) / np.array(m["scaler_scale"])
    d = xs - np.array(m["location"])
    dist = float(d @ np.array(m["precision"]) @ d)
    is_fault = (-dist - m["offset"]) < 0

    result = {"is_fault": bool(is_fault), "fault_type": None, "reason": None,
              "energy_kwh": f["energy_kwh"]}
    if not is_fault:
        return result

    # 2) which feature is most abnormal
    z = np.abs((x - np.array(m["z_mu"])) / np.array(m["z_sd"]))
    i = int(z.argmax())
    result["reason"] = f"{m['cols'][i]} is far from normal (z={z[i]:.1f})"

    # 3) fault type from the decision tree
    t, node = m["tree"], 0
    while t["left"][node] != -1:
        node = t["left"][node] if x[t["feature"][node]] <= t["threshold"][node] else t["right"][node]
    result["fault_type"] = t["classes"][int(np.argmax(t["value"][node]))]
    return result
