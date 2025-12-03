# Avaliação Institucional – Plataforma de Análise

Projeto desenvolvido para o Hackathon 2025

## Resumo do Projeto

Este repositório contém a plataforma desenvolvida para análise de dados de avaliações institucionais. O sistema oferece visualizações, filtros por período, métricas consolidadas e comparação entre anos quando aplicável. A aplicação foi construída em Python com o framework Streamlit.

Acesse o projeto:
[https://avaliacaoinstitucionalmath.streamlit.app](https://avaliacaoinstitucionalmath.streamlit.app)

Observação: o site utiliza hospedagem gratuita do Streamlit. Caso esteja offline devido à inatividade, entre em contato pelo número informado no Guia do Avaliador.

## Arquitetura do Projeto

O projeto foi estruturado seguindo princípios S.O.L.I.D e inspirado no padrão MVC, com clara separação de responsabilidades:

### data/

Contém dados brutos (Raw) e processados (Processed), além da lógica de pré-processamento documentada.

### services/

Classes responsáveis pelos cálculos, métricas e regras de negócio.

### view/

Componentes de interface utilizados pelo Streamlit.

### Data Loader

Classe principal responsável por carregar os dados com segurança.

### app.py

Arquivo que orquestra toda a execução da aplicação.

## Execução Local

Para rodar o projeto em sua máquina:

Instale as dependências:

```bash
pip install -r requirements.txt
```

Execute a aplicação:

```bash
streamlit run app.py
```

## Observações Sobre Atualização de Dados

Foi considerada uma solução intermediária com uma página para upload de arquivos Excel, permitindo atualização automática dos dados. Essa abordagem não foi totalmente implementada por não ser ideal para escalabilidade, mas o conceito foi documentado.

## Documento Necessário para Avaliação

Para entender completamente o funcionamento, decisões de arquitetura, fluxograma do projeto e instruções detalhadas, o avaliador deve acessar o arquivo **"Guia do Avaliador.pdf"** incluído neste repositório.
