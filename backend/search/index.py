def index_post(content):
    tags = extract_hashtags(content)
    save_tags(tags)
