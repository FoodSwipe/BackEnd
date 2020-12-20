import os


def generate_url_for_media_resources_in_object(serializer, object_name=None):
    front = "http" if os.getenv("IS_SECURE") else "https"
    if object_name is None:
        object_name = {}
    for target, field_name in object_name.items():
        if isinstance(serializer.data[target], list):
            for pivot_target in serializer.data[target]:
                pivot_target[field_name] = "{}://{}{}".format(front, os.getenv("BASE_URL"), pivot_target[field_name])
        else:
            t = serializer.data[target]
            t[field_name] = "{}://{}{}".format(front, os.getenv("BASE_URL"), t[field_name])
    return serializer


def generate_url_for_media_resources(serializer, param="image"):
    for target in serializer.data:
        front = "http" if os.getenv("IS_SECURE") else "https"
        if target[param]:
            target[param] = "{}://{}{}".format(front, os.getenv("BASE_URL"), target[param])
    return serializer


def generate_url_for_media_resource(serializer, param="image"):
    front = "http" if os.getenv("IS_SECURE") else "https"
    serializer[param] = "{}://{}{}".format(front, os.getenv("BASE_URL"), serializer[param])
    return serializer
