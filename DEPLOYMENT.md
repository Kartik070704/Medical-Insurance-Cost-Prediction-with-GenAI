# Deployment Guide

This app is deployment-ready as a Flask + scikit-learn + Grok API + Neon Postgres project.

## Free Deployment Recommendation

Use this stack for a free final-year demo:

- GitHub for source code.
- Render Free Web Service for the Flask app.
- Neon Free Plan for Postgres storage.
- Groq Cloud free API limits for prediction reasoning.

Render Free Web Services sleep after idle traffic, so the first request after inactivity can take around a minute to start. This is acceptable for a college project demo, but not ideal for production.

## Required Services

- A deployment platform that supports Python web apps, such as Render, Railway, or Heroku.
- A Neon Postgres database.
- An xAI API key for Grok reasoning.

## Environment Variables

Set these on your deployment platform:

```text
XAI_API_KEY=your_xai_api_key
XAI_MODEL=grok-4.3
GROQ_API_KEY=your_groq_cloud_api_key
GROQ_MODEL=llama-3.1-8b-instant
DATABASE_URL=your_neon_postgres_connection_string
```

Use `XAI_API_KEY` for xAI Grok. Use `GROQ_API_KEY` for Groq Cloud keys that start with `gsk_`.

## Neon Setup

1. Create a Neon project.
2. Copy the pooled Postgres connection string.
3. Add it to the deployment platform as `DATABASE_URL`.

The app automatically creates the `insurance_predictions` table on startup. The schema is also available in `schema.sql`.

## Grok or Groq Setup

For xAI Grok:

1. Create an xAI API key.
2. Add it as `XAI_API_KEY`.
3. Keep `XAI_MODEL=grok-4.3`, or change it to another enabled xAI chat model.

For Groq Cloud:

1. Create a Groq Cloud API key.
2. Add it as `GROQ_API_KEY`.
3. Keep `GROQ_MODEL=llama-3.1-8b-instant`, or change it to another enabled Groq chat model.

If the key is missing or the API call fails, the app still predicts using a local fallback explanation.

## Render Deployment

Recommended simple path:

1. Push this folder to GitHub.
2. Create a new Render Web Service from the repository.
3. Use:

```text
Build command: pip install -r requirements.txt
Start command: gunicorn app:app
```

4. Add your AI provider key, model variable, and `DATABASE_URL` in Render environment variables.
5. Deploy.

This repository also includes `render.yaml` for Render Blueprint deployment.

## Local Production-Style Run

Create local environment variables:

```powershell
./setup_env.ps1
```

Check Neon and Groq/Grok integrations:

```powershell
python src/check_integrations.py
```

```bash
pip install -r requirements.txt
gunicorn app:app
```

On Windows, use Flask locally:

```powershell
python app.py
```
