import pytest
from src.utils.validators import assert_post_schema, assert_comment_schema


@pytest.mark.consistency
def test_user_posts_and_comments_relationship(posts_client, comments_client):
    """
    Scenariu mai complex:
    - alegem un user_id (ex: 1)
    - luăm posts pentru acel user
    - alegem un post_id din listă
    - luăm comments pentru acel post
    - verificăm că:
        * comments aparțin acelui post
        * schema de comment este validă
    """
    user_id = 1

    # 1) Luăm posts pentru user_id
    posts_response = posts_client.get_posts_by_user(user_id)
    assert posts_response.status_code == 200, "Nu am primit 200 pentru posts by user"

    posts = posts_response.json()
    assert len(posts) > 0, f"Userul {user_id} nu are niciun post în API."

    # 2) alegem un post_id
    first_post = posts[0]
    assert_post_schema(first_post)
    post_id = first_post["id"]

    # 3) luăm comments pentru post_id
    comments_response = comments_client.get_comments_by_post(post_id)
    assert comments_response.status_code == 200, "Nu am primit 200 pentru comments by post"

    comments = comments_response.json()
    assert len(comments) > 0, f"Postul {post_id} nu are comentarii în API."

    # 4) verificăm consistența
    for comment in comments:
        assert_comment_schema(comment)
        assert comment["postId"] == post_id, (
            f"Comentul are postId diferit ({comment['postId']}) față de post_id={post_id}"
        )
