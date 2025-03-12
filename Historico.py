import flet as ft
from models import HistoricoModel
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime

CONN = "sqlite:///projeto2.db"
engine = create_engine(CONN, echo=True)
Session = sessionmaker(bind=engine)
session = Session()

def Historico(page: ft.Page, session):
    def go_back(e):
        page.views.pop()
        page.update()

    def carregar_historico(page, session):
        historico = session.query(HistoricoModel).all()
        pedidos_agrupados = {}

        for pedido in historico:
            chave = (pedido.nome_produto, pedido.data.strftime("%m/%Y"))
            if chave not in pedidos_agrupados:
                pedidos_agrupados[chave] = []
            pedidos_agrupados[chave].append(pedido)

        lista_historico = ft.ListView()
        itens_historico = []

        for chave, pedidos in pedidos_agrupados.items():
            nome_produto, data_entrega = chave
            lista_pedidos = []
            for pedido in pedidos:
                lista_pedidos.append(ft.ListTile(title=ft.Text(f"{pedido.nome} - {pedido.quantidade} - {pedido.data}")))

            itens_historico.append(
                ft.ExpansionTile(
                    title=ft.Text(f"{nome_produto} - {data_entrega}"),
                    controls=lista_pedidos,
                )
            )

        lista_historico.controls = itens_historico
        return lista_historico

    lista_historico_view = carregar_historico(page, session)

    return ft.View(
        "/historico",
        [
            ft.Text("Página de Histórico", style=ft.TextThemeStyle.HEADLINE_MEDIUM),
            lista_historico_view,
            ft.ElevatedButton("Voltar", on_click=go_back),
        ],
    )