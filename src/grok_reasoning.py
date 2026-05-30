import os
from typing import Any

import requests


XAI_CHAT_COMPLETIONS_URL = "https://api.x.ai/v1/chat/completions"
GROQ_CHAT_COMPLETIONS_URL = "https://api.groq.com/openai/v1/chat/completions"


def fallback_reasoning(inputs: dict[str, Any], prediction: float) -> str:
    factors = []

    if inputs.get("smoker") == "yes":
        factors.append("smoking status usually increases expected medical insurance charges")
    else:
        factors.append("non-smoker status helps keep the predicted cost lower")

    if inputs.get("chronic_disease") == "yes":
        factors.append("chronic disease status increases the estimated risk level")

    age = inputs.get("age", 0)
    if age >= 50:
        factors.append("higher age is associated with higher healthcare cost risk")
    elif age <= 30:
        factors.append("younger age generally reduces the predicted cost")

    bmi = inputs.get("bmi", 0)
    if bmi >= 30:
        factors.append("BMI is above the common obesity threshold, which can raise estimated cost")
    elif bmi < 25:
        factors.append("BMI is in a lower-risk range compared with higher BMI values")

    exercise_frequency = inputs.get("exercise_frequency", 0)
    if exercise_frequency >= 4:
        factors.append("regular exercise helps reduce the risk profile")

    if not factors:
        factors.append("the estimate is mainly driven by the combined profile of age, BMI, lifestyle, and health features")

    return (
        f"The estimated insurance charge is {prediction:,.2f}. "
        f"The main reasons are: {', '.join(factors)}. "
        "This explanation is generated from the model inputs and should be treated as an estimate, not medical advice."
    )


def build_prompt(personal: dict[str, Any], inputs: dict[str, Any], prediction: float, metrics: dict[str, Any]) -> str:
    display_name = personal.get("full_name") or "the user"
    return f"""
Explain why a medical insurance cost prediction model estimated charges of {prediction:,.2f} for {display_name}.

Model inputs:
- age: {inputs.get("age")}
- sex: {inputs.get("sex")}
- BMI: {inputs.get("bmi")}
- children: {inputs.get("children")}
- smoker: {inputs.get("smoker")}
- region: {inputs.get("region")}
- income: {inputs.get("income")}
- exercise frequency: {inputs.get("exercise_frequency")}
- chronic disease: {inputs.get("chronic_disease")}
- alcohol consumption: {inputs.get("alcohol_consumption")}

Model metrics:
- R2: {metrics.get("r2", "unknown")}
- RMSE: {metrics.get("rmse", "unknown")}
- MAE: {metrics.get("mae", "unknown")}

Write 4-6 short sentences for a student project UI.
Mention the strongest likely cost drivers in plain language.
Do not claim a medical diagnosis.
Do not say the value is exact.
End with a short caution that this is an ML estimate.
""".strip()


def generate_reasoning(personal: dict[str, Any], inputs: dict[str, Any], prediction: float, metrics: dict[str, Any]) -> tuple[str, str]:
    xai_api_key = os.getenv("XAI_API_KEY")
    groq_api_key = os.getenv("GROQ_API_KEY")

    if xai_api_key:
        provider = "xai"
        api_key = xai_api_key
        url = XAI_CHAT_COMPLETIONS_URL
        model = os.getenv("XAI_MODEL") or os.getenv("GROK_MODEL", "grok-4.3")
    elif groq_api_key:
        provider = "groq"
        api_key = groq_api_key
        url = GROQ_CHAT_COMPLETIONS_URL
        model = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")
    else:
        provider = "local"
        api_key = None
        url = ""
        model = ""

    if not api_key:
        return fallback_reasoning(inputs, prediction), "local_fallback"

    payload = {
        "model": model,
        "messages": [
            {
                "role": "system",
                "content": "You explain ML insurance predictions clearly and cautiously for a final-year student project.",
            },
            {
                "role": "user",
                "content": build_prompt(personal, inputs, prediction, metrics),
            },
        ],
        "temperature": 0.2,
        "max_tokens": 240,
    }

    try:
        response = requests.post(
            url,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            json=payload,
            timeout=20,
        )
        response.raise_for_status()
        data = response.json()
        content = data["choices"][0]["message"]["content"].strip()
        return content, f"{provider}:{model}"
    except Exception as exc:
        return (
            fallback_reasoning(inputs, prediction)
            + f" Grok reasoning was unavailable, so local fallback reasoning was used. API error: {exc}",
            "local_fallback_after_grok_error",
        )
