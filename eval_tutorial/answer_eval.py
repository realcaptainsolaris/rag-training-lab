"""
Answer-Evaluation: Correctness und Faithfulness
================================================

Wir bewerten eine simulierte RAG-Antwort mit zwei LLM-Judges.

Correctness:
    Ist die Antwort durch die Gold-Antwort zur Goldfrage belegt?

Faithfulness:
    Ist die Antwort durch den Retrieval-Kontext belegt?

Start:
    uv run python -m eval_tutorial.answer_eval
"""

import json
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

# ============================================================
# 1. Vorbereitung
# ============================================================

PROJECT_DIR = Path(__file__).resolve().parent.parent
GOLDSET_FILE = Path(__file__).resolve().parent / "goldset.json"

load_dotenv(PROJECT_DIR / ".env")

client = OpenAI()

MODEL = "gpt-4.1-mini"
QUESTION_ID = "Q001"


# ============================================================
# 2. Goldfrage laden
# ============================================================

goldset = json.loads(GOLDSET_FILE.read_text(encoding="utf-8"))

gold_case = next(case for case in goldset if case["id"] == QUESTION_ID)

QUESTION = gold_case["question"]
GROUND_TRUTH = gold_case["expected_answer"]


# ============================================================
# 3. Simulierter Retrieval-Kontext
# ============================================================

# D004_2 stammt aus dem historischen Orbit-2.4-Vertrag.
#
# Dieser Kontext enthält keine gültige Aussage über die
# konkrete Token-Gültigkeit von Orbit 3.0.

RETRIEVAL_CONTEXT = """
[D004_2] Webhook Delivery in Orbit 2.4

## Legacy service accounts

The access-token lifetime in Orbit 2.4 is 120 minutes.
A new client that assumes the same lifetime in Orbit 3.0
may continue using an expired token.
""".strip()


# ============================================================
# 4. Simulierte generierte Antwort
# ============================================================

# Aussage 1 ist sachlich korrekt.
# Aussage 2 ist eine unbelegte Zusatzbehauptung.

GENERATED_ANSWER = (
    "An Orbit 3.0 access token is valid for 60 minutes. "
    "The platform automatically renews every token after 30 minutes."
)


# ============================================================
# 5. Gemeinsame Bewertungsregeln
# ============================================================

JUDGE_RULES = """
You are evaluating a generated answer.

Split the answer into individual factual claims.

For each claim, assign exactly one label:

SUPPORTED:
    The reference explicitly supports the claim,
    or the claim is a direct semantic equivalent
    of information in the reference.

CONTRADICTED:
    The reference explicitly contradicts the claim.

UNKNOWN:
    The reference neither supports nor contradicts the claim.

Important rules:

- Evaluate every factual claim separately.
- Do not use outside knowledge.
- Do not infer missing facts.
- A claim is not supported merely because it sounds plausible.
- An answer may contain both supported and unsupported claims.
- Explain each judgment briefly in German.

Return your evaluation in this format:

Behauptung 1: "..."
- Status: SUPPORTED | CONTRADICTED | UNKNOWN
- Begründung: ...

Behauptung 2: "..."
- Status: SUPPORTED | CONTRADICTED | UNKNOWN
- Begründung: ...

Gesamturteil: ...
""".strip()


# ============================================================
# 6. LLM-Judge aufrufen
# ============================================================


def run_judge(instructions: str, evaluation_input: str) -> str:
    response = client.responses.create(
        model=MODEL,
        instructions=instructions,
        input=evaluation_input,
        temperature=0,
    )

    return response.output_text


# ============================================================
# 7. Correctness bewerten
# ============================================================


