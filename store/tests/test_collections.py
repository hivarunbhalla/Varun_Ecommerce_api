from django.contrib.auth.models import User
from rest_framework import status
import pytest
from model_bakery import baker
from store.models import Collection


@pytest.fixture
def create_collection(api_client):
    def do_create_collection(collection): # extra fn to take collection as input
        return api_client.post(path = '/store/collections/', data = collection,  format='json')
    return do_create_collection


@pytest.mark.django_db
class TestCreateCollection:
    # AAA (Arrange, Act, Assert) -> for any test
    
    # api_client  is a fixture definesd in test/conftest.py {it will be automatically executed}
    def test_if_user_is_anonymous_returns_401(self, create_collection):
        
        response = create_collection({
                'title' : 'a',
                'description' : 'Short Desc',
            }) 
        
        #assert
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        
    def test_if_user_is_not_admin_returns_403(self, authenticate,create_collection):
        authenticate()
        
        response = create_collection({
                'title' : 'a',
                'description' : 'Short Desc',
            })    
        
        assert response.status_code == status.HTTP_403_FORBIDDEN
        
    def test_if_data_is_invalid_returns_400(self, authenticate, create_collection):
        authenticate(is_staff = True)
        
        response = create_collection({
                'title' : '',
                'description' : '',
            })     
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['title'] is not None
        assert response.data['description'] is not None
    
    def test_if_data_is_valid_returns_201(self, authenticate, create_collection):
        authenticate(is_staff = True)
          
        response = create_collection({
                'title' : 'Test',
                'description' : 'Testing if data is valid',
            }) 
        
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['id'] > 0   # as id will be returened
    
 
@pytest.fixture
def retrieve_collection(api_client):
    def do_retrieve_collection(collection_id):
        return api_client.get(path = f'/store/collections/{collection_id}/')
    return do_retrieve_collection

@pytest.mark.django_db
class TestRetreiveCollection:
    def test_if_collection_exists_return_200(self, retrieve_collection):
        
        collection = baker.make(Collection)
        response = retrieve_collection(collection.id)
        
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data == {
            'id' : collection.id,
            'title' : collection.title,
            'description' : collection.description,
            'featured_product' : collection.featured_product
        }
        
           