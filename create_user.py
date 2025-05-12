from database import session
from models import User

# 🔧 Dados do novo usuário:
username = input("Nome de usuário: ")
password = input("Senha: ")
role = "client"  # ou 'admin' se quiser criar um administrador

# 🔍 Verificar se o usuário já existe
existing_user = session.query(User).filter_by(username=username).first()
if existing_user:
    print(f" O usuário '{username}' já existe.")
else:
    user = User(username=username, password=password, role=role)
    session.add(user)
    session.commit()
    print(f" Usuário '{username}' criado com sucesso!")

