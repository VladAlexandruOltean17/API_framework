def assert_user_schema(user: dict):
    """
    Verifică schema de bază pentru un user.
    Aruncă AssertionError dacă lipsesc câmpuri importante.
    """
    for key in ("id", "name", "username", "email", "address"):
        assert key in user, f"Userul nu contine campul obligatoriu: {key}"


def assert_post_schema(post: dict):
    """
    Verifică schema de bază pentru un post.
    """
    for key in ("userId", "id", "title", "body"):
        assert key in post, f"Postul nu contine campul obligatoriu: {key}"


def assert_comment_schema(comment: dict):
    """
    Verifică schema de bază pentru un comment.
    """
    for key in ("postId", "id", "name", "email", "body"):
        assert key in comment, f"Commentul nu contine campul obligatoriu: {key}"


def assert_valid_email(email: str):
    assert isinstance(email, str), "Email has to be a string"
    assert "@" in email, f"Invalid email (missing '@'): {email}"


def assert_post_title(title: str):
    assert isinstance(title, str), "Title has to be a string"
    assert len(title) > 3, f"Title has no more than 3 characters: {title}"


def assert_albums_schema(album: dict):
    for key in ("userId", "id", "title"):
        assert key in album, f"The album does not contain the field: {key}"
