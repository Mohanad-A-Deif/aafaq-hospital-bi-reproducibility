import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from aafaq_bi.modeling import MultiTaskConfig, build_label_maps, create_multitask_model, require_ml_dependencies
from aafaq_bi.schema import CLASSIFICATION_TARGET_COLUMNS
from aafaq_bi.data_io import read_csv


def main():
    parser = argparse.ArgumentParser(description="Optional AAFAQ multi-task classifier training scaffold.")
    parser.add_argument("--data", default="data/raw/AAFAQ_Dataset.csv")
    parser.add_argument("--model", default="aubmindlab/bert-base-arabertv02")
    parser.add_argument("--epochs", type=int, default=3)
    parser.add_argument("--batch-size", type=int, default=8)
    parser.add_argument("--max-length", type=int, default=128)
    parser.add_argument("--output-dir", default="models/aafaq_multitask_classifier")
    args = parser.parse_args()

    require_ml_dependencies()
    import torch
    from torch.utils.data import Dataset, DataLoader, random_split
    from transformers import AutoTokenizer, AdamW
    from sklearn.metrics import f1_score, accuracy_score

    data_path = Path(args.data)
    if not data_path.exists():
        raise FileNotFoundError(f"AAFAQ dataset not found: {data_path}")

    df = read_csv(data_path)
    label_columns = [c for c in CLASSIFICATION_TARGET_COLUMNS if c in df.columns]
    if not label_columns:
        raise ValueError("No taxonomy label columns found in the input dataset.")

    label_maps = build_label_maps(df, label_columns)
    num_labels = {task: len(mapping) for task, mapping in label_maps.items()}
    tokenizer = AutoTokenizer.from_pretrained(args.model)
    model = create_multitask_model(args.model, num_labels)

    class AAFAQDataset(Dataset):
        def __init__(self, frame):
            self.frame = frame.reset_index(drop=True)
        def __len__(self):
            return len(self.frame)
        def __getitem__(self, idx):
            row = self.frame.iloc[idx]
            enc = tokenizer(
                str(row["QuestionText"]),
                truncation=True,
                padding="max_length",
                max_length=args.max_length,
                return_tensors="pt",
            )
            item = {k: v.squeeze(0) for k, v in enc.items()}
            item["labels"] = {
                task: torch.tensor(label_maps[task][str(row[task])], dtype=torch.long)
                for task in label_columns
            }
            return item

    def collate(batch):
        return {
            "input_ids": torch.stack([b["input_ids"] for b in batch]),
            "attention_mask": torch.stack([b["attention_mask"] for b in batch]),
            "labels": {
                task: torch.stack([b["labels"][task] for b in batch])
                for task in label_columns
            },
        }

    dataset = AAFAQDataset(df)
    val_size = max(1, int(0.1 * len(dataset)))
    train_size = len(dataset) - val_size
    train_ds, val_ds = random_split(dataset, [train_size, val_size], generator=torch.Generator().manual_seed(42))
    train_loader = DataLoader(train_ds, batch_size=args.batch_size, shuffle=True, collate_fn=collate)
    val_loader = DataLoader(val_ds, batch_size=args.batch_size, shuffle=False, collate_fn=collate)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)
    optimizer = AdamW(model.parameters(), lr=2e-5)

    for epoch in range(args.epochs):
        model.train()
        total_loss = 0.0
        for batch in train_loader:
            batch = {k: (v.to(device) if not isinstance(v, dict) else {kk: vv.to(device) for kk, vv in v.items()}) for k, v in batch.items()}
            optimizer.zero_grad()
            out = model(**batch)
            out["loss"].backward()
            optimizer.step()
            total_loss += out["loss"].item()
        print(f"Epoch {epoch+1}/{args.epochs} - train_loss={total_loss/max(1,len(train_loader)):.4f}")

    model.eval()
    preds = {task: [] for task in label_columns}
    golds = {task: [] for task in label_columns}
    with torch.no_grad():
        for batch in val_loader:
            labels = batch["labels"]
            batch = {k: (v.to(device) if not isinstance(v, dict) else {kk: vv.to(device) for kk, vv in v.items()}) for k, v in batch.items()}
            out = model(**batch)
            for task in label_columns:
                pred = out["logits"][task].argmax(dim=-1).cpu().tolist()
                gold = labels[task].cpu().tolist()
                preds[task].extend(pred)
                golds[task].extend(gold)

    metrics = {}
    for task in label_columns:
        metrics[task] = {
            "accuracy": float(accuracy_score(golds[task], preds[task])),
            "macro_f1": float(f1_score(golds[task], preds[task], average="macro", zero_division=0)),
        }
    outdir = Path(args.output_dir)
    outdir.mkdir(parents=True, exist_ok=True)
    torch.save(model.state_dict(), outdir / "model_state.pt")
    (outdir / "label_maps.json").write_text(json.dumps(label_maps, ensure_ascii=False, indent=2), encoding="utf-8")
    (outdir / "metrics.json").write_text(json.dumps(metrics, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(metrics, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
