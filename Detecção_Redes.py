

import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from scipy.sparse.linalg import svds
from sklearn.cluster import KMeans



dados = nx.les_miserables_graph()


dados = nx.relabel_nodes(dados, {"Woman1": "Oldwoman1", "Woman2": "Oldwoman2"})


#rede sem direção e peso
un_lesmis = nx.Graph()
un_lesmis.add_nodes_from(dados.nodes)
un_lesmis.add_edges_from(dados.edges)  #descarta os pesos
print(un_lesmis)


nomes = list(un_lesmis.nodes)
A = nx.to_numpy_array(un_lesmis, nodelist=nomes)
A = np.where(A >= 1, 1, 0)


#grau dos vértices
Grau = pd.Series(dict(un_lesmis.degree()), name="Grau").loc[nomes]
print(Grau)

#histograma do grau
plt.figure()
plt.hist(Grau, density=True, color="lightblue", edgecolor="black")
plt.ylim(0, 0.1)
plt.title("Distribuição do Grau dos Vértices")
plt.xlabel("Grau (Número de Conexões)")
plt.ylabel("Frequência")
plt.figtext(0.5, 0.01, "Figura 1: Histograma do grau dos vértices.", ha="center")

#representação gráfica da rede
lay = nx.spring_layout(un_lesmis, seed=3)  # Fruchterman-Reingold


def plota_rede(cores, titulo, legenda, rotulos=True, tamanho_rotulo=5):
    """Equivalente ao plot() do igraph: vértices dimensionados pelo grau."""
    plt.figure(figsize=(10, 8))
    nx.draw_networkx_edges(un_lesmis, lay, edge_color="gray")
    nx.draw_networkx_nodes(
        un_lesmis, lay, nodelist=nomes,
        node_size=[g * 25 for g in Grau], node_color=cores,
        edgecolors="black", linewidths=0.5,
    )
    if rotulos:
        nx.draw_networkx_labels(un_lesmis, lay, font_size=tamanho_rotulo)
    plt.title(titulo)
    plt.figtext(0.5, 0.02, legenda, ha="center")
    plt.axis("off")


plota_rede(
    "lightblue",
    "Rede de Interação dos Personagens de Les Misérables",
    "Figura 2: Representação gráfica da rede com os vértices dimensionados pelo grau.",
)

#estatísticas descritivas do grau
print(Grau.describe())                       
print("Desvio padrão:", Grau.std(ddof=1))    
print("Grau máximo:", Grau.max())           
print(Grau.sort_values(ascending=False))     
print(Grau.sort_values(ascending=False).head(10))



#métodos de agrupamento espectral (equivalentes a randnet::reg.SP / reg.SSP)
def _autovetores_regularizados(A, K, tau=1.0):
    """K primeiros vetores singulares de A + tau * grau_médio / n."""
    n = A.shape[0]
    avg_d = A.sum(axis=0).mean()
    A_tau = A + tau * avg_d / n
    U, s, Vt = svds(A_tau.astype(float), k=K)
    return U[:, np.argsort(-s)]


def _kmeans(X, K, nstart=30, max_iter=100, seed=0):
    km = KMeans(n_clusters=K, n_init=nstart, max_iter=max_iter, random_state=seed)
    return km.fit_predict(X) + 1  # rótulos 1..K, como no R


def reg_SP(A, K, tau=1.0):
    """Spectral Clustering Regularizado."""
    U = _autovetores_regularizados(A, K, tau)
    return _kmeans(U, K)


def reg_SSP(A, K, tau=1.0):
    U = _autovetores_regularizados(A, K, tau)
    norma = np.linalg.norm(U, axis=1, keepdims=True)
    norma[norma == 0] = 1
    return _kmeans(U / norma, K)


PALETA = {1: "olivedrab", 2: "lightblue", 3: "red", 4: "gold", 5: "pink"}


#agrupamento dos vértices em cinco comunidades (K = 5)

# Spectral clustering regularizado
z_hat_SP = reg_SP(A, K=5)
col_SP = [PALETA[c] for c in z_hat_SP]
plota_rede(
    col_SP,
    "Spectral Clustering Regularizado",
    "Figura 3: Representação gráfica da rede com Spectral Clustering Regularizado.",
    rotulos=False,
)

#spectral clustering regularizado esférico
z_hat_SSP = reg_SSP(A, K=5)
col_SSP = [PALETA[c] for c in z_hat_SSP]
plota_rede(
    col_SSP,
    "Spectral Clustering Regularizado Esférico",
    "Figura 4: Representação gráfica da rede com Spectral Clustering Regularizado Esférico.",
    rotulos=True,
    tamanho_rotulo=4,
)

#comparação das comunidades
dados_comunidades = pd.DataFrame({
    "Personagem": nomes,
    "SP": z_hat_SP,
    "SSP": z_hat_SSP,
    "Grau": Grau.values,
})

print(dados_comunidades.sort_values("SP"))
print(dados_comunidades.sort_values("Grau", ascending=False))

print(pd.Series(z_hat_SP).value_counts().sort_index())    
print(pd.Series(z_hat_SSP).value_counts().sort_index())   

if __name__ == "__main__":
    plt.show()
