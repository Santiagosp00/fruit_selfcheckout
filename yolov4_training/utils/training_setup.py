import configparser
import json
import os
from shutil import copy, copytree
from file_management import update_simple, update_multiple_pattern, create_file_from_content, create_file_from_list
import subprocess
from datetime import timezone, datetime

utc_time = int(datetime.now(tz=timezone.utc).timestamp() * 1000)

config = configparser.RawConfigParser()
config.read('config/config.ini')
training_config = dict(config.items('YOLO'))

LIST_CLASSES = json.loads(training_config['list_classes'])
ROOT_PATH = training_config['root_path']
BATCH = training_config['batch']
SUBDIVISIONS = training_config['subdivisions']
WIDTH = training_config['width']
HEIGHT = training_config['height']

num_classes = len(LIST_CLASSES)
max_batches = str(num_classes*2000)
steps = str(int(0.8*int(max_batches)))+','+str(int(0.9*int(max_batches)))
filters = str((num_classes+5)*3)
num_classes = str(num_classes)

TRAINING_PATH = os.path.join(ROOT_PATH, "yolov4")
OBJ_ROOT_PATH = os.path.join(ROOT_PATH, "data/obj")
TEST_ROOT_PATH = os.path.join(ROOT_PATH, "data/test")
DARKNET_PATH = os.path.join(ROOT_PATH, "darknet")
DARKNET_DATA_PATH = os.path.join(DARKNET_PATH, "data")
OBJ_DARKNET_PATH = os.path.join(DARKNET_DATA_PATH, "obj")
TEST_DARKNET_PATH = os.path.join(DARKNET_DATA_PATH, "test")
DARKNET_CFG_PATH = os.path.join(DARKNET_PATH, "cfg/yolov4-custom.cfg")
DARKNET_CUSTOM_CFG_PATH = os.path.join(DARKNET_PATH, "cfg/yolov4-obj.cfg")
OBJ_NAMES_PATH = os.path.join(TRAINING_PATH, 'obj.names')
OBJ_DATA_PATH = os.path.join(TRAINING_PATH, 'obj.data')
BACKUP_PATH = os.path.join(TRAINING_PATH, 'backup')
GENERATE_TRAIN_PATH = os.path.join(ROOT_PATH, 'utils/generate_train.py')
GENERATE_TEST_PATH = os.path.join(ROOT_PATH, 'utils/generate_test.py')
PREV_TRAINING_PATH = os.path.join(ROOT_PATH, "prev_trainings")

if not os.path.exists(TRAINING_PATH):
    os.makedirs(TRAINING_PATH)
else:
    print("TRAINING_PATH already exists")
    if not os.path.exists(PREV_TRAINING_PATH):
        os.makedirs(PREV_TRAINING_PATH)
    subprocess.call('mv {} {}'.format(TRAINING_PATH, os.path.join(PREV_TRAINING_PATH, 'yolov4_{}'.format(utc_time))), cwd=ROOT_PATH, shell=True)
    print("Moving and copying...")
    os.makedirs(TRAINING_PATH)
    print("Done!")

if not os.path.exists(OBJ_DARKNET_PATH):
    copytree(OBJ_ROOT_PATH, OBJ_DARKNET_PATH)
else:
    print("OBJ_DARKNET_PATH already exists")
    print("Deleting previous obj and copying new...")
    subprocess.call('rm -rf {}'.format(OBJ_DARKNET_PATH), cwd=ROOT_PATH, shell=True)
    copytree(OBJ_ROOT_PATH, OBJ_DARKNET_PATH)
    print("Done!")

if not os.path.exists(TEST_DARKNET_PATH):
    copytree(TEST_ROOT_PATH, TEST_DARKNET_PATH)
else:
    print("TEST_ROOT_PATH already exists")
    print("Deleting previous test and copying new...")
    subprocess.call('rm -rf {}'.format(TEST_DARKNET_PATH), cwd=ROOT_PATH, shell=True)
    copytree(TEST_ROOT_PATH, TEST_DARKNET_PATH)
    print("Done!")

if not os.path.exists(BACKUP_PATH):
    os.makedirs(BACKUP_PATH)
else:
    print("BACKUP_PATH already exists")

copy(DARKNET_CFG_PATH, DARKNET_CUSTOM_CFG_PATH)

vars = ['classes', 'batch', 'subdivisions', 'width',
        'height', 'max_batches', 'steps']
new_values = [num_classes, BATCH, SUBDIVISIONS, WIDTH, 
              HEIGHT, max_batches, steps]
what_to_change = dict(zip(vars,new_values))

old = '[convolutional]\nsize=1\nstride=1\npad=1\nfilters=255'
new = '[convolutional]\nsize=1\nstride=1\npad=1\nfilters='+filters

update_simple(DARKNET_CUSTOM_CFG_PATH, what_to_change)
update_multiple_pattern(DARKNET_CUSTOM_CFG_PATH, old, new)
copy(DARKNET_CUSTOM_CFG_PATH, TRAINING_PATH)

# Create YOLO data file
content_name = "classes = {}\ntrain = data/train.txt\nvalid = data/test.txt\nnames = data/obj.names\nbackup = {}".format(num_classes, BACKUP_PATH)
create_file_from_content(OBJ_DATA_PATH, content_name)
copy(OBJ_DATA_PATH, DARKNET_DATA_PATH)

# Create YOLO name file
create_file_from_list(OBJ_NAMES_PATH, LIST_CLASSES)
copy(OBJ_NAMES_PATH, DARKNET_DATA_PATH)

# Copy generation scripts to darknet
copy(GENERATE_TRAIN_PATH, DARKNET_PATH)
copy(GENERATE_TEST_PATH, DARKNET_PATH)

subprocess.call('python generate_train.py', cwd=DARKNET_PATH, shell=True)
subprocess.call('python generate_test.py', cwd=DARKNET_PATH, shell=True)