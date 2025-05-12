from spyne import Application, rpc, ServiceBase, Integer, Unicode, Iterable
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from database import session, init_db
from models import User, Package

class TrackingService(ServiceBase):

    @rpc(Unicode, Unicode, _returns=Unicode)
    def login(ctx, username, password):
        user = session.query(User).filter_by(username=username, password=password).first()
        if user:
            return f"Login bem-sucedido. ID: {user.id}"
        return "Usuário ou senha inválidos."


    @rpc(Integer, _returns=Iterable(Unicode))
    def list_packages(ctx, user_id):
        packages = session.query(Package).filter_by(sender_id=user_id).all()
        if not packages:
            return []
        return [f"{p.name} - {p.description}" for p in packages]

    @rpc(Integer, Unicode, _returns=Unicode)
    def check_package_status(ctx, user_id, package_name):
        pkg = session.query(Package).filter_by(sender_id=user_id, name=package_name).first()
        if not pkg:
            return "Pacote não encontrado."
        return "Rastreando" if pkg.is_tracked else "Não rastreado"

    @rpc(Integer, Unicode, _returns=Unicode)
    def get_package_id(ctx, user_id, package_name):
        pkg = session.query(Package).filter_by(sender_id=user_id, name=package_name).first()
        if not pkg:
            return "Pacote não encontrado."
        return f"ID da encomenda: {pkg.id}"

    @rpc(Integer, Unicode, _returns=Unicode)
    def update_destination(ctx, package_id, new_city):
        pkg = session.query(Package).filter_by(id=package_id).first()
        if not pkg:
            return "Encomenda não encontrada."
        pkg.dest_city = new_city
        session.commit()
        return "Destino atualizado com sucesso."
    
    @rpc(Integer, Unicode, Unicode, Unicode, Unicode, _returns=Unicode)
    def add_package(ctx, sender_id, receiver_name, name, description, dest_city):
        sender = session.query(User).filter_by(id=sender_id).first()
        if not sender:
         return "Remetente inválido."

        receiver = session.query(User).filter_by(username=receiver_name).first()
        if not receiver:
            return "Destinatário não encontrado."

        package = Package(
            name=name,
            description=description,
            sender_id=sender.id,
            receiver_id=receiver.id,
            origin_city="Desconhecida",  # você pode mudar isso depois
            dest_city=dest_city,
            is_tracked=False
        )

        session.add(package)
        session.commit()
        return "Pacote adicionado com sucesso."


# Inicializa banco
init_db()

# Cria a aplicação SOAP
app = Application([TrackingService],
                  tns='tracking.soap',
                  in_protocol=Soap11(validator='lxml'),
                  out_protocol=Soap11())

# Servidor WSGI
wsgi_app = WsgiApplication(app)

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    print("Servidor WS1 SOAP rodando em http://localhost:8000")
    make_server('0.0.0.0', 8000, wsgi_app).serve_forever()
