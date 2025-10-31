from dataclasses import dataclass
from typing import List, Dict


# Estrutura de dados para os custos, para clareza e type hints
@dataclass
class CostParameters:
    K_fixo: float
    c_p: float
    c_h: float
    c_s: float


# Estrutura principal para todos os parâmetros do problema
@dataclass
class ModelParameters:
    horizonte_T: int
    capacidade_S_max: int
    estoque_inicial_s1: int
    costs: CostParameters
    demandas_d_t: List[int]


def calculate_immediate_cost(
        s_t: int,
        x_t: int,
        d_t: int,
        costs: CostParameters,
        S_max: int
) -> tuple[float, int]:
    """
    Calcula o custo imediato para um período t e o estado do próximo período.

    Retorna:
        - Custo imediato total (float).
        - Nível de estoque no próximo período s_{t+1} (int).
    """
    # Custo do pedido
    cost_pedido = costs.K_fixo + costs.c_p * x_t if x_t > 0 else 0.0

    # Estoque disponível e cálculo de falta
    estoque_disponivel = s_t + x_t
    falta = max(0, d_t - estoque_disponivel)
    cost_falta = costs.c_s * falta

    # Transição de estado e custo de manutenção
    s_t_plus_1 = max(0, estoque_disponivel - d_t)
    s_t_plus_1 = min(s_t_plus_1, S_max)  # Garante capacidade máxima
    cost_manutencao = costs.c_h * s_t_plus_1

    immediate_cost = cost_pedido + cost_falta + cost_manutencao
    return immediate_cost, s_t_plus_1