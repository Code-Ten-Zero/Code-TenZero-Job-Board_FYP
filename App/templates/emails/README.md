# 📧 EMAIL TEMPLATES

All email templates must include both `.html.j2` and `.txt.j2` versions.

## Why Two Versions?

`.html.j2` – This is the HTML version of the email. It allows for rich formatting like bold text, clickable links, colors, and images. Most modern email clients support and prefer HTML emails.

`.txt.j2` – This is the plain text fallback version. It is displayed when:

* The recipient's email client does not support HTML

* The recipient has chosen to view only plain text emails

* There's a deliverability issue that strips HTML content

Ensuring both versions are available increases compatibility and improves email deliverability, accessibility, and readability.

## File Naming Convention

Each email template should have the following structure:

```txt
emails/
  └── job_posted.html.j2
  └── job_posted.txt.j2
```

The two files should have matching base names and live in the `templates/emails/` directory (or wherever Flask/Jinja templates are located).

## Jinja Support

These templates use [Jinja2](https://jinja.palletsprojects.com/en/stable/) syntax, which allows you to:

* Inject variables (e.g. `{{ user.first_name }}`, `{{ job_title }}`)

* Use control logic (e.g. `{% if ... %}` / `{% for ... %}`)

Variables passed into these templates will come from your Flask views or email-sending utility.

## ✅ Best Practices

* Keep `.txt.j2` messages clean and readable without relying on HTML formatting.

* Use the same content and structure between `.html.j2` and `.txt.j2` where possible.

* Test your email output by rendering and sending both versions.

## ✨ Example Templates

`job_posted.html.j2` (HTML version)

```html
<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{{ job_title }} - New Job Listing</title>
        <style>
            body { font-family: Arial, sans-serif; color: #333; }
            h1 { color: #4CAF50; }
            .footer { font-size: 12px; color: #aaa; }
        </style>
    </head>
    <body>
        <h1>New Job Listing: {{ job_title }}</h1>
        <p>Hello {{ recipient_name }},</p>
        <p>We are excited to inform you about a new job posting:</p>
        <ul>
            <li><strong>Title:</strong> {{ job_title }}</li>
            <li><strong>Company:</strong> {{ company_name }}</li>
            <li><strong>Location:</strong> {{ job_location }}</li>
        </ul>
        <p><a href="{{ job_url }}" style="color: #4CAF50;">Click here</a> to view the job listing and apply.</p>
        <p>Best regards,<br>Your Job Board Team</p>
        <hr>
        <p class="footer">This email was sent to you because you are subscribed to job notifications.</p>
    </body>
</html>
```

`job_posted.txt.j2` (Plain text version)

```txt
New Job Listing: {{ job_title }}

Hello {{ recipient_name }},

We are excited to inform you about a new job posting:

Title: {{ job_title }}
Company: {{ company_name }}
Location: {{ job_location }}

Click here to view the job listing and apply: {{ job_url }}

Best regards,
Your Job Board Team

--------------------------------------------------
This email was sent to you because you are subscribed to job notifications.
```

## ✨ Example Output

Assuming you pass the following context to the templates:

```python
context = {
    'job_title': 'Software Engineer',
    'company_name': 'Tech Innovators Ltd.',
    'job_location': 'New York, NY',
    'job_url': 'https://example.com/jobs/software-engineer',
    'recipient_name': 'John Doe',
}
```

HTML version (`job_posted.html.j2`):

```html
<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Software Engineer - New Job Listing</title>
        <style>
            body { font-family: Arial, sans-serif; color: #333; }
            h1 { color: #4CAF50; }
            .footer { font-size: 12px; color: #aaa; }
        </style>
    </head>
    <body>
        <h1>New Job Listing: Software Engineer</h1>
        <p>Hello John Doe,</p>
        <p>We are excited to inform you about a new job posting:</p>
        <ul>
            <li><strong>Title:</strong> Software Engineer</li>
            <li><strong>Company:</strong> Tech Innovators Ltd.</li>
            <li><strong>Location:</strong> New York, NY</li>
        </ul>
        <p><a href="https://example.com/jobs/software-engineer" style="color: #4CAF50;">Click here</a> to view the job listing and apply.</p>
        <p>Best regards,<br>Your Job Board Team</p>
        <hr>
        <p class="footer">This email was sent to you because you are subscribed to job notifications.</p>
    </body>
</html>
```

Plain Text version (job_posted.txt.j2):

```txt
New Job Listing: Software Engineer

Hello John Doe,

We are excited to inform you about a new job posting:

Title: Software Engineer
Company: Tech Innovators Ltd.
Location: New York, NY

Click here to view the job listing and apply: https://example.com/jobs/software-engineer

Best regards,
Your Job Board Team

--------------------------------------------------
This email was sent to you because you are subscribed to job notifications.
```
