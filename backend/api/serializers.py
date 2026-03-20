from rest_framework import serializers


class PlanStepSerializer(serializers.Serializer):
    title = serializers.CharField()
    description = serializers.CharField()


class StructuredPlanSerializer(serializers.Serializer):
    goal = serializers.CharField()
    method = serializers.CharField()
    steps = PlanStepSerializer(many=True)
    timeline = serializers.CharField()


class AnalyzePlanRequestSerializer(serializers.Serializer):
    idea = serializers.CharField(min_length=1, max_length=5000)


class AnalyzePlanResponseSerializer(serializers.Serializer):
    clarity_score = serializers.IntegerField(min_value=0, max_value=100)
    structured_plan = StructuredPlanSerializer()
    missing_elements = serializers.ListField(child=serializers.CharField())
    simplified_version = serializers.CharField()
    actionable_steps = serializers.ListField(child=serializers.CharField())
