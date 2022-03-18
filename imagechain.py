#!/usr/bin/python3
import argparse, json, os, subprocess, sys

import imagetools






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
        
        image_collection_list = imagetools.get_image_collection_list()
        images = []
        
        for image in image_collection_list:
            image_obj = {}
            name = '_'.join(image.tags)
            image_parent = image.attrs['Parent']
            image_obj[name] = f"parent:{image_parent}" if len(image_parent) > 0 else "None"
            images.append(image_obj)
        #     image_obj = dict()
        #     iagmage_obj['tags'] = image.tags
        #     parent = image.attrs['parent']
        #     image_obj['layers'] = layers
        #     image_ht[image.id] = image_obj
        
        # for image in image_ht:
        #     print(image, '-->')
        #     for layer in image_ht[image]['layers']:
        #         print('...', layer)
        #         if layer in image_ht.keys():
        #             print(image_ht[layer]['tags'])

        Main.send_stdout(images)
        


if __name__ == '__main__':
    Main.run()
  