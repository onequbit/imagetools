import subprocess


def get_docker_images():
    output = subprocess.run('docker images', capture_output=True, shell=True, check=True).stdout
    lines = str(output, 'utf-8').split('\n')
    if len(lines) == 1:
        print("no docker images detected")
    headers = lines[0].split()
    assert headers[0] == 'REPOSITORY', 'unexpected output from "docker images"'
    return lines[1:]

def get_image_ids(images):
    results = []
    for image in images:
        parts = image.split()
        results.append(parts[2])
    return results

def delete_images(image_ids):
    for id in image_ids:
        delete_cmd = f"docker image rm --force {id}"
        output = subprocess.run(delete_cmd, capture_output=True, shell=True, check=True).stdout
        print(str(output, 'utf-8'))