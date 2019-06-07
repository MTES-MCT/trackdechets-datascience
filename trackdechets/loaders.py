
from .connectors import get_irep_data, get_gerep_data
from .serializers import IREPSerializer, GEREPSerializer
from .models import IREP, GEREP, db


def load_irep_data():
    db.connect()
    db.create_tables([IREP])
    data = get_irep_data()
    instances = []
    for irep in data:
        serializer = IREPSerializer(irep)
        serializer.to_internal_value()
        instances.append(serializer.instance)
    with db.atomic():
        IREP.bulk_create(instances, chunk_size=100)


def load_gerep_data():
    db.connect()
    db.create_tables([GEREP])
    (producteurs, traiteurs) = get_gerep_data()
    instances = []
    for producteur in producteurs:
        serializer = GEREPSerializer(producteur, 'producteur')
        serializer.to_internal_value()
        instances.append(serializer.instance)
    for traiteur in traiteurs:
        serializer = GEREPSerializer(traiteur, 'traiteur')
        serializer.to_internal_value()
        instances.append(serializer.instance)
    print("Start loading data")
    with db.atomic():
        GEREP.bulk_create(instances, batch_size=100)
