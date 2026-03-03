import pytest

from src.utils.validators import assert_user_schema, assert_post_schema, assert_comment_schema


def test_the_comments_of_the_first_3_posts_of_a_user(users_client, posts_client, comments_client, test_data):
    # get the userId and check the details
    response_user = users_client.get_user_by_id(test_data["sample_user_ids"][0])
    assert response_user.status_code == 200, f"Status is not 200"
    data_user = response_user.json()
    user_id = data_user["id"]
    assert_user_schema(data_user)

    # get the first 3 posts of the user previously selected
    response_posts = posts_client.get_posts_by_user(user_id)
    assert response_posts.status_code == 200, f"Status is not 200"
    data_post = response_posts.json()
    total_posts = 3  # set the limit for how many posts we need per user
    all_3_posts_per_user = []
    list_of_posts_ids = []
    for post in data_post:
        if total_posts > 0:
            all_3_posts_per_user.append(post)  # add each post in a list
            list_of_posts_ids.append(post["id"])  # add the first 3 postIds in another list
            total_posts = total_posts - 1
            assert_post_schema(post)

    # get all comments for those 3 posts previously selected
    list_of_comments = []
    for post_id in list_of_posts_ids:
        response_comments = comments_client.get_comments_by_post(post_id)
        assert response_comments.status_code == 200, f"Status is not 200"
        data_comments = response_comments.json()
        assert data_comments[0]["postId"] == post_id, f"The comment ID: {data_comments[0]["id"]} is not part of the post"
        list_of_comments.append(data_comments)  # add all comments from each post in a list

    # go through the list of each 5 comments of the list of comments and check its schema
    for comments_per_post in list_of_comments:
        for comment in comments_per_post:
            assert_comment_schema(comment)
