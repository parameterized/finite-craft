from transformers import pipeline


pipe = pipeline(model="distilgpt2")

# prompt_template = """
# System: Suggest two items to combine, and I will tell you what they make.

# User: "Fire" and "Water"

# System: "Steam"

# User: "Earth" and "Wind"

# System: "Dust"

# User: "{}" and "{}"

# System: "
# """.strip()

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
        resp = pipe(
            prompt,
            return_full_text=False,
            max_new_tokens=80,
        )
        resp = resp[0]["generated_text"]
        print(resp)
        result = resp.split("\n")[0].replace('"', "").strip()

    return result
