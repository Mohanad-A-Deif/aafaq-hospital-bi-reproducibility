from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List


@dataclass
class MultiTaskConfig:
    model_name: str = "aubmindlab/bert-base-arabertv02"
    max_length: int = 128
    label_columns: tuple[str, ...] = (
        "QuestionParticle",
        "QuestionParticleType",
        "QuestionType",
        "List",
        "AnswerType",
        "Intent",
        "CognitiveLevel",
        "Subjectivity",
        "TemporalContext",
        "PurposeContext",
    )


class OptionalDependencyError(RuntimeError):
    pass


def require_ml_dependencies():
    try:
        import torch  # noqa: F401
        import transformers  # noqa: F401
    except ImportError as exc:
        raise OptionalDependencyError(
            "Machine-learning dependencies are not installed. Run: pip install -r requirements-ml.txt"
        ) from exc


def build_label_maps(df, label_columns: List[str]) -> Dict[str, Dict[str, int]]:
    label_maps = {}
    for col in label_columns:
        values = sorted(df[col].astype(str).fillna("<NA>").unique().tolist())
        label_maps[col] = {label: idx for idx, label in enumerate(values)}
    return label_maps


def create_multitask_model(model_name: str, num_labels_per_task: Dict[str, int]):
    """Create a HuggingFace encoder with one linear classification head per taxonomy dimension."""
    require_ml_dependencies()
    import torch
    from torch import nn
    from transformers import AutoModel

    class MultiTaskTransformer(nn.Module):
        def __init__(self):
            super().__init__()
            self.encoder = AutoModel.from_pretrained(model_name)
            hidden = self.encoder.config.hidden_size
            self.heads = nn.ModuleDict({
                task: nn.Linear(hidden, n_labels) for task, n_labels in num_labels_per_task.items()
            })

        def forward(self, input_ids, attention_mask=None, labels=None):
            outputs = self.encoder(input_ids=input_ids, attention_mask=attention_mask)
            pooled = outputs.last_hidden_state[:, 0, :]
            logits = {task: head(pooled) for task, head in self.heads.items()}
            loss = None
            if labels is not None:
                criterion = nn.CrossEntropyLoss()
                losses = [criterion(logits[task], labels[task]) for task in logits]
                loss = torch.stack(losses).mean()
            return {"loss": loss, "logits": logits}

    return MultiTaskTransformer()
