# Appends a path to import python scripts that are in other directories.
import os
import sys
sys.path.append(os.path.join(os.environ["HOME"], "ucllm_nedo_prod/pipeline/common/"))

import argparse
import sentencepiece as spm
from special_token_list import BOS_TOKEN, EOS_TOKEN, PAD_TOKEN, CLS_TOKEN, SEP_TOKEN, EOD_TOKEN, MASK_TOKEN, NEWLINE_TOKEN


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=str, required=False, default="../step2_dedup_dataset/output/debuped_documents/results.dedup.jsonl")
    parser.add_argument("--output_base", type=str, required=False, default="./output")
    parser.add_argument("--model_prefix", type=str, required=False, default="botchan")
    parser.add_argument("--vocab_size", type=int, required=False, default=8000)
    parser.add_argument("--character_coverage", type=float, default=0.9995)
    parser.add_argument("--model_type", type=str, default="bpe", choices=["unigram", "bpe", "word", "char"])
    parser.add_argument("--num_threads", type=int, default=16)
    parser.add_argument("--train_extremely_large_corpus", type=bool, default=True)
    args = parser.parse_args()
    print(f"{args = }")
    return args


def main():
    args = parse_arguments()
    if not os.path.exists(args.output_base):
        os.makedirs(args.output_base)
    model_prefix = os.path.join(args.output_base, args.model_prefix)

    # Trains a SentencePiece tokenizer. After training, *.model and *.vocab will be saved in the current directory.
    spm.SentencePieceTrainer.train(
        input=args.input,
        model_prefix=model_prefix,
        vocab_size=args.vocab_size,
        character_coverage=args.character_coverage,
        model_type=args.model_type,
        num_threads=args.num_threads,
        max_sentencepiece_length=512,
        train_extremely_large_corpus=args.train_extremely_large_corpus,
        user_defined_symbols=[
            BOS_TOKEN,
            EOS_TOKEN,
            PAD_TOKEN,
            CLS_TOKEN,
            SEP_TOKEN,
            EOD_TOKEN,
            MASK_TOKEN,
            NEWLINE_TOKEN,
        ],  # Note: `NEWLINE_TOKEN` is needed in `user_defined_symbols`.
        byte_fallback=True,
        split_digits=True,
        allow_whitespace_only_pieces=True,
        remove_extra_whitespaces=False,
    )


if __name__ == "__main__":
    main()
