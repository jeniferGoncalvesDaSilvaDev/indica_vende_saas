# SaasIndicaVende

Sistema SaaS de gestão de leads e vendas com backend FastAPI e frontend Streamlit.

## Visão Geral
Projeto clonado de: https://github.com/jeniferGoncalvesDaSilvaDev/SaasIndicaVende.git

Sistema completo de gestão de indicações e vendas com:
- **Backend**: FastAPI (porta 8000) com SQLAlchemy
- **Frontend**: Streamlit (porta 5000) com interfaces específicas por perfil
- **Banco de Dados**: SQLite (indicavende.db)

## Estrutura do Projeto

```
.
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── auth.py          # Autenticação e gestão de usuários
│   │   ├── database.py      # Operações de banco de dados
│   │   ├── main.py          # API FastAPI
│   │   ├── models.py        # Modelos SQLAlchemy
│   │   └── schemas.py       # Schemas Pydantic
│   ├── indicavende.db       # Banco de dados SQLite
│   ├── populate_db.py
│   └── requirements.txt
│
├── frontend/
│   ├── .streamlit/
│   │   └── config.toml      # Configuração do Streamlit
│   ├── app.py              # Aplicação principal
│   ├── auth.py             # Funções de autenticação do frontend
│   ├── gestor.py           # Interface do Gestor
│   ├── indicador.py        # Interface do Indicador
│   ├── vendedor.py         # Interface do Vendedor
│   └── requirements.txt
│
└── pyproject.toml
```

## Perfis de Usuário

O sistema possui 3 tipos de perfis:

1. **Gestor**: Visão completa do sistema, gerenciamento de leads e usuários
2. **Vendedor**: Visualização e gestão dos leads atribuídos
3. **Indicador**: Criação e acompanhamento de leads indicados

## Usuários Cadastrados

### Gestor:
- **Gestor Admin**: gestor@indicavende.me / gestor123

### Vendedores:
- **João Silva**: joao@indicavende.me / vendedor123
- **Maria Santos**: maria@indicavende.me / vendedora123

### Indicadores:
- **Carlos Oliveira**: carlos@indicavende.me / indicador123
- **Ana Paula**: ana@indicavende.me / indicadora123

## Configuração Atual

### Workflows Configurados

1. **Backend API** (porta 8000):
   - Comando: `cd backend && uvicorn app.main:app --host 0.0.0.0 --port 8000`
   - API REST com FastAPI
   - Autenticação por email/senha
   - CORS habilitado

2. **Frontend** (porta 5000):
   - Comando: `cd frontend && BACKEND_URL=http://localhost:8000 streamlit run app.py --server.port 5000 --server.address 0.0.0.0 --server.enableCORS false --server.enableXsrfProtection false`
   - Interface web com Streamlit
   - Conecta ao backend via localhost:8000

### Dependências Instaladas

**Backend:**
- fastapi==0.104.1
- uvicorn==0.24.0
- sqlalchemy==2.0.23
- bcrypt==4.1.2
- python-multipart==0.0.6
- pydantic[email]==2.5.0

**Frontend:**
- streamlit==1.28.0
- requests==2.31.0
- pandas==2.1.1
- scipy==1.11.3
- matplotlib==3.8.0

## Estado Atual (08/10/2025)

✅ Repositório clonado com sucesso
✅ Python 3.11 instalado
✅ Todas as dependências instaladas (backend e frontend)
✅ Workflows configurados e executando corretamente
✅ Banco de dados populado com usuários de teste
✅ Sistema de autenticação funcionando
✅ Frontend renderizando tela de login corretamente
✅ API backend respondendo às requisições

## Funcionalidades do Dashboard do Gestor

O dashboard do gestor possui as seguintes funcionalidades:

### 📊 Estatísticas Avançadas:
- **Medidas de Tendência Central**: Média, Mediana e Moda
- **Medidas de Dispersão**: Amplitude, Desvio Padrão e Intervalo de Confiança (95%)
- **Forma da Distribuição**: Assimetria (Skewness) e Curtose (Kurtosis)

### 🔄 Atualização em Tempo Real:
- **Botão de Atualização Manual**: Atualiza os dados instantaneamente
- **Atualização Automática**: Opção para ativar atualização periódica
- **Intervalos Configuráveis**: 10, 30, 60 ou 120 segundos
- **Dados Sempre Atualizados**: Conecta diretamente ao banco de dados

### 📈 Visualizações:
- **Distribuição de Leads**: Histograma interativo com explicações didáticas
- **Métricas Visuais**: Cards com indicadores principais
- **Explicações Detalhadas**: Guia completo sobre como interpretar cada estatística

## Como Usar

1. Os workflows já estão configurados e rodando automaticamente
2. Acesse a interface web (porta 5000) para fazer login
3. Use as credenciais dos usuários listados acima
4. Cada perfil terá acesso a funcionalidades específicas
5. No dashboard do gestor, ative "🔄 Atualização Automática" para ver dados em tempo real

## Endpoints da API

- `POST /auth/login` - Login de usuário
- `POST /auth/register` - Registro de novo usuário
- `POST /leads/` - Criar lead
- `GET /leads/` - Listar leads (filtra por perfil)
- `PUT /leads/{lead_id}` - Atualizar status do lead
- `GET /users/` - Listar usuários (apenas gestor)
- `GET /vendedores/` - Listar vendedores
- `POST /seed` - Popular banco com dados de teste
