import copy
import requests
import time
import os
from loguru import logger
import openai
import anthropic
from groq import Groq
import json

DEBUG = int(os.environ.get("DEBUG", "0"))
DEFAULT_CONFIG = "config/archon-1-110bFuser-2-110bM.json"


def clean_messages(messages):
    messages_alt = messages.copy()
    for msg in messages_alt:
        if isinstance(msg["content"], dict) and "content" in msg["content"]:
            msg["content"] = msg["content"]["content"]
    return messages_alt


def load_config(config_path=None):
    """
    Load the configuration from a given file path.
    If no path is provided or the file doesn't exist, use the default configuration.
    """

    config = config_path if config_path else DEFAULT_CONFIG
    if os.path.isfile(config):
        with open(config_path, "r") as file:
            config = json.load(file)
            return config
    else:
        raise ValueError(
            f"config_path points to missing file. Reimport {DEFAULT_CONFIG} to config directory"
        )


def format_prompt(messages):
    prompt = ""
    for msg in messages:
        role = msg["role"]
        content = msg["content"]
        prompt += f"{role.capitalize()}: {content}\n\n"
    prompt += "Assistant: "
    return prompt


class vllmWrapper:
    def __init__(self, model_name):
        from vllm import LLM
        from transformers import AutoTokenizer

        if DEBUG:
            logger.debug("Initializing vLLM model")
        self.model = LLM(model=model_name)

        if DEBUG:
            logger.debug("Initializing vLLM tokenizer")

        self.tokenizer = AutoTokenizer.from_pretrained(model_name)

    def __call__(self, model_name, messages, max_tokens, temperature):
        from vllm import SamplingParams

        if DEBUG:
            logger.debug(
                f"Sending messages ({len(messages)}) (last message: `{messages[-1]['content'][:20]}...`) to `{model_name}` with temperature {temperature}."
            )

        if (
            hasattr(self.tokenizer, "chat_template")
            and self.tokenizer.chat_template is not None
        ):
            prompt = self.tokenizer.apply_chat_template(
                messages, tokenize=False, add_generation_prompt=True
            )

        else:
            logger.info("No chat template, formatting as seen in util")
            prompt = format_prompt(messages)

        if DEBUG:
            logger.debug(f"Full prompt being sent: {prompt}")

        sampling_params = SamplingParams(temperature=temperature, max_tokens=max_tokens)
        outputs = self.model.generate([prompt], sampling_params, use_tqdm=False)
        response = outputs[0].outputs[0].text

        if DEBUG:
            logger.debug(f"Output: `{response[:50]}...`.")

        return response


def generate_together(
    model,
    messages,
    max_tokens=2048,
    temperature=0.7,
):
    output = None

    for sleep_time in [1, 2, 4, 8, 16, 32]:

        try:

            if DEBUG:
                logger.debug(
                    f"Sending messages ({len(messages)}) (last message: `{messages[-1]['content'][:20]}...`) to `{model}` with temperature {temperature}."
                )
                logger.debug(f"Full message being sent: {messages}")

            endpoint = "https://api.together.xyz/v1/chat/completions"

            time.sleep(2)

            res = requests.post(
                endpoint,
                json={
                    "model": model,
                    "max_tokens": max_tokens,
                    "temperature": (temperature if temperature > 1e-4 else 0),
                    "messages": messages,
                },
                headers={
                    "Authorization": f"Bearer {os.environ.get('TOGETHER_API_KEY')}",
                },
            )
            if "error" in res.json():

                print("------------------------------------------")
                print(f"Model with Error: {model}")
                print(res.json())
                print("------------------------------------------")

                if res.json()["error"]["type"] == "invalid_request_error":
                    return None

            output = res.json()["choices"][0]["message"]["content"]

            break

        except Exception as e:
            logger.error(f"{e} on response: {res}")
            print(f"Retry in {sleep_time}s..")
            time.sleep(sleep_time)

    if output is None:
        return output

    if DEBUG:
        logger.debug(f"Output: `{output[:50]}...`.")

    return output.strip()


def generate_openai(
    model,
    messages,
    max_tokens=2048,
    temperature=0.7,
):

    client = openai.OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY"),
    )
    time.sleep(2)

    for sleep_time in [1, 2, 4, 8, 16, 32]:
        try:

            if DEBUG:
                logger.debug(
                    f"Sending messages ({len(messages)}) (last message: `{messages[-1]['content'][:20]}`) to `{model}`."
                )

            completion = client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
            )
            output = completion.choices[0].message.content
            break

        except Exception as e:
            logger.error(e)
            logger.info(f"Retry in {sleep_time}s..")
            time.sleep(sleep_time)

    output = output.strip()

    return output


