# Computação Móvel - TP2: Solitaire

Este repositório contém a implementação do famoso jogo do [Solitário](https://en.wikipedia.org/wiki/Solitaire) desenvolvida em Python utilizando a *framework* **Flet**. O projeto começa já bastante avançado, de um jogo funcional, para um programa mais complexo, desenhado com funcionalidades extra com o intuito de melhorar de forma significativa a experiência do jogo.

---

## Requisitos e Instalação

Antes de correr o programa, certifique-se de que cumpre os seguintes requisitos:

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

>Nota Importante: O tutorial do primeiro link encontra-se desatualizado face à versão mais recente do Flet (no primeire commit/merge, o meu próprio Flet encontrava-se desatualizado face à versão 0.82.2, que é a mais recente) desde do cumprimento do objetivo (19/03/2026). O(s) autor(es) do tutorial, no entanto disponibilizaram o código-fonte mais atualizado face às versões que têm sido publicadas. Ao longo do desenvolvimento do projeto, irão existir commits com a tag ``keeping-up``, que visa dar continuidade a este processo de manter o código atualizado para prevenir erros por funcionalidades, classes, métodos de classe e objetos de classe terem tornado-se obsoletos por parte da equipa do Flet.

### Objetivo 2: Funcionalidades Extra

Irão ser implementadas (se já não existirem vindo do tutorial) as seguintes funcionalidades:

* Reiniciar o jogo
* Desfazer a(s) jogada(s)
* Salvar e carregar o estado do jogo
* Escolher a imagem traseira das cartas, entre 4 opções diferentes
* Sistema de pontuação com cronómetro visível durante toda a partida.

### Objetivo 3: Duas funcionalidades à sua escolha

Em pensamento livre, irão ser adicionadas duas funcionalidades (por definir).

Guidelines do TP para este objetivo:

1. "Pode inspirar-se noutras aplicações semelhantes; ou nas funcionalidades dos TPs anteriores, mas com alguma inovação."

2. "As funcionalidades avançadas serão valorizadas, enquanto as muito simples (ou totalmente repetidas de outros TPs) serão penalizadas na avaliação atribuída a este objetivo."

3. "Se tiver dúvidas, consulte o docente."

4. "Certifique-se de que as funcionalidades escolhidas estão bem implementadas e não comprometem a usabilidade da aplicação."

5. "Elabore um ficheiro README.md (formato markdown) na raiz do projeto, onde apresente os motivos de inclusão das funcionalidades extra e uma descrição detalhada das mesmas (~20% da avaliação deste objetivo):"

    5.1. "Escreva cerca de 200 – 300 palavras por funcionalidade, em português (pt-PT)."

    5.2. "Inclua instruções de utilização, se necessário."

## Execução do programa

```bash
flet run main.py
```
