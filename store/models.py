import uuid
from django.db import models
from django.db.models import Sum, F

class Produto(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    estoque = models.IntegerField()
    desconto = models.IntegerField(default=0)

    def __str__(self):
        return self.nome
    
    def add_estoque(self, quantidade):
        self.estoque += quantidade
        self.save()

    def remove_estoque(self, quantidade):
        self.estoque -= quantidade
        if self.estoque < 0:
            self.estoque = 0
        self.save()

class ItemCarrinho(models.Model):
    cliente = models.ForeignKey('Cliente', on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.IntegerField()

    def subtotal(self):
        return self.produto.preco * self.quantidade

    def __str__(self):
        return f'{self.quantidade}x {self.produto.nome} do carrinho de {self.cliente.nome}'

class Cliente(models.Model):
    nome = models.CharField(max_length=20)
    sobrenome = models.CharField(max_length=100)
    cpf_cnpj = models.CharField(max_length=14, unique=True)
    email = models.EmailField(unique=True)
    telefone = models.CharField(max_length=15)
    endereco = models.TextField()
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return self.nome
    
    def update_cart(self, produto, quantidade):
        item = ItemCarrinho.objects.filter(cliente=self, produto=produto).first()
        quantidade = min(quantidade, produto.estoque)
        if item:
            if quantidade > 0:
                item.quantidade = quantidade
                item.save()
            else:
                item.delete()
            
        else:
            if quantidade > 0:
                ItemCarrinho.objects.create(cliente=self, produto=produto, quantidade=quantidade)
    
    def clear_cart(self):
        ItemCarrinho.objects.filter(cliente=self).delete()

class ItemCompra(models.Model):
    compra = models.ForeignKey('Compra', on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    preco_unidade = models.DecimalField(max_digits=10, decimal_places=2)
    quantidade = models.IntegerField()
    desconto_aplicado = models.IntegerField(default=0)

    def subtotal(self):
        return self.preco_unidade * self.quantidade

class Compra(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    data_compra = models.DateTimeField(auto_now_add=True)
    valor_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        itens = ItemCompra.objects.filter(compra=self)
        itens_str = ', '.join([f'{item.quantidade}x {item.produto.nome}' for item in itens])
        return f'{self.cliente.nome} comprou {itens_str}'
    
    def add_item(self, produto, quantidade):
        item = ItemCompra.objects.filter(compra=self, produto=produto).first()
        if item:
            item.quantidade += quantidade
            item.save()
        else:
            preco_com_desconto = produto.preco - ((produto.preco * produto.desconto) / 100)
            ItemCompra.objects.create(compra=self, produto=produto, preco_unidade=preco_com_desconto, quantidade=quantidade, desconto_aplicado=produto.desconto)
            
        produto.remove_estoque(quantidade)
        self.valor_total = self.total()
        self.save()

    def total(self):
        
        total = ItemCompra.objects.filter(compra=self).aggregate(
            total=Sum(F('preco_unidade') * F('quantidade'))
        )['total'] or 0
        return total
