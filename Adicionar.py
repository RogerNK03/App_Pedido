import flet as ft
from models import Produto, CatalogoProduto, session
from datetime import datetime

def Adicionar(page: ft.Page, atualizar_lista):
    produtos_catalogo = session.query(CatalogoProduto).all()
    opcoes_produtos = [ft.dropdown.Option(text=p.nome_produto, key=p.id) for p in produtos_catalogo]

    produto_dropdown = ft.Dropdown(
        label="Nome do produto...",
        options=opcoes_produtos,
        on_change=lambda e: preencher_campos(e.control.value),
        width=300,
    )

    produto = ft.TextField(label='Nome do produto...', text_align=ft.TextAlign.LEFT, disabled=True, width=300)
    preco = ft.TextField(label='Preco do produto...', text_align=ft.TextAlign.LEFT, disabled=True, width=300)
    remetente = ft.TextField(label='Remetente...', text_align=ft.TextAlign.LEFT, width=300)
    quantidade = ft.TextField(label='Quantidade...', text_align=ft.TextAlign.LEFT, width=300)
    data = ft.TextField(label='Data (AAAA-MM-DD)...', text_align=ft.TextAlign.LEFT, width=300)

    def preencher_campos(produto_id):
        produto_selecionado = session.query(CatalogoProduto).filter_by(id=produto_id).first()
        if produto_selecionado:
            produto.value = produto_selecionado.nome_produto
            preco.value = str(produto_selecionado.preco)
            page.update()

    def cadastrar(e):
        if not produto.value or not preco.value or not remetente.value or not quantidade.value or not data.value:
            page.snack_bar = ft.SnackBar(ft.Text("Preencha todos os campos obrigatórios."))
            page.snack_bar.open = True
            page.update()
            return

        try:
            novo_produto = Produto(
                nome_produto=produto.value,
                preco=float(preco.value),
                nome=remetente.value,
                quantidade=int(quantidade.value),
                data=datetime.strptime(data.value, "%Y-%m-%d").date()
            )
            session.add(novo_produto)
            session.commit()
            page.snack_bar = ft.SnackBar(ft.Text("Pedido cadastrado com sucesso!"))
            page.snack_bar.open = True
            page.update()
            atualizar_lista()
            page.update() # Adicionado page.update()
        except ValueError:
            page.snack_bar = ft.SnackBar(ft.Text("Erro: Verifique os formatos dos campos (Preço: número, Quantidade: número, Data: AAAA-MM-DD)"))
            page.snack_bar.open = True
            page.update()
        except Exception as ex:
            page.snack_bar = ft.SnackBar(ft.Text(f"Erro ao cadastrar: {ex}"))
            page.snack_bar.open = True
            page.update()

    def go_back(e):
        page.views.pop()
        page.update()

    return ft.View(
        "/adicionar",
        [
            ft.Text("Adicionar Pedido", size=24, weight=ft.FontWeight.BOLD),
            ft.Column(
                controls=[
                    ft.Container(produto_dropdown, margin=ft.margin.only(bottom=10)),
                    ft.Container(produto, margin=ft.margin.only(bottom=10)),
                    ft.Container(preco, margin=ft.margin.only(bottom=10)),
                    ft.Container(remetente, margin=ft.margin.only(bottom=10)),
                    ft.Container(quantidade, margin=ft.margin.only(bottom=10)),
                    ft.Container(data, margin=ft.margin.only(bottom=10)),
                ],
                width=300,
            ),
            ft.ElevatedButton("Cadastrar", on_click=cadastrar, icon=ft.icons.ADD_SHOPPING_CART),
            ft.ElevatedButton("Voltar", on_click=go_back, icon=ft.icons.ARROW_BACK),
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )