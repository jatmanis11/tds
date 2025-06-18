import json
import logging
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .unified_service import process_tds_question

logger = logging.getLogger(__name__)

@csrf_exempt
@require_http_methods(["POST", "GET"])
def api_handler(request):
    """Single API handler for all TDS Virtual TA requests"""
    
    if request.method == "GET":
        path = request.path
        if 'health' in path:
            return JsonResponse({'status': 'healthy', 'service': 'TDS Virtual TA'})
        else:
            return JsonResponse({
                'message': 'TDS Virtual TA API',
                'version': '1.0.0',
                'usage': 'POST with {"question": "your question"}'
            })
    
    elif request.method == "POST":
        try:
            data = json.loads(request.body)
            question = data.get('question', '').strip()
            image_b64 = data.get('image', '')
            
            if not question:
                return JsonResponse({
                    'answer': 'Please provide a question.',
                    'links': [{'url': 'https://discourse.onlinedegree.iitm.ac.in/', 'text': 'TDS Forum'}]
                }, status=400)
            
            # Use single unified function
            response = process_tds_question(question, image_b64)
            
            return JsonResponse(response, json_dumps_params={'ensure_ascii': False})
            
        except json.JSONDecodeError:
            return JsonResponse({
                'answer': 'Invalid JSON format.',
                'links': [{'url': 'https://discourse.onlinedegree.iitm.ac.in/', 'text': 'TDS Forum'}]
            }, status=400)
        except Exception as e:
            logger.error(f"API error: {e}")
            return JsonResponse({
                'answer': 'An error occurred. Please try again.',
                'links': [{'url': 'https://discourse.onlinedegree.iitm.ac.in/', 'text': 'TDS Forum'}]
            }, status=500)
