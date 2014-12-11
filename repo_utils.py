__author__ = 'cbarne02'

import os
import json
from repo_dir import get_directory
from metadata_type import get_metadata_type
from xml.dom.minidom import *

# REPO_PATH = "/usr/local/metadata"
# REPO_PATH = "/Users/cbarne02/Documents/code/git/edu.tufts"
REPO_PATH = "/Users/cbarne02/Documents/code/git/edu.harvard"



def get_filename_from_type(f):
    d = {'FGDC': 'fgdc.xml', 'ISO19139': 'iso19139.xml'}
    mt, tree = get_metadata_type(f)
    return d.get(mt), tree


def write_metadata(tree, path, overwrite):

    if not os.path.exists(path) or overwrite:
        try:
            with open(path, "w+") as d:
                d.write('<?xml version="1.0" encoding="utf-8" ?>')
                d.write('<!DOCTYPE metadata SYSTEM "http://www.fgdc.gov/metadata/fgdc-std-001-1998.dtd">')
                tree.write(d, xml_declaration=False, encoding="utf-8")
            print "Metadata written at: " + path
        except:
            raise Exception("Error writing metadata")

    else:
        raise Exception("A metadata directory with that id already exists in the repository.")


def update_layers_json(layer_id, path, repo_path=REPO_PATH):
    layers = get_layers_json(repo_path)
    layers[layer_id] = os.path.relpath(path, repo_path)
    set_layers_json(layers, repo_path)


def get_layers_json(repo_path=REPO_PATH):
    lpath = os.path.join(repo_path, "layers.json")
    layers = {}
    if os.path.exists(lpath):
        with open(lpath, 'r') as fr:
            layers = json.load(fr)

    return layers


def set_layers_json(layers, repo_path=REPO_PATH):
    lpath = os.path.join(repo_path, "layers.json")
    with open(lpath, 'w+') as fw:
        json.dump(layers, fw, indent=4, sort_keys=True)


def write_to_repository(file_id, fs, repo_path=REPO_PATH, overwrite=False):
    type_name = None
    tree = None
    try:
        type_name, tree = get_filename_from_type(fs)
    except Exception as e:
        print file_id
        print e.message
        return

    path = get_directory(file_id, repo_path)

    fname = os.path.join(path, type_name)

    if os.path.exists(fname):
        print file_id
        print path
        if overwrite:
            print "Warning: overwriting file!"
        else:
            raise Exception("A metadata directory with that id already exists in the repository.")

    write_metadata(tree, fname, overwrite)
    # create/update a json object at repository root mapping layer ids to directories
    update_layers_json(file_id, path, repo_path)

    return path


def find_from_layer_id(layer_id, repo_path=REPO_PATH):
    layers = get_layers_json(repo_path)
    if not layers.has_key(layer_id):
        raise Exception("layer['" + layer_id + "'] not found!")
    path = layers[layer_id]
    path = os.path.join(repo_path, path)
    if os.path.exists(path):
        return path, os.listdir(path)
    else:
        raise Exception("layer['" + layer_id + "'] not found!")





