import datasets
import json
import shortuuid
import time
import tiktoken


class Benchmark:
    def __init__(self, debug_data=False):
        self.debug_data = debug_data
        self.dataset = None
        self.save_type = "json"

    def load_dataset(self):
        raise NotImplementedError("Subclasses should implement this method")

    def get_answer(self):
        raise NotImplementedError("Subclasses should implement this method")

    def save_answers(self):
        raise NotImplementedError("Subclasses should implement this method")


class AlpacaEvalBenchmark(Benchmark):

    def __init__(self, debug_data=False):
        super().__init__(debug_data)

    def load_dataset(self):
        self.dataset = datasets.load_dataset(
            "tatsu-lab/alpaca_eval", "alpaca_eval_gpt4_baseline", trust_remote_code=True
        )["eval"]
        self.dataset = self.dataset.remove_columns(["output", "generator"])

        if self.debug_data:
            self.dataset = self.dataset.select(range(5))

        return self.dataset

    def get_answer(self, item, model, config):
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": item["instruction"]},
        ]
        output = model.generate(messages)
        return {"output": output, "generator": config["name"]}

    def process_results(self, results):
        self.dataset = self.dataset.add_column("output", [r["output"] for r in results])
        self.dataset = self.dataset.add_column(
            "generator", [r["generator"] for r in results]
        )
        return self.dataset

    def save_answers(self, output_path, answers=None):
        if answers is None:
            answers = self.dataset

        with open(output_path, "w") as f:
            json.dump(list(answers), f, indent=2)


class MtBenchBenchmark(Benchmark):

    def __init__(self, debug_data=False):
        super().__init__(debug_data)
        self.save_type = "jsonl"

    def load_dataset(self):
        question_file = "FastChat/fastchat/llm_judge/data/mt_bench/question.jsonl"
        self.dataset = datasets.load_dataset("json", data_files=question_file)["train"]
        if self.debug_data:
            self.dataset = self.dataset.select(range(5))
        return self.dataset

    def get_answer(self, item, model, config, num_choices=1):

        temperature_config = {
            "writing": 0.7,
            "roleplay": 0.7,
            "extraction": 0.0,
            "math": 0.0,
            "coding": 0.0,
            "reasoning": 0.0,
            "stem": 0.1,
            "humanities": 0.1,
            "arena-hard-200": 0.0,
        }

        temperature = None
        if "required_temperature" in item.keys():
            temperature = item["required_temperature"]
        elif item["category"] in temperature_config:
            temperature = temperature_config[item["category"]]

        choices = []
        for i in range(num_choices):
            turns = []
            conv = [
                {"role": "system", "content": "You are a helpful assistant."},
            ]

            for j in range(len(item["turns"])):
                conv.append({"role": "user", "content": item["turns"][j]})
                output = model.generate(conv, temperature=temperature)

                conv.append({"role": "assistant", "content": output})
                turns.append(output)

            choices.append({"index": i, "turns": turns})

        ans = {
            "answer_id": shortuuid.uuid(),
            "model_id": config["name"],
            "choices": choices,
            "tstamp": time.time(),
        }
        return ans

    def process_results(self, results):

        # TODO: Better way to do this lol

        self.dataset = self.dataset.add_column(
            "answer_id", [r["answer_id"] for r in results]
        )
        self.dataset = self.dataset.add_column(
            "model_id", [r["model_id"] for r in results]
        )
        self.dataset = self.dataset.add_column(
            "choices", [r["choices"] for r in results]
        )
        self.dataset = self.dataset.add_column("tstamp", [r["tstamp"] for r in results])

        return self.dataset

    def save_answers(self, output_path, answers=None):
        if answers is None:
            answers = self.dataset

        # mt_bench expects jsonl format
        with open(output_path, "w") as f:
            for result in answers:
                f.write(json.dumps(result) + "\n")


class ArenaHardAutoBenchmark(Benchmark):

    def __init__(self, debug_data=False):
        super().__init__(debug_data)
        self.save_type = "jsonl"

    def load_dataset(self):
        question_file = "arena_hard_auto/arena-questions.jsonl"
        self.dataset = datasets.load_dataset("json", data_files=question_file)["train"]
        if self.debug_data:
            self.dataset = self.dataset.select(range(5))
        return self.dataset

    def get_answer(self, item, model, config, num_choices=1):
        temperature = 0.7
        encoding = tiktoken.encoding_for_model(
            "gpt-3.5-turbo"
        )  # arena benchamrks on gpt 3.5 encoding
        choices = []
        for i in range(num_choices):
            turns = []
            conv = [
                {"role": "system", "content": "You are a helpful assistant."},
            ]

            for j in range(len(item["turns"])):
                conv.append({"role": "user", "content": item["turns"][j]["content"]})
                output = model.generate(conv, temperature=temperature)

                conv.append({"role": "assistant", "content": output})
                turns.append(
                    {
                        "content": output,
                        "token_len": len(
                            encoding.encode(output, disallowed_special=())
                        ),
                    }
                )

            choices.append({"index": i, "turns": turns})

        ans = {
            "question_id": item["question_id"],
            "answer_id": shortuuid.uuid(),
            "model_id": config["name"],
            "choices": choices,
            "tstamp": time.time(),
        }
        return ans

    def process_results(self, results):

        # TODO: Better way to do this lol
        self.dataset = self.dataset.add_column(
            "answer_id", [r["answer_id"] for r in results]
        )
        self.dataset = self.dataset.add_column(
            "model_id", [r["model_id"] for r in results]
        )
        self.dataset = self.dataset.add_column(
            "choices", [r["choices"] for r in results]
        )
        self.dataset = self.dataset.add_column("tstamp", [r["tstamp"] for r in results])

        return self.dataset

    def save_answers(self, output_path, answers=None):
        if answers is None:
            answers = self.dataset

        with open(output_path, "w") as f:
            for result in answers:
                f.write(json.dumps(result) + "\n")
