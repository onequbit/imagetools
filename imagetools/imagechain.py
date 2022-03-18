#!/usr/bin/python3
import argparse, json, os, subprocess, sys
import docker # https://docker-py.readthedocs.io/en/stable/




class Main:
    @staticmethod
    def parse_cmd_args(args_to_parse):
        cli = argparse.ArgumentParser(
            prog=(os.path.basename(__file__)),
            description=" - a tool for mapping the contents of a directory")
        # cli.add_argument( '-d', '--delete', action='store_true',
        #     help="delete the indicated items")
        # cli.add_argument(dest='text', nargs='*', default='', type=str, 
        #     help='substrings to filter images list.')
        
        result = cli.parse_args(args_to_parse)        
        return result

    @staticmethod
    def send_stdout(data):
        if data is not None:
            for item in data:
                print(item)

    @staticmethod
    def get_docker_images():
        output = subprocess.run('docker images', capture_output=True, shell=True, check=True).stdout
        lines = str(output, 'utf-8').split('\n')
        if len(lines) == 1:
            print("no docker images detected")
        headers = lines[0].split()
        assert headers[0] == 'REPOSITORY', 'error invoking "docker images" - is docker installed?'
        return lines[1:]

    @staticmethod
    def get_image_ids(images):
        results = []
        for image in images:
            parts = image.split()
            results.append(parts[2])
        return results

    @staticmethod
    def run():
        args = sys.argv[1:]
        options = Main.parse_cmd_args(args)

        client = docker.from_env()

        for image in client.images.list():
            # attrs = json.loads(image.attrs)
            #print(image.tags, image.short_id, image.attrs)
            print("#" * 40)
            print(image.tags, image.id, '==> Layers:')
            print(image.attrs['RootFS']['Layers'])
        


if __name__ == '__main__':
    Main.run()
  