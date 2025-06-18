import json
import logging
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .ai_service import MultiAIService
from .data_scraper import DataScraper

logger = logging.getLogger(__name__)

@csrf_exempt
@require_http_methods(["POST", "GET"])
def api_handler(request):
    """Single handler for all API requests"""
    
    if request.method == "GET":
        # Health check or info endpoint
        path = request.path
        if path.endswith('/health/'):
            return health_check(request)
        elif path.endswith('/info/'):
            return api_info(request)
        else:
            return JsonResponse({
                'message': 'TDS Virtual TA API',
                'version': '1.0.0',
                'endpoints': {
                    'main': '/api/',
                    'health': '/api/health/',
                    'info': '/api/info/'
                }
            })
    
    elif request.method == "POST":
        # Main virtual TA functionality
        return virtual_ta_main(request)

def virtual_ta_main(request):
    """Main TDS Virtual TA logic"""
    try:
        data = json.loads(request.body)
        question = data.get('question', '').strip()
        image_b64 = data.get('image', '')
        
        if not question:
            return JsonResponse({
                'answer': 'Please provide a question for the TDS Virtual TA.',
                'links': [{'url': 'https://discourse.onlinedegree.iitm.ac.in/', 'text': 'TDS Course Forum'}]
            }, status=400)
        
        # Initialize services
        ai_service = MultiAIService()
        data_scraper = DataScraper()
        
        # Get context and generate answer
        context = data_scraper.search_relevant_content(question)
        answer_data = ai_service.generate_answer(question, context, "")
        
        return JsonResponse(answer_data, json_dumps_params={'ensure_ascii': False})
        
    except Exception as e:
        logger.error(f"API error: {e}")
        return JsonResponse({
            'answer': 'An error occurred. Please try again.',
            'links': [{'url': 'https://discourse.onlinedegree.iitm.ac.in/', 'text': 'TDS Forum'}]
        }, status=500)

def health_check(request):
    """Health check endpoint"""
    return JsonResponse({
        'status': 'healthy',
        'service': 'TDS Virtual TA'
    })

def api_info(request):
    """API info endpoint"""
    return JsonResponse({
        'name': 'TDS Virtual TA',
        'version': '1.0.0',
        'description': 'Virtual Teaching Assistant for IIT Madras Tools in Data Science course'
    })
