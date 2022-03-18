#!/usr/bin/python3
import argparse, os, subprocess, sys
import imagetools

from colorama import Fore, Back, Style

# Fore: BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET.
# Back: BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET.
# Style: DIM, NORMAL, BRIGHT, RESET_ALL

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
        answer = input(Style.BRIGHT + Fore.YELLOW + message).lower()
    print(Style.RESET_ALL + '', end='')
    return answer == "y"



class Main:
    @staticmethod
    def parse_cmd_args(args_to_parse):
        cli = argparse.ArgumentParser(
            prog=(os.path.basename(__file__)),
            description=" - a tool for deleting docker images via filters")
        cli.add_argument( '-d', '--delete', action='store_true',
            help="delete the indicated items")
        cli.add_argument(dest='text', nargs='*', default='', type=str, 
            help='substrings to filter images list.')
        
        result = cli.parse_args(args_to_parse)        
        return result

    @staticmethod
    def read_stdin():
        lines = []
        first_line = input()
        if not imagetools.is_docker_images_header(first_line):
            lines.append(first_line)
        while True:
            try:
                line = input()          
                lines.append(line)
            except EOFError:
                break
        return lines


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

        image_ids = imagetools.get_image_ids(lines)
        lineage = imagetools.get_lineage()
        leaf_node_short_ids = imagetools.get_leaves(lineage)
        root_node_short_ids = imagetools.get_roots(lineage)

        if options.delete:
            print("The following images are selected for deletion:")

        for line in lines:
            id = imagetools.parse_image_id(line)
            if id in leaf_node_short_ids:
                print(Fore.GREEN + line)
            elif id in root_node_short_ids:
                print(Fore.RED + line)
            else:
                print(Style.RESET_ALL + line)
            
        if options.delete:
            
            confirmed = user_confirm("Are you sure you want to delete these images? [y|n]")
            if confirmed:
                imagetools.delete_images(image_ids)

                
if __name__ == '__main__':
    Main.run()
  