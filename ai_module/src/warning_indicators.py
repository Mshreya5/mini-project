import re
from typing import Dict, List, Optional


class WarningIndicatorDetector:

    def __init__(self):
        self.urgent_payment_patterns = [
            re.compile(r"\b(?:transfer|wire|send)\s+(?:money|funds|cash|payment)\s+(?:to|via|immediately|urgently|now)\b", re.IGNORECASE),
            re.compile(r"\b(?:processing|release|customs|delivery|admin|unpaid)\s+(?:fee|charge|deposit|penalty)\b", re.IGNORECASE),
            re.compile(r"\b(?:pay|settle)\s+(?:now|immediately|within\s+\d+\s*(?:hours|mins|minutes)|urgently)\b", re.IGNORECASE),
            re.compile(r"\b(?:pay\s+with|buy)\s+(?:gift\s*cards?|google\s*play\s*card|itunes\s*card|crypto|bitcoin|giftcard)\b", re.IGNORECASE),
            re.compile(r"\bmake\s+(?:a\s+)?payment\s+(?:now|urgently|immediately)\b", re.IGNORECASE),
            re.compile(r"\bdemand\s+immediate\s+payment\b", re.IGNORECASE),
        ]

        self.otp_patterns = [
            re.compile(r"\b(?:send|share|enter|provide|reply\s+with|give|forward)\b.*?\b(?:otp|one[- ]time\s+password|pin|security\s+code|verification\s+code|passcode)\b", re.IGNORECASE),
            re.compile(r"\b(?:share|tell)\s+(?:us|me)\s+your\s+(?:code|otp|pin|password)\b", re.IGNORECASE),
            re.compile(r"\b(?:your\s+)?(?:otp|pin|password)\s+is\s+required\s+to\b", re.IGNORECASE),
            re.compile(r"\bdo\s+not\s+share\s+this\s+otp\b", re.IGNORECASE),
        ]

        self.fake_prize_patterns = [
            re.compile(r"\b(?:congratulations|congrats|selected|chosen|awarded)\b.*?\b(?:winner|won|cash|prize|reward|lottery|jackpot|gift\s*card)\b", re.IGNORECASE),
            re.compile(r"\b(?:claim|collect|redeem|receive)\s+(?:your\s+)?(?:free\s+)?(?:prize|reward|cash|bonus|gift|voucher|grant|jackpot)\b", re.IGNORECASE),
            re.compile(r"\b(?:won|win)\s+(?:a\s+)?(?:cash|lottery|jackpot|fortune|\$|£|€|\d+[\d,]*\s*(?:pounds|dollars|rupees))\b", re.IGNORECASE),
            re.compile(r"\b(?:lottery|sweepstake|lucky\s+draw)\s+(?:winner|award|ticket)\b", re.IGNORECASE),
            re.compile(r"\bguaranteed\s+(?:winner|cash|payout)\b", re.IGNORECASE),
        ]

        self.bank_impersonation_patterns = [
            re.compile(r"\b(?:bank|barclays|hsbc|lloyds|natwest|santander|chase|wells\s+fargo|citi|hdfc|sbi|icici|axis)\b.*?\b(?:account|security|fraud\s+team|alert|unauthorized|activity)\b", re.IGNORECASE),
            re.compile(r"\b(?:fraud\s+department|security\s+division|official\s+bank\s+notice)\b", re.IGNORECASE),
            re.compile(r"\b(?:bank|credit|debit)\s+card\s+(?:details|number|blocked|cancelled)\b", re.IGNORECASE),
        ]

        self.account_verification_patterns = [
            re.compile(r"\b(?:login|sign[- ]in|verify|validate|update|confirm)\s+(?:your\s+)?(?:account|identity|details|credentials|kyc|profile|records)\b", re.IGNORECASE),
            re.compile(r"\bclick\s+here\s+to\s+verify\s+your\s+account\b", re.IGNORECASE),
            re.compile(r"\bverify\s+your\s+(?:bank\s+)?information\s+to\s+avoid\b", re.IGNORECASE),
            re.compile(r"\bsecurity\s+update\s+required\b", re.IGNORECASE),
        ]

        self.account_suspension_patterns = [
            re.compile(r"\b(?:account|card|service|access|profile)\s+(?:has\s+been|will\s+be|is\s+temporarily)\s+(?:suspended|blocked|locked|terminated|cancelled|frozen|restricted)\b", re.IGNORECASE),
            re.compile(r"\b(?:final|last)\s+(?:notice|warning|reminder|alert)\b", re.IGNORECASE),
            re.compile(r"\b(?:threatened\s+with\s+legal|legal\s+action|warrant\s+issued|arrest)\b", re.IGNORECASE),
            re.compile(r"\bto\s+avoid\s+(?:suspension|account\s+closure|penalty|deactivation)\b", re.IGNORECASE),
            re.compile(r"\bimmediate\s+action\s+required\s+or\s+your\s+account\b", re.IGNORECASE),
        ]

        self.suspicious_link_patterns = [
            re.compile(r"https?://[^\s]+", re.IGNORECASE),
            re.compile(r"\b(?:bit\.ly|tinyurl\.com|t\.co|goo\.gl|is\.gd|ow\.ly|buff\.ly|cli\.re)/[^\s]+", re.IGNORECASE),
            re.compile(r"\bwww\.[a-z0-9\-]+\.[a-z]{2,}(?:/[^\s]*)?", re.IGNORECASE),
            re.compile(r"\b[a-z0-9\-]+(?:\.(?:xyz|top|work|click|link|club|online|site|live|vip))/[^\s]*", re.IGNORECASE),
        ]

        self.categories = [
            {
                "id": "urgent_payment",
                "label": "Urgent payment request",
                "patterns": self.urgent_payment_patterns,
                "description": "Pressures you to transfer funds, pay unexpected fees, or send gift cards.",
            },
            {
                "id": "otp_request",
                "label": "OTP request",
                "patterns": self.otp_patterns,
                "description": "Asks you to reveal, enter, or send confidential details like an OTP or PIN.",
            },
            {
                "id": "fake_prize",
                "label": "Fake lottery or prize",
                "patterns": self.fake_prize_patterns,
                "description": "Claims you have won an unexpected lottery or prize that you never entered.",
            },
            {
                "id": "bank_impersonation",
                "label": "Bank impersonation",
                "patterns": self.bank_impersonation_patterns,
                "description": "Impersonates a bank or financial institution to sound authoritative.",
            },
            {
                "id": "account_verification",
                "label": "Suspicious account verification",
                "patterns": self.account_verification_patterns,
                "description": "Requests verification of identity, credentials, or personal records.",
            },
            {
                "id": "account_suspension",
                "label": "Threatening account suspension",
                "patterns": self.account_suspension_patterns,
                "description": "Uses threats of account closure, legal action, or service suspension.",
            },
            {
                "id": "suspicious_link",
                "label": "Suspicious link",
                "patterns": self.suspicious_link_patterns,
                "description": "Contains an external web link that may direct to a fraudulent website.",
            },
        ]

    def extract_indicators(self, message: Optional[str]) -> List[str]:
        if not message or not isinstance(message, str):
            return []

        clean = message.strip()
        detected: List[str] = []

        for cat in self.categories:
            for pattern in cat["patterns"]:
                if pattern.search(clean):
                    detected.append(cat["label"])
                    break

        return detected

    def extract_detailed_indicators(self, message: Optional[str]) -> List[Dict[str, str]]:
        if not message or not isinstance(message, str):
            return []

        clean = message.strip()
        detailed: List[Dict[str, str]] = []

        for cat in self.categories:
            for pattern in cat["patterns"]:
                if pattern.search(clean):
                    detailed.append({
                        "id": cat["id"],
                        "label": cat["label"],
                        "description": cat["description"],
                    })
                    break

        return detailed


_DETECTOR_INSTANCE = WarningIndicatorDetector()


def detect_suspicious_indicators(message: Optional[str]) -> List[str]:
    return _DETECTOR_INSTANCE.extract_indicators(message)


def detect_detailed_indicators(message: Optional[str]) -> List[Dict[str, str]]:
    return _DETECTOR_INSTANCE.extract_detailed_indicators(message)
