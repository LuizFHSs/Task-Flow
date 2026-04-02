import json # Para trabalhar com leituras e gravações de arquivos JSON

from django.http import JsonResponse # Para retornar respostas JSON
from django.views.decorators.csrf import csrf_exempt 
from django.db import IntegrityError

from .models import CustomUser

@csrf_exempt
def create_user(request):
    if request.method != 'POST': # Verificar se o método da requisição. Se foi feita uma requisição do tipo POST
        return JsonResponse({"error": "Método não permitido."}, status=405) # 405 (Método não permitido)
    
    # Tratativa de erro, caso a requisição não tenha enviado um body
    try:
        data = json.loads(request.body) # Armazena o body da requisição ( o que o Front está enviando para o back)
    except json.JSONDecodeError:
        return JsonResponse({"error": "JSON inválido."}, status=400) # Caso não receba um body, retorna mensagem de erro, informando que não foi possível ler o body e retorna para o response o status_code de 400 (erro no lado cliente, ao enviar uma requisição)
    
    name = data.get("name")
    email = data.get("email")
    
    if not name or not email: # Se o body estiver vazio ou não conter um contéudo: Nome ou email
        return JsonResponse({"error": "Nome e email são campos obrigatórios!"}, status=400) # Retorna uma mensagem de erro, informando que não foi passado nenhum valor obrigatório, passando para o response o status_code de 400 (erro no lado do cliente, pois cliente errou ao digitar algo ou passar valores em branco)
    
    try:
        # Salva um usuário, com nome e email fornecidos no body
        user = CustomUser.objects.create(name=name, email=email)

        return JsonResponse({
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "created_at": user.created_at
            }, status=201) # Retornar uma mensagem informando que um usuário foi criado, retornando para o response o status_code de 201 (Todos os passos de conexão, requisição e resposta foram bem sucedidos e usuário foi criado)
    except IntegrityError:
        return JsonResponse({"error": "Este email já está cadastrado!"}, status=409) # Retornar um erro, informado que não foi possível criar um usuário, retornando para o response o status_code de 409 (erro no lado do servidor, pois não foi possível enviar os dados para o banco de dados)
    except Exception as e:
        return JsonResponse({"error": "Erro interno no servidor.", "error_message": str(e)}, status=500)
      
@csrf_exempt  
def list_user(request):
    # Valida se o método é GET, caso contrário retornar um mensagem de erro, informado que o método de envio da requisição não é permitido (405)
    if request.method != 'GET':
        return JsonResponse({"error": "Método não permitido."}, status=405)
   
    users = CustomUser.objects.all() # Busca todos os usuários já cadastrados
   
    data = [] # Criado para guardar os valores dos usuários e retornar no response
    
    for user in users:
        data.append({"id": user.id, "name": user.name, "email": user.email}) # Adiciona os valores de cada usuário na lista
            
    return JsonResponse(data, safe=False, status=200)