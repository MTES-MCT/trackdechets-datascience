
from .connectors import get_irep_data
from .serializers import IREPSerializer
from .models import IREP, db


def load_irep_data():
    db.connect()
    db.create_tables([IREP])
    data = get_irep_data()
    instances = []
    for irep in data:
        serializer = IREPSerializer(irep)
        serializer.to_internal_value()
        instances.append(serializer.instance)
        serializer.instance.save()