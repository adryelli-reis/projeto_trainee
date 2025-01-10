from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import AllowAny
from rest_framework import status
from store.models import Cliente

class ClienteView(ViewSet):
    permission_classes = [AllowAny]

    def retrieve(self, request, pk=None):
        """
        Retorna um cliente
        """

        try:
            cliente = Cliente.objects.get(pk=pk)
            data = {
                'id': cliente.id,
                'nome': cliente.nome,
                'sobrenome': cliente.sobrenome,
                "cpf_cnpj": cliente.cpf_cnpj,
                'email': cliente.email,
                'telefone': cliente.telefone,
                'endereco': cliente.endereco,
            }

            return Response(data, status=status.HTTP_200_OK)
        
        except Cliente.DoesNotExist:
            return Response({'error': 'Cliente não encontrado'}, status=status.HTTP_404_NOT_FOUND)
        
    def list(self, request):
        """
        Lista todos os clientes
        """

        clientes = Cliente.objects.all()
        data = []
        for cliente in clientes:
            data.append({
                'id': cliente.id,
                'nome': cliente.nome,
                'sobrenome': cliente.sobrenome,
                "cpf_cnpj": cliente.cpf_cnpj,
                'email': cliente.email,
                'telefone': cliente.telefone,
                'endereco': cliente.endereco,
            })

        return Response(data, status=status.HTTP_200_OK)
    
    def create(self, request):
        """
        Cria um cliente
        """

        try:
            nome = request.data['nome']
            sobrenome = request.data['sobrenome']
            cpf_cnpj = request.data['cpf_cnpj']
            email = request.data['email']
            telefone = request.data['telefone']
            endereco = request.data['endereco']

            # Verifica se os campos existem
            if not nome or not sobrenome or not email or not telefone or not endereco or not cpf_cnpj:
                return Response({'error': 'Dados inválidos'}, status=status.HTTP_400_BAD_REQUEST)
            
            # Verifica os campos são válidos
            if len(nome) < 3 or len(sobrenome) < 3 or len(email) < 3 or len(telefone) < 3 or len(endereco) < 3:
                return Response({'error': 'Dados inválidos', 'message': 'O minimo de caracteres para os campos é 3'}, status=status.HTTP_400_BAD_REQUEST)
            
            # Verifica se o cpf_cnpj é valido
            if len(cpf_cnpj) != 11 and len(cpf_cnpj) != 14:
                return Response({'error': 'Dados inválidos', 'message': 'CPF/CNPJ inválido'}, status=status.HTTP_400_BAD_REQUEST)


            # Verifica se o email é valido
            if '@' not in email:
                return Response({'error': 'Dados inválidos', 'message': 'Email inválido'}, status=status.HTTP_400_BAD_REQUEST)
            
            
            # Verifica se o email já foi cadastrado
            if Cliente.objects.filter(email=email).exists():
                return Response({'error': 'Dados inválidos', 'message': 'Email já cadastrado'}, status=status.HTTP_400_BAD_REQUEST)
            
            # Verifica se o cpf_cnpj já foi cadastrado
            if Cliente.objects.filter(cpf_cnpj=cpf_cnpj).exists():
                return Response({'error': 'Dados inválidos', 'message': 'CPF/CNPJ já cadastrado'}, status=status.HTTP_400_BAD_REQUEST)

            cliente = Cliente.objects.create(
                nome=nome,
                sobrenome=sobrenome,
                cpf_cnpj=cpf_cnpj,
                email=email,
                telefone=telefone,
                endereco=endereco
            )

            return Response({'id': cliente.id}, status=status.HTTP_201_CREATED)
        
        except KeyError:
            return Response({'error': 'Dados inválidos', 'message': 'Campos obrigatórios faltando'}, status=status.HTTP_400_BAD_REQUEST)
            
    
    def update(self, request, pk):
        """
        Atualiza um cliente existente
        """

        try:
            cliente = Cliente.objects.get(pk=pk)

            if not cliente.ativo:
                return Response({'error': 'Cliente desativado'}, status=status.HTTP_400_BAD_REQUEST)
            

            nome = request.data.get('nome')
            sobrenome = request.data.get('sobrenome')
            cpf_cnpj = request.data.get('cpf_cnpj')
            email = request.data.get('email')
            telefone = request.data.get('telefone')
            endereco = request.data.get('endereco')

            if nome:
                if len(nome) < 3:
                    return Response({'error': 'Dados inválidos', 'message': 'O minimo de caracteres para o nome é 3'}, status=status.HTTP_400_BAD_REQUEST)
                cliente.nome = nome
            elif sobrenome:
                if len(sobrenome) < 3:
                    return Response({'error': 'Dados inválidos', 'message': 'O minimo de caracteres para o sobrenome é 3'}, status=status.HTTP_400_BAD_REQUEST)
                cliente.sobrenome = sobrenome
            elif cpf_cnpj:
                if len(cpf_cnpj) != 11 and len(cpf_cnpj) != 14:
                    return Response({'error': 'Dados inválidos', 'message': 'CPF/CNPJ inválido'}, status=status.HTTP_400_BAD_REQUEST)
                if Cliente.objects.filter(cpf_cnpj=cpf_cnpj).exists():
                    return Response({'error': 'Dados inválidos', 'message': f'CPF/CNPJ já cadastrado {cpf_cnpj}'}, status=status.HTTP_400_BAD_REQUEST)
                cliente.cpf_cnpj = cpf_cnpj
            elif email:
                if '@' not in email:
                    return Response({'error': 'Dados inválidos', 'message': 'Email inválido'}, status=status.HTTP_400_BAD_REQUEST)
                if Cliente.objects.filter(email=email).exists():
                    return Response({'error': 'Dados inválidos', 'message': f'Email já cadastrado {email}'}, status=status.HTTP_400_BAD_REQUEST)
                cliente.email = email
            elif telefone:
                if len(telefone) < 3:
                    return Response({'error': 'Dados inválidos', 'message': 'O minimo de caracteres para o telefone é 3'}, status=status.HTTP_400_BAD_REQUEST)
                cliente.telefone = telefone
            elif endereco:
                if len(endereco) < 3:
                    return Response({'error': 'Dados inválidos', 'message': 'O minimo de caracteres para o endereco é 3'}, status=status.HTTP_400_BAD_REQUEST)
                cliente.endereco = endereco
            else:
                return Response({'error': 'Dados inválidos', 'message': 'Nenhum campo para atualizar'}, status=status.HTTP_400_BAD_REQUEST)

            cliente.save()

            data = {
                'id': cliente.id,
                'nome': cliente.nome,
                'sobrenome': cliente.sobrenome,
                "cpf_cnpj": cliente.cpf_cnpj,
                'email': cliente.email,
                'telefone': cliente.telefone,
                'endereco': cliente.endereco,
            }

            return Response(data, status=status.HTTP_200_OK)
        
        except Cliente.DoesNotExist:
            return Response({'error': 'Cliente não encontrado'}, status=status.HTTP_404_NOT_FOUND)
        
    def destroy(self, request, pk):
        """
        Desativa um cliente
        """

        try:
            cliente = Cliente.objects.get(pk=pk)
            if not cliente.ativo:
                return Response({'error': 'Cliente já desativado'}, status=status.HTTP_400_BAD_REQUEST)
            cliente.ativo = False
            cliente.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        
        except Cliente.DoesNotExist:
            return Response({'error': 'Cliente não encontrado'}, status=status.HTTP_404_NOT_FOUND)
    