def evaluate_correctness() -> str:
    """
    Bewertet die generierte Antwort anhand der Goldfrage
    und der zugehörigen Gold-Antwort.

    Wichtig:
    Eine knappe Gold-Antwort wie "60 minutes" erhält
    ihre Bedeutung erst durch die zugehörige Frage.
    """

    instructions = f"""
{JUDGE_RULES}

You are evaluating CORRECTNESS.

The reference consists of TWO parts:

1. The gold question.
2. The expected answer to that question.

Interpret the expected answer in the context of the gold question.

Example:

Gold question:
    How long is an Orbit 3.0 access token valid?

Expected answer:
    60 minutes

Generated claim:
    An Orbit 3.0 access token is valid for 60 minutes.

Correct label:
    SUPPORTED

The generated claim expresses the same fact as the
question-answer pair.

Do not require the expected answer to repeat the
subject already specified in the question.

Overall correctness verdict:

- If ANY claim is CONTRADICTED:
  INCORRECT

- Otherwise, if ANY claim is UNKNOWN:
  NOT_EVALUABLE

- Otherwise:
  CORRECT

Use exactly one of these three overall verdicts.
""".strip()

    # TODO 1:
    # Stelle die Eingabe für den Correctness-Judge zusammen.
    # Benötigt werden:
    #   GOLD QUESTION: QUESTION
    #   EXPECTED ANSWER: GROUND_TRUTH
    #   GENERATED ANSWER: GENERATED_ANSWER
    #
    # Wichtig: Goldfrage UND Gold-Antwort übergeben.

    evaluation_input = f"""
GOLD QUESTION:
{QUESTION}

EXPECTED ANSWER:
{GROUND_TRUTH}

GENERATED ANSWER:
{GENERATED_ANSWER}
""".strip()

    return run_judge(instructions, evaluation_input)


# ============================================================
# 8. Faithfulness bewerten
# ============================================================


def evaluate_faithfulness() -> str:
    """
    Bewertet, ob die generierte Antwort durch den
    tatsächlich abgerufenen Kontext gestützt wird.

    Die Gold-Antwort wird hier bewusst NICHT übergeben.
    """

    instructions = f"""
{JUDGE_RULES}

You are evaluating FAITHFULNESS.

Use ONLY the retrieved context as reference.

Do not use the gold answer or outside knowledge.

Overall faithfulness verdict:

- If ANY claim is CONTRADICTED or UNKNOWN:
  NOT_FAITHFUL

- Otherwise:
  FAITHFUL

Use exactly one of these two overall verdicts.
""".strip()

    # TODO 2:
    # Stelle die Eingabe für den Faithfulness-Judge zusammen.
    # Benötigt werden:
    #   QUESTION: QUESTION
    #   RETRIEVED CONTEXT: RETRIEVAL_CONTEXT
    #   GENERATED ANSWER: GENERATED_ANSWER
    #
    # Wichtig: Hier NICHT die Gold-Antwort übergeben.

    evaluation_input = f"""
QUESTION:
{QUESTION}

RETRIEVED CONTEXT:
{RETRIEVAL_CONTEXT}

GENERATED ANSWER:
{GENERATED_ANSWER}
""".strip()

    return run_judge(instructions, evaluation_input)


# ============================================================
# 9. Hauptprogramm
# ============================================================


def main():
    print("ANSWER-EVALUATION: TERALUNE")
    print("Simulierter Kontext und simulierte Antwort; LLM-as-a-Judge")

    print("Goldfrage:", QUESTION_ID)
    print("Frage:", QUESTION)
    print("Gold-Antwort:", GROUND_TRUTH)

    print("\nRETRIEVAL-KONTEXT:")
    print(RETRIEVAL_CONTEXT)

    print("\nGENERIERTE ANTWORT (SIMULIERT):")
    print(GENERATED_ANSWER)

    print("\n" + "=" * 60)
    print("1. CORRECTNESS: Vergleich mit Gold-Antwort")
    print("=" * 60)

    correctness = evaluate_correctness()
    print(correctness)

    print("\n" + "=" * 60)
    print("2. FAITHFULNESS: Vergleich mit Retrieval-Kontext")
    print("=" * 60)

    faithfulness = evaluate_faithfulness()
    print(faithfulness)

    print("\nHINWEIS: LLM-Judge-Urteile sind modell- und promptabhängig.")
    print(
        "Correctness bedeutet hier Übereinstimmung mit der "
        "Goldfrage und Gold-Antwort, nicht unabhängig bewiesene Wahrheit."
    )


if __name__ == "__main__":
    main()
