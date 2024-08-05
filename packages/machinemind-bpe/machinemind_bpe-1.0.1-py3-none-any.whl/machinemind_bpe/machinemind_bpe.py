import numpy as np
from tqdm import tqdm
import torch
import json
import base64
from typing import Dict, List, Tuple
import regex as re
from .dependency_check import check_dependencies

check_dependencies()


################################Tokenizer Training on CPU######################################


class TrainTokenizer:
    """
    A class to train a tokenizer on a CPU device.

    This class implements byte-pair encoding (BPE) algorithm for tokenization,
    utilizing ndarrays for faster computation and memory efficiency.

    Attributes:
        data (np.ndarray): The input text converted to a numpy array of bytes.
    """

    def __init__(self, text: str):
        """
        Initialize the TrainTokenizer with input text.

        Args:
            text (str): The input text to be used for training the tokenizer.
        """
        assert isinstance(text, str), "Input must be a string"
        self.data = np.frombuffer(text.encode('utf-8'), dtype=np.uint8)

    def _get_stats(self, ids:np.ndarray) -> np.ndarray:
        """
        Find the most frequent pair of adjacent bytes in the data.

        Returns:
            np.ndarray: The most frequent pair of adjacent bytes.
        """
        pair_view = np.lib.stride_tricks.sliding_window_view(ids, 2)
        sorted_indices = np.lexsort(pair_view.T[::-1])
        sorted_pairs = np.asfortranarray(pair_view[sorted_indices])
        diff = np.any(sorted_pairs[1:] != sorted_pairs[:-1], axis=-1)
        idx = np.concatenate(([0],  np.nonzero(diff)[0] + 1, [len(sorted_pairs)]))
        counts = np.diff(idx)
        max_index = idx[:-1][np.argmax(counts)]
        return sorted_pairs[max_index]

    def _merge(self, ids: np.ndarray, pair: np.ndarray, idx: int) -> np.ndarray:
        """
        Merge the most frequent pair in the data.

        Args:
            ids (np.ndarray): The current state of the data.
            pair (np.ndarray): The pair to be merged.
            idx (int): The new token ID for the merged pair.

        Returns:
            np.ndarray: The updated state of the data after merging.
        """
        assert isinstance(ids, np.ndarray), "ids must be a numpy array"
        assert isinstance(pair, np.ndarray) and pair.shape == (2,), "pair must be a numpy array of shape (2,)"
        assert isinstance(idx, int), "idx must be an integer"

        mask = (ids[:-1] == pair[0]) & (ids[1:] == pair[1])
        mask_ind = np.where(mask)[0]
        ids[mask_ind] = idx
        ids[mask_ind + 1] = -1
        return ids[ids != -1]

    def train(self, vocab_size: int = 1256, merges_file: str = 'merges.json', vocab_file: str = 'vocab.json') -> Dict[Tuple[int, int], int]:
        """
        Train the tokenizer using the BPE algorithm.

        Args:
            vocab_size (int): The desired vocabulary size. Must be greater than 256.
            merges_file (str): The file path to save the merges.
            vocab_file (str): The file path to save the vocabulary.

        Returns:
            Dict[Tuple[int, int], int]: A dictionary of the merges performed during training.

        Raises:
            AssertionError: If vocab_size is not greater than 256.
        """
        assert vocab_size > 256, "vocab_size should be greater than 256"
        assert isinstance(merges_file, str), "merges_file must be a string"
        assert isinstance(vocab_file, str), "vocab_file must be a string"

        num_merges = vocab_size - 256
        ids = np.array(self.data, dtype=np.int32)
        merges = {}

        for i in tqdm(range(num_merges)):
            most_frequent = self._get_stats(ids)
            idx = 256 + i
            ids = self._merge(ids, most_frequent, idx)
            merges[tuple(most_frequent)] = idx

        self._save_merges_json(merges, merges_file)
        self._save_vocab_json(merges, vocab_file)
        return merges

    def _save_merges_json(self, merges: Dict[Tuple[int, int], int], path: str) -> None:
        """
        Save the merges to a JSON file.

        Args:
            merges (Dict[Tuple[int, int], int]): The merges to be saved.
            path (str): The file path to save the merges.
        """
        assert isinstance(merges, dict), "merges must be a dictionary"
        assert isinstance(path, str), "path must be a string"

        serializable_merges = {f"{k[0]},{k[1]}": v for k, v in merges.items()}
        tokenizer_data = {"merges": serializable_merges}
        with open(path, 'w') as f:
            json.dump(tokenizer_data, f, indent=2)

    def _save_vocab_json(self, merges: Dict[Tuple[int, int], int], path: str) -> None:
        """
        Save the vocabulary to a JSON file.

        Args:
            merges (Dict[Tuple[int, int], int]): The merges used to construct the vocabulary.
            path (str): The file path to save the vocabulary.
        """
        assert isinstance(merges, dict), "merges must be a dictionary"
        assert isinstance(path, str), "path must be a string"

        vocab = {idx: bytes([idx]) for idx in range(256)}
        for (p0, p1), idx in merges.items():
            vocab[idx] = vocab[p0] + vocab[p1]
        
        serializable_vocab = {str(k): base64.b64encode(v).decode('utf-8') for k, v in vocab.items()}
        with open(path, 'w') as f:
            json.dump(serializable_vocab, f, indent=2)





