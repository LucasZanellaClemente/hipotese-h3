# Teste de Hipótese: Seguidores Locais x Lucro em Turnês de K-pop

Trabalho de Data Science (FIAP) com dados simulados de 1.902 shows de turnês de K-pop.

## Hipótese (H3)

Quanto mais seguidores locais o grupo tem no país do show, maior o lucro operacional.

- **H₀:** não existe correlação positiva entre seguidores locais e lucro (ρ ≤ 0)
- **H₁:** existe correlação positiva (ρ > 0)
- **α = 0,05**, teste unicaudal

## Metodologia

1. Remoção dos 24 shows cancelados (restam 1.878).
2. Divisão aleatória da base em duas metades (seed = 42): uma para escolher a hipótese (exploração) e outra para testá-la (confirmação, 903 shows com seguidores preenchidos).
3. Teste de normalidade Shapiro-Wilk, com histograma e QQ-plot.
4. Correlação de Spearman (as variáveis não são normais).
5. Intervalo de confiança de 95% por bootstrap (2.000 reamostragens).
6. Teste de robustez: a correlação repetida dentro de cada tipo de local (teatro, arena, estádio).

## Resultados

| Etapa | Resultado |
|---|---|
| Shapiro-Wilk (seguidores) | W = 0,9715, p < 0,001 → não normal |
| Shapiro-Wilk (lucro) | W = 0,8392, p < 0,001 → não normal |
| Spearman | ρ = 0,633, p < 0,001 |
| IC 95% (bootstrap) | [0,589; 0,672] |
| Tamanho de efeito | ρ² = 0,40 |

| Tipo de local | n | ρ | p |
|---|---|---|---|
| Arena | 616 | 0,616 | < 0,001 |
| Estádio | 101 | 0,680 | < 0,001 |
| Teatro | 186 | 0,322 | < 0,001 |

## Conclusão

H₀ foi rejeitada. Há correlação positiva e moderada entre seguidores locais e lucro operacional, que explica cerca de 40% da sua variação e se mantém dentro de cada tipo de local.

**Limitações:** correlação não implica causalidade, e os dados são simulados.

## Como rodar

```bash
pip install pandas scipy matplotlib openpyxl
python h3_seguidores.py
```

## Arquivos

- `h3_seguidores.py`: script do teste de hipótese
- `kpop_shows.xlsx`: base de dados
