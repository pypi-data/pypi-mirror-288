
## Archon - Create and Benchmark LLM Chains with JSON

As the number of large language models available increases, using different models in tandem can provide better results than one alone. Archon provides a modular framework for sampling, ranking, and fusing model responses to surpass the capabilities of existing closed-source APIs.

## QuickStart
Archon works by taking in a config file in JSON format that specifies the model you want to run and its available parameters. 
Let's start with the basics. Say I want to ask GPT 4 Turbo a question and output a singular response. We could create a config that looks like this:
```
archon_config = {
    "name": "gpt-4-turbo-quickstart",
    "layers": [
         [
            {
                "type": "model",
                "model": "gpt-4-turbo",
                "model_type": "OpenAI_API",
                "checkpoint": "",
                "top_k": 1,
                "temperature": 0.7,
                "max_context_length": 2048,
                "samples": 1
            }
        ]
    ]
}
```
To generate a response:
```
# The config can be read from a .json file or directly from a python dictionary
archon = Archon(archon_config)

testing_instruction = [{"role": "user", "content": "How do I make a cake?"}]

response = archon.generate(testing_instruction)

print(response)
```

Let's move on to something more complicated. Let's say I want to query Qwen 2 from Together, have Claude 3.5 Sonnet critique the response, and then merge both responses into a final output using Qwen 1.5. Here's what our config would look like:
```
archon_config =  {
    "name": "archon-testing",
    "layers": [
        [   
            {
                "type": "model",
                "model": "Qwen/Qwen2-72B-Instruct",
                "model_type": "Together_API",
                "checkpoint": "",
                "temperature": 0.7,
                "max_context_length": 2048,
                "samples": 10
            }
        ],
        [
            {
                "type": "critic",
                "model": "claude-3-5-sonnet-20240620",
                "model_type": "Anthropic_API",
                "checkpoint": "",
                "temperature": 0.7,
                "max_context_length": 8192,
                "samples": 1
            }
        ],
        [
            {
                "type": "fuser",
                "model": "Qwen/Qwen1.5-110B-Chat",
                "model_type": "Together_API",
                "checkpoint": "",
                "top_k": 1,
                "temperature": 0.7,
                "max_context_length": 2048,
                "samples": 1
            }
        ]
    ]
}
```
Under ```archon/configs```, you can find more examples of increasingly complex LLM chains.
## Benchmarks
Once you have created a config, you can leverage pre-existing benchmark frameworks to assess accuracy. We provide classes for [AlpacaEval](https://github.com/tatsu-lab/alpaca_eval), [ArenaHardAuto](https://github.com/lm-sys/arena-hard-auto), and [MT Bench](https://huggingface.co/spaces/lmsys/mt-bench). The classes are under ```archon/benchmarks.py``` where you can modify the input question files under the class ```load_dataset()``` call.
Here is an example command for running your config against ArenaHardAuto:
```
python3 archon/gen_answers.py --benchmark arena_hard_auto --config archon/configs/<your-config-file>.json --output_dir results --parallel 16
```
This will run the model structure specified in your config file against the question set specified under the ArenaHardAuto class and output the responses in `.jsonl` format under the results folder. 

Todo: add a complete list of available cli commands

## Config Details
More info on the config and complete list of commands

## Resources
### Inspiration
- 📚 [PyTorch](https://github.com/pytorch/pytorch/): placeholder
- 📚 [DSPy](https://github.com/stanfordnlp/dspy): placeholder
- 📚 [ARES](https://github.com/stanford-futuredata/ARES.git): placeholder
- 📚 [TextGrad](https://github.com/zou-group/textgrad?tab=readme-ov-file): placeholder

### Citation
```bibtex
@article{placeholder,
      title={Archon: Bending the Scaling Curves with Model Ensembling, Sampling, and Ranking},
      author={placeholder},
      year={2024},
      eprint={placeholder},
      archivePrefix={arXiv}
}
```

