import os
import pickle
import re
import string
import pkg_resources

"""
Kin_tokenizer is a python module which includes class and methods
for Kinyarwanda tokenizeer
"""


class KinTokenizer:
    def __init__(self):
        self.__vocab = {}
        self.merged_tokens = {}
        self.tokens = None
        self.vocab_size = None


    @property
    def vocab(self):
        return {
            key: value.decode("UTF-8", errors="replace") if key != -1 else value for key, value in self.__vocab.items()
        }

    
    def set_vacab(self, vocab):
        """
        method for setting vocabulary of the tokenizer
        vocab: dictionary of int, bytes
        """

        if (self.__vocab) < 1:
            if type(vocab) == dict:
                self.__vocab = vocab
            else:
                raise ValueError("Expected a dictionary of {integer: bytes}")
        else:
            raise ValueError("Vocab cannot be overriden")


    def set_merged_tokens(self, merged_tokens):
        """
        method of setting merged_tokens
        merged_tokens: dictionary of merged_tokens ((int, int), int)
        """

        if (self.merged_tokens) < 1:
            if type(merged_tokens) == dict:
                self.merged_tokens = merged_tokens
            else:
                raise ValueError("Expected a dictionary of {(integer, integer): integer}")
        else:
            raise ValueError("merged_tokens cannot be overriden")
        
    
    def save(self, path):
        """
        method for saving the tokenizer state
        path: the path to the directory where the tokenizer will be saved
        """

        if not os.path.exists(path) or not os.path.isdir(path):
            raise ValueError("Check is the path exist. it should be a diractory")
            
        path = os.path.join(path, "kin_tokenizer.pkl")
        with open(path, "wb") as f:
            pickle.dump(self, f)
            f.close()
        path = path.replace("\\", "\\\\")
        print(f"\n\n{'='*(len(path)+ 33)}\nTokenizer saved successfully at {path}\n{'='*(len(path)+ 33)}\n")
        print(f""" 
        To load tokenizer and start using it\n{'='*(len(path) + 33)}\n
        with open('{path}', 'rb') as f:
            kin_tokenizer = pickle.load(f)
            kin_tokenizer.vocab # to get vocab
            f.close()
        """) 


    def load(self, path=None):
        """
        method for loading the tokenizer state
        path: the full path to the tokenizer file(.pkl)
        """
        if path is None:
            path = pkg_resources.resource_filename('kin_tokenizer', 'data/kin_tokenizer.pkl')

        try:
            with open(path, 'rb') as f:
                tokenizer = pickle.load(f)
            self.__vocab = tokenizer.__vocab
            self.vocab_size = tokenizer.vocab_size
            self.merged_tokens = tokenizer.merged_tokens
            self.tokens = tokenizer.tokens
        except Exception as e:
            print(f"{str(e)}")

    
    def create_bpe(self, tokens):
        """
        Generator for creating token pairs
        params:
            tokens: list of tokens(integers)
        """
        n = len(tokens) - 1
        i = 0
        while i < n:
            yield (tokens[i], tokens[i+1])
            i += 1     

    
    def get_tokens_pair_stats(self, tokens):
        """
        method for creating frequencies of tokens
        tokens: list of tokens(int)
        """

        tokens_pairs_stats = {}
        for pair in self.create_bpe(tokens):
            tokens_pairs_stats[pair] = tokens_pairs_stats.get(pair, 0) + 1
        return dict(sorted(tokens_pairs_stats.items(), key=lambda v: v[1], reverse=True))

    
    def create_tokens(self, text, train=True):
        """
        method for creating tokens from text
        text: string of character
        train: boolean value to specify if tokens will be created for training the tokenizer
        """

        if type(text) == str:
            text = text.encode("UTF-8")
        elif type(text) != bytes:
            raise ValueError("Expected string or bytes")

        if train:
            self.tokens = list(map(int, text))
            return self.tokens
        else:
            return list(map(int, text))

    
    def merge_tokens(self, pair, tokens, new_token):
        """
        method for merging tokens
        pair: the pair to be merged(most frequent pair of tokens)
        tokens: list of tokens
        new_token: the new token to replace the most frequent pair of tokens(int, int)
        """

        new_tokens = []
        index = 0
        changed = False
        while index < len(tokens):
            if index < len(tokens) - 1 and pair[0] == tokens[index] and pair[1] == tokens[index+1]:
                new_tokens.append(new_token)
                index += 2
                changed = True
            else:
                new_tokens.append(tokens[index])
                index += 1
                
        if changed:
            self.merged_tokens[pair] = new_token
        return new_tokens    


    def replace_punctuation_mark(self, text):
        """
        method for removing punctuation marks and new line from the text for training tokenizer
        text: text to be used for training the tokenizer
        """

        text = text.replace("\n", "")
        punctuation_marks = string.punctuation.replace("'", "")
        pattern = r'' + f'([{punctuation_marks}])'
        return re.sub(pattern, r'', text)    
    

    def train(self, text, vocab_size=276):
        """
        method for training the tokenizer
        text: the text to be used for training the tokenizer
        vocab_size: the size of the vocabulary for the tokenizer after training
        """

        text = self.replace_punctuation_mark(text)
        tokens = self.create_tokens(text)
        self.vocab_size = vocab_size
        if vocab_size > 256:
            num_merges = vocab_size - 256 # We have encode tokens into range of 0 255
        else:
            num_merges = 0
        for idx in range(num_merges):
            if len(tokens) > 1:
                new_token = 256 + idx
                stats = self.get_tokens_pair_stats(tokens) # calculating the statistics(pair frequencies)
                top_pair = max(stats, key=stats.get) # getting the top pair(pair with highest frequency)
                tokens = self.merge_tokens(top_pair, tokens, new_token) # Tokens were create in range between 0 t0 255, merging tokens with new token
                print(f"Step {idx + 1}/{num_merges}: Merged token {top_pair} to {new_token}\t Remaining merges: {num_merges - (idx + 1)}")
            else:
                break # no more pairs

        # Building vocabulary
        self.__vocab = {index: bytes([index]) for index in range(256) }
        # adding merges
        for (p0, p1), key in self.merged_tokens.items():
            self.__vocab[key] = self.__vocab[p0] + self.__vocab[p1]
        self.__vocab[-1] = "<EOS>"
        return tokens

    
    def encode(self, text):
        """
        method to be used for converting text to token using method used for training the tokenizer
        text: text to be encoded
        """
        if type(text) != str:
            raise ValueError("Expected a string!")
            
        tokens = self.create_tokens(text, train=False)
        while True:
            stats = self.get_tokens_pair_stats(tokens)
            top_pair = max(stats, key=stats.get)
            if top_pair not in self.merged_tokens:
                break
            new_token = self.merged_tokens[top_pair]
            tokens = self.merge_tokens(top_pair, tokens, new_token) 
        return tokens

    
    def decode(self, indices):
        """
        method for converting tokens(int) back to text
        indices: list of tokens to be decoded
        """

        if type(indices) not in (list, tuple):
            raise ValueError("Expected list of integers")
        tokens = []
        eos = ""
        for idx in indices:
            if idx == -1:
                eos = self.__vocab[idx]
                continue
            tokens.append(self.__vocab[idx])
        tokens = b"".join(tokens)
        text = tokens.decode("UTF-8", errors="replace")
        return text + eos