from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import AllowAny
from rest_framework import status
from store.models import Compra, Cliente, Produto, ItemCompra, ItemCarrinho

class CompraView(ViewSet):
    permission_classes = [AllowAny]

    def retrieve(self, request, pk=None):
        """
        Retorna uma compra
        """

        try:

            compra = Compra.objects.get(pk=pk)

            if not compra:
                return Response({'error': 'Compra não encontrada'}, status=status.HTTP_404_NOT_FOUND)
            
            items = ItemCompra.objects.filter(compra=compra)

            data = {
                'id': compra.id,
                'cliente_cpf_cnpj': compra.cliente.cpf_cnpj,
                'itens': [],
                'valor_total': compra.valor_total,
            }

            for item in items:
                data['itens'].append({
                    'produto': {
                        'id': item.produto.id,
                        'nome': item.produto.nome,
                        'preco': item.preco_unidade,
                    },
                    'desconto_aplicado': item.desconto_aplicado,
                    'quantidade': item.quantidade,
                    'subtotal': item.subtotal(),
                })

            return Response(data, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({'error': 'Erro interno', 'message': f'{e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def list(self, request):
        """
        Lista todas as compras
        """

        compras = Compra.objects.all()
        data = []
        for compra in compras:
            items = ItemCompra.objects.filter(compra=compra)
            itens = []
            for item in items:
                itens.append({
                    'produto': {
                        'id': item.produto.id,
                        'nome': item.produto.nome,
                        'preco': item.preco_unidade,
                    },
                    'desconto_aplicado': item.desconto_aplicado,
                    'quantidade': item.quantidade,
                })

            data.append({
                'id': compra.id,
                'cliente_cpf_cnpj': compra.cliente.cpf_cnpj,
                'itens': itens,
                'valor_total': compra.valor_total,
            })

        return Response(data, status=status.HTTP_200_OK)
    
    def create(self, request):
        """
        Cria uma compra
        """

        try:
            cliente_id = request.data['cliente_id']
            
            if not cliente_id:
                return Response({'error': 'Dados inválidos', 'message': 'Informe o ID do Cliente'}, status=status.HTTP_400_BAD_REQUEST)

            cliente = Cliente.objects.get(pk=cliente_id)
            if not cliente:
                return Response({'error': 'Cliente não encontrado'}, status=status.HTTP_404_NOT_FOUND)
            
            # Verifica se o cliente está ativo
            if not cliente.ativo:
                return Response({'error': 'Cliente inativo'}, status=status.HTTP_400_BAD_REQUEST)
            
            itens_carrinho = ItemCarrinho.objects.filter(cliente=cliente)

            if not itens_carrinho:
                return Response({'error': 'Carrinho vazio'}, status=status.HTTP_400_BAD_REQUEST)
            
            # Verifica se a quantidade de produtos é válida
            for item in itens_carrinho:
                if item.quantidade <= 0:
                    return Response({'error': 'Dados inválidos', 'message': 'A quantidade deve ser maior que 0'}, status=status.HTTP_400_BAD_REQUEST)
                if item.quantidade > item.produto.estoque:
                    return Response({'error': 'Dados inválidos', 'message': 'Quantidade maior que o estoque'}, status=status.HTTP_400_BAD_REQUEST)

            compra = Compra.objects.create(cliente=cliente)

            for item in itens_carrinho:
                compra.add_item(item.produto, item.quantidade)

            # limpa o carrinho
            cliente.clear_cart()

            data = {
                'id': compra.id,
                'cliente_cpf_cnpj': compra.cliente.cpf_cnpj,
                'itens': [],
                'valor_total': compra.valor_total,
            }

            items = ItemCompra.objects.filter(compra=compra)
            for item in items:
                data['itens'].append({
                    'produto': {
                        'id': item.produto.id,
                        'nome': item.produto.nome,
                        'preco': item.preco_unidade,
                    },
                    'desconto_aplicado': item.desconto_aplicado,
                    'quantidade': item.quantidade,
                    'subtotal': item.subtotal(),
                })


            return Response(data, status=status.HTTP_201_CREATED)
        
        except KeyError:
            return Response({'error': 'Dados inválidos'}, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            return Response({'error': 'Erro interno'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)