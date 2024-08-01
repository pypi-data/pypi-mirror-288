from rest_framework import serializers
from nautobot_ui_plugin.models import NautobotSavedTopology
import datetime


class NautobotSavedTopologySerializer(serializers.ModelSerializer):

    created_by = serializers.CharField(read_only=True)
    timestamp = serializers.DateTimeField(read_only=True)

    def to_internal_value(self, data):
        validated = {
            'name': str(data.get('name').strip() or f"{self.context['request'].user} - {datetime.datetime.now()}"),
            'topology': data.get('topology'),
            'layout_context': data.get('layout_context'),
            'created_by': self.context['request'].user,
            'timestamp': str(datetime.datetime.now())
        }
        return validated

    class Meta:
        model = NautobotSavedTopology
        fields = [
            "id", "name", "topology", "layout_context", "created_by", "timestamp",
        ]
