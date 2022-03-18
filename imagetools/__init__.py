import subprocess

import docker # https://docker-py.readthedocs.io/en/stable/

_docker_client = docker.from_env()

def get_image_collection_list():
    images = _docker_client.images.list()
    images_listing = [f"{image.short_id}:{image.tags}" for image in images]
    return images_listing

def get_docker_images():
    output = subprocess.run('docker images --all', capture_output=True, shell=True, check=True).stdout
    lines = str(output, 'utf-8').split('\n')
    if len(lines) == 1:
        print("no docker images detected")
    headers = lines[0].split()
    assert headers[0] == 'REPOSITORY', 'unexpected output from "docker images"'
    return filter(lambda item: item, lines[1:])

def find_short_id(short_id):
    for image in _docker_client.images.list():
        if image.short_id == short_id:
            return image
    return None

def get_image_ids(images):
    results = []
    for image in images:
        parts = image.split()
        results.append(parts[2])
    return results

def delete_image(image_id):
    try:
        _docker_client.images.remove(image_id, force=True)
    except:
        print(f"error occurred attempting to remove image with id: {image_id}")

def delete_images(image_ids):
    for id in image_ids:
        py_short_id = f"sha256:{id[:-2]}"
        image = find_short_id(py_short_id)
        if image is not None:
            print(f"deleting: {image.id} --> {image.tags}")
            delete_image(image.id)
                
        