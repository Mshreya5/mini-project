from typing import List, Optional

from ai_module.src.config import STANDARD_DISCLAIMER


def generate_explanation(
    prediction: str,
    confidence: float,
    suspicious_indicators: List[str],
) -> str:
    has_indicators = len(suspicious_indicators) > 0

    if prediction == "scam":
        if has_indicators:
            if len(suspicious_indicators) == 1:
                indicator_phrase = suspicious_indicators[0].lower()
            elif len(suspicious_indicators) == 2:
                indicator_phrase = f"{suspicious_indicators[0].lower()} and {suspicious_indicators[1].lower()}"
            else:
                indicator_phrase = f"{', '.join(ind.lower() for ind in suspicious_indicators[:-1])}, and {suspicious_indicators[-1].lower()}"

            return (
                f"The message contains suspicious language patterns associated with {indicator_phrase}. "
                f"These tactics are commonly used in fraudulent messages to rush decisions or acquire sensitive credentials."
            )
        else:
            return (
                "The message shares language structures commonly observed in unsolicited or fraudulent messages, "
                "even though specific common buzzwords were not explicitly found."
            )

    else:
        if has_indicators:
            indicator_phrase = " and ".join(suspicious_indicators[:2]).lower()
            return (
                f"The message appears largely legitimate, but contains phrases mentioning {indicator_phrase}. "
                f"Exercise standard caution and verify the sender before taking action."
            )
        else:
            return (
                "The message appears to be normal everyday communication with no obvious scam indicators detected."
            )
