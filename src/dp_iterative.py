from typing import List, Tuple
from utils import ModelParameters, calculate_immediate_cost


def solve_iterative(params: ModelParameters) -> Tuple[List[List[float]], List[List[int]]]:
    """Calcula a política ótima com iteração e tabulação (Bottom-Up)."""
    T = params.horizonte_T
    S_max = params.capacidade_S_max
    # Tabela de Custo Mínimo (dp): dp[t][s] armazena o C_t(s)
    dp = [[0.0 for _ in range(S_max + 1)] for _ in range(T + 2)]
    # Tabela de Política Ótima: policy[t][s] armazena o x_t ótimo
    policy = [[0 for _ in range(S_max + 1)] for _ in range(T + 1)]

    # Itera de trás para frente, de t=T até t=1
    for t in range(T, 0, -1):
        d_t = params.demandas_d_t[t - 1]

        for s_t in range(S_max + 1):
            min_total_cost = float('inf')
            best_x_t = 0
            # Itera sobre todas as decisões x_t possíveis
            max_decision = S_max - s_t
            for x_t in range(max_decision + 1):
                # Usa a função centralizada para calcular custos e próximo estado
                immediate_cost, s_t_plus_1 = calculate_immediate_cost(s_t, x_t, d_t, params.costs, S_max)
                future_cost = dp[t + 1][s_t_plus_1]
                total_cost = immediate_cost + future_cost

                if total_cost < min_total_cost:
                    min_total_cost = total_cost
                    best_x_t = x_t
            # Armazena o resultado na tabela
            dp[t][s_t] = min_total_cost
            policy[t][s_t] = best_x_t

    return dp, policy
