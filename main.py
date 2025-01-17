import argparse
import os
import sys

from llama_cpp import Llama
from termcolor import cprint

cwd = os.getcwd()
model_path = os.path.join(cwd, "solar-10.7b-instruct-v1.0-uncensored.Q4_K_M.gguf")

print_bot = lambda x: cprint(x, 'green', end='')

def main(
    model_path="solar-10.7b-instruct-v1.0-uncensored.Q4_K_M.gguf",
    verbose=False,
    n_threads=2,
    seed=12,
    n_gpu_layers=None
):
    params = {
        "model_path": model_path,
        #"n_ctx": 768, #32768
        #"seed": seed,
        "n_threads": n_threads,
        "verbose": verbose,
    }

    if n_gpu_layers:
        params.update({'n_gpu_layers': n_gpu_layers})

    llm = Llama(**params)
    os.system("clear")

    messages = ""
    while True:
        prompt = input("\n>>> ")

        if prompt == "clear":
            print("=== Clear! ===")
            messages = ""
            continue

        if prompt == "bye":
            break

        messages += f"User: {prompt}\nAssistant: "

        stream = llm(
            messages,
            max_tokens=512,
            stream=True,
        )

        for output in stream:
            out_text = output["choices"][0]["text"]
            messages += out_text
            print_bot(out_text)
            sys.stdout.flush()

        messages += " "


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--model_path", default=model_path, help="Full path to the quantized model GGUF file."
    )
    parser.add_argument(
        "--n_threads", default=16, help="Number of threads to run the LLM."
    )
    parser.add_argument(
        "--n_gpu_layers", default=None, help="Number of GPU layers to offload to the GPU if available."
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Whether to have verbose outputs."
    )
    args = parser.parse_args()
    main(model_path=args.model_path, n_threads=args.n_threads, verbose=args.verbose)