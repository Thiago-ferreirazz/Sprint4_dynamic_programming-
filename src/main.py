# src/main.py

import json

from pathlib import Path

from typing import Optional

from dp_recursive import solve_recursive_wrapper

from dp_iterative import solve_iterative

from utils import ModelParameters, CostParameters


def load_config(config_file: Path) -> Optional[ModelParameters]:
    """Carrega os parâmetros do arquivo JSON usando dataclasses."""

    if not config_file.exists():
        print(f"Erro: Arquivo de configuração '{config_file}' não encontrado.")

        return None

    try:

        with open(config_file, 'r') as f:

            data = json.load(f)

        # Validações

        if len(data["demandas_d_t"]) != data["horizonte_T"]:
            raise ValueError("O número de demandas não corresponde ao horizonte T.")

        if data["estoque_inicial_s1"] > data["capacidade_S_max"]:
            raise ValueError("Estoque inicial maior que capacidade máxima.")

        if any(d < 0 for d in data["demandas_d_t"]):
            raise ValueError("Demandas não podem ser negativas.")

        # Converte dicionários para dataclasses

        cost_params = CostParameters(**data["custos"])

        params = ModelParameters(

            horizonte_T=data["horizonte_T"],

            capacidade_S_max=data["capacidade_S_max"],

            estoque_inicial_s1=data["estoque_inicial_s1"],

            demandas_d_t=data["demandas_d_t"],

            costs=cost_params

        )

        return params

    except (json.JSONDecodeError, KeyError, ValueError) as e:

        print(f"Erro ao carregar ou validar a configuração: {e}")

        return None


def print_optimal_policy(

        policy: list,

        dp_table: list,

        params: ModelParameters,

        method_name: str

):
    """Imprime a trajetória ótima usando a tabela DP para mostrar os custos por período."""

    print(f"\n--- Política de Pedidos Ótima ({method_name}) ---")

    header = (

        f"{'Período (t)':<12} {'Estoque Inicial (s_t)':<23} {'Demanda (d_t)':<15} "

        f"{'Decisão (x_t)':<15} {'Custo do Período':<20} {'Estoque Final (s_t+1)':<23}"

    )

    print(header)

    print("-" * 110)

    s_t = params.estoque_inicial_s1

    total_cost_from_path = 0

    for t in range(1, params.horizonte_T + 1):
        d_t = params.demandas_d_t[t - 1]

        x_t = policy[t][s_t]

        estoque_disponivel = s_t + x_t

        s_t_plus_1 = min(params.capacidade_S_max, max(0, estoque_disponivel - d_t))

        # Custo do período é a diferença do custo total entre o estado atual e o próximo

        # C_t(s_t) = c(s_t, x_t) + C_{t+1}(s_{t+1})

        # => c(s_t, x_t) = C_t(s_t) - C_{t+1}(s_{t+1})

        cost_of_period = dp_table[t][s_t] - dp_table[t + 1][s_t_plus_1]

        total_cost_from_path += cost_of_period

        row = (

            f"{t:<12} {s_t:<23} {d_t:<15} {x_t:<15} "

            f"{cost_of_period:<20.2f} {s_t_plus_1:<23}"

        )

        print(row)

        s_t = s_t_plus_1

    print(f"\nCusto total calculado na trajetória: {total_cost_from_path:.2f}")


def main():
    """Função principal para executar e comparar as soluções."""

    # Caminho robusto para o arquivo de configuração

    CONFIG_FILE = Path(__file__).parent / "config.json"

    params = load_config(CONFIG_FILE)

    if not params:
        return

    # Executa Abordagem Iterativa (Bottom-Up)

    print("Executando Abordagem Iterativa (Bottom-Up)...")

    dp_table, iterative_policy = solve_iterative(params)

    cost_iterative = dp_table[1][params.estoque_inicial_s1]

    print(f"Custo Total Mínimo (Iterativo): {cost_iterative:.2f}")

    # Executa Abordagem Recursiva (Top-Down)

    print("\nExecutando Abordagem Recursiva (Top-Down)...")

    cost_recursive, recursive_policy = solve_recursive_wrapper(params)

    print(f"Custo Total Mínimo (Recursivo): {cost_recursive:.2f}")

    # Validação Cruzada

    print("\n--- Validação Cruzada ---")

    if abs(cost_iterative - cost_recursive) < 1e-6:

        print("SUCESSO: Ambas as abordagens produziram o mesmo custo total.")

    else:

        print(f"FALHA: Custos diferentes! Iterativo: {cost_iterative:.2f}, Recursivo: {cost_recursive:.2f}")

    print_optimal_policy(iterative_policy, dp_table, params, "Iterativa")

    print_optimal_policy(recursive_policy, dp_table, params, "Recursiva (custos via tabela iterativa)")


if __name__ == "__main__":
    main()

