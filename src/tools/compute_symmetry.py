import numpy as np

def compute_symmetrical_components(voltages, currents):
    """Compute symmetrical components of a 3-phase system."""
    alpha = np.exp(2j * np.pi / 3)
    
    A = np.array([
        [1, 1, 1],
        [1, alpha, alpha**2],
        [1, alpha**2, alpha]
    ])

    components_v = np.dot(np.linalg.inv(A), voltages)
    components_i = np.dot(np.linalg.inv(A), currents)

    # Extracting components
    vi, vo, vd = components_v
    io, ii, id = components_i

    return {
        "Positive Sequence Voltage": vi.real,
        "Negative Sequence Voltage": vo.real,
        "Zero Sequence Voltage": vd.real,
        "Positive Sequence Current": io.real,
        "Negative Sequence Current": ii.real,
        "Zero Sequence Current": id.real
    }
