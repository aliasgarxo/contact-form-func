# Contact Form with Azure Function and SendGrid Integration

This project enables you to integrate a contact form into your website or application. It uses an Azure Function as the backend API to process form submissions and SendGrid to send the contact form data (name, email, subject, and message) to a specified email address.

## Features
- **Seamless Contact Form Integration**: Easily integrate this solution into your web application.
- **Email Notifications**: Send contact form submissions to your desired email address.
- **Flexible Deployment**: Run locally or host it on Azure Functions for scalability.

## Tools and Technologies Used
- **Azure Functions**: For serverless backend API hosting.
- **SendGrid**: For sending email notifications.
- **Python 3.10**: For the function logic.
- **cURL**: For testing the function locally.

---

## Setup Instructions

### 1. **Configure SendGrid**
1. Create a [SendGrid account](https://sendgrid.com/).
2. Generate an API Key:
   - Go to Settings -> API Keys.
   - Create a new API Key with "Full Access" permissions.
3. Note down the API Key for later use.
4. Identify the email address you will use to send emails (`SENDER_EMAIL`) and ensure it is verified in SendGrid.

---

### 2. **Set Up the Project Locally**

#### Clone the Repository
```bash
git clone <repository-url>
cd contact-form-func
```

#### Create the Python Azure Function App
1. Install [Azure Functions Core Tools](https://learn.microsoft.com/en-us/azure/azure-functions/functions-run-local).
    ```bash
    npm install -g azure-functions-core-tools@4 --unsafe-perm true
   ```

2. Initialize the Azure Function app:
   ```bash
   func init --worker-runtime python
   ```
3. Create an HTTP-triggered function:
   ```bash
   func new --name ContactFormFunction --template "HTTP trigger"
   ```

#### Add the Python Code
1. Replace the contents of `contact-form-func/function_app.py` with the [Azure Function Code](./contact-form-func/function_app.py)
  
#### Add `function.json`
Replace the contents of `ContactFormFunction/function.json` with [Function.json](./contact-form-func/function.json)

#### Update `local.settings.json`
```json
{
  "IsEncrypted": false,
  "Values": {
    "AzureWebJobsStorage": "UseDevelopmentStorage=true",
    "FUNCTIONS_WORKER_RUNTIME": "python",
    "SENDGRID_API_KEY": "<your-sendgrid-api-key>",
    "SENDER_EMAIL": "<your-sender-email>",
    "RECEIVER_EMAIL": "<your-receiver-email>"
  }
}
```

#### Add `requirements.txt`
```txt
python-http-client==3.3.7
sendgrid==6.11.0
starkbank-ecdsa==2.2.0
azure-functions==1.13.3
```

#### Install Dependencies
```bash
pip install -r requirements.txt
```

### Set Environment variable
Add the required environment variables locally in a .env file at the project root:
```bash
SENDGRID_API_KEY=<your-sendgrid-api-key>
SENDER_EMAIL=<your-verified-sender-email>
RECEIVER_EMAIL=<your-receiver-email>
```
Install python-dotenv to load environment variables from .env:
```bash
pip install python-dotenv
```

#### Run the Function Locally
Start the function:
```bash
func start --verbose
```

Test with `curl`:
```bash
curl -X POST -H "Content-Type: application/json" \
-d '{"name":"Aliasgar Husain","email":"contact@aliasgar.cloud","subject":"Hello","message":"This is a test message"}' \
http://localhost:7071/api/contact-form
```

---

### 3. **Deploy to Azure**

#### Create an Azure Function App
1. Log in to Azure:
   ```bash
   az login
   ```
2. Create a Function App:
   ```bash
   az functionapp create --name <app-name> --storage-account <storage-account> --resource-group <resource-group> --runtime python --runtime-version 3.10 --consumption-plan-location <region>
   ```

#### Deploy the Function
```bash
func azure functionapp publish <app-name>
```

---

### 4. **Configure Environment Variables on Azure**
1. Go to your Function App in the Azure Portal.
2. Navigate to **Configuration** -> **Application Settings**.
3. Add the following keys:
   - `SENDGRID_API_KEY`: Your SendGrid API Key.
   - `SENDER_EMAIL`: The verified sender email.
   - `RECEIVER_EMAIL`: The destination email address.

---

### 5. **Enable CORS**
1. In the Azure Portal, go to your Function App.
2. Under **API** -> **CORS**, add your website domain (e.g., `https://your-domain.com`).
3. Save changes.

---

### 6. **Testing the Deployed Function**
Make a `POST` request to your Azure Function endpoint:
```bash
curl -X POST -H "Content-Type: application/json" \
-d '{"name":"Aliasgar Husain","email":"contact@aliasgar.cloud","subject":"Hello","message":"This is a test message"}' \
"https://<app-name>.azurewebsites.net/api/contact-form?code=<function-key>"
```

---

### 7. **Integrate with Your Website**
Update your contact form to send data to the Azure Function endpoint:
```javascript
fetch("https://<app-name>.azurewebsites.net/api/contact-form?code=<function-key>", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    name: formData.name,
    email: formData.email,
    subject: formData.subject,
    message: formData.message
  })
})
  .then(response => response.json())
  .then(data => console.log("Success:", data))
  .catch(error => console.error("Error:", error));
```

---

## Notes
- Ensure all email addresses are verified in SendGrid.
- Test thoroughly both locally and after deployment.
- Keep API keys secure and avoid hardcoding them in your code.
