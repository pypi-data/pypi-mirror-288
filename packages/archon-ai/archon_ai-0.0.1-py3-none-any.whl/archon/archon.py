from archon.fuser import Fuser
from archon.ranker import Ranker
from archon.critic import Critic
from archon.verifier import Verifier
from archon.unit_test_generator import Unit_Test_Generator
import archon.utils as utils
from archon.model import Model
from loguru import logger

# from ranking import Ranker


class Layer:
    def __init__(self, layer_config):
        self.config = layer_config
        self.models = []
        self.initialize_layer()

    def initialize_layer(self):

        model_list = self.config
        if isinstance(self.config, dict):
            model_list = self.config["models"]
        for model in model_list:
            if model["type"] == "model":
                self.models.append(Model(model))
            elif model["type"] == "ranker":
                self.models.append(Ranker(model))
            elif model["type"] == "fuser":
                self.models.append(Fuser(model))
            elif model["type"] == "critic":
                self.models.append(Critic(model))
            elif model["type"] == "verifier":
                self.models.append(Verifier(model))
            elif model["type"] == "unit_test_generator":
                self.models.append(Unit_Test_Generator(model))
            else:
                raise ValueError(f"Unsupported object type: {model['type']}")
        logger.info(f"Initialized layer with {len(self.models)} models")

    def process(
        self,
        init_input,
        prev_outputs=[],
        prev_critiques=None,
        temperature=None,
        unit_tests=None,
    ):

        query = init_input[-1]["content"]
        output = []
        output_critiques = None

        # if self.prev_layer is not None:
        #     prev_outputs, prev_critques = self.prev_layer.process()
        # else:
        #     prev_outputs = []
        #     prev_critques = []

        if len(prev_outputs) > 32:
            logger.info(
                "WARNING: Previous inputs are too long! Will likely exceed context window of generator LMs"
            )

        for model in self.models:

            if unit_tests is not None:
                assert init_input[-1]["role"] == "user"
                current_query = init_input[-1]["content"]
                current_query += (
                    " Your response should pass the following unit tests: \n"
                )
                current_query += "- " + "\n- ".join(unit_tests)
                init_input[-1]["content"] = current_query
                unit_tests = None

            if isinstance(model, Model):  # Generating responses from ensemble
                assert len(prev_outputs) == 0
                output.extend(model.generate_from_messages(init_input, temperature))

            elif isinstance(
                model, Fuser
            ):  # Generating fused responses from ensemble candidates
                # assert len(layer) == 1 and isinstance(model, Fuser)
                fused_output = model.fuse(
                    init_input, prev_outputs, critiques=prev_critiques
                )
                output.extend(fused_output)

            elif isinstance(
                model, Ranker
            ):  # Ranking the responses from ensemble candidates
                assert len(self.models) == 1 and isinstance(model, Ranker)
                ranked_outputs, ranked_critiques = model.rank(
                    query, prev_outputs, critiques=prev_critiques
                )
                output.extend(ranked_outputs)
                output_critiques = ranked_critiques

            elif isinstance(
                model, Critic
            ):  # Evaluating the responses from ensemble candidates
                assert len(self.models) == 1 and isinstance(model, Critic)
                evaluations = model.evaluate_candidates(
                    query, prev_outputs, temperature
                )

                output = prev_outputs
                output_critiques = evaluations

            elif isinstance(
                model, Verifier
            ):  # Verifying the responses from ensemble candidates

                assert len(self.models) == 1 and isinstance(model, Verifier)
                verified_outputs, verified_critiques = model.filter_responses(
                    init_input, prev_outputs, output_critiques
                )
                output.extend(verified_outputs)
                output_critiques = verified_critiques

            elif isinstance(
                model, Unit_Test_Generator
            ):  # Generating unit tests for the responses from ensemble candidates
                assert len(self.models) == 1 and isinstance(model, Unit_Test_Generator)
                unit_tests = model.generate_unit_tests(init_input, temperature)

            else:
                raise ValueError(f"Unsupported object type: {type(model).__name__}")

        # breakpoint()
        return output, output_critiques, unit_tests


class Archon:
    """
    Archon class to generate responses given an input by applying multiple layers
    of Models, Rankers, and Fusers sequentially.
    """

    def __init__(self, config):
        """
        Initialize the Archon with configuration settings.

        Parameters:
        config (dict): Configuration dictionary containing layers and other settings.
        """
        self.config = config

        self.initialize_layers()

    def initialize_layers(self):
        """
        Initialize the models, rankers, and fusers based on the configuration.
        """

        self.layers = []
        for layer_config in self.config["layers"]:
            layer = Layer(layer_config)
            self.layers.append(layer)

        print(f"Archon initialized with {len(self.layers)} layers.")

    def generate(self, conv, temperature=None):

        response, critique = self._generate(conv, temperature)

        assert (
            len(response) > 0
            and isinstance(response[0], str)
            and isinstance(response, list)
        ), f"response not valid: {response}"
        return response[0]

    def _generate(self, conv, temperature=None):
        """
        Generate responses by applying each layer sequentially to the inputs.

        Parameters:
        conv (str): list of dicts

        Returns:
        list of str: The final generated responses.
        """

        # messages should just be a single list of optional system and user messages
        init_input = conv
        # query = conv[-1]["content"]

        prev_output = []
        prev_critiques = []
        unit_tests = None

        for i in range(len(self.layers)):

            layer = self.layers[i]
            layer_output = []
            layer_critique = []

            if utils.DEBUG:
                logger.debug(
                    f"Running layer {i}, with {len(prev_output)} previous outputs and {len(prev_critiques) if prev_critiques else 0} previous critiques"
                )

            if utils.DEBUG:
                logger.debug(f"Running layer {i}")

            layer_output, layer_critique, unit_tests = layer.process(
                init_input,
                prev_output,
                prev_critiques,
                temperature=temperature,
                unit_tests=unit_tests,
            )

            prev_output = layer_output

            # None if empty
            prev_critiques = layer_critique if layer_critique else None

        return prev_output, prev_critiques