def generate_anthropic(
    model,
    messages,
    max_tokens=2048,
    temperature=0.7,
):
    client = anthropic.Client(
        api_key=os.environ.get("ANTHROPIC_API_KEY"),
    )

    time.sleep(2)

    max_tokens = 4096
    for sleep_time in [1, 2, 4, 8, 16, 32]:
        try:
            if DEBUG:
                logger.debug(
                    f"Sending messages ({len(messages)}) (last message: `{messages[-1]['content'][:20]}`) to `{model}`."
                )

            system = ""
            for message in messages:
                if message["role"] == "system":
                    system = message["content"]
                    break

            if system == "":
                logger.warning("No system message")

            messages_alt = [msg for msg in messages if msg["role"] != "system"]
            completion = client.messages.create(
                model=model,
                system=system,
                messages=messages_alt,
                temperature=temperature,
                max_tokens=max_tokens,
            )
            output = completion.content[0].text

        except Exception as e:
            logger.error(e)
            logger.info(f"Retry in {sleep_time}s..")
            time.sleep(sleep_time)

    if output is None:
        return None

    output = output.strip()

    return output


def generate_groq(
    model,
    messages,
    max_tokens=2048,
    temperature=0.7,
):

    client = Groq(
        api_key=os.environ.get("GROQ_API_KEY"),
    )

    for sleep_time in [1, 2, 4, 8, 16, 32]:
        try:

            if DEBUG:
                logger.debug(
                    f"Sending messages ({len(messages)}) (last message: `{messages[-1]['content'][:20]}`) to `{model}`."
                )

            completion = client.chat.completions.create(
                messages=messages,
                model=model,
                temperature=temperature,
                max_tokens=max_tokens,
            )

            output = completion.choices[0].message.content
            break

        except Exception as e:
            logger.error(e)
            logger.info(f"Retry in {sleep_time}s..")
            time.sleep(sleep_time)

    return output.strip()


def generate_tgi(
    model,
    messages,
    max_tokens=2048,
    temperature=0.7,
):
    client = openai.OpenAI(base_url=model, api_key="-")  # TGI endpoint

    output = client.chat.completions.create(
        model="tgi",
        messages=clean_messages(messages),
        temperature=temperature,
        max_tokens=max_tokens,
        stream=False,
    )

    return output.strip()


def inject_references_to_messages(messages, references, critiques=None):

    if critiques is not None:

        messages = copy.deepcopy(messages)

        system = """You have been provided with a set of responses with their individual critiques of strengths/weaknesses from various open-source models to the latest user query. Your task is to synthesize these responses into a single, high-quality response. It is crucial to critically evaluate the information provided in these responses and their provided critiques of strengths/weaknesses, recognizing that some of it may be biased or incorrect. Your response should not simply replicate the given answers but should offer a refined, accurate, and comprehensive reply to the instruction. Ensure your response is well-structured, coherent, and adheres to the highest standards of accuracy and reliability.

        Responses from models:\n\n"""

        count = 0
        assert len(references) == len(critiques)
        for reference, critique in zip(references, critiques):
            system += f"{count+1}. {reference} \n\nCritique:\n{critique}"
            count += 1
            if count != len(references):
                system += "\n\n"

        if messages[0]["role"] == "system":

            messages[0]["content"] += "\n\n" + system

        else:

            messages = [{"role": "system", "content": system}] + messages

        # breakpoint()

        return messages

    else:

        messages = copy.deepcopy(messages)

        system = """You have been provided with a set of responses from various open-source models to the latest user query. Your task is to synthesize these responses into a single, high-quality response. It is crucial to critically evaluate the information provided in these responses, recognizing that some of it may be biased or incorrect. Your response should not simply replicate the given answers but should offer a refined, accurate, and comprehensive reply to the instruction. Ensure your response is well-structured, coherent, and adheres to the highest standards of accuracy and reliability.

        Responses from models:"""

        for i, reference in enumerate(references):

            system += f"\n{i+1}. {reference}"

        if messages[0]["role"] == "system":

            messages[0]["content"] += "\n\n" + system

        else:

            messages = [{"role": "system", "content": system}] + messages

        return messages


def generate_with_references(
    model,
    messages,
    references=[],
    max_tokens=2048,
    temperature=0.7,
    generate_fn=generate_together,
):

    if len(references) > 0:

        messages = inject_references_to_messages(messages, references)

    return generate_fn(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
    )
