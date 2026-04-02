import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist

from .models import Task
from user.models import CustomUser

@csrf_exempt
def task_handler(request):
    if request.method == 'GET':
        return list_task(request)
    
    if request.method == 'POST':
        return create_task(request)

    return JsonResponse({"Error": "Método não permitido."}, status=405)

@csrf_exempt
def task_detail_or_delete(request, id):
    if request.method == 'GET':
        return task_detailed(request, id)
    
    if request.method == 'DELETE':
        return delete_task(request, id)
    
    return JsonResponse({"Error": "Método não permitido."}, status=405)

def create_task(request):
    # Ler JSON
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "JSON inválido."}, status=400)

    # Validar campos obrigatórios
    title = data.get("title")
    description = data.get("description")
    user_id = data.get("user")

    if not title or not user_id:
        return JsonResponse({"error": "Título e usuário são obrigatórios."}, status=400)

    # Validar usuário
    try:
        user = CustomUser.objects.get(id=user_id)
    except ObjectDoesNotExist:
        return JsonResponse({"error": "Usuário não encontrado."}, status=404)

    # Criar tarefa
    try:
        task = Task.objects.create(
            title=title,
            description=description,
            user=user
        )

        return JsonResponse({
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "status": task.status,
            "user": task.user_id,
            "created_at": task.created_at
        }, status=201)

    except Exception:
        return JsonResponse({"error": "Erro interno do servidor."}, status=500)

def list_task(request):
    data = []
    
    tasks = Task.objects.all()
    
    for task in tasks:
        data.append({
            "id": task.id,
            "title": task.title,
            "status": task.status,
            "user_id": task.user_id
        })
    
    return JsonResponse(data, safe=False, status=200)

def task_detailed(request, id):
    if not id:
        return JsonResponse({'error': "Paramêtro 'id' é obrigatório."}, status=400)
    
    task = Task()
    
    try:
        task = Task.objects.get(id=id)
    except task.DoesNotExist:
        return JsonResponse({'erro': "Tarefa não encontrada."}, status=404)
    
    data = {
        "id": task.id,
        "title": task.title,
        "description": task.description,
        "status": task.status,
        "user_id": task.user_id,
        "created_at": task.created_at,
        "completed_at": task.completed_at
    }
    
    return JsonResponse(data, safe=False, status=200)

@csrf_exempt
def mark_task_completed(request, id):
    if not id:
        return JsonResponse({'error': "Paramêtros 'id' é obrigatório."}, status=400)
    
    task = Task()
    
    try:
        task = Task.objects.get(id=id)
    except task.DoesNotExist:
        return JsonResponse({'error': "Tarefa não encontrada."}, status=404)
    
    if task.status != "completed":
        task.status = "completed"
        
        try:
            task.save()
        except Exception:
            return JsonResponse({'error': "Erro interno no servidor."}, status=500)
    
    data = {
        "id": task.id,
        "title": task.title,
        "description": task.description,
        "status": task.status,
        "user": task.user_id,
        "completed_at": task.completed_at
    }
    
    return JsonResponse(data, safe=False, status=200)

@csrf_exempt
def delete_task(request, id):    
    if not id:
        return JsonResponse({'error': "O paramêtro 'task_id' é obrigatório."}, 400)
    
    task = Task()
    
    try:
        task = Task.objects.get(id=id)
    except task.DoesNotExist:
        return JsonResponse({'erro': "Tarefa não registrada ou já deletada."}, status=404)
    
    try:
        task.delete()
        return JsonResponse({'warning': "Deletado com sucesso."}, status=204)  
    except Exception:
        return JsonResponse({'erro': "Erro interno no servidor."}, status=500)