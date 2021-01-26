"""Build vocabularies of words and tags from datasets"""

from collections import Counter
import json
import os
import csv
import sys
import pandas as pd

def load_dataset(path_csv):
    """Loads dataset into memory from csv file"""
    # Open the csv file, need to specify the encoding for python3
    use_python3 = sys.version_info[0] >= 3
    data = pd.load_csv(path_csv)

    with (open(path_csv, encoding="windows-1252") if use_python3 else open(path_csv)) as f:
        csv_file = csv.reader(f, delimiter=';')
        dataset = []
        words, tags = [], []

        # Each line of the csv corresponds to one word
        for idx, row in enumerate(csv_file):
            if idx == 0: continue
            sentence, word, pos, tag = row
            # If the first column is non empty it means we reached a new sentence
            if len(sentence) != 0:
                if len(words) > 0:
                    assert len(words) == len(tags)
                    dataset.append((words, tags))
                    words, tags = [], []
            try:
                word, tag = str(word), str(tag)
                words.append(word)
                tags.append(tag)
            except UnicodeDecodeError as e:
                print("An exception was raised, skipping a word: {}".format(e))
                pass

    return dataset


def save_dataset(dataset, save_dir):
    """Writes sentences.txt and labels.txt files in save_dir from dataset

    Args:
        dataset: ([(["a", "cat"], ["O", "O"]), ...])
        save_dir: (string)
    """
    # Create directory if it doesn't exist
    print("Saving in {}...".format(save_dir))
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    # Export the dataset
    with open(os.path.join(save_dir, 'sentences.txt'), 'w') as file_sentences:
        with open(os.path.join(save_dir, 'labels.txt'), 'w') as file_labels:
            for words, tags in dataset:
                file_sentences.write("{}\n".format(" ".join(words)))
                file_labels.write("{}\n".format(" ".join(tags)))
    print("- done.")

def save_dict_to_json(d, json_path):
    """Saves dict to json file

    Args:
        d: (dict)
        json_path: (string) path to json file
    """
    with open(json_path, 'w') as f:
        d = {k: v for k, v in d.items()}
        json.dump(d, f, indent=4)


def update_vocab(txt_path, vocab):
    """Update word and tag vocabulary from dataset

    Args:
        txt_path: (string) path to file, one sentence per line
        vocab: (dict or Counter) with update method

    Returns:
        dataset_size: (int) number of elements in the dataset
    """
    with open(txt_path) as f:
        for i, line in enumerate(f):
            vocab.update(line.strip().split(' '))

    return i + 1

def build_vocab(path_dir, min_count_word=1, min_count_tag=1) :
    # Build word vocab with train and test datasets
    print("Building word vocabulary...")
    words = Counter()
    size_train_sentences = update_vocab(os.path.join(path_dir, 'train/sentences.txt'), words)
    #size_dev_sentences = update_vocab(os.path.join(path_dir, 'dev/sentences.txt'), words)
    #size_test_sentences = update_vocab(os.path.join(path_dir, 'test/sentences.txt'), words)
    print("- done.")

    # Save vocabularies to file
    print("Saving vocabularies to file...")
    save_vocab_to_txt_file(words, os.path.join(path_dir, 'words.txt'))
    save_vocab_to_txt_file(tags, os.path.join(path_dir, 'tags.txt'))
    save_vocab_to_txt_file(tags_count, os.path.join(path_dir, 'tags_count.txt'))
    print("- done.")

    # Save datasets properties in json file
    sizes = {
        'train_size': size_train_sentences,
        'dev_size': size_dev_sentences,
        'test_size': size_test_sentences,
        'max_size_size': len(words),
        'number_of_features': len(tags),
    }
    save_dict_to_json(sizes, os.path.join(path_dir, 'dataset_params.json'))

    # Logging sizes
    to_print = "\n".join("- {}: {}".format(k, v) for k, v in sizes.items())
    print("Characteristics of the dataset:\n{}".format(to_print))
    

if __name__ == '__main__':

    print("Building vocabulary for science dataset...")
    build_vocab("data/science", 1, 1)

    print("Building vocabulary for disease dataset...")
    build_vocab("data/disease", 1, 1)






    
    
