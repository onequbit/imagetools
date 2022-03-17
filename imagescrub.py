#!/usr/bin/python3
import argparse, os, subprocess, sys
import docker # <-- pip install docker

# client = docker.from_env()

# for image in client.images.list():
#     i = client.images.list().index(image)
#     if image.tags == []:
#         print(image.short_id, image.tags)

class Main:
    @staticmethod
    def parse_cmd_args(args_to_parse):
        cli = argparse.ArgumentParser(
            prog=(os.path.basename(__file__)),
            description=" - a tool for mapping the contents of a directory")
        cli.add_argument(
            "--delete",
            type=bool,
            help="delete the indicated items")
            
        result = cli.parse_args(args_to_parse)        
        return result

    @staticmethod
    def read_stdin():
        pass

    @staticmethod
    def send_stdout(data):
        for item in data:
            print(item)

    @staticmethod
    def use_docker():
        output = subprocess.run('docker images', capture_output=True, shell=True, check=True).stdout
        lines = str(output, 'utf-8').split('\n')
        return lines

    @staticmethod
    def run():
        args = sys.argv[1:]
        options = Main.parse_cmd_args(args)
        if options.delete:
            print("delete option selected!")
            
        pipe_detected = not sys.stdin.isatty()
        lines = []
        if pipe_detected:
            lines = Main.read_stdin()
        else:
            lines = Main.use_docker()

        if len(args) > 0:
            results = set()
            for a in args:
                for line in lines:
                    if a in line:
                        results.add(line)
                lines = list(results)
                results = set()

        Main.send_stdout(lines)

if __name__ == '__main__':
    Main.run()
  