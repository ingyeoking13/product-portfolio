from fastapi import Depends
from src.repository.product import ProductRepo
from src.models.product_dto import ProductDto
from elasticsearch import Elasticsearch

class SearchService:

    def __init__(self, 
                 product_db: ProductRepo =  Depends(ProductRepo)) -> None:
        self.product_db = product_db
    
    def search(self, keyword: str):
        es = Elasticsearch('https://localhost:9200/',
                           api_key='bTNzeFdJMEI3b21QWkltSE9IMjQ6X0d6bkIxOEFTbmFUNF9VWEJTUHNKdw==',
                           verify_certs=False)
        
        result = es.search(index='search-*', query={
            "wildcard":{
                'description': '*e*'
            }
        },size=100)

        results = []
        for hit in result['hits']['hits']:
            results.append(ProductDto(**hit['_source']))
        return results
        

    def insert_to_elastic(self):
        es = Elasticsearch('https://localhost:9200/',
                           api_key='bTNzeFdJMEI3b21QWkltSE9IMjQ6X0d6bkIxOEFTbmFUNF9VWEJTUHNKdw==',
                           verify_certs=False
                           )
                    #    {
                    #   "id": "9VMeWI0BoZhnFhddALYT",
                    #   "name": "정요한",
                    #   "api_key": "qQc-1ttjSnqHIzirxSPujw",
                    #   "encoded": "OVZNZVdJMEJvWmhuRmhkZEFMWVQ6cVFjLTF0dGpTbnFISXppcnhTUHVqdw==",
                    #   "beats_logstash_format": "9VMeWI0BoZhnFhddALYT:qQc-1ttjSnqHIzirxSPujw"
                    # }
        # sou = es.get(index='*', id=1, error_trace=True)
        es.info()
        # print(sou)
        all_products = self.product_db.get_all_product()

        for product in all_products:
            es.index(
                index=f'search-{product.user_id}',
                id=product.id,
                document= product.model_dump()
            )