##################################Tokenizer Training on GPU######################################

class TrainTokenizerGPU:
    """
    A class for training a tokenizer using GPU acceleration.

    This class implements byte-pair encoding (BPE) algorithm for tokenization,
    utilizing GPU for faster computation. It finds the most frequent pairs of tokens
    and iteratively merges them to create a new vocabulary.

    Attributes:
        data (np.ndarray): The input text converted to a numpy array of bytes.
    """

    def __init__(self, text: str):
        """
        Initialize the TrainTokenizerGPU with input text.

        Args:
            text (str): The input text to be used for training the tokenizer.

        Raises:
            AssertionError: If a GPU is not available.
        """
        assert torch.cuda.is_available(), "GPU not available"
        assert isinstance(text, str), "Input must be a string"
        self.data = np.frombuffer(text.encode('utf-8'), dtype=np.uint8)

    def _get_stats(self, ids: torch.Tensor) -> torch.Tensor:
        """
        Find the most common pair of adjacent tokens in the data.

        Args:
            ids (torch.Tensor): The current state of the data.

        Returns:
            torch.Tensor: The most common pair of adjacent tokens.
        """
        assert isinstance(ids, torch.Tensor), "ids must be a torch.Tensor"

        indices = torch.stack([ids[:-1], ids[1:]])
        values = torch.ones(indices.size(1), dtype=torch.int8, device='cuda')
        sparse_counts = torch.sparse_coo_tensor(
            indices,
            values,
            size=(torch.max(ids)+1, torch.max(ids)+1),
            dtype=torch.int32,
            device='cuda'
        )
        coalesced_counts = sparse_counts.coalesce()
        return coalesced_counts.indices()[:, coalesced_counts.values().argmax()]

    def _merge(self, ids: torch.Tensor, pair: torch.Tensor, idx: int) -> torch.Tensor:
        """
        Merge the most frequent pair in the data.

        Args:
            ids (torch.Tensor): The current state of the data.
            pair (torch.Tensor): The pair to be merged.
            idx (int): The new token ID for the merged pair.

        Returns:
            torch.Tensor: The updated state of the data after merging.
        """
        assert isinstance(ids, torch.Tensor), "ids must be a torch.Tensor"
        assert isinstance(pair, torch.Tensor) and pair.shape == (2,), "pair must be a torch.Tensor of shape (2,)"
        assert isinstance(idx, int), "idx must be an integer"

        mask = (ids[:-1] == pair[0]) & (ids[1:] == pair[1])
        mask_ind = torch.where(mask)[0]
        ids[mask_ind] = idx
        ids[mask_ind + 1] = -1
        return ids[ids != -1]

    def train(self, vocab_size: int = 1256, merges_file: str = 'merges.json', vocab_file: str = 'vocab.json') -> Dict[Tuple[int, int], int]:
        """
        Train the tokenizer using the BPE algorithm on GPU.

        Args:
            vocab_size (int): The desired vocabulary size. Must be greater than 256.
            merges_file (str): The file path to save the merges.
            vocab_file (str): The file path to save the vocabulary.

        Returns:
            Dict[Tuple[int, int], int]: A dictionary of the merges performed during training.

        Raises:
            AssertionError: If vocab_size is not greater than 256.
        """
        assert vocab_size > 256, "vocab_size should be greater than 256"
        assert isinstance(merges_file, str), "merges_file must be a string"
        assert isinstance(vocab_file, str), "vocab_file must be a string"

        num_merges = vocab_size - 256
        ids = torch.from_numpy(self.data.copy()).type(torch.int32).cuda()

        merges = {}
        with torch.no_grad():
            for i in tqdm(range(num_merges)):
                most_frequent = self._get_stats(ids)
                idx = 256 + i
                ids = self._merge(ids, most_frequent, idx)
                merges[tuple(most_frequent.cpu().numpy())] = idx
        
        self._save_merges_json(merges, merges_file)
        self._save_vocab_json(merges, vocab_file)
        return merges

    def _save_merges_json(self, merges: Dict[Tuple[int, int], int], path: str) -> None:
        """
        Save the merges to a JSON file.

        Args:
            merges (Dict[Tuple[int, int], int]): The merges to be saved.
            path (str): The file path to save the merges.
        """
        assert isinstance(merges, dict), "merges must be a dictionary"
        assert isinstance(path, str), "path must be a string"

        serializable_merges = {f"{k[0]},{k[1]}": v for k, v in merges.items()}
        tokenizer_data = {"merges": serializable_merges}
        with open(path, 'w') as f:
            json.dump(tokenizer_data, f, indent=2)

    def _save_vocab_json(self, merges: Dict[Tuple[int, int], int], path: str) -> None:
        """
        Save the vocabulary to a JSON file.

        Args:
            merges (Dict[Tuple[int, int], int]): The merges used to construct the vocabulary.
            path (str): The file path to save the vocabulary.
        """
        assert isinstance(merges, dict), "merges must be a dictionary"
        assert isinstance(path, str), "path must be a string"

        vocab = {idx: bytes([idx]) for idx in range(256)}
        for (p0, p1), idx in merges.items():
            vocab[idx] = vocab[p0] + vocab[p1]
        
        serializable_vocab = {str(k): base64.b64encode(v).decode('utf-8') for k, v in vocab.items()}
        with open(path, 'w') as f:
            json.dump(serializable_vocab, f, indent=2)




