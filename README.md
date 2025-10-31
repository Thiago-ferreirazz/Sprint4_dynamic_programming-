# Otimização de Estoque com Programação Dinâmica

### Integrantes do Grupo
- Gabriel Gouvea - 555528
- Leonardo Correa de Mello - 555573
- Miguel Kapicius Caires - 556198
- Pedro Visconti Guidotte - 556630
- Thiago Ferreira Oliveira - 555608

## 📄 Sumário

- [Descrição do Problema](#-descrição-do-problema)
- [Formulação com Programação Dinâmica](#-formulação-com-programação-dinâmica)
- [Estrutura do Projeto](#-estrutura-do-projeto)
- [Como Executar](#-como-executar)
- [Análise dos Algoritmos Implementados](#-análise-dos-algoritmos-implementados)
- [Exemplo de Saída](#-exemplo-de-saída)
- [Conclusão](#-conclusão)

## 📝 Descrição do Problema

Em unidades de diagnóstico, o controle de insumos (como reagentes e descartáveis) é um desafio. A falta de registros precisos sobre o consumo diário dificulta a previsão de demanda e a reposição de estoque, levando a dois problemas principais:
1. **Falta de Insumos (Stockout):** Interrompe as operações e pode impactar o atendimento.
2. **Excesso de Estoque:** Gera custos de armazenamento e risco de desperdício por vencimento ou obsolescência.

Este projeto modela o problema como um processo de decisão sequencial e aplica a Programação Dinâmica para encontrar a política de pedidos que equilibra esses custos, garantindo a maior eficiência operacional possível.

## 🧠 Formulação com Programação Dinâmica

Para resolver este problema com PD, definimos os seguintes componentes, baseados na equação de Bellman:

- **Períodos (`t`):** Etapas de tempo discretas (ex: dias) no horizonte de planejamento, de `t=1` a `T`.
- **Estados (`s_t`):** O nível de estoque disponível no **início** do período `t`.
- **Decisões (`x_t`):** A quantidade de insumos a ser pedida no início do período `t`. A decisão é restrita pela capacidade máxima de armazenamento (`S_max`).
- **Função de Transição de Estado:** Define como o estoque evolui. O estoque no início do próximo período (`s_{t+1}`) é o que resta do estoque atual mais o que foi pedido, após atender à demanda (`d_t`).

$$ s_{t+1} = \max(0, s_t + x_t - d_t) $$

O estoque também é limitado pela capacidade máxima `S_max`.

- **Função Objetivo (Custo):** O objetivo é minimizar o custo total, que é a soma dos custos em cada período. O custo de um período é composto por:
    1. **Custo Fixo de Pedido (`K_fixo`):** Incorrido se um pedido (`x_t > 0`) é feito.
    2. **Custo Variável de Pedido (`c_p`):** Custo por unidade pedida.
    3. **Custo de Manutenção (`c_h`):** Custo por unidade mantida em estoque ao final do período.
    4. **Custo de Falta (`c_s`):** Penalidade por unidade de demanda não atendida.

A equação de Bellman para o problema é:

$$ C_t(s_t) = \min_{0 \le x_t \le S_{max} - s_t} \left\{ \text{CustoImediato}(s_t, x_t) + C_{t+1}(s_{t+1}) \right\} $$

Onde `CustoImediato` inclui os quatro componentes de custo listados acima, e `C_{t+1}(s_{t+1})` é o custo futuro ótimo, que já foi (ou será) calculado.

## 📂 Estrutura do Projeto

O código está organizado de forma modular para separar responsabilidades, facilitar a manutenção e a clareza.

```
.
├── __pycache__
└── src
    ├── config.json
    ├── dp_iterative.py
    ├── dp_recursive.py
    └── main.py
```

**Arquivos do Projeto:**

- `config.json`: Arquivo de configuração em formato JSON. Centraliza todos os parâmetros do modelo (horizonte, custos, demandas, capacidade), permitindo testar diferentes cenários sem alterar o código.

- `dp_iterative.py`: Implementa a solução de Programação Dinâmica usando a abordagem **iterativa (Bottom-Up / Tabulação)**.
    - Resolve o problema de trás para frente no tempo (`t=T, T-1, ..., 1`).
    - Usa uma tabela (`dp_table`) para armazenar os custos ótimos já calculados para os períodos futuros, garantindo que cada subproblema seja resolvido apenas uma vez.

- `dp_recursive.py`: Implementa a solução usando a abordagem **recursiva (Top-Down / Memoização)**.
    - Resolve o problema a partir do estado inicial (`t=1`) e usa chamadas recursivas para explorar os estados futuros.
    - Utiliza um dicionário (`memo_cost`) como cache para armazenar os resultados dos subproblemas já visitados, evitando recálculos e o problema de "explosão" de chamadas recursivas.

- `main.py`: Ponto de entrada (entry point) da aplicação. Suas responsabilidades são:
    1. Carregar e validar os parâmetros do `config.json`.
    2. Executar ambas as abordagens (iterativa e recursiva).
    3. Realizar a **validação cruzada**, comparando os custos totais obtidos para garantir que ambas as implementações estão corretas e produzem o mesmo resultado.
    4. Imprimir a política de pedidos ótima de forma clara e legível, mostrando a trajetória de estoque e decisões ao longo do tempo.

## 🚀 Como Executar

### Pré-requisitos

- Python 3.7 ou superior. Nenhuma biblioteca externa é necessária.

### Passos

1. Navegue até o diretório do projeto:
```bash
cd src
```

2. Execute o script principal:
```bash
python main.py
```

O script executará ambas as implementações, comparará os resultados e imprimirá a política ótima e os custos associados no console.

## 📊 Análise dos Algoritmos Implementados

O projeto implementa as duas abordagens clássicas de Programação Dinâmica para demonstrar sua equivalência:

1. **Abordagem Iterativa (Bottom-Up):**
    - **Como funciona:** Preenche uma tabela de custos (`dp_table`) começando do último período (`T`) e avançando para o primeiro (`1`). Para calcular o custo ótimo no período `t`, ele consulta os valores já calculados para o período `t+1`.
    - **Vantagens:** Geralmente mais eficiente em termos de velocidade, pois evita o overhead de chamadas recursivas. É ideal quando o espaço de estados é denso (a maioria dos estados será visitada).

2. **Abordagem Recursiva com Memoização (Top-Down):**
    - **Como funciona:** Começa do problema original (`t=1`, `estoque_inicial`) e o divide em subproblemas menores através de chamadas de função recursivas. Um cache (memoização) armazena a solução de cada subproblema `(t, s_t)` para que não precise ser recalculado.
    - **Vantagens:** O código tende a ser mais intuitivo e mais próximo da formulação matemática da equação de Bellman. Pode ser mais eficiente se o espaço de estados for esparso, pois explora apenas os estados alcançáveis a partir da condição inicial.

A **validação cruzada** em `main.py` confirma que `abs(cost_iterative - cost_recursive) < 1e-6`, provando que ambas as implementações são funcionalmente idênticas e corretas.

## 📈 Exemplo de Saída

A execução do script produzirá uma saída detalhada, incluindo:

1. O custo total mínimo calculado por cada método.
2. A confirmação de que os custos são idênticos.
3. A política de pedidos ótima, detalhada período a período:

```
--- Política de Pedidos Ótima (Iterativa) ---
Período (t)  Estoque Inicial (s_t)   Demanda (d_t)   Decisão (x_t)   Estoque Final (s_t+1)
--------------------------------------------------------------------------------
1            20                      25              5               0
2            0                       30              45              15
3            15                      15              0               0
4            0                       20              20              0

Custo total calculado na trajetória: 290.00
```

Esta tabela fornece um guia de ação claro para o gestor de estoque. Por exemplo, no período 1, começando com 20 unidades, a decisão ótima é pedir mais 5 unidades.

## ✅ Conclusão

Este projeto demonstra com sucesso como a Programação Dinâmica pode ser aplicada para resolver um problema real de otimização de estoque. As duas implementações (iterativa e recursiva com memoização) foram validadas e produzem uma política de pedidos ótima e acionável. A estrutura modular e configurável do código o torna uma ferramenta flexível e robusta para análise e tomada de decisão.
