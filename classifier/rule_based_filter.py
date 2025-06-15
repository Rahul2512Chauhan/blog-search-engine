def is_valid_blog(post:dict) -> bool:
    
    """
    Rule-based filter for checking if a post is a real blog.
    Input: post = {
        "title": ...,
        "author": ...,
        "date": ...,
        "content": ...
    }
    """

    title = post.get("title","")
    content = post.get("content","")
    date = post.get("date","")
    word_count = len(content.split())
    paargraph_count = content.count("\n")

    if len(title)< 20 :
        return False

    if not date or date == "Unknown":
        return False

    if word_count < 300:
        return False

    if paargraph_count<5:
        return False

    return True    