#########################Encoder##################################


class Encoder:
    """
    A class for encoding and decoding text using byte-pair encoding (BPE).

    This class implements the encoding and decoding processes using a trained BPE model.
    It handles special tokens and uses regex for initial tokenization.

    Attributes:
        regex (re.Pattern): A compiled regex pattern for initial tokenization.
        special_tk (List[str]): A list of special tokens.
        merges (Dict[Tuple[int, int], int]): The trained merges.
        vocab (Dict[int, bytes]): The vocabulary mapping token IDs to byte sequences.
    """

    def __init__(
            self, 
            merges_file_path: str = "merges.json",
            vocab_file_path: str = "vocab.json",
            special_tokens: List[str] = ['[PAD]','[UNK]','[STR]','[END]','[SEP]'],
            regex_pattern: str = r""" ?\b(?:\w*'\w*)+\b|\[[A-Z]{3}\]| ?\b\w+\b| ?[,.!?(){}["-\]]|\s""", 
            ):
        """
        Initialize the Encoder with special tokens and load the trained model.

        Args:
            merges_file_path (str): A path to file of merges. Default is 'merges.json'.
            vocab_file_path (str): A path to file of vocabulary. Default is 'vocab.json'.
            special_tokens (List[str]): A list of special tokens to be used in the encoding process.
            regex_pattern (str): A regex pattern to control over merges.
        """
        assert isinstance(merges_file_path, str), "merges_file_path must be a string"
        assert isinstance(vocab_file_path, str), "vocab_file_path must be a string"
        assert isinstance(special_tokens, list) and all(isinstance(t, str) for t in special_tokens), "special_tokens must be a list of strings"
        assert isinstance(regex_pattern, str), "regex_pattern must be a string"

        self.regex = re.compile(regex_pattern)
        self.special_tk = special_tokens
        self.merges = self._load_merges(merges_file_path)
        self.vocab = self._load_vocab(vocab_file_path)

    def encode(self, text:str):
        """
        Encode the input text into token IDs.

        Args:
            text (str): The input text to be encoded.

        Returns:
            List[int]: A list of token IDs representing the encoded text.
        """
        assert isinstance(text, str), "Input text must be a string"

        bpe_tokens = []
        for token in tqdm(re.findall(self.regex, text)):
            if token in self.special_tk:
                # Handle special tokens
                token_id = list(self.vocab.values()).index(token.encode('utf-8'))
                bpe_tokens.append(token_id)
            else:
                # Encode regular tokens
                bpe_tokens.extend(self._encode_chunk(token))
        return bpe_tokens

    def decode(self, ids:List[int]):
        """
        Decode the input list of integers into string.

        Args:
            ids (list): The input list to be decoded.

        Returns:
            str: A text decoded back.
        """

        assert isinstance(ids, list), "Input ids must be a List[int]"
        # Decode token IDs back to text
        tokens = b''.join(self.vocab[idx] for idx in ids)
        text = tokens.decode('utf-8', errors='replace')
        return text
    
    def _encode_chunk(self, text: str):
        # Encode a single chunk of text
        ids = list(map(int, text.encode('utf-8')))
        pairs = list(zip(ids[:-1], ids[1:]))
        for pair in pairs:
            if pair in self.merges.keys():
                ids = self._encode_merge(ids, list(pair), self.merges[pair])
        return ids

    def _encode_merge(self, ids, pairs, idx):
        # Perform merges on the token IDs
        new_ids = []
        i = 0
        while i < len(ids):
            if i < len(ids) - 1 and ids[i:i+2] == pairs:
                new_ids.append(idx)
                i += 2
            else:
                new_ids.append(ids[i])
                i += 1
        return new_ids

    def _load_vocab(self, file_path):
        # Load vocabulary from JSON file
        with open(file_path, 'r') as f:
            loaded_data = json.load(f)
        end_index = len(loaded_data)
        # Add special tokens to vocabulary
        sp_tk = {str(end_index+i): base64.b64encode(v.encode('utf-8')).decode('ascii') for i,v in enumerate(self.special_tk)}
        loaded_data.update(sp_tk)
        vocab = {int(k): base64.b64decode(v) for k, v in loaded_data.items()}
        return vocab

    def _load_merges(self, file_path):
        # Load merges from JSON file
        with open(file_path, 'r') as f:
            tokenizer_data = json.load(f)
        merges = dict(sorted(
                ((tuple(map(int, k.split(','))), v) for k, v in tokenizer_data['merges'].items()),
                key=lambda x: x[1],
                reverse=True
                ))  
        return merges