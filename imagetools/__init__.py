import subprocess

import docker # https://docker-py.readthedocs.io/en/stable/

_docker_client = docker.from_env()

def get_image_collection_list():
    images = _docker_client.images.list(all=True)
    # images_listing = [f"{image.short_id}:{image.tags}" for image in images]
    return images

def is_docker_images_header(input_line):
    parts = input_line.split()
    return parts[0] == 'REPOSITORY'

def get_docker_images():
    output = subprocess.run('docker images --all', capture_output=True, shell=True, check=True).stdout
    lines = str(output, 'utf-8').split('\n')
    if len(lines) == 1:
        print("no docker images detected")
    
    assert is_docker_images_header(lines[0]), 'unexpected output from "docker images"'
    return filter(lambda item: item, lines[1:])

def find_short_id(short_id):
    for image in _docker_client.images.list():
        if image.short_id == short_id:
            return image
    return None

def parse_image_id(docker_images_str):
    parts = docker_images_str.split()
    assert len(parts) == 7, 'error parsing output from "docker images"'
    return parts[2]

def get_image_ids(images):
    results = []
    for image_str in images:
        results.append(parse_image_id(image_str))
    
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
        assert image is not None, f"image: {image.short_id} not found"
        print(f"deleting: {image.id} --> {image.tags}")
        delete_image(image.id)

def get_lineage():
    image_collection_list = get_image_collection_list()
    images = []
    for image in image_collection_list:
        image_obj = {}
        name = '_'.join(image.tags) 
        image_parent = image.attrs['Parent']
        image_obj['name'] = name
        image_obj['id'] = image.id
        image_obj['short_id'] = image.id[7:19]
        image_obj['parent'] = image_parent if len(image_parent)>0 else 'None'
        images.append(image_obj)

    parents, children = [],[]
    for i in images:
        children.append(i['id'])
        if i['parent'] != 'None':
            parents.append(i['parent'])        
        
    leaf_children = []
    root_parents = []

    for image in images:
        if image['id'] in children and image['id'] not in parents:
            leaf_children.append(image['id'])
            image['node'] = 'leaf'
        elif image['id'] in parents and image['parent'] == 'None':
            root_parents.append(image['id'])
            image['node'] = 'root'
        else:
            image['node'] = 'node'
    return images

def get_leaves(lineage):
    leaves = []
    for member in lineage:
        if member['node'] == 'leaf':
            leaves.append(member['short_id'])
    return leaves

def get_roots(lineage):
    roots = []
    for member in lineage:
        if member['node'] == 'root':
            roots.append(member['short_id'])
    return roots
  
        