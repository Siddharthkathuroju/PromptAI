from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import JsonResponse

from .serializers import AnalyzePlanRequestSerializer, AnalyzePlanResponseSerializer
from .gemini_service import GeminiService


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
                {'detail': 'Invalid request', 'errors': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            idea = serializer.validated_data['idea']
            
            # Initialize Gemini service and analyze
            gemini_service = GeminiService()
            result = gemini_service.analyze_plan(idea)
            
            # Validate output
            output_serializer = AnalyzePlanResponseSerializer(data=result)
            if not output_serializer.is_valid():
                return Response(
                    {'detail': 'Error validating response', 'errors': output_serializer.errors},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            
            return Response(output_serializer.validated_data, status=status.HTTP_200_OK)
        
        except ValueError as e:
            return Response(
                {'detail': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {'detail': f'An error occurred: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
