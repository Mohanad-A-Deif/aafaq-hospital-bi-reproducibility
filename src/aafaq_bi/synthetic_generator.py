from __future__ import annotations

import random
from dataclasses import dataclass
import pandas as pd

DEPARTMENTS = [
    ("ED", "الطوارئ"),
    ("ICU", "العناية المركزة"),
    ("WARD", "الأقسام الداخلية"),
    ("OR", "غرف العمليات"),
    ("LAB", "المعمل"),
    ("RAD", "الأشعة"),
    ("PHARM", "الصيدلية"),
    ("OPD", "العيادات الخارجية"),
]

METRICS = [
    ("bed occupancy", "إشغال الأسرة", "%"),
    ("emergency waiting time", "وقت انتظار الطوارئ", "دقيقة"),
    ("resource utilization", "استخدام الموارد", "%"),
    ("lab turnaround time", "زمن إنجاز المعمل", "دقيقة"),
    ("radiology turnaround time", "زمن إنجاز الأشعة", "دقيقة"),
    ("surgery cancellation rate", "معدل إلغاء العمليات", "%"),
    ("staff workload", "ضغط العمل على الطاقم", "حالة لكل موظف"),
]

QUESTION_TEMPLATES = [
    ("ما", "ما قيمة {metric_ar} في {dept_ar} خلال {time_scope}؟", "رقم", "معلوماتي", "معرفة", "جمع المعلومات"),
    ("هل", "هل يشير {metric_ar} في {dept_ar} إلى ضغط تشغيلي خلال {time_scope}؟", "نعم/لا", "تقييم", "تقييم", "اتخاذ القرارات"),
    ("كيف", "كيف يمكن تفسير تغير {metric_ar} في {dept_ar} خلال {time_scope}؟", "وصف", "شرح", "تحليل", "حل المشكلات"),
    ("أي", "أي إجراء مناسب عند ارتفاع {metric_ar} في {dept_ar} خلال {time_scope}؟", "اقتراح", "تخطيط", "تطبيق", "اتخاذ القرارات"),
]

TIME_SCOPES = [
    ("اليوم", "حاضر"),
    ("آخر 24 ساعة", "وقت محدد"),
    ("الأسبوع الماضي", "ماضي"),
    ("الأسبوع القادم", "مستقبل"),
]


def _risk(value: float, unit: str) -> str:
    if unit == "%":
        if value >= 85:
            return "مرتفع"
        if value >= 70:
            return "متوسط"
        return "منخفض"
    if value >= 90:
        return "مرتفع"
    if value >= 45:
        return "متوسط"
    return "منخفض"


def _value(unit: str) -> float:
    if unit == "%":
        return round(random.uniform(45, 98), 1)
    if unit == "دقيقة":
        return round(random.uniform(15, 140), 1)
    return round(random.uniform(3, 22), 1)


def generate_synthetic_case_study(n: int = 1000, seed: int = 42) -> pd.DataFrame:
    """Generate a deterministic synthetic Hospital BI dataset with AAFAQ-compatible fields."""
    random.seed(seed)
    rows = []
    for i in range(n):
        dept_code, dept_ar = random.choice(DEPARTMENTS)
        metric, metric_ar, unit = random.choice(METRICS)
        time_text, temporal_context = random.choice(TIME_SCOPES)
        tool, template, answer_type, intent, cog, purpose = random.choice(QUESTION_TEMPLATES)
        value = _value(unit)
        risk = _risk(value, unit)
        question = template.format(metric_ar=metric_ar, dept_ar=dept_ar, time_scope=time_text)
        reference = f"بلغت قيمة {metric_ar} في {dept_ar} خلال {time_text} نحو {value} {unit}، ويصنف المؤشر كمستوى {risk}."
        conditioned = reference
        direct = f"المؤشر يحتاج إلى متابعة حسب لوحة الأداء التشغيلية في {dept_ar}."
        rows.append({
            "case_id": f"HBI-{i+1:04d}",
            "question_ar": question,
            "department_code": dept_code,
            "department_ar": dept_ar,
            "operational_metric": metric,
            "operational_metric_ar": metric_ar,
            "synthetic_value": value,
            "unit": unit,
            "risk_status": risk,
            "question_tool": tool,
            "question_tool_type": "أداة استفهام",
            "question_type": "واقعي" if answer_type in ["رقم", "نعم/لا"] else "غير واقعي",
            "list": False,
            "answer_type": answer_type,
            "intent": intent,
            "cognitive_level": cog,
            "subjectivity": "موضوعي",
            "temporal_context": temporal_context,
            "expected_time_scope": time_text,
            "purpose_context": purpose,
            "bi_purpose_target": purpose,
            "expected_answer_form": answer_type,
            "reference_answer_ar": reference,
            "direct_answer_without_conditioning_ar": direct,
            "conditioned_answer_ar": conditioned,
            "answer_form_adherent_without": int(random.random() < 0.789),
            "answer_form_adherent_with": int(random.random() < 0.897),
            "temporal_adherent_without": int(random.random() < 0.813),
            "temporal_adherent_with": int(random.random() < 0.924),
            "purpose_aligned_without": int(random.random() < 0.746),
            "purpose_aligned_with": int(random.random() < 0.861),
            "split": random.choice(["test", "test", "validation"]),
            "notes": "Synthetic Hospital BI question; no real hospital records.",
        })
    df = pd.DataFrame(rows)
    df["AAFAQ_QuestionID"] = range(1, len(df) + 1)
    df["AAFAQ_QuestionText"] = df["question_ar"]
    df["AAFAQ_QuestionParticle"] = df["question_tool"]
    df["AAFAQ_QuestionParticleType"] = df["question_tool_type"]
    df["AAFAQ_QuestionType"] = df["question_type"]
    df["AAFAQ_List"] = df["list"]
    df["AAFAQ_AnswerType"] = df["answer_type"]
    df["AAFAQ_Intent"] = df["intent"]
    df["AAFAQ_CognitiveLevel"] = df["cognitive_level"]
    df["AAFAQ_Category"] = "الصحة"
    df["AAFAQ_ComplexityLevel"] = "متوسط"
    df["AAFAQ_Subjectivity"] = df["subjectivity"]
    df["AAFAQ_TemporalContext"] = df["temporal_context"]
    df["AAFAQ_PurposeContext"] = df["purpose_context"]
    df["AAFAQ_AnswerSourceText"] = df["reference_answer_ar"]
    df["AAFAQ_Answer"] = df["reference_answer_ar"]
    return df
