# Rasa Models Directory

This directory contains trained Rasa chatbot models.

## Files (Generated, not in Git)

Trained models are stored as `.tar.gz` files with timestamps:
- `20251031-143409-spicy-url.tar.gz`
- `20251102-000705-fat-outpost.tar.gz`

## How to Generate Models

```bash
cd Rasa
rasa train
```

**Training time:** 2-3 minutes

**Note:** Models are excluded from git due to size (~50-100 MB each). Train locally before running Rasa.

## Model Contents

Each model contains:
- NLU pipeline (132 symptom entities + synonyms)
- Dialogue policies
- Medical domain configuration

See `Rasa/README.md` for complete setup instructions.
