#!/usr/bin/python3
import argparse, os, subprocess, sys
import imagetools

def user_confirm(message):
    # https://gist.github.com/gurunars/4470c97c916e7b3c4731469c69671d06
    """
    Ask user to enter Y or N (case-insensitive).
    :return: True if the answer is Y.
    :rtype: bool
    """
    sys.stdin = open("/dev/tty")
    answer = ""
    while answer not in ["y", "n"]:
        answer = input(message).lower()
    return answer == "y"



class Main:
    @staticmethod
    def parse_cmd_args(args_to_parse):
        cli = argparse.ArgumentParser(
            prog=(os.path.basename(__file__)),
            description=" - a tool for mapping the contents of a directory")
        cli.add_argument( '-d', '--delete', action='store_true',
            help="delete the indicated items")
        cli.add_argument(dest='text', nargs='*', default='', type=str, 
            help='substrings to filter images list.')
        
        result = cli.parse_args(args_to_parse)        
        return result

    @staticmethod
    def read_stdin():
        lines = []
        while True:
            try:
                lines.append(input())
            except EOFError:
                break
        return lines

    @staticmethod
    def send_stdout(data):
        if data is not None:
            for item in data:
                print(item)

    # @staticmethod
    # def get_docker_images():
    #     output = subprocess.run('docker images', capture_output=True, shell=True, check=True).stdout
    #     lines = str(output, 'utf-8').split('\n')
    #     if len(lines) == 1:
    #         print("no docker images detected")
    #     headers = lines[0].split()
    #     assert headers[0] == 'REPOSITORY', 'unexpected output from "docker images"'
    #     return lines[1:]

    # @staticmethod
    # def get_image_ids(images):
    #     results = []
    #     for image in images:
    #         parts = image.split()
    #         results.append(parts[2])
    #     return results

    # @staticmethod
    # def delete_images(image_ids):
    #     for id in image_ids:
    #         delete_cmd = f"docker image rm --force {id}"
    #         output = subprocess.run(delete_cmd, capture_output=True, shell=True, check=True).stdout
    #         print(str(output, 'utf-8'))

    @staticmethod
    def run():
        args = sys.argv[1:]
        options = Main.parse_cmd_args(args)
        
        pipe_detected = not sys.stdin.isatty()
        lines = []
        if pipe_detected:
            lines = Main.read_stdin()
        else:
            lines = imagetools.get_docker_images()

        if options.text:
            results = set()
            for a in options.text:
                for line in lines:
                    if a in line:
                        results.add(line)
                lines = list(results)
                results = set()
        
        if options.delete:
            print("The following images are selected for deletion:")
        
        Main.send_stdout(lines)

        if options.delete:
            images_to_delete = imagetools.get_image_ids(lines)
            confirmed = user_confirm("Are you sure you want to delete these images? [y|n]")
            if confirmed:
                imagetools.delete_images(images_to_delete)
if __name__ == '__main__':
    Main.run()
  