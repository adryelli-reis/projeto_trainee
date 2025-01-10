from django.core.management.base import BaseCommand
from store.models import Produto, Cliente, Compra, ItemCompra

class Command(BaseCommand):
    help = 'Popula o banco de dados com dados iniciais'

    def handle(self, *args, **kwargs):
        # Produtos
        camiseta = Produto.objects.create(nome='Camiseta', descricao='Camiseta branca', preco=29.90, estoque=100)
        calca = Produto.objects.create(nome='Calça', descricao='Calça jeans', preco=59.90, estoque=50)
        sapato = Produto.objects.create(nome='Sapato', descricao='Sapato social', preco=89.90, estoque=30)
        bone = Produto.objects.create(nome='Boné', descricao='Boné preto', preco=19.90, estoque=24)
        meia = Produto.objects.create(nome='Meia', descricao='Meia branca', preco=9.90, estoque=200)

        # Clientes
        adry = Cliente.objects.create(nome='Adry', sobrenome='Reis', cpf_cnpj='12345678901', email='adryreis@gmail.com', telefone='123456789', endereco='Rua 1, 123')
        joao = Cliente.objects.create(nome='João', sobrenome='Souza', cpf_cnpj='23456789012', email='joaosouza@gmail.com', telefone='234567890', endereco='Rua 2, 456')
        maria = Cliente.objects.create(nome='Maria', sobrenome='Rodrigues', cpf_cnpj='34567890123', email='mariarodrigues@gmail.com', telefone='345678901', endereco='Rua 3, 789')

        # Carrinhos dos clientes
        adry.update_cart(meia, 2)
        joao.update_cart(bone, 1)
        maria.update_cart(sapato, 1)

        # Compras
        adry_compra = Compra.objects.create(cliente=adry)
        joao_compra = Compra.objects.create(cliente=joao)
        maria_compra = Compra.objects.create(cliente=maria)

        # Itens das compras
        adry_compra.add_item(produto=bone, quantidade=1)
        adry_compra.add_item(produto=camiseta, quantidade=2)
        joao_compra.add_item(produto=sapato, quantidade=1)
        maria_compra.add_item(produto=meia, quantidade=2)

        self.stdout.write(self.style.SUCCESS('Dados inseridos com sucesso!'))