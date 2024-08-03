from archon.archon import Archon
from loguru import logger
import json
import datasets
from functools import partial
import argparse
import concurrent.futures
from tqdm import tqdm
from archon.utils import load_config
import archon.utils as utils
import os
from archon.benchmarks import AlpacaEvalBenchmark, MtBenchBenchmark, ArenaHardAutoBenchmark
import time


BENCHMARK_CLASSES = {
    "alpaca_eval": AlpacaEvalBenchmark,
    "mt_bench": MtBenchBenchmark,
    "arena_hard_auto": ArenaHardAutoBenchmark,
}


def load_benchmark(benchmark_name, debug):
    if benchmark_name in BENCHMARK_CLASSES:
        return BENCHMARK_CLASSES[benchmark_name](debug)
    else:
        raise ValueError(
            f"Unsupported benchmark: {benchmark_name}. Only 'alpaca_eval', 'mt_bench, and 'arena_hard_auto' are supported."
        )


def main(args):
    logger.info(f"Start.")

    if args.debug:
        utils.DEBUG = 1
        logger.debug("In DEBUG mode")

    # Initialize the Archon with the specified configuration settings.
    logger.info("loading: " + args.config)
    archon_config = load_config(args.config)
    if "name" not in archon_config:
        archon_config["name"] = "archon-" + time.strftime("%m%d%Y-%H:%M:%S")

    if utils.DEBUG:
        logger.debug(f"{archon_config=}")

    archon = Archon(config=archon_config)

    logger.info("Finished initializing archon")

    benchmark = load_benchmark(args.benchmark, args.debug_data)
    eval_set = benchmark.load_dataset()

    if args.debug_data:
        logger.debug(f"{eval_set}")

    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.parallel) as executor:
        results = list(
            tqdm(
                executor.map(
                    partial(benchmark.get_answer, model=archon, config=archon_config),
                    eval_set,
                ),
                total=len(eval_set),
            )
        )
    if args.debug_data:
        print(results)

    eval_set = benchmark.process_results(results)

    ########### Save Output #########
    output_dir = f"{args.output_dir.rstrip('/')}/{args.benchmark}/"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    test = "" if not args.debug_data else "TEST"
    timestamp = time.strftime("%I%M%S%p%m%d%Y")
    output_path = f"{output_dir}{archon_config['name']}{test}.{benchmark.save_type}"

    # add timestamp if it already exits
    if os.path.isfile(output_path):
        output_path = f"{output_dir}{archon_config['name']}{test}-{timestamp}.{benchmark.save_type}"

    logger.info(f"Saving outputs to {output_path}.")

    # save answers intermediately, not just at end
    benchmark.save_answers(output_path, eval_set)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--benchmark",
        type=str,
        choices=["alpaca_eval", "mt_bench", "arena_hard_auto"],
        required=True,
        help="The benchmark to use for evaluation",
    )

    parser.add_argument("--config", type=str, help="Archon config to gen answers from")

    parser.add_argument(
        "--output_dir",
        type=str,
        default="outputs/",
        help="output directory",
    )

    parser.add_argument(
        "--parallel", type=int, default=16, help="The number of concurrent API calls."
    )

    parser.add_argument("--debug_data", action="store_true")
    parser.add_argument("--debug", action="store_true")

    args = parser.parse_args()

    main(args)
