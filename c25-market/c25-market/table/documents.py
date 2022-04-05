from django_elasticsearch_dsl import Document
from django_elasticsearch_dsl.registries import registry
from .models import Advertisement, Comment

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
            

@registry.register_document
class CommentDocument(Document):
    class Index:
        name = 'comments'
        settings = {
        'number_of_shards': 1,
        'number_of_replicas': 0
        }

    class Django:
        model = Comment
        fields = [
            'advertiser_no',
            'comment'
        ]
    



# @registry.register_document
# class SignUp(Document):
#     class Index:
#         name = 'register'
#         settings = {
#         'number_of_shards': 1,
#         'number_of_replicas': 0
#         }

#     class Django:
#         model = register
#         fields = [
#             'firstname',
#             'lastname',
#             'email',
#             'status',
#             'role',
#         ]
    