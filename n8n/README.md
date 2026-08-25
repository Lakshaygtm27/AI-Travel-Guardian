# n8n automation workflows

Import these four JSON files into the n8n instance at http://localhost:5678.

1. `01-trip-created-pdf-email.json`: webhook -> PDF API -> email attachment.
2. `02-weather-alert-notification.json`: webhook -> rain threshold check -> notification email.
3. `03-budget-warning-email.json`: webhook -> 80% budget check -> warning email.
4. `04-trip-completed-journal.json`: webhook -> journal API -> saved text journal.

The workflows are intentionally inactive until SMTP credentials and any production API URLs are configured in n8n. Webhook payloads should include `email`; weather payloads include `rain`; and budget payloads include `spent`, `budget`, and `email`.

## Gmail SMTP

Create a Gmail app password, then configure an n8n SMTP credential with host `smtp.gmail.com`, port `587`, secure `false`, username `SMTP_USER`, and password `SMTP_PASSWORD`. Keep these values in n8n credentials or environment variables; never commit them.
