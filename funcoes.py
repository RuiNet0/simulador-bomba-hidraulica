import numpy as np

def altura_mano(Q, H0, k):
    """
    Calcula a altura manométrica da bomba em função da vazão.
    
    H(Q) = H0 - k * Q²
    """
    return H0 - k * Q**2


def eficiencia(Q, eta_max, Q_opt, largura):
    """
    Calcula a eficiência da bomba com base em uma curva parabólica.
    
    - Q: array de vazões
    - eta_max: eficiência máxima (0.80, por exemplo)
    - Q_opt: vazão de eficiência máxima
    - largura: controle da largura da curva (padrão 0.5)

    Retorna array com a eficiência para cada Q.
    """
    eta = eta_max * np.exp(-((Q - Q_opt) / (Q_opt * largura))**2)
    return np.clip(eta, 0.01, eta_max)  # evita valores menores que 1%


def potencia_hidraulica(Q_lps, H, rho=1000, g=9.81):
    """
    Calcula a potência hidráulica da bomba.
    
    P = ρ * g * Q * H
    """
    Q_m3s = Q_lps / 1000  # Converte L/s para m³/s
    return rho * g * Q_m3s * H  # Em Watts

def potencia_bomba(P_hidraulica, eta):
    """
    Calcula a potência da bomba considerando a eficiência.
    """
    return P_hidraulica / eta  # Em Watts

def potencia_cv(P_watts):
    """
    Converte potência de Watts para cavalos-vapor (CV).
    """
    return P_watts / 735.5

def npsh_disponivel(hs, hfs, Pv, Patm):
    """
    Calcula o NPSHa disponível.
    NPSH = Patm - Pv + hs - hfs
    """
    return Patm - Pv + hs - hfs

def dados_bombas():
    return {
        "Schneider BCS-32": {
            "Q_npshr": [10, 15, 20, 25, 30],
            "NPSHr":   [2.0, 2.5, 3.0, 3.5, 4.0],
        },
        "Schneider BCS-50": {
            "Q_npshr": [10, 20, 30],
            "NPSHr":   [2.5, 3.2, 4.0],
        },
        "WEG BMC 32-160": {
            "Q_npshr": [10, 15, 20, 25],
            "NPSHr":   [2.8, 3.2, 3.5, 4.0],
        }
    }