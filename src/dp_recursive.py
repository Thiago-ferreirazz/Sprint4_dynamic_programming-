import sys
from typing import List, Tuple, Dict
from src.utils import ModelParameters, calculate_immediate_cost

sys.setrecursionlimit(2000)


def solve_recursive_wrapper(params: ModelParameters) -> Tuple[float, List[List[int]]]:
    """Função principal para inicializar e executar a solução recursiva."""
    T = params.horizonte_T
    S_max = params.capacidade_S_max
    memo_cost: Dict[Tuple[int, int], float] = {}
    policy = [[0 for _ in range(S_max + 1)] for _ in range(T + 1)]

    def find_min_cost(t: int, s_t: int) -> float:
        """Calcula o custo mínimo C_t(s_t) com recursão e memoização (Top-Down)."""
        if t > T:
            return 0
        if (t, s_t) in memo_cost:
            return memo_cost[(t, s_t)]

        d_t = params.demandas_d_t[t - 1]
        min_total_cost = float('inf')
        best_x_t = 0
        max_decision = S_max - s_t

        for x_t in range(max_decision + 1):
            immediate_cost, s_t_plus_1 = calculate_immediate_cost(s_t, x_t, d_t, params.costs, S_max)
            future_cost = find_min_cost(t + 1, s_t_plus_1)
            total_cost = immediate_cost + future_cost

            if total_cost < min_total_cost:
                min_total_cost = total_cost
                best_x_t = x_t

        memo_cost[(t, s_t)] = min_total_cost
        policy[t][s_t] = best_x_t
        return min_total_cost

    min_cost = find_min_cost(1, params.estoque_inicial_s1)
    return min_cost, policy