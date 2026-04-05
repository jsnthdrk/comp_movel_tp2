# Computação Móvel - TP2: Solitaire

Este repositório contém a implementação do famoso jogo do [Solitário](https://en.wikipedia.org/wiki/Solitaire) desenvolvida em Python utilizando a *framework* **Flet**. O projeto começa já bastante avançado, de um jogo funcional, para um programa mais complexo, desenhado com funcionalidades extra com o intuito de melhorar de forma significativa a experiência do jogo.

---

## Requisitos e Instalação

Antes de executar o programa, certifique-se de que cumpre os seguintes requisitos:

1. **Python:** Versão 3.10 ou superior.
2. **Ambiente Virtual (Recomendado):**
    Para manter as dependências organizadas, crie e ative um ambiente virtual:

    ```bash
    python -m venv .venv
    # Windows:
    .venv\Scripts\activate
    # macOS/Linux:
    source .venv/bin/activate
    ```

3. **Instalação do Flet:**
    Instale a biblioteca Flet (com todas as dependências) via terminal:

    ```bash
    pip install "flet[all]"
    ```

    *Para verificar a instalação:*

    ```bash
    flet --version
    ```

    *Caso precise de atualizar uma versão antiga:*

    ```bash
    pip install "flet[all]" --upgrade
    ```

> **Documentação Oficial:** Se tiver dúvidas durante a instalação, consulte [Installation - Flet](https://docs.flet.dev/getting-started/installation/).

---

## Objetivos do Projeto

### Objetivo 1: Base

Os passos do [tutorial](https://docs.flet.dev/tutorials/solitaire) foram seguidos e implementados através do código-fonte final presente [neste link](https://github.com/flet-dev/flet/blob/main/sdk/python/examples/tutorials/solitaire/solitaire-final-part1).

>Nota Importante: O tutorial do primeiro link encontra-se desatualizado face à versão mais recente do Flet (no primeiro commit/merge, o meu próprio Flet encontrava-se desatualizado face à versão 0.82.2, que é a mais recente desde do cumprimento do objetivo a 19/03/2026). Os autores do tutorial, no entanto, disponibilizaram o código-fonte mais atualizado face às versões que têm sido publicadas.

### Objetivo 2: Funcionalidades Extra

Foram implementadas (se já não existissem no tutorial) as seguintes funcionalidades:

* Reiniciar o jogo
* Desfazer a(s) jogada(s)
* Salvar e carregar o estado do jogo
* Escolher a imagem traseira das cartas, entre 4 opções diferentes
* Sistema de pontuação com cronómetro visível durante toda a partida.

### Objetivo 3: Duas funcionalidades à sua escolha

#### 1. Sistema de Dicas Inteligente (Smart Hint)

**Motivo de Inclusão:** A inclusão de um sistema de dicas surge da necessidade de mitigar a frustração do jogador em momentos de bloqueio. O Solitário é um jogo de paciência, mas a incapacidade de detetar uma jogada válida pode levar ao abandono da partida sob a falsa premissa de que o jogo atual é impossível. Do ponto de vista técnico, esta funcionalidade foi escolhida por representar um excelente desafio algorítmico, exigindo a análise em tempo real do estado de todas as pilhas de cartas (*Tableau*, *Waste*, *Foundations*), analisando o seu naipe, cor e valor (*rank*).

**Descrição Detalhada:** Ao invés de um sistema rudimentar que sugere a primeira jogada legal disponível (o que poderia levar a *loops* infinitos ou sugerir jogadas ineficazes, como mover cartas entre colunas sem revelar cartas novas), este sistema possui uma heurística baseada em prioridades. O algoritmo avalia as opções na seguinte ordem: primeiro, verifica se é possível mover cartas para as fundações (o objetivo principal); em segundo, procura movimentos no *Tableau* que revelem cartas viradas para baixo (procurando sempre a carta base da pilha); em terceiro, tenta mover cartas do *Waste* para o *Tableau*; e, por fim, se não houver jogadas ativamente úteis na mesa, sugere a compra de uma nova carta. Para a interface, foi utilizada programação assíncrona (`asyncio`), permitindo que a carta sugerida seja destacada temporariamente com uma borda amarela de forma fluida, sem bloquear a *thread* principal da interface gráfica (UI).

#### 2. Manual de Regras

**Motivo de Inclusão:** A inclusão de um "livro" de regras prende-se com o facto de ser uma boa prática de usabilidade em qualquer aplicação de entretenimento. É fundamental ter um manual acessível para ajudar novos jogadores a compreender a mecânica ou para esclarecer dúvidas pontuais sobre movimentações e pontuações.

**Descrição Detalhada:** Foi incluído um botão com um ícone de livro que aciona uma função simples responsável por instanciar um *modal*. Este componente apresenta um texto detalhado (em inglês) que explica como o jogo é montado, como as cartas são distribuídas pelo *tableau*, as áreas de jogo, as regras de movimentação e como o sistema de pontuação funciona. O texto é renderizado de forma nativa utilizando *Markdown* para garantir uma formatação limpa e legível. Ao clicar no botão "Understood", o modal é encerrado e o utilizador regressa ao jogo.

#### 3. Contagem de Jogadas

**Motivo de Inclusão:** Trata-se de uma funcionalidade que, apesar de simples, introduz uma forte componente de retenção e desafio. Ao permitir que o jogador tente completar o jogo com o menor número de movimentos possível, e combinando esta métrica com o cronómetro existente, cultiva-se um ambiente competitivo e fomenta-se o pensamento estratégico.

**Descrição Detalhada:** A implementação desta funcionalidade baseou-se na adição de um contador numérico global ao estado do jogo, que é incrementado sempre que o jogador realiza uma ação válida e intencional. O código foi desenhado para intercetar eventos específicos de manipulação de cartas (arrastar e largar no *Tableau* ou nas *Foundations*, virar uma carta fechada, ou mover uma carta do *Stock* para o *Waste*). Além disso, o sistema está perfeitamente integrado com o histórico de jogadas, garantindo que, caso o jogador utilize a funcionalidade de "Desfazer" (*Undo*), o contador retrocede de forma sincronizada. O valor é atualizado na interface do utilizador em tempo real, lado a lado com a pontuação e o cronómetro, proporcionando *feedback* visual constante. A persistência dos dados foi também acautelada, sendo o número de jogadas guardado no ficheiro JSON aquando da ação de *Save/Load*, permitindo retomar a partida com as métricas exatas. Estas atualizações tiram partido da programação assíncrona para aliviar a carga no processamento visual da aplicação.

---

## Execução do programa

```bash
flet run main.py
```
