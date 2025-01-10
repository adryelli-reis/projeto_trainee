from decimal import Decimal
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import AllowAny
from rest_framework import status
from store.models import Produto
from store.tasks import atualizar_desconto

class ProdutoView(ViewSet):
    permission_classes = [AllowAny]

    def retrieve(self, request, pk=None):
        """
        Retorna um produto
        """

        try:
            produto = Produto.objects.get(pk=pk)
            data = {
                'id': produto.id,
                'nome': produto.nome,
                'descricao': produto.descricao,
                'preco': produto.preco,
                'estoque': produto.estoque,
                'desconto': produto.desconto,
            }

            return Response(data, status=status.HTTP_200_OK)
        
        except Produto.DoesNotExist:
            return Response({'error': 'Produto não encontrado'}, status=status.HTTP_404_NOT_FOUND)
        
    def list(self, request):
        """
        Lista todos os produtos
        """

        produtos = Produto.objects.all()
        data = []
        for produto in produtos:
            data.append({
                'id': produto.id,
                'nome': produto.nome,
                'descricao': produto.descricao,
                'preco': produto.preco,
                'estoque': produto.estoque,
                'desconto': produto.desconto,
            })

        return Response(data, status=status.HTTP_200_OK)
        
    def create(self, request):
        """
        Cria um produto
        """

        try:
            nome = request.data['nome']
            descricao = request.data['descricao']
            preco = request.data['preco']
            estoque = request.data['estoque']

            # Verifica se os campos existem
            if not nome or not descricao or not preco or not estoque:
                return Response({'error': 'Dados inválidos'}, status=status.HTTP_400_BAD_REQUEST)
            
            # Verifica os campos são válidos
            if len(nome) < 3 or len(descricao) < 3:
                return Response({'error': 'Dados inválidos', 'message': 'O minimo de caracteres para os campos é 3'}, status=status.HTTP_400_BAD_REQUEST)

            # Verifica se o preco é valido
            if preco < 0:
                return Response({'error': 'Dados inválidos', 'message': 'Preço inválido'}, status=status.HTTP_400_BAD_REQUEST)
            
            # Verifica se o estoque é valido
            if estoque < 0:
                return Response({'error': 'Dados inválidos', 'message': 'Estoque inválido'}, status=status.HTTP_400_BAD_REQUEST)
            
            produto = Produto.objects.create(nome=nome, descricao=descricao, preco=preco, estoque=estoque)
            data = {
                'id': produto.id,
                'nome': produto.nome,
                'descricao': produto.descricao,
                'preco': produto.preco,
                'estoque': produto.estoque,
            }

            return Response(data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': 'Erro ao criar produto', 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def update(self, request, pk=None):
        """
        Atualiza um produto
        """

        try:
            produto = Produto.objects.get(pk=pk)
            
            nome = request.data.get('nome')
            descricao = request.data.get('descricao')
            preco = request.data.get('preco')
            estoque = request.data.get('estoque')
            desconto = request.data.get('desconto')

            # Verifica se os campos existem
            if nome:
                if len(nome) < 3:
                    return Response({'error': 'Dados inválidos', 'message': 'O minimo de caracteres para os campos é 3'}, status=status.HTTP_400_BAD_REQUEST)
                produto.nome = nome
            elif descricao:
                if len(descricao) < 3:
                    return Response({'error': 'Dados inválidos', 'message': 'O minimo de caracteres para os campos é 3'}, status=status.HTTP_400_BAD_REQUEST)
                produto.descricao = descricao
            elif preco:
                if preco < 0:
                    return Response({'error': 'Dados inválidos', 'message': 'Preço inválido'}, status=status.HTTP_400_BAD_REQUEST)
                produto.preco = preco
            elif estoque:
                if estoque < 0:
                    return Response({'error': 'Dados inválidos', 'message': 'Estoque inválido'}, status=status.HTTP_400_BAD_REQUEST)
                produto.estoque = estoque
            elif desconto:
                if desconto < 0 or desconto > 100:
                    return Response({'error': 'Dados inválidos', 'message': 'Desconto inválido'}, status=status.HTTP_400_BAD_REQUEST)
                produto.desconto = int(desconto)
            else:
                return Response({'error': 'Dados inválidos', 'message': 'Nenhum campo para atualizar'}, status=status.HTTP_400_BAD_REQUEST)
            
            produto.save()

            data = {
                'id': produto.id,
                'nome': produto.nome,
                'descricao': produto.descricao,
                'preco': produto.preco,
                'estoque': produto.estoque,
                'desconto': produto.desconto,
            }

            return Response(data, status=status.HTTP_200_OK)
        
        except Produto.DoesNotExist:
            return Response({'error': 'Produto não encontrado'}, status=status.HTTP_404_NOT_FOUND)
        
    def destroy(self, request, pk=None):
        """
        Deleta um produto
        """

        try:
            produto = Produto.objects.get(pk=pk)
            produto.remove_estoque(produto.estoque) # Deixa o produto sem itens em estoque

            return Response({'message': 'Produto declarado como em falta no estoque'}, status=status.HTTP_200_OK)
        
        except Produto.DoesNotExist:
            return Response({'error': 'Produto não encontrado'}, status=status.HTTP_404_NOT_FOUND)
        
    def aplicar_desconto(self, request):
        """
        Atualiza os preços dos produtos
        """

        try:
            percentual_desconto = request.data.get('percentual_desconto', None)
            
            if percentual_desconto is None:
                return Response({'error': 'Dados inválidos', 'message': 'Informe o percentual de desconto'}, status=status.HTTP_400_BAD_REQUEST)
            

            if percentual_desconto <= 0:
                return Response({'error': 'Dados inválidos', 'message': 'O percentual de desconto deve ser maior que 0'}, status=status.HTTP_400_BAD_REQUEST)
            
            percentual_desconto = Decimal(percentual_desconto)

            tarefa = atualizar_desconto.delay(percentual_desconto)

            return Response({'task_id': tarefa.id, 'message': 'Tarefa para atualização de preços enviada'}, status=status.HTTP_202_ACCEPTED)
        except Exception as e:
            return Response({'error': 'Erro ao atualizar preços', 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
