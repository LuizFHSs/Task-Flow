import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt 
from django.db import IntegrityError

from .models import CustomUser
from task.models import Task


@csrf_exempt
def users_handler(request):
    if request.method == 'GET':
        return list_user(request)
    
    if request.method == 'POST':
        return create_user(request)
    
    return JsonResponse({"error": "Método não permitido."}, status=405)

@csrf_exempt
def create_user(request):    
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "JSON inválido."}, status=400)
    
    name = data.get("name")
    email = data.get("email")
    
    if not name or not email:
        return JsonResponse({"error": "Nome e email são campos obrigatórios!"}, status=400)
    
    try:
        user = CustomUser.objects.create(name=name, email=email)

        return JsonResponse({
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "created_at": user.created_at
            }, status=201)
    except IntegrityError:
        return JsonResponse({"error": "Este email já está cadastrado!"}, status=409)
    except Exception as e:
        return JsonResponse({"error": "Erro interno no servidor.", "error_message": str(e)}, status=500)
      
@csrf_exempt  
def list_user(request):
    users = CustomUser.objects.all()
   
    data = []
    
    for user in users:
        data.append({"id": user.id, "name": user.name, "email": user.email})
            
    return JsonResponse(data, safe=False, status=200)

def list_tasks_by_user(request, id):
    if request.method != 'GET':
        return JsonResponse({"error": "Método não permitido."}, status=405)

    if not id:
        return JsonResponse({"error": "Parâmetro 'id' é obrigatório."}, status=400)
    
    try:
        user = CustomUser.objects.get(id=id)
    except CustomUser.DoesNotExist:
        return JsonResponse({"error": "Usuário não encontrado."}, status=404)
    
    tasks = Task.objects.filter(user=user)
    
    data = []
    
    for task in tasks:
        data.append({
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "status": task.status,
            "user_id": task.user_id,
            "created_at": task.created_at,
            "completed_at": task.completed_at
        })
    
    return JsonResponse(data, safe=False, status=200)