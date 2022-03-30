from django_elasticsearch_dsl import Document
from django_elasticsearch_dsl.registries import registry
from .models import Advertisement

@registry.register_document
class AdvertisementDocument(Document):
    class Index:
        name = 'advertisements'
        settings = {
        'number_of_shards': 1,
        'number_of_replicas': 0
        }
        
    class Django:
        model = Advertisement
        fields = [
            'exchange',
            'advertiser_no',
            'advertiser',
            'orders',
            'completion',
            'price',
            'fiat',
            'payment',
            'available',
            'limit'
        ]
            