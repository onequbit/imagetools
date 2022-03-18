#!/usr/bin/python3
import argparse, json, os, subprocess, sys

import imagetools


from colorama import Fore, Back, Style

# Fore: BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET.
# Back: BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET.
# Style: DIM, NORMAL, BRIGHT, RESET_ALL



class Main:
    @staticmethod
    def parse_cmd_args(args_to_parse):
        cli = argparse.ArgumentParser(
            prog=(os.path.basename(__file__)),
            description=" - a tool for viewing docker image layer hashes")
        
        
        result = cli.parse_args(args_to_parse)        
        return result

    @staticmethod
    def send_stdout(data):
        if data is not None:
            for item in data:
                print(item)
    

    @staticmethod
    def run():        
        images = imagetools.get_lineage()
                
        for image in images:
            if image['node'] == 'root':
                print(Fore.RED + Style.BRIGHT + str(image))
            elif image['node'] == 'leaf':
                print(Fore.GREEN + Style.BRIGHT + str(image))
            else:
                print(Style.RESET_ALL + str(image))

if __name__ == '__main__':
    Main.run()
    print(Style.RESET_ALL)

