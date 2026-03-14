# Cesta_Solidaria

## 1. Objetivo do Projeto 

O projeto **Cesta Solidária** tem como objetivo fomentar um sistema de controle e busca de informações e dados sobre a distribuição de cestas básicas pelo órgão público, destinado a famílias em situação de vulnerabilidade, residentes da região onde o órgão atua. 

O Cesta Solidária surge para consolidar informações, permitir a interação de diferentes âmbitos da máquina pública, receber constantes atualizações sobre a situação socioeconômica das famílias cadastradas e definir parâmetros de prioridade de atendimento emergencial, afim de padronizar fluxos de trabalho, reduzir perdas de estoque e aumentar a eficiência de atendimento à população civil.

## 2. Principais Atores do Projeto

1. **Família** - Entidade alvo do projeto, representada pelos dependentes de cada pessoa que se beneficia da distribuição das cestas solidárias, afim de combater a insegurança alimentar e garentindo uma integridade no núcleo familiar;
2. **beneficiado** - Pessoa responsável pelo núcleo familiar, que irá solicitar e receber o auxílio, considerando a sua condição socioeconômica;
3. **Unidades de Tratamento** - Coordenação geral do programa, administração e burocracia do projeto. Contempla as diversas ferramentasdo município como armazéns e almoxarifados, cadastro e administração de agentes sociais, logística e controle de tráfego de frota de veículos da prefeitura e de produtos, além de receber as cestas doadas de empresas Fornecedoras, conforme exigências de portaria vigente.
4. **Agente** - Responsável pelo registro de beneficiados e famílias no sistema, bem como o controle dos recursos disponíveis para doação das cestas;
5. **Fornecedores** - Instituições privadas ou Organizações responsáveis pelo fornecimento dos recursos necessários para as cestas.

## 3. Tecnologias Utilizadas
O sistema **Cesta Solidária** tem como objetivo a implementação dos conceitos obtidos ao decorrer da disciplina de **Banco de Dados**, ministrada pelo professor Rafael Will, como componente curricular da graduação em Engenharia de Software da Universidade Federal do Cariri (UFCA). 

O Sistema Gerenciador de Banco de Dados utilizado é o MySQL, que utiliza a Structured Query Language (SQL) como linguagem para estruturação e manipulação dos dados que são inseridos, transferidos e encaminhados dentro da interface, incluindo criação de tabelas, chaves primárias, chaves estrangeiras e restrições de integridade, além da normalização da estrutura dos dados. Essa estruturração é baseada em modelos previamente construidos e validados, afim de garantir a sustentação e prevenção de inconsistências.

A aplicação utiliza o Python como principal linguagem de programação e interface, no qual o código é estruturado baseando-se na modelagem DDD (Domain-Driven-Design), que se caracteriza na divisão de classes dentro do projeto, com foco uma linguagem ubíqua, baseando-se em um modelo de negócio.

## Estruturação dos Arquivos

```

cesta_solidaria
|
├── source/
|   ├── cesta_solidaria_bd/           
|   |   ├── database/
|   |   |   ├── __init__.py
|   |   |   ├── database.py
|   |   |   └── tabelas.py
|   |   |
|   |   ├── modules/
|   |   |   ├── __init__.py
|   |   |   ├── agente.py
|   |   |   ├── atendimento.py
|   |   |   ├── entrega.py
|   |   |   └── familia.py
|   |   ├── repositories/
|   |   |   ├── __init__.py
|   |   |   ├── repository_agente.py
|   |   |   ├── repository_atendimento.py
|   |   |   ├── repository_beneficiado.py
|   |   |   ├── repository_deficiencia.py
|   |   |   ├── repository_entrega.py
|   |   |   └── repository_familia.py
|   |   ├── __init__.py
|   |   ├── config_database.py
|   |   └── main.py
├── README.md  #Este arquivo
└── requirements.txt

```


