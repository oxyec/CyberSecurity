import pytest
from websitebackend.models import Post

@pytest.mark.django_db
def test_create_post():
    post = Post.objects.create(title="Merhaba", content="Bu bir testtir.")
    assert Post.objects.count() == 1
