import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist

from .models import Task
from user.models import CustomUser

@csrf_exempt
def create_task(request):
    if request.method != 'POST':
        return JsonResponse({"error": "Método não permitido."}, status=405)

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
    if request.method != 'GET':
        return JsonResponse({"Error": "Método não permitido."}, status=405)
    
    data = []
    
    tasks = Task.objects.all()
    
    for task in tasks:
        data.append({
            "id": task.id,
            "title": task.title,
            "status": task.status,
            "user_id": task.user_id
        })
    
    return JsonResponse(data, safe=False)

def list_task_by_user(request):
    if request.method != 'GET':
        return JsonResponse({"error": "Método não permitido."}, status=405)
    
    user_id = request.GET.get('id')

    if not user_id:
        return JsonResponse({"error": "Parâmetro 'id' é obrigatório."}, status=400)

    try:
        user = CustomUser.objects.get(id=user_id)
    except ObjectDoesNotExist:
        return JsonResponse({"error": "Usuário não encontrado."}, status=404)
    
    tasks = Task.objects.filter(user=user)
    
    data = []
    
    for task in tasks:
        data.append({
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "status": task.status,
        })

    
    
    return JsonResponse(data, safe=False, status=200)

@csrf_exempt
def mark_task_completed(request):
    if request.method != 'PATCH':
        return JsonResponse({'error': "Método não permitido."}, status=405)
    
    task_id = request.GET.get('task_id')
    
    if not task_id:
        return JsonResponse({'error': "Paramêtros 'task' é obrigatório."}, status=400)
    
    task = Task.objects.get(id=task_id)
    
    try:
        task.status = "completed"
        task.save()
        
        return JsonResponse({
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "status": task.status,
            "user": task.user_id
        }, status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
   
@csrf_exempt 
def delete_task(request):
    if request.method != 'DELETE':
        return JsonResponse({'error': "Método não permitido."}, status=405)
    
    task_id = request.GET.get('task_id')
    
    if not task_id:
        return JsonResponse({'error': "O paramêtro 'task_id' é obrigatório."}, 400)
    
    task = Task.objects.get(id=task_id)
    
    try:
        task.delete()
        return JsonResponse({'warning': "Deletado com sucesso."}, status=204)
    except Exception:
        return JsonResponse({'erro': "Erro interno no servidor."}, status=500)