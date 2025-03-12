import flet as ft
from models import CatalogoProduto, session

def Cad_Produto(page: ft.Page, atualizar_catalogo):
    nome_produto = ft.TextField(label="Nome do Produto", text_align=ft.TextAlign.LEFT)
    preco = ft.TextField(label="Preço", text_align=ft.TextAlign.LEFT)

    def cadastrar_produto(e):
        if not nome_produto.value or not preco.value:
            page.snack_bar = ft.SnackBar(ft.Text("Preencha todos os campos obrigatórios."))
            page.snack_bar.open = True
            page.update()
            return

        try:
            novo_produto = CatalogoProduto(
                nome_produto=nome_produto.value,
                preco=float(preco.value)
            )
            session.add(novo_produto)
            session.commit()
            page.snack_bar = ft.SnackBar(ft.Text("Produto cadastrado com sucesso!"))
            page.snack_bar.open = True
            page.update()
            atualizar_catalogo()
            page.update() # Adicionado page.update()
        except ValueError:
            page.snack_bar = ft.SnackBar(ft.Text("Erro: Verifique o formato do preço (deve ser um número)."))
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
        "/cadastro_produto",
        [
            ft.Text("Cadastro de Produto"),
            nome_produto,
            preco,
            ft.ElevatedButton("Cadastrar", on_click=cadastrar_produto),
            ft.ElevatedButton("Voltar", on_click=go_back),
        ],
    )