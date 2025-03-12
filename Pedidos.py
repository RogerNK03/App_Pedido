import flet as ft
from Adicionar import Adicionar
from Alterar import AlterarPedido
from models import Produto, CatalogoProduto, HistoricoModel
from Cad_Produto import Cad_Produto
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from functools import partial

CONN = "sqlite:///projeto2.db"

engine = create_engine(CONN, echo=True)
Session = sessionmaker(bind=engine)
session = Session()

def Pedidos(page: ft.Page, session):
    produtos_pedidos = {}
    lista_view = ft.ListView()

    def carregar_dados():
        produtos = session.query(CatalogoProduto).all()
        for produto in produtos:
            pedidos = session.query(Produto).filter_by(nome_produto=produto.nome_produto).all()
            produtos_pedidos[produto.id] = pedidos

    def atualizar_lista_catalogo():
        print("Atualizando lista de catálogo...")
        carregar_dados()
        lista_produtos = []

        produtos_ordenados = sorted(
            produtos_pedidos.items(),
            key=lambda item: session.query(CatalogoProduto).filter_by(id=item[0]).first().nome_produto
            if session.query(CatalogoProduto).filter_by(id=item[0]).first() else ""
        )

        for produto_id, pedidos in produtos_ordenados:
            produto = session.query(CatalogoProduto).filter_by(id=produto_id).first()
            if produto:
                lista_pedidos = []
                for pedido in pedidos:
                    if not pedido.entregue:
                        btn_alterar = ft.ElevatedButton("Alterar", on_click=partial(abrir_alterar, pedido.id))
                        btn_excluir_pedido = ft.ElevatedButton("Excluir", on_click=partial(excluir_pedido, pedido.id))
                        btn_entregue = ft.ElevatedButton("Entregue", on_click=partial(marcar_entregue, pedido.id))
                        lista_pedidos.append(
                            ft.Row([
                                ft.Text(f"{pedido.nome} - {pedido.quantidade} - {pedido.data}"),
                                btn_alterar,
                                btn_excluir_pedido,
                                btn_entregue
                            ])
                        )

                btn_excluir_produto = ft.ElevatedButton("Excluir Produto", on_click=partial(excluir_produto, produto.id))

                lista_produtos.append(
                    ft.ExpansionTile(
                        title=ft.Row([ft.Text(produto.nome_produto), btn_excluir_produto]),
                        controls=lista_pedidos,
                    )
                )

        lista_view.controls = lista_produtos
        page.update()
        print("Lista de catálogo atualizada.")

    def navigate_to(view):
        page.views.append(view)
        page.update()

    def abrir_cadastro(e):
        navigate_to(Cad_Produto(page, atualizar_lista_catalogo))

    def abrir_adicionar(e):
        navigate_to(Adicionar(page, atualizar_lista_catalogo))
        atualizar_lista_catalogo()

    def abrir_alterar(pedido_id, e):
        print(f"Abrindo página de alteração para pedido com ID: {pedido_id}")
        pedido = session.query(Produto).filter_by(id=pedido_id).first()
        if pedido:
            def atualizar_e_voltar():
                print("Atualizando e voltando da página de alteração...")
                session.refresh(pedido)
                atualizar_lista_catalogo()
                page.update()
                print("Atualização e volta concluídas.")
            navigate_to(AlterarPedido(page, pedido, atualizar_e_voltar))
            print("Página de alteração aberta.")

    def excluir_produto(produto_id, e):
        print(f"Excluindo produto ID: {produto_id}")
        produto = session.query(CatalogoProduto).filter_by(id=produto_id).first()
        if produto:
            session.delete(produto)
            session.commit()
            session.expire_all()
            atualizar_lista_catalogo()
            page.update()

    def excluir_pedido(pedido_id, e):
        print(f"Excluindo pedido ID: {pedido_id}")
        pedido = session.query(Produto).filter_by(id=pedido_id).first()
        if pedido:
            session.delete(pedido)
            session.commit()
            session.expire_all()
            atualizar_lista_catalogo()
            page.update()

    def marcar_entregue(pedido_id, e):
        print(f"Marcando pedido {pedido_id} como entregue...")
        pedido = session.query(Produto).filter_by(id=pedido_id).first()
        if pedido:
            pedido.entregue = True
            session.commit()
            verificar_e_mover_para_historico(pedido)
            atualizar_lista_catalogo()

    def verificar_e_mover_para_historico(pedido):
        print(f"Movendo pedido {pedido.id} para o histórico...")
        historico_pedido = HistoricoModel(
            nome_produto=pedido.nome_produto,
            preco=pedido.preco,
            nome=pedido.nome,
            quantidade=pedido.quantidade,
            data=pedido.data
        )
        session.add(historico_pedido)
        session.delete(pedido)
        session.commit()
        atualizar_lista_catalogo()

    def go_back(e):
        print("Voltando para página anterior...")
        if page.views:
            page.views.pop()
        atualizar_lista_catalogo()
        page.update()

    atualizar_lista_catalogo()

    return ft.View(
        "/pedidos",
        [
            # ... (seus controles) ...
            ft.ResponsiveRow(
                [
                    lista_view,
                    ft.Container(content=ft.ElevatedButton("Cadastrar Produto", on_click=abrir_cadastro), col={"xs": 12, "sm": 6}),
                    ft.Container(content=ft.ElevatedButton("Adicionar Pedido", on_click=abrir_adicionar), col={"xs": 12, "sm": 6}),
                    ft.Container(content=ft.ElevatedButton("Voltar", on_click=go_back), col={"xs": 12}),
                ]
            ),
        ],
    )