"""
Elderly-Friendly Warning and Action Recommendation Generator
Member 4: Risk Aggregation, Warning Logic and System Integration

Generates plain-language, non-intimidating, practical safety guidance for elderly citizens.
Supports English, Hindi, and Kannada.
"""
from typing import List, Dict
from backend.schemas import OverallRiskLevel


class WarningGenerator:
    """
    Transforms aggregated risk evaluations into empathetic, senior-friendly
    warnings and actionable checklist steps.
    """

    # Base Warnings by Risk Level
    BASE_WARNINGS: Dict[str, Dict[str, str]] = {
        "English": {
            OverallRiskLevel.LOW.value: "No major suspicious activity was detected. Stay cautious.",
            OverallRiskLevel.MEDIUM.value: "This message contains some suspicious elements. Verify the sender before responding.",
            OverallRiskLevel.HIGH.value: "Warning! This message may be fraudulent. Do not share OTPs, passwords or banking details."
        },
        "Hindi": {
            OverallRiskLevel.LOW.value: "कोई बड़ा संदिग्ध खतरा नहीं मिला। फिर भी सतर्क रहें।",
            OverallRiskLevel.MEDIUM.value: "इस संदेश में कुछ संदिग्ध संकेत हैं। जवाब देने से पहले भेजने वाले की जाँच करें।",
            OverallRiskLevel.HIGH.value: "चेतावनी! यह संदेश फर्जी हो सकता है। अपना OTP, पासवर्ड या बैंक विवरण कभी साझा न करें।"
        },
        "Kannada": {
            OverallRiskLevel.LOW.value: "ಯಾವುದೇ ಪ್ರಮುಖ ಅನುಮಾನಾಸ್ಪದ ಚಟುವಟಿಕೆ ಕಂಡುಬಂದಿಲ್ಲ. ಎಚ್ಚರಿಕೆಯಿಂದಿರಿ.",
            OverallRiskLevel.MEDIUM.value: "ಈ ಸಂದೇಶದಲ್ಲಿ ಕೆಲವು ಅನುಮಾನಾಸ್ಪದ ಅಂಶಗಳಿವೆ. ಪ್ರತಿಕ್ರಿಯಿಸುವ ಮೊದಲು ಕಳುಹಿಸಿದವರನ್ನು ಪರಿಶೀಲಿಸಿ.",
            OverallRiskLevel.HIGH.value: "ಎಚ್ಚರಿಕೆ! ಈ ಸಂದೇಶವು ವಂಚನೆಯಾಗಿರಬಹುದು. ಯಾವುದೇ OTP, ಪಾಸ್‌ವರ್ಡ್ ಅಥವಾ ಬ್ಯಾಂಕ್ ವಿವರಗಳನ್ನು ಹಂಚಿಕೊಳ್ಳಬೇಡಿ."
        }
    }

    # Actionable safety advice bank
    ACTIONS_MAP = {
        "OTP": {
            "English": "Do not share OTPs, PINs, or security codes with anyone.",
            "Hindi": "किसी के साथ भी अपना OTP, PIN या गुप्त कोड साझा न करें।",
            "Kannada": "ಯಾರಿಗೂ ನಿಮ್ಮ OTP, PIN ಅಥವಾ ಭದ್ರತಾ ಕೋಡ್ ಹಂಚಿಕೊಳ್ಳಬೇಡಿ."
        },
        "MONEY": {
            "English": "Do not transfer money or enter your UPI PIN for unexpected requests.",
            "Hindi": "अपरिचित संदेशों पर पैसे न भेजें और UPI PIN न डालें।",
            "Kannada": "ಅಪರಿಚಿತ ಸಂದೇಶಗಳಿಗೆ ಹಣ ವರ್ಗಾಯಿಸಬೇಡಿ ಅಥವಾ UPI PIN ನಮೂದಿಸಬೇಡಿ."
        },
        "LINK": {
            "English": "Do not click any links or website addresses in this message.",
            "Hindi": "इस संदेश में दिए गए किसी भी लिंक या वेबसाइट पते पर क्लिक न करें।",
            "Kannada": "ಈ ಸಂದೇಶದಲ್ಲಿರುವ ಯಾವುದೇ ಲಿಂಕ್ ಅಥವಾ ವೆಬ್‌ಸೈಟ್ ವಿಳಾಸವನ್ನು ಕ್ಲಿಕ್ ಮಾಡಬೇಡಿ."
        },
        "VERIFY_SENDER": {
            "English": "Verify the sender by contacting the organization using official numbers from your passbook or bills.",
            "Hindi": "बैंक या संस्था के आधिकारिक नंबर (पासबुक या बिल पर दिए गए) पर कॉल करके पुष्टि करें।",
            "Kannada": "ಪಾಸ್‌ಬುಕ್ ಅಥವಾ ಬಿಲ್‌ಗಳಲ್ಲಿರುವ ಅಧಿಕೃತ ಸಂಖ್ಯೆಗೆ ಕರೆ ಮಾಡಿ ಕಳುಹಿಸಿದವರನ್ನು ಪರಿಶೀಲಿಸಿ."
        },
        "FAMILY_HELPER": {
            "English": "Take your time and discuss this message with your trusted family helper or caregiver.",
            "Hindi": "जल्दबाजी न करें, इस संदेश के बारे में अपने परिवार के किसी भरोसेमंद सदस्य से बात करें।",
            "Kannada": "ನಿಧಾನವಾಗಿ ಯೋಚಿಸಿ ಮತ್ತು ನಿಮ್ಮ ನಂಬಿಕಸ್ಥ ಕುಟುಂಬದ ಸದಸ್ಯರೊಂದಿಗೆ ಮಾತನಾಡಿ."
        },
        "DIGITAL_ARREST": {
            "English": "Police, CBI, or judges never conduct trials or demand bail money over WhatsApp or video calls.",
            "Hindi": "पुलिस या CBI कभी भी WhatsApp या वीडियो कॉल पर गिरफ्तारी की धमकी या पैसे की मांग नहीं करती।",
            "Kannada": "ಪೊಲೀಸರು ಅಥವಾ ನ್ಯಾಯಾಲಯಗಳು ಎಂದಿಗೂ ವಾಟ್ಸಾಪ್ ಅಥವಾ ವೀಡಿಯೊ ಕರೆ ಮೂಲಕ ಹಣ ಕೇಳುವುದಿಲ್ಲ."
        },
        "GENERAL_SAFE": {
            "English": "Always verify unexpected callers before taking financial actions.",
            "Hindi": "वित्तीय लेन-देन करने से पहले हमेशा कॉल करने वाले की सत्यता की पुष्टि करें।",
            "Kannada": "ಹಣಕಾಸಿನ ವ್ಯವಹಾರ ಮಾಡುವ ಮೊದಲು ಯಾವಾಗಲೂ ಪರಿಶೀಲಿಸಿ."
        }
    }

    @classmethod
    def generate_warning(
        cls,
        overall_risk: OverallRiskLevel,
        risk_indicators: List[str],
        language: str = "English"
    ) -> str:
        """
        Produces the primary high-visibility warning message.
        """
        lang = language if language in cls.BASE_WARNINGS else "English"
        base_msg = cls.BASE_WARNINGS[lang].get(
            overall_risk.value,
            cls.BASE_WARNINGS["English"][overall_risk.value]
        )
        return base_msg

    @classmethod
    def generate_recommended_actions(
        cls,
        overall_risk: OverallRiskLevel,
        risk_indicators: List[str],
        has_url: bool = False,
        message_text: str = "",
        language: str = "English"
    ) -> List[str]:
        """
        Constructs tailored, bulleted practical safety suggestions.
        """
        lang = language if language in cls.ACTIONS_MAP["OTP"] else "English"
        actions: List[str] = []

        # Analyze context from indicators and raw message
        combined_text = (" ".join(risk_indicators) + " " + message_text).lower()

        # Contextual actions
        if has_url or "url" in combined_text or "link" in combined_text:
            actions.append(cls.ACTIONS_MAP["LINK"][lang])

        if any(term in combined_text for term in ["otp", "password", "credential", "pin", "cvv", "code"]):
            actions.append(cls.ACTIONS_MAP["OTP"][lang])

        if any(term in combined_text for term in ["money", "payment", "transfer", "financial", "prize", "rupee", "cash", "gpay", "upi"]):
            actions.append(cls.ACTIONS_MAP["MONEY"][lang])

        if any(term in combined_text for term in ["arrest", "police", "cbi", "law", "court", "warrant"]):
            actions.append(cls.ACTIONS_MAP["DIGITAL_ARREST"][lang])

        # Standard core actions based on risk level
        if overall_risk in [OverallRiskLevel.HIGH, OverallRiskLevel.MEDIUM]:
            if cls.ACTIONS_MAP["VERIFY_SENDER"][lang] not in actions:
                actions.append(cls.ACTIONS_MAP["VERIFY_SENDER"][lang])
            if cls.ACTIONS_MAP["FAMILY_HELPER"][lang] not in actions:
                actions.append(cls.ACTIONS_MAP["FAMILY_HELPER"][lang])
        else:
            # Low risk suggestions
            actions.append(cls.ACTIONS_MAP["GENERAL_SAFE"][lang])
            actions.append(cls.ACTIONS_MAP["FAMILY_HELPER"][lang])

        # Ensure we always provide at least 2 clear, practical actions
        if len(actions) < 2:
            actions.append(cls.ACTIONS_MAP["VERIFY_SENDER"][lang])

        return actions
