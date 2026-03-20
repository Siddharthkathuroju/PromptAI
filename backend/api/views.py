import logging

# Initialize logger
logger = logging.getLogger(__name__)

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import JsonResponse, HttpResponse
from reportlab.pdfgen import canvas
from django.urls import path

from .serializers import AnalyzePlanRequestSerializer, AnalyzePlanResponseSerializer
from .gemini_service import GeminiService
from django.http import JsonResponse

def api_root(request):
    return JsonResponse({
        "project": "Explain My Plan AI",
        "status": "online",
        "endpoints": ["/api/analyze-plan/"]
    })

def health_check(request):
    """Health check endpoint for monitoring."""
    return JsonResponse({'status': 'healthy', 'service': 'intuitive-draft-api'})


class AnalyzePlanView(APIView):
    """
    API endpoint for analyzing plans.
    """
    
    def post(self, request):
        """
        Analyze a plan idea.
        """
        serializer = AnalyzePlanRequestSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(
                {
                    'detail': 'Invalid request',
                    'errors': serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            idea = serializer.validated_data['idea']
            
            # Initialize Gemini service and analyze
            gemini_service = GeminiService()
            result = gemini_service.analyze_plan(idea)

            # Log the raw response
            logger.info(f"Raw response from GeminiService: {result}")

            # Validate output
            output_serializer = AnalyzePlanResponseSerializer(data=result)
            if not output_serializer.is_valid():
                logger.error(f"Response validation errors: {output_serializer.errors}")
                return Response(
                    {
                        'detail': 'Error validating response',
                        'errors': output_serializer.errors,
                        'raw_response': result  # Include raw response for debugging
                    },
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            
            return Response(output_serializer.validated_data, status=status.HTTP_200_OK)
        
        except ValueError as e:
            logger.warning(f"ValueError: {str(e)}")
            return Response(
                {
                    'detail': str(e)
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logger.error(f"Unhandled exception: {str(e)}")
            return Response(
                {
                    'detail': f'An error occurred: {str(e)}'
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


def export_to_pdf(request):
    """Export the results as a PDF file."""
    # Create a PDF response
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="results.pdf"'

    # Generate PDF content
    p = canvas.Canvas(response)
    p.drawString(100, 750, "Exported Results")
    p.drawString(100, 730, "Here is the content of the results.")
    # Add more content as needed
    p.showPage()
    p.save()

    return response


# Define urlpatterns as an empty list
urlpatterns = [
    path('health-check/', health_check, name='health_check'),
]

# Add the new endpoint to the URL patterns
urlpatterns += [
    path('export-to-pdf/', export_to_pdf, name='export_to_pdf'),
]
