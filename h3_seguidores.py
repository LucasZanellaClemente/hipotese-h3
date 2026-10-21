"""
H3 - Quanto mais seguidores locais o grupo tem no país do show, maior o lucro operacional.

H0: não existe correlação positiva entre seguidores locais e lucro (rho <= 0)
H1: existe correlação positiva (rho > 0)
alfa = 0,05 | teste unicaudal

Metodologia: a hipótese foi escolhida olhando metade da base (exploração).
O teste formal é feito na OUTRA metade (confirmação), que não foi usada na escolha.

Bibliotecas: pip install pandas scipy matplotlib openpyxl
"""
import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

ALFA = 0.05
SEED = 42
X = "seguidores_locais_milhoes"
Y = "lucro_operacional_usd"

# ===== 1. Carregar e limpar =====
shows = pd.read_excel("kpop_shows.xlsx")
df = shows[shows["status_show"] == "realizado"].copy()
print(f"Shows realizados: {len(df)} (removidos {len(shows) - len(df)} cancelados)")

# ===== 2. Dividir exploração / confirmação =====
explor = df.sample(frac=0.5, random_state=SEED)
conf = df.drop(explor.index)

dados = conf[[X, Y, "tipo_local"]].dropna()
print(f"Metade de confirmação: {len(conf)} shows | "
      f"usados no teste: {len(dados)} (removidos {len(conf) - len(dados)} sem seguidores)\n")

# ===== 3. Estatística descritiva =====
print("--- Estatística descritiva ---")
print(dados[[X, Y]].describe().round(2).to_string())

# ===== 4. Normalidade: Shapiro-Wilk =====
print("\n--- Shapiro-Wilk (alfa = 0,05) ---")
normais = True
for col in [X, Y]:
    W, p = stats.shapiro(dados[col])
    if p <= ALFA:
        normais = False
    print(f"{col}: W={W:.4f}, p={p:.4g} -> {'normal' if p > ALFA else 'NÃO normal'}")

# ===== 5. Teste de correlação =====
print("\n--- Correlação (unicaudal, H1: rho > 0) ---")
r, p_pearson = stats.pearsonr(dados[X], dados[Y], alternative="greater")
rho, p_spearman = stats.spearmanr(dados[X], dados[Y], alternative="greater")
print(f"Pearson:  r   = {r:.3f}, p = {p_pearson:.4g}")
print(f"Spearman: rho = {rho:.3f}, p = {p_spearman:.4g}")

if normais:
    print("As duas variáveis são normais -> teste escolhido: PEARSON")
    coef, p_final = r, p_pearson
else:
    print("Pelo menos uma variável não é normal -> teste escolhido: SPEARMAN")
    coef, p_final = rho, p_spearman

# ===== 6. Intervalo de confiança de 95% (bootstrap) =====
rng = np.random.default_rng(SEED)
boot = []
for _ in range(2000):
    amostra = dados.sample(len(dados), replace=True, random_state=rng.integers(1e9))
    boot.append(stats.spearmanr(amostra[X], amostra[Y])[0])
ic_inf, ic_sup = np.percentile(boot, [2.5, 97.5])
print(f"IC 95% do rho (bootstrap, 2000 reamostragens): [{ic_inf:.3f}; {ic_sup:.3f}]")

# ===== 7. Conclusão =====
forca = "fraca" if abs(coef) < 0.3 else "moderada" if abs(coef) < 0.7 else "forte"
print("\n--- Conclusão ---")
if p_final < ALFA:
    print(f"p = {p_final:.4g} < 0,05 -> REJEITA H0")
else:
    print(f"p = {p_final:.4g} >= 0,05 -> NÃO rejeita H0")
print(f"Correlação {forca} e positiva (rho = {coef:.3f}).")
print(f"Tamanho de efeito: rho² = {coef**2:.3f} -> os seguidores explicam "
      f"~{coef**2*100:.0f}% da variação (em postos) do lucro.")

# ===== 8. Robustez: variável de confusão (tamanho do local) =====
# Pergunta: os seguidores só parecem importar porque bandas populares tocam em locais maiores?
print("\n--- Robustez: a correlação se mantém dentro de cada tipo de local? ---")
for tipo, d in dados.groupby("tipo_local"):
    r_t, p_t = stats.spearmanr(d[X], d[Y], alternative="greater")
    print(f"{tipo:8s} n={len(d):4d}  rho={r_t:.3f}, p={p_t:.4g}")

# ===== 9. Gráficos =====
fig, ax = plt.subplots(1, 3, figsize=(15, 4.5))

# 9a. dispersão por tipo de local
for tipo, d in dados.groupby("tipo_local"):
    ax[0].scatter(d[X], d[Y], alpha=0.5, s=14, label=tipo)
ax[0].set_xlabel("Seguidores locais (milhões)")
ax[0].set_ylabel("Lucro operacional (USD)")
ax[0].set_title(f"Seguidores x Lucro (Spearman rho = {coef:.2f})")
ax[0].legend()
ax[0].grid(alpha=0.3)

# 9b. histograma do lucro (mostra a assimetria que viola a normalidade)
ax[1].hist(dados[Y], bins=40, color="gray", edgecolor="white")
ax[1].set_title("Distribuição do lucro (não normal)")
ax[1].set_xlabel("Lucro operacional (USD)")

# 9c. QQ-plot do lucro
stats.probplot(dados[Y], dist="norm", plot=ax[2])
ax[2].set_title("QQ-plot do lucro")

plt.tight_layout()
plt.show()
