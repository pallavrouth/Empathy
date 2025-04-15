import json
from openai import OpenAI


class ResponseGenerator:
    def __init__(self, api_key):
        """
        Initialize the ResponseGenerator with the OpenAI API key.
        Parameters:api_key (str): OpenAI API key.
        """
        self.openai_client = OpenAI(api_key=api_key)

    def generate_response(self, review_text, component_input, base_input):
        """
        Generate a structured response using OpenAI's API.
        Parameters:
            review_text (str): Text of the review document.
            component_input (list): Component-specific input prompts.
            base_input (list): Base input prompts for the API.
            json_format (dict): JSON schema for the API response.

        Returns:
            list: Extracted feedback from the API response.
        """
        response_template_input = [
            {
                "role": "assistant",
                "content": "Great. Provide the review document. I will provide constructive feedback using the traits.",
            },
            {
                "role": "user",
                "content": f"""Here is the review document:
                {review_text}

                1. Identify all sentences that can be improved under each trait using the typical examples, as truthfully as possible. Avoid forcing classification into traits when it does not apply.
                2. Generate suggested improvements for these sentences using the constructive examples. If these are for sentences enclosed by '<<>>', they already contain changes. Make sure the suggestions retain retains key aspects of the sentences. 
                3. Use the description of the trait to generate a comment that highlights why the sentence needs improvement strictly using the template 'The following sentence(s) does not [description of trait] instead it [issue]....'. 
                Format output strictly using the following template: 
                <Trait:> <Comment highlighting issue> <Sentences that needs improvement:> <Suggested improvement for each sentence:>""",
            },
        ]

        gpt_input = base_input + component_input + response_template_input

        completion_structured = self.openai_client.chat.completions.create(
            model="gpt-4o",
            messages=gpt_input,
            max_tokens=5000,
            response_format={
                "type": "json_schema",
                "json_schema": {
                    "name": "cre_improvement_feedback",
                    "schema": {
                        "type": "object",
                        "properties": {
                            "improvements": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "trait": {"type": "string"},
                                        "comment": {"type": "string"},
                                        "sentences_needing_improvement": {
                                            "type": "array",
                                            "items": {"type": "string"},
                                        },
                                        "suggested_improvement": {
                                            "type": "array",
                                            "items": {"type": "string"},
                                        },
                                    },
                                    "required": [
                                        "trait",
                                        "comment",
                                        "sentences_needing_improvement",
                                        "suggested_improvement",
                                    ],
                                    "additionalProperties": False,
                                },
                            }
                        },
                        "required": ["improvements"],
                        "additionalProperties": False,
                    },
                    "strict": True,
                },
            },
        )

        response_structured = completion_structured.choices[0].message.content
        sdata = json.loads(response_structured)

        extracted_info = [
            {
                "trait": entry["trait"],
                "comment": entry["comment"],
                "sentences_needing_improvement": entry["sentences_needing_improvement"],
                "suggested_improvement": entry["suggested_improvement"],
            }
            for entry in sdata["improvements"]
        ]

        return extracted_info

    def resolve_conflicts(self, gpt_response, trait_definitions, component):
        """
        Resolve conflicts in the GPT-generated response by assigning sentences to a single trait.
        Parameters:
            gpt_response: The GPT-generated response that contains potential conflicts.
            component: The specific component of the framework being analyzed.
            trait_definitions: Dictionary containing trait definitions for all components.
        Returns: A refined response with conflicts resolved.
        """

        prompt = f"""Below is a response from ChatGPT. Some of the sentences have been
    classified into multiple traits. Break the tie by reassigning
    these sentences into one traits. Keep the remaining result intact.
    
    Here is relevant information about the traits.
    {trait_definitions[component]}

    GPT Response:
    {gpt_response}"""

        gpt_input = [
            {"role": "system", "content": "You are expert at decision making."},
            {"role": "user", "content": prompt},
        ]

        completion_structured = self.openai_client.chat.completions.create(
            model="gpt-4o",
            messages=gpt_input,
            max_tokens=5000,
            response_format={
                "type": "json_schema",
                "json_schema": {
                    "name": "cre_improvement_feedback",
                    "schema": {
                        "type": "object",
                        "properties": {
                            "improvements": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "trait": {"type": "string"},
                                        "comment": {"type": "string"},
                                        "sentences_needing_improvement": {
                                            "type": "array",
                                            "items": {"type": "string"},
                                        },
                                        "suggested_improvement": {
                                            "type": "array",
                                            "items": {"type": "string"},
                                        },
                                    },
                                    "required": [
                                        "trait",
                                        "comment",
                                        "sentences_needing_improvement",
                                        "suggested_improvement",
                                    ],
                                    "additionalProperties": False,
                                },
                            }
                        },
                        "required": ["improvements"],
                        "additionalProperties": False,
                    },
                    "strict": True,
                },
            },
        )

        # Parse the structured response
        response_structured = completion_structured.choices[0].message.content
        sdata = json.loads(response_structured)

        # Extract the refined information
        extracted_info = [
            {
                "trait": entry["trait"],
                "comment": entry["comment"],
                "sentences_needing_improvement": entry["sentences_needing_improvement"],
                "suggested_improvement": entry["suggested_improvement"],
            }
            for entry in sdata["improvements"]
        ]

        return extracted_info
