import argparse
from .instruct import load_model, infer
from flask import Flask, render_template, request
from flask_socketio import SocketIO
import time
from flask_cors import CORS
from concurrent.futures import ThreadPoolExecutor
import os
from llama_index.llms.llama_cpp import LlamaCPP

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--name", type=str, default="Mistral-instruct", help="Name of the model or path to the model file")
    parser.add_argument("--temperature", type=float, default=0.5, help="Temperature for sampling")
    parser.add_argument("--max_new_tokens", type=int, default=512, help="Maximum number of new tokens to generate")
    parser.add_argument("--model_kwargs", type=dict, default={"n_gpu_layers":0}, help="Arguments for the model")
    args = parser.parse_args()
    model_dir = os.path.join(os.getcwd(), 'model')
    print(model_dir)


    if not os.path.exists(model_dir):
        print('creating dir')
        # If the directory doesn't exist, create it
        os.makedirs(model_dir, exist_ok=True)
        print('created model directory')
    model_path = load_model(args.name)
    print(model_path)
    print("Starting CLI-based inference...\n")
    infer(model_path, args.temperature, args.max_new_tokens, args.model_kwargs)


if __name__ == "__main__":
    main()
