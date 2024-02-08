import os

from openai import OpenAI


client = OpenAI(api_key=os.environ["FINITE_OPENAI_KEY"])


prompt_template = """
Fire + Water = Steam
Earth + Wind = Dust
{} + {} =
""".strip()


recipes = {
    ("Fire", "Water"): "Steam",
    ("Earth", "Wind"): "Dust",
    ("Dust", "Steam"): "Cloud",
}


def combine(text1, text2):
    combo = tuple(sorted((text1, text2)))
    result = recipes.get(combo)
    if result is None:
        prompt = prompt_template.format(text1, text2)
        resp = client.completions.create(
            model="gpt-3.5-turbo-instruct",
            prompt=prompt,
            max_tokens=10,
        )
        resp = resp.choices[0].text
        print(resp)
        result = resp.split("\n")[0].replace('"', "").strip()

    return result
