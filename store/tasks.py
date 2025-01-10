from decimal import Decimal
from celery import shared_task
from store.models import Produto

@shared_task
def atualizar_desconto(percentual_desconto):
    """
    Atualiza os preços dos produtos
    """

    # Filtra os produtos que possuem estoque
    produtos = Produto.objects.filter(estoque__gt=0)

    for produto in produtos:
        try:
            produto.desconto = percentual_desconto
            produto.save()
        except Exception as e:
            print(f'Erro ao atualizar preço do produto {produto.id}: {e}')

    return f'Desconto de {percentual_desconto}% aplicado para {produtos.count()} produtos'