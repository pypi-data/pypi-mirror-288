import re
from archon.model import Model

class Verifier:
    def __init__(self, config):
        """
        Initialize the Verifier with configuration settings.

        Parameters:
        config (dict): Configuration dictionary containing model settings and other parameters.
        """
        self.config = config
        self.initialize_verifier()

    def initialize_verifier(self):
        """
        Initialize the verifier model and tokenizer with the specified settings.
        """
        self.model_name = self.config["model"]
        self.model_type = self.config["model_type"]
        self.temperature = self.config["temperature"]
        self.max_context_length = self.config["max_context_length"]
        self.samples = self.config["samples"]

        self.verifier = Model(config=self.config)

        print(f"Verifier model initialized: {self.model_name}")

    def generate_reasoning(self, query, candidate, temperature=None):
        """
        Generate reasoning for a candidate.

        Parameters:
        query (str): The input query.
        candidate (str): The candidate generation.
        temperature (float, optional): Sampling temperature.

        Returns:
        str: The reasoning for the candidate.
        """
        assert isinstance(query, str) and len(query) > 0
        assert isinstance(candidate, str) and len(candidate) > 0

        if temperature is None:
            temperature = self.temperature

        user_prompt = f"I will provide you with a response indicated by the identifier 'Response'. Provide reasoning for why the response accurately and completely addresses the instruction: {query}.\n"
        user_prompt += f"\nResponse: {candidate}"
        user_prompt += f"\n\nInstruction: {query}.\n\nProvide the reasoning for the response above based on its relevance, completeness, and accuracy when compared to the instruction. "
        user_prompt += f"Do not include any preface or text after the reasoning."

        messages = [
            {"role": "system", "content": "You are a reasoning generator for instructions and their responses."},
            {"role": "user", "content": user_prompt},
        ]

        for retry in range(10):
            try:
                reasoning = self.verifier.generate_from_messages(messages)
                return reasoning[0]
            except Exception as e:
                print(f"Error generating reasoning: {e}")
                print(f"Retry #{retry + 1}...")
                continue

        raise ValueError("Failed to generate reasoning with verifier!")

    def extract_verdict(generated_response: str):
        """
        Extract the verdict from the generated response.
        """
        assert "[Correct]" in generated_response or "[Incorrect]" in generated_response, f"Verdict not found in generated response. Found: {generated_response}"
        assert not ("[Correct]" in generated_response and "[Incorrect]" in generated_response), f"Both '[Correct]' and '[Incorrect]' found in generated response. Found: {generated_response}"
        #return "[Correct]" if "[Correct]" in generated_response else "[Incorrect]"
        return 1 if "[Correct]" in generated_response else 0

    def verify_query_reasoning_pairs(self, query, candidate, reasoning, temperature=None):
        """
        Verify the query-reasoning pair.

        Parameters:
        query (str): The input query.
        candidate (str): The candidate generation.
        reasoning (str): The reasoning for the candidate.
        temperature (float, optional): Sampling temperature.

        Returns:
        int: 1 if the reasoning is correct, 0 otherwise.
        """
        assert isinstance(query, str) and len(query) > 0
        assert isinstance(candidate, str) and len(candidate) > 0
        assert isinstance(reasoning, str) and len(reasoning) > 0

        if temperature is None:
            temperature = self.temperature

        user_prompt = [
            f"Given the following query, response, and reasoning, evaluate whether or not the response is correct.\n"
            f"- In your evaluation, you should consider how the response aligns with the reasoning and query.\n"
            f"- You should also consider whether or not the logic in the reasoning is correct and complete.\n"
            f"- Provide an explanation for your verdict before you return your evaluation. At the end of your explanation, you should finish with your verdict of either '[Correct]' or '[Incorrect]'.\n"
            f"- You must include a verdict with one of these formatted options: '[Correct]' or '[Incorrect]'.\n\n"
            f"Query: {query}\n"
            f"Response: {candidate}\n"
            f"Reasoning: {reasoning}\n"
        ]
        user_prompt = "".join(user_prompt)

        messages = [
            {"role": "system", "content": "You are a verification system for judging responses and their reasoning."},
            {"role": "user", "content": user_prompt},
        ]

        for retry in range(10):
            try:
                output = self.verifier.generate_from_messages(messages)
                #breakpoint()
                verification_result = self.parse_verification_output(output[0])
                return verification_result
            except Exception as e:
                print(f"Error verifying query-reasoning pair: {e}")
                print(f"Retry #{retry + 1}...")
                continue

        raise ValueError("Failed to verify query-reasoning pair with verifier!")

    def parse_verification_output(self, output):
        """
        Parse the output from the verification model to extract the verdict.

        Parameters:
        output (str): The raw output from the verification model.

        Returns:
        int: 1 if the reasoning is correct, 0 otherwise.
        """
        assert isinstance(output, str) and len(output) > 0

        if "[Correct]" in output and "[Incorrect]" in output:
            raise ValueError("Both '[Correct]' and '[Incorrect]' found in verification output.")
        elif "[Correct]" in output:
            return 1
        elif "[Incorrect]" in output:
            return 0
        else:
            raise ValueError("Verdict not found in verification output.")

    def filter_responses(self, init_input, candidates, critiques):
        """
        Filter responses based on verification results.

        Parameters:
        init_input (dict): The input conversation.
        candidates (list of str): The list of candidate generations.

        Returns:
        list: A list of verified correct candidate responses.
        """

        query = init_input[-1]["content"]
        query = ""
        for message in init_input:
            if message["role"] == "user":
                query += message["content"] + " "
        query = query.strip()

        assert isinstance(init_input, list) and isinstance(init_input[-1], dict)
        assert isinstance(query, str) and len(query) > 0
        assert isinstance(candidates, list) and len(candidates) > 0

        ####################################

        verified_responses = []
        verified_critiques = []
        incorrect_responses = []

        if critiques is not None:
            assert isinstance(critiques, list) and all(isinstance(critique, str) for critique in critiques)
            assert len(critiques) == len(candidates) 

        for cand_index in range(len(candidates)):
            cand = candidates[cand_index]
            try:
                reasoning = self.generate_reasoning(query, cand)
                verification_result = self.verify_query_reasoning_pairs(query, cand, reasoning)
                if verification_result == 1:
                    verified_responses.append(cand)
                    if critiques is not None:
                        verified_critiques.append(critiques[cand_index])
                else:
                    incorrect_responses.append(cand)
            except Exception as e:
                print(f"Error processing candidate for verification: {e}")

        ####################################
        
        print(f"Verified Responses Length: {len(verified_responses)}")
        print(f"Incorrect Responses Length: {len(incorrect_responses)}")

        verified_critiques = verified_critiques if len(verified_critiques) > 0 else None
        return verified_responses, verified_critiques

