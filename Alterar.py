import flet as ft
from models import Produto
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime

CONN = "sqlite:///projeto2.db"
engine = create_engine(CONN, echo=True)
Session = sessionmaker(bind=engine)

def AlterarPedido(page: ft.Page, pedido_obj: Produto, atualizar_e_voltar):
    session = Session()
    pedido_id = pedido_obj.id
    print(f"Abrindo página de alteração para pedido com ID: {pedido_id}")
    pedido = session.get(Produto, pedido_id)
    if not pedido:
        print("Erro: Pedido não encontrado!")
        return
    nome_input = ft.TextField(label="Nome", value=pedido.nome)
    quantidade_input = ft.TextField(label="Quantidade", value=str(pedido.quantidade))
    data_input = ft.TextField(label="Data", value=pedido.data.strftime("%Y-%m-%d"))
    entregue_checkbox = ft.Checkbox(label="Entregue", value=pedido.entregue)

    def alterar_pedido(e):
        try:
            print("Alterando pedido...")
            pedido.nome = nome_input.value
            pedido.quantidade = int(quantidade_input.value)
            pedido.data = datetime.strptime(data_input.value, "%Y-%m-%d").date()
            pedido.entregue = entregue_checkbox.value
            session.commit()
            verificar_e_mover_para_historico(pedido.nome_produto)
            atualizar_e_voltar()
            page.views.pop()
            page.update()
        except Exception as ex:
            session.rollback()
            print(f"Erro ao alterar pedido: {ex}")

    return ft.View(
        "/alterar_pedido",
        controls=[
            ft.Text("Alterar Pedido"),
            nome_input,
            quantidade_input,
            data_input,
            entregue_checkbox,
            ft.ElevatedButton("Salvar", on_click=alterar_pedido),
            ft.ElevatedButton("Voltar", on_click=lambda e: page.views.pop()),
        ],
    )

def verificar_e_mover_para_historico(nome_produto):
    print(f"Verificando e movendo pedidos de {nome_produto} para o histórico...")
    session = Session() # Cria uma nova sessão aqui
    pedidos = session.query(Produto).filter_by(nome_produto=nome_produto).all()
    if all(pedido.entregue for pedido in pedidos):
        print(f"Todos os pedidos de {nome_produto} foram entregues.")
        for pedido in pedidos:
            session.delete(pedido)
        session.commit()