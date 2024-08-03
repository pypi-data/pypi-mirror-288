from typing import Set
#
from nutcracker.data.instance import FRQInstance
#
#
from openai import OpenAI
import openai
#
#
#
class FRQJudge:
    def __init__(self, model):
        self.model = model



    def is_correct(self, instance: FRQInstance) -> bool:
        found_options = self._parse_model_response_intent_matching(instance.model_response, instance.correct_options)

        instance.response_parsed = found_options
        if 'true' in found_options.lower() and 'false' not in found_options.lower():
            return True
        elif 'true' not in found_options.lower() and 'false' in found_options.lower():
            return False
        else:
            return False



    def _parse_model_response_intent_matching(self, response: str, correct_options: list) -> str:
        client = OpenAI()
        few_shot = f"""
        Your job is: given a response, determine if the answer is correct or not. Say True or False and nothing else.

        Examples:
        
        Answer: '\\frac{625}{648}'
        Response: 'It's 625/648.'
        Interpretation: True

        Answer: '\\frac{2}{5}'
        Response: 'It's 4/6'
        Interpretation: False

        Answer: '$42'
        Response: '42'
        Interpretation: True

        Answer: '42.00'
        Response: '42'
        Interpretation: True

        Answer: '72'
        Response: '72 people'
        Interpretation: True

        Answer: '336 grapes at the beginning
        (Note: 6 grapes eaten + 6 x 5 = 30 grapes used for grape juice + 4 x 12 = 48 grapes used for pies, total 84 grapes, so 336 grapes at the beginning)'
        Response: '84'
        Interpretation: False
        
        Answer: '{", ".join(correct_options)}'
        Response: '{response}'
        Interpretation: 
        """

        interpreted_response = None
        while interpreted_response is None:
            try:
                completion = self.model.respond(
                    'You respond with True or False and nothing else.\n\n' + few_shot
                )
                interpreted_response = completion.strip().upper()
                break
            except KeyboardInterrupt:
                sys.exit()

        return set(interpreted_response.split(', ')) if interpreted_response else set()