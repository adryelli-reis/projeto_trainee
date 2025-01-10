from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import AllowAny
from rest_framework import status
from store.models import ItemCarrinho, Cliente, Produto

class ItemCarrinhoView(ViewSet):
    permission_classes = [AllowAny]

    def retrieve(self, request, pk=None):
        """
        Retorna um item de um carrinho
        """

        try:
            item = ItemCarrinho.objects.get(pk=pk)
            data = {
                'id': item.id,
                'produto': {
                    'id': item.produto.id,
                    'nome': item.produto.nome,
                    'preco': item.produto.preco,
                    'desconto': item.produto.desconto,
                },
                'quantidade': item.quantidade,
            }

            return Response(data, status=status.HTTP_200_OK)
        
        except ItemCarrinho.DoesNotExist:
            return Response({'error': 'Item não encontrado'}, status=status.HTTP_404_NOT_FOUND)
        
    def list(self, request):
        """
        Lista todos os itens de um carrinho de um cliente
        """

        try:
            pk = request.query_params.get('id_cliente', None)
            if not pk:
                return Response({'error': 'Cliente ID não informado'}, status=status.HTTP_400_BAD_REQUEST)
            
            cliente = Cliente.objects.filter(pk=pk).first()
            if not cliente:
                return Response({'error': 'Cliente não encontrado'}, status=status.HTTP_404_NOT_FOUND)

            itens = ItemCarrinho.objects.filter(cliente=cliente)  

            data = []

            for item in itens:
                data.append({
                    'id': item.id,
                    'produto': {
                        'id': item.produto.id,
                        'nome': item.produto.nome,
                        'preco': item.produto.preco,
                        'desconto': item.produto.desconto,
                    },
                    'quantidade': item.quantidade,
                })

            return Response(data, status=status.HTTP_200_OK)
        
        except Cliente.DoesNotExist:
            return Response({'error': 'Cliente não encontrado'}, status=status.HTTP_404_NOT_FOUND)
    
    def create(self, request):
        """
        Adiciona um item em um carrinho
        """

        try:
            cliente_id = request.data['cliente_id']
            produto_id = request.data['produto_id']
            quantidade = request.data['quantidade']

            # Verifica se os campos existem
            if not cliente_id or not produto_id or not quantidade:
                return Response({'error': 'Dados inválidos'}, status=status.HTTP_400_BAD_REQUEST)
            
            # Verifica se os campos são válidos
            if quantidade <= 0:
                return Response({'error': 'Dados inválidos', 'message': 'A quantidade deve ser maior que 0'}, status=status.HTTP_400_BAD_REQUEST)
            
            cliente = Cliente.objects.get(pk=cliente_id)
            if not cliente.ativo:
                return Response({'error': 'Cliente inativo'}, status=status.HTTP_400_BAD_REQUEST)
            
            produto = Produto.objects.get(pk=produto_id)

            if not produto:
                return Response({'error': 'Produto não encontrado'}, status=status.HTTP_404_NOT_FOUND)
            if quantidade > produto.estoque:
                return Response({'error': 'Estoque insuficiente'}, status=status.HTTP_400_BAD_REQUEST)
            
            cliente.update_cart(produto, quantidade)

            return Response({'message': 'Item adicionado ao carrinho'}, status=status.HTTP_200_OK)
        
        except KeyError:
            return Response({'error': 'Dados inválidos'}, status=status.HTTP_400_BAD_REQUEST)
        
        except Cliente.DoesNotExist:
            return Response({'error': 'Cliente não encontrado'}, status=status.HTTP_404_NOT_FOUND)
        
    def update(self, request, pk=None): 
        """
        Atualiza a quantidade de um item em um carrinho
        """

        try:
            cliente = request.data.get('cliente_id')
            quantidade = request.data.get('quantidade')

            # Verifica se os campos existem
            if not cliente:
                return Response({'error': 'Dados inválidos'}, status=status.HTTP_400_BAD_REQUEST)
            
            # Verifica se os campos são válidos
            if quantidade < 0:
                return Response({'error': 'Dados inválidos', 'message': 'A quantidade não pode ser negativa'}, status=status.HTTP_400_BAD_REQUEST)
            
            item_carrinho = ItemCarrinho.objects.filter(pk=pk, cliente=cliente).first()

            if not item_carrinho:
                return Response({'error': 'Item não encontrado'}, status=status.HTTP_404_NOT_FOUND)
            
            Cliente.objects.get(pk=cliente).update_cart(Produto.objects.get(pk=item_carrinho.produto.id), quantidade)

            return Response({'message': 'Item atualizado'}, status=status.HTTP_200_OK)
        
        except KeyError:
            return Response({'error': 'Dados inválidos'}, status=status.HTTP_400_BAD_REQUEST)
        
        except ItemCarrinho.DoesNotExist:
            return Response({'error': 'Item não encontrado'}, status=status.HTTP_404_NOT_FOUND)
        except Cliente.DoesNotExist:
            return Response({'error': 'Cliente não encontrado'}, status=status.HTTP_404_NOT_FOUND)
        
    def destroy(self, request, pk=None):
        """
        Remove um item de um carrinho
        """

        try:
            item = ItemCarrinho.objects.get(pk=pk)
            item.delete()

            return Response({'message': 'Item removido do carrinho'}, status=status.HTTP_200_OK)
        
        except ItemCarrinho.DoesNotExist:
            return Response({'error': 'Item não encontrado'}, status=status.HTTP_404_NOT_FOUND)
        