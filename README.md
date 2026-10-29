# FilaSmart

Sistema web de gerenciamento de filas virtuais desenvolvido como projeto acadêmico da Facens.

## Sobre o projeto

O **FilaSmart** tem como objetivo facilitar o gerenciamento de filas de atendimento, permitindo que clientes ingressem em filas virtuais e que os responsáveis pelos estabelecimentos organizem e acompanhem os atendimentos.

A plataforma oferece funcionalidades para cadastro e autenticação de usuários, visualização de serviços disponíveis, entrada em filas e acompanhamento da situação do atendimento.

Para os responsáveis, o sistema disponibiliza recursos para cadastrar e gerenciar serviços, chamar clientes e atualizar as etapas do atendimento.

## Funcionalidades

### Clientes
- Cadastro de usuários.
- Login e logout.
- Visualização dos serviços disponíveis.
- Entrada em filas virtuais.
- Consulta das filas em que o usuário está inscrito.
- Cancelamento da participação enquanto estiver aguardando atendimento.
- Acompanhamento da situação do atendimento.

### Responsáveis pelos serviços
- Acesso à área de gerenciamento.
- Criação de serviços.
- Ativação e desativação de serviços.
- Gerenciamento da fila de atendimento.
- Chamada de clientes.
- Atualização das etapas do atendimento.
- Conclusão dos atendimentos.

## Tecnologias utilizadas

- **Python:** linguagem de programação utilizada no backend.
- **Flask:** framework para desenvolvimento da aplicação web.
- **SQLite:** banco de dados para armazenamento das informações.
- **HTML:** estrutura das páginas.
- **CSS:** estilização e apresentação da interface.
- **Jinja2:** renderização dos templates HTML.
- **Werkzeug:** recursos utilizados pelo Flask, incluindo a proteção de senhas por hash.

## Como executar o projeto

### Pré-requisitos

- Python instalado.
- Pip disponível para instalar as dependências.

### 1. Clonar o repositório

```bash
git clone https://github.com/gustavoofreitas05/filasmart.git
```

Entre na pasta do projeto:

```bash
cd filasmart
```

> Se o repositório estiver com outro nome ou endereço, substitua a URL pelo endereço correto do projeto.

### 2. Instalar as dependências

```bash
pip install -r requirements.txt
```

### 3. Executar a aplicação

Execute:

```bash
python app.py
```

Se o comando `python` não funcionar no Windows, tente:

```bash
py app.py
```

### 4. Acessar o sistema

Abra o navegador e acesse:

```text
http://127.0.0.1:5000
```

A aplicação utiliza o banco de dados SQLite para armazenar as informações. Verifique se o arquivo do banco é criado ou inicializado corretamente conforme a configuração do projeto.

## Estrutura geral

O projeto está organizado em componentes responsáveis pelas seguintes áreas:

- `app.py`: rotas, regras de negócio e inicialização da aplicação.
- `templates/`: páginas HTML renderizadas pelo Flask.
- `static/`: arquivos estáticos, como folhas de estilo CSS.
- `requirements.txt`: dependências necessárias para executar o projeto.
- `filasmart.db`: banco de dados SQLite, quando criado durante a execução.

## Objetivos

- Reduzir a necessidade de espera presencial desorganizada.
- Facilitar o acompanhamento das filas de atendimento.
- Simplificar o gerenciamento dos serviços pelos responsáveis.
- Organizar as etapas do atendimento.
- Melhorar a experiência dos clientes e dos estabelecimentos.

## Melhorias futuras

Entre as possibilidades de evolução do projeto estão:

- Notificações automáticas para os clientes.
- Atualização das filas em tempo real.
- Aprimoramento do acompanhamento da posição na fila.
- Ampliação dos recursos de monitoramento e gerenciamento.

Essas melhorias dependem de implementação e validação adicionais.

## Equipe

- Bernard Motta Rosa — RA 248879
- Felipe Neris dos Santos — RA 248433
- Pedro Gustavo Freitas de Souza — RA 248979

## Projeto acadêmico

Projeto desenvolvido para a disciplina **UPX – Usina de Projetos Experimentais V**, no curso de Análise e Desenvolvimento de Sistemas da Facens.

**Ano:** 2026  
**Local:** Sorocaba – SP
