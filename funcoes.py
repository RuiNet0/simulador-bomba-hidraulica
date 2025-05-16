import numpy as np

def altura_mano(Q, H0, k):
    """
    Calcula a altura manométrica da bomba em função da vazão.
    
    H(Q) = H0 - k * Q²
    """
    return H0 - k * Q**2


def eficiencia(Q, eta_max, Q_opt):
    """
    Calcula a eficiência da bomba em função da vazão.
    
    eta(Q) = eta_max * [1 - ((Q - Q_opt)/Q_opt)²]
    """
    eta = eta_max * (1 - ((Q - Q_opt) / Q_opt)**2)
    return np.clip(eta, 0, 1)  # Garante que a eficiência fique entre 0 e 100%


def potencia_hidraulica(Q_lps, H, rho=1000, g=9.81):
    """
    Calcula a potência hidráulica da bomba.
    
    P = ρ * g * Q * H
    """
    Q_m3s = Q_lps / 1000  # Converte L/s para m³/s
    return rho * g * Q_m3s * H  # Em Watts