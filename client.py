from zeep import Client

# URL do seu serviço SOAP rodando localmente
wsdl = 'http://localhost:8000/?wsdl'
client = Client(wsdl=wsdl)

# Dados de login
username = "joao_user"
password = "senha123"

# 1. Login
print("Login:")
response = client.service.login(username, password)
print("Resposta:", response)

# Verifica se o login foi bem-sucedido e extrai o ID do usuário
if "ID:" in response:
    user_id = int(response.split("ID:")[1].strip())
else:
    print("Login falhou. Encerrando.")
    exit()

# 2. Listar encomendas do usuário
print("\nEncomendas do usuário:")
packages = client.service.list_packages(user_id)

if not packages:
    print("Nenhuma encomenda encontrada.")
    exit()

for p in packages:
    print("-", p)

# 3. Pergunta o nome de uma encomenda específica
nome_encomenda = input("\nDigite o nome de uma encomenda para ver detalhes: ").strip()

# 4. Obter ID da encomenda
response = client.service.get_package_id(user_id, nome_encomenda)
print("ID da encomenda:", response)

# 5. Ver status
status = client.service.check_package_status(user_id, nome_encomenda)
print("Status da encomenda:", status)
