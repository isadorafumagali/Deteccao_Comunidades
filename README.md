# Análise da Rede de Interação entre os Personagens de *Os Miseráveis*

Análise de comunidades em R. Analisa a rede entre os personagens de *Os Miseráveis*, disponível no pacote `igraph` como `lesmis`, e compara dois métodos de agrupamento espectral para identificar comunidades de personagens.

## Dados

A rede vem do conjunto `lesmis` do pacote `igraph`: **77 personagens** (vértices) e **254 arestas** após a conversão para rede não direcionada e sem peso. Uma aresta indica que dois personagens interagem na obra, independentemente da direção ou da intensidade da interação.

## Metodologia

1. **Preparação da rede**: a matriz de adjacência original é convertida em grafo, transformada em rede não direcionada (`collapse`) e binarizada (`A = 1` se há ligação, `0` caso contrário).
2. **Análise descritiva**: distribuição dos graus (histograma) e visualização da rede com o tamanho dos vértices proporcional ao grau, usando o layout de Fruchterman-Reingold (`set.seed(3)`). Jean Valjean é o personagem mais conectado (grau 36).
3. **Agrupamento em K = 5 comunidades**, número escolhido após comparar valores de K em aula e justificado pela narrativa: quatro grandes núcleos dramáticos (lei e redenção, miséria e fábrica, ganância e trapaça, revolução e romance) e um quinto formado por personagens centrais que transitam entre os grupos.
   - **Regularized Spectral Clustering** (`reg.SP`)
   - **Spherical Regularized Spectral Clustering** (`reg.SSP`)
4. **Comparação dos métodos**: tamanho das comunidades, estabilidade da classificação dos personagens entre os dois métodos e interpretação à luz da narrativa.

## Principais resultados

- O Spectral Clustering Regularizado gerou comunidades de tamanhos desiguais (46, 8, 9, 1 e 13 personagens); a versão esférica gerou grupos mais equilibrados (8, 23, 9, 24 e 13).
- Alguns agrupamentos são estáveis nos dois métodos, como o núcleo revolucionário (Enjolras, Combeferre, Courfeyrac, Bahorel, Bossuet, Joly, Grantaire, entre outros), além de Gavroche e Marius (mesma comunidade) e Thenardier.
- Personagens de grau alto e ligados a vários núcleos (Valjean, Javert, Fantine) mudam de comunidade conforme o método, o que é coerente com o papel de articulação (*hubs*) entre grupos.
- Conclusão: há correspondência parcial entre a estrutura de comunidades e os papéis narrativos; os dois métodos se complementam.

## Autora

Isadora Fumagali — [@isadorafumagali](https://github.com/isadorafumagali)
