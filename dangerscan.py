# danger_scan.py
from typing import List, Dict

SUSPICIOUS_PATTERNS = [
    "rm -rf",
    "drop table",
    "shutdown",
    "format c:",
    "delete from",
    "insert into",
    "wget ",
    "curl ",
    "os.system",
    "subprocess",
    "exec ",
    "&&",
    "||",
    ";",
]


def _split_sentences(text: str) -> List[str]:
    # Çok kaba bir ayırma, bizim için yeterli
    parts = []
    for line in text.splitlines():
        for piece in line.replace("?", ".").replace("!", ".").split("."):
            s = piece.strip()
            if s:
                parts.append(s)
    return parts


def analyze_text(text: str) -> Dict:
    sentences = _split_sentences(text)
    flagged = []
    threat_delta = 0

    lower_text = text.lower()

    for sentence in sentences:
        ls = sentence.lower()
        for pattern in SUSPICIOUS_PATTERNS:
            if pattern in ls:
                flagged.append(sentence)
                threat_delta += 1
                break

    # threat_delta çok abartılı olmasın
    if threat_delta > 5:
        threat_delta = 5

    return {
        "flagged_sentences": flagged,
        "threat_delta": threat_delta,
    }
