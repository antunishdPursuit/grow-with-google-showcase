"""Scoring and report generation for the Business Readiness Check."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping


YES = "Yes"
NO = "No"
NOT_APPLICABLE = "Not applicable"
VALID_ANSWERS = {YES, NO, NOT_APPLICABLE}


@dataclass(frozen=True)
class Question:
    """One diagnostic question and its project-defined risk weight."""

    label: str
    prompt: str
    weight: int
    recommendation: str
    explanation: str


@dataclass(frozen=True)
class AssessmentResult:
    """Calculated assessment values used by both the UI and report."""

    risk_points: int
    applicable_points: int
    risk_percentage: float | None
    risk_level: str


QUESTIONS: dict[str, Question] = {
    "inventory": Question(
        label="Inventory synchronization",
        prompt=(
            "Does your POS automatically synchronize inventory with your "
            "online store?"
        ),
        weight=5,
        recommendation="Prioritize POS and online inventory synchronization.",
        explanation=(
            "Disconnected inventory systems can cause incorrect stock counts, "
            "overselling, and manual reconciliation."
        ),
    ),
    "payments": Question(
        label="Payments and checkout",
        prompt="Does checkout support digital wallets and guest checkout?",
        weight=4,
        recommendation="Add digital-wallet support and guest checkout.",
        explanation=(
            "Limited checkout options can create avoidable friction for customers."
        ),
    ),
    "customers": Question(
        label="Customer email capture",
        prompt="Are customer emails captured at the point of sale?",
        weight=3,
        recommendation="Add customer email capture and follow-up automation.",
        explanation=(
            "Missing contact information limits customer follow-up and retention "
            "workflows."
        ),
    ),
    "booking": Question(
        label="Online booking",
        prompt="Can customers book appointments online at any time?",
        weight=2,
        recommendation="Add a secure 24/7 online booking system.",
        explanation=(
            "Manual scheduling can prevent customers from booking outside business "
            "hours."
        ),
    ),
}


def clean_user_text(value: str, max_length: int) -> str:
    """Normalize optional report text and remove control characters."""

    printable = "".join(
        character if character.isprintable() else " " for character in value
    )
    return " ".join(printable.split())[:max_length]


def _validate_answers(answers: Mapping[str, str]) -> None:
    """Reject missing, unknown, or invalid answers before calculating a score."""

    expected = set(QUESTIONS)
    provided = set(answers)

    missing = expected - provided
    unknown = provided - expected
    if missing:
        raise ValueError(f"Missing answers for: {', '.join(sorted(missing))}")
    if unknown:
        raise ValueError(f"Unknown question keys: {', '.join(sorted(unknown))}")

    invalid = {
        key: answer for key, answer in answers.items() if answer not in VALID_ANSWERS
    }
    if invalid:
        details = ", ".join(f"{key}={answer!r}" for key, answer in invalid.items())
        raise ValueError(f"Invalid answers: {details}")


def classify_risk(risk_percentage: float | None) -> str:
    """Return the project-designed risk category for a percentage."""

    if risk_percentage is None:
        return "Not calculated"
    if risk_percentage < 25:
        return "Low"
    if risk_percentage < 50:
        return "Moderate"
    if risk_percentage < 75:
        return "High"
    return "Critical"


def calculate_risk(answers: Mapping[str, str]) -> AssessmentResult:
    """Calculate weighted risk while excluding not-applicable questions."""

    _validate_answers(answers)
    risk_points = 0
    applicable_points = 0

    for key, question in QUESTIONS.items():
        answer = answers[key]
        if answer == NOT_APPLICABLE:
            continue
        applicable_points += question.weight
        if answer == NO:
            risk_points += question.weight

    risk_percentage = (
        round(risk_points / applicable_points * 100, 1)
        if applicable_points
        else None
    )
    return AssessmentResult(
        risk_points=risk_points,
        applicable_points=applicable_points,
        risk_percentage=risk_percentage,
        risk_level=classify_risk(risk_percentage),
    )


def find_priorities(answers: Mapping[str, str]) -> list[tuple[str, Question]]:
    """Return failed areas ordered by highest project-defined weight first."""

    _validate_answers(answers)
    failed = [(key, QUESTIONS[key]) for key, answer in answers.items() if answer == NO]
    return sorted(failed, key=lambda item: item[1].weight, reverse=True)


def generate_report(
    answers: Mapping[str, str],
    result: AssessmentResult,
    business_name: str = "",
    business_type: str = "",
) -> str:
    """Create a plain-text report without retaining or transmitting user input."""

    _validate_answers(answers)
    priorities = find_priorities(answers)
    name = clean_user_text(business_name, max_length=80) or "Not provided"
    kind = clean_user_text(business_type, max_length=60) or "Not provided"
    lines = [
        "BUSINESS READINESS CHECK",
        "========================",
        f"Business name: {name}",
        f"Business type: {kind}",
        "",
    ]

    if result.risk_percentage is None:
        lines.extend(
            [
                "Overall result: Not calculated",
                (
                    "A score could not be calculated because every diagnostic "
                    "area was marked Not applicable."
                ),
            ]
        )
    else:
        lines.extend(
            [
                f"Overall risk: {result.risk_percentage:.1f}% ({result.risk_level})",
                f"Risk points: {result.risk_points} of {result.applicable_points}",
            ]
        )

    lines.extend(["", "AREA RESULTS", "------------"])
    for key, question in QUESTIONS.items():
        lines.append(f"{question.label}: {answers[key]}")

    lines.extend(["", "RECOMMENDED NEXT STEPS", "----------------------"])
    if priorities:
        for index, (_, question) in enumerate(priorities, start=1):
            lines.append(f"{index}. {question.recommendation}")
            lines.append(f"   {question.explanation}")
    elif result.risk_percentage is None:
        lines.append("Complete at least one applicable area to receive recommendations.")
    else:
        lines.append("No priority gaps were identified from the answers provided.")

    lines.extend(
        [
            "",
            "IMPORTANT",
            "---------",
            (
                "This educational tool provides general guidance. It is not a "
                "formal security, financial, compliance, or technology audit."
            ),
        ]
    )
    return "\n".join(lines) + "\n"
