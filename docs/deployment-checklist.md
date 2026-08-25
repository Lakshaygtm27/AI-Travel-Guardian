# Production deployment checklist

## GitHub

The production branch is `feature/travel-command-center`. Authenticate GitHub in the browser, then run:

```powershell
git push -u origin feature/travel-command-center
```

## Supabase

Create a project named `travel-guardian` in Singapore. Run `database/schema.sql`, then `database/seed.sql` from the SQL editor or psql. Put the pooler connection string in `backend/.env` as `DATABASE_URL`. Never commit `backend/.env`.

## Render

Use the repository `AI-Travel-Guardian`, root directory `backend`, build command `pip install -r requirements.txt`, and start command `uvicorn app.main:app --host 0.0.0.0 --port $PORT`. Configure `DATABASE_URL`, `OLLAMA_BASE_URL`, `SMTP_USER`, and `SMTP_PASSWORD`.

## Vercel

Use the `frontend` root directory and set `VITE_API_URL` to the deployed Render API URL. The included `vercel.json` rewrites client-side routes to `index.html`.

## Gmail SMTP / n8n

Create a Gmail app password with 2-step verification enabled. In n8n configure `smtp.gmail.com`, port `587`, secure `false`, then import the files in `n8n/`. Activate workflows only after replacing placeholder email and API values.

## Production AI

Set `OLLAMA_BASE_URL` to a reachable hosted Ollama service. A local Docker Ollama address is not reachable from Render. Test `POST /api/itinerary` after deployment.
