# FilaSmart — MVP funcional (tema escuro)

Protótipo acadêmico de filas virtuais com Flask + SQLite. Os cadastros, serviços e movimentações de fila são gravados no banco `filasmart.db`; a interface não depende de dados fictícios para mostrar serviços ou atendimentos.

## Funcionalidades implementadas
- Cadastro de clientes e estabelecimentos, com senha armazenada por hash.
- Login, sessão e separação de acesso por tipo de conta.
- Cadastro, pausa e reativação de serviços.
- Listagem dos serviços ativos cadastrados no banco.
- Entrada de cliente em fila e prevenção de entradas duplicadas na mesma fila ativa.
- Posição calculada a partir das entradas reais da fila.
- Cancelamento da entrada enquanto estiver aguardando.
- Fluxo do estabelecimento: chamar, iniciar e concluir atendimento.
- Contagens do painel calculadas a partir do banco.
- Endpoint `/health` para verificação básica.
- Interface responsiva com tema escuro.

## Executar no Windows
1. Instale Python 3.10 ou superior.
2. Extraia o ZIP e abra o terminal dentro da pasta `para atualizar`.
3. Crie o ambiente virtual: `python -m venv .venv`
4. Ative: `.\.venv\Scripts\Activate.ps1`
5. Instale as dependências: `python -m pip install -r requirements.txt`
6. Execute: `python app.py`
7. Acesse `http://127.0.0.1:5000`.

Se o comando `python` não funcionar no seu Windows, confira a instalação do Python e desative aliases quebrados da Microsoft Store em Configurações do Windows > Aplicativos > Configurações avançadas de aplicativo > Aliases de execução de aplicativo.

## Roteiro de demonstração com dados reais
1. Cadastre uma conta do tipo **Estabelecimento** e faça login.
2. Cadastre um serviço no painel.
3. Abra uma janela anônima, cadastre uma conta **Cliente** e faça login.
4. Entre na fila do serviço criado.
5. Volte à conta do estabelecimento e clique em **Chamar próximo**, depois **Iniciar atendimento** e **Concluir**.
6. Atualize **Minhas filas** na conta do cliente e confira a mudança de status.
7. Cancele uma entrada enquanto estiver aguardando para demonstrar essa regra.
8. Pare e reinicie o servidor; confirme que usuários, serviços e entradas continuam salvos.

## Verificação de saúde
Acesse `http://127.0.0.1:5000/health`. Uma resposta esperada é `{"status":"ok","database":"connected"}`.

## Limitações conhecidas
O MVP ainda não possui notificações push, atualização em tempo real, previsão de espera por IA, testes automatizados integrados ou proteção CSRF. A chave de sessão pode ser definida pela variável de ambiente `FILASMART_SECRET_KEY`; o valor padrão serve apenas para desenvolvimento local. Antes de publicar na internet, configure uma chave secreta forte, proteção CSRF, HTTPS, limitação de tentativas de login e revisão de segurança. Para uso multiusuário em produção, avalie PostgreSQL e aprovação de contas de estabelecimento.

## Sobre o requisito de 70%
Este pacote contém funcionalidades reais conectadas ao SQLite, mas o percentual formal de requisitos atendidos só pode ser calculado comparando cada item com a rubrica/especificação oficial do projeto. Não declare o percentual como comprovado sem essa conferência e uma demonstração prática.
