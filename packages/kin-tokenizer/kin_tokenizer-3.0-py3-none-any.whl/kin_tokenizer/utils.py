from .tokenizer import KinTokenizer


def train_kin_tokenizer(text, vocab_size=256, save=False, tokenizer_path=None):
    """
    Function for training the tokenizer
    params:
        text: the string text that will be used for training the tokenizer
        vocab_size: the final size of the voacabulary for the tokenizer
        save: boolean to indicate if tokenizer has to be saved after training for future use
        tokenizer_path: the path to which the tokenizer will be saved if save is True
    Returns:
        returns tokenizer object after training
    """
    tokenizer = KinTokenizer()
    if len(text) < vocab_size or type(text) != str:
        raise ValueError("length of text should be greater or equal to vocab_size, vocab_size should be at least 256 and text should be a string")
    _ = tokenizer.train(text, vocab_size)

    if save == True and tokenizer is None:
        print("Cannot save because the path is not provided")
    elif save == True:
        tokenizer.save(tokenizer_path)
    
    return tokenizer


def create_sequences(tokens, seq_len):
    """
    Function for creating sequences for next word prediction
    params:
        tokens: list of tokens(integers)
        seq_len: the length for each sequence to be created
    returns:
        the list of sequences(list of tokens with length of seq_len)
    """
    tokens_len = len(tokens)
    source, target = [], []
    for i in range(tokens_len):
        sequence = tokens[i: i + seq_len + 1]
        source.append(sequence[:-1])
        target.append(sequence[-1])
    return source, target

