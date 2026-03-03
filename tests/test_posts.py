import pytest
from src.utils.validators import assert_post_schema, assert_post_title, assert_comment_schema


@pytest.mark.posts
def test_get_all_posts_returns_list_of_valid_posts(posts_client):
    response = posts_client.get_all_posts()

    assert response.status_code == 200, "Status code nu este 200 pentru /posts"
    data = response.json()
    assert isinstance(data, list), "Răspunsul /posts nu este listă"
    assert len(data) > 0, "Lista de posts este goală"

    for post in data:
        assert_post_schema(post)


@pytest.mark.posts
@pytest.mark.parametrize("user_id", [1, 2, 3])
def test_get_posts_by_user(posts_client, user_id):
    """
    Verificăm:
    - /posts?userId={id} răspunde 200
    - toate postările au userId = id
    """
    response = posts_client.get_posts_by_user(user_id)
    assert response.status_code == 200, f"Status code nu este 200 pentru userId={user_id}"

    posts = response.json()
    # Pot fi 0 postări, dar dacă există, toate trebuie să aibă userId = user_id
    for post in posts:
        assert_post_schema(post)
        assert post["userId"] == user_id, (
            f"Post cu userId diferit ({post['userId']}) față de cel cerut ({user_id})"
        )
        # test new post title validation
        assert_post_title(post["title"]), f"Title {post["title"]} has less than 3 characters"


@pytest.mark.posts
@pytest.mark.parametrize("post_id", [1, 2])
def test_get_all_comments_for_multiple_posts(comments_client, post_id):
    response = comments_client.get_comments_by_post(post_id)
    assert response.status_code == 200, f"Status cod is not 200 for postId={post_id}"

    comments = response.json()
    for comment in comments:
        assert_comment_schema(comment)
        assert comment["postId"] == post_id, (f"Comment with different postId {comment["postId"]} "
                                              f"than the expected one {post_id}")
