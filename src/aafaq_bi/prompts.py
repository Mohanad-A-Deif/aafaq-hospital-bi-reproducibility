from __future__ import annotations

import json
import pandas as pd


def taxonomy_control_block(row: pd.Series) -> str:
    return (
        "[TAXONOMY]\n"
        f"QuestionParticle: {row.get('AAFAQ_QuestionParticle', row.get('question_tool', ''))}\n"
        f"QuestionType: {row.get('AAFAQ_QuestionType', row.get('question_type', ''))}\n"
        f"AnswerType: {row.get('AAFAQ_AnswerType', row.get('answer_type', ''))}\n"
        f"Intent: {row.get('AAFAQ_Intent', row.get('intent', ''))}\n"
        f"CognitiveLevel: {row.get('AAFAQ_CognitiveLevel', row.get('cognitive_level', ''))}\n"
        f"TemporalContext: {row.get('AAFAQ_TemporalContext', row.get('temporal_context', ''))}\n"
        f"PurposeContext: {row.get('AAFAQ_PurposeContext', row.get('purpose_context', ''))}\n"
        "[/TAXONOMY]"
    )


def build_prompt(row: pd.Series, conditioned: bool = True) -> str:
    question = row.get("question_ar", row.get("AAFAQ_QuestionText", ""))
    if conditioned:
        return (
            "أجب عن السؤال العربي التالي مع الالتزام الصريح بالتصنيف المعطى.\n\n"
            f"{taxonomy_control_block(row)}\n\n"
            f"السؤال: {question}\n"
            "الإجابة:"
        )
    return f"أجب عن السؤال العربي التالي بإجابة مباشرة.\n\nالسؤال: {question}\nالإجابة:"


def build_prompt_records(df: pd.DataFrame) -> list[dict]:
    records = []
    for _, row in df.iterrows():
        records.append({
            "case_id": row.get("case_id"),
            "question": row.get("question_ar"),
            "reference_answer": row.get("reference_answer_ar"),
            "prompt_without_conditioning": build_prompt(row, conditioned=False),
            "prompt_with_conditioning": build_prompt(row, conditioned=True),
            "taxonomy": {
                "answer_type": row.get("AAFAQ_AnswerType", row.get("answer_type")),
                "intent": row.get("AAFAQ_Intent", row.get("intent")),
                "cognitive_level": row.get("AAFAQ_CognitiveLevel", row.get("cognitive_level")),
                "temporal_context": row.get("AAFAQ_TemporalContext", row.get("temporal_context")),
                "purpose_context": row.get("AAFAQ_PurposeContext", row.get("purpose_context")),
            },
        })
    return records


def write_jsonl(records: list[dict], path) -> None:
    with open(path, "w", encoding="utf-8") as f:
        for rec in records:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
