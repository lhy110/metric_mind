# Put MetricMind v2 on a public URL

## Recommended: Streamlit Community Cloud

The app is ready to deploy, but this archive is not itself a live deployment.

1. Extract `metricmind_v2.zip`.
2. Create a GitHub repository, for example `metricmind-v2`.
3. Upload the **contents** of the extracted `metricmind_v2` folder to the repository root. `app.py`, `requirements.txt`, `demo.py`, and `.streamlit/config.toml` should retain their relative paths. Do not upload your `mm` environment or the ZIP itself. Git-based upload preserves the `.streamlit` folder reliably.
4. Visit https://share.streamlit.io/ and connect your GitHub account.
5. Create an app from that repository and branch. Set **Main file path** to `app.py`. Under advanced settings select **Python 3.12**. No secrets are required.
6. Deploy, then set/check the app's sharing access is public and copy the resulting `https://...streamlit.app` URL. Test that URL in an incognito browser and on your Android tablet without signing in.

If you uploaded the whole folder instead of its contents, set the main file path to `metricmind_v2/app.py`. Root-level contents are simpler and ensure the theme config is found from the working directory.

The deployed server stays online independently of your Windows laptop. Viewers need only a browser. This app displays only generated synthetic data and allows visitors to download that data. Workflow/reset state belongs to each browser session; one visitor's Reset does not reset other visitors. It does not persist progress after a session is lost.

For a live demo, open the public URL beforehand and check all four stages. Hosting services can have startup delays after inactivity; keep a local copy as backup.

## Other Python hosting services

Create a **web service**, not a static website. Use Python 3.12, set the root directory to the directory containing `app.py`, and configure:

- Build command: `python -m pip install -r requirements.txt`
- Start command: `python start.py`
- Health-check path: `/_stcore/health`

`start.py` listens on `0.0.0.0` and reads the platform's `PORT` environment variable (default 8501). Keep WebSocket support enabled at your hosting proxy; Streamlit uses it for interactivity. Use your provider's HTTPS public URL. No app API keys or database are needed. Hosting accounts and any provider charges are separate from the app.

## Docker hosting

A Dockerfile is included for services that accept container builds. It runs as an unprivileged user, installs the pinned requirements and includes only app code and theme config. It reads the provider's PORT value and includes a health check.

```powershell
docker build -t metricmind-v2 .
docker run --rm -p 8501:8501 metricmind-v2
```

That command tests the image locally. To obtain a public URL, deploy the image to a hosting provider with an HTTPS endpoint; running Docker on your laptop alone does not publish it.

Do not disable CORS or XSRF protection to deploy. The supplied launcher leaves their normal Streamlit settings intact. No public upload functionality or execution of user-provided code is exposed.

## Verification performed

The Python public-host launcher was tested with a platform-assigned PORT and returned HTTP 200 for both `/` and `/_stcore/health`. Automated tests check session isolation and the complete demo. No hosting account was connected or live deployment created. Docker is not installed in the build environment, so the container image itself was not built here.

## Official documentation

- Streamlit Community Cloud deployment: https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy
- Dependencies: https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/app-dependencies
- Docker deployment: https://docs.streamlit.io/deploy/tutorials/docker
- Render web services (alternative Python host): https://render.com/docs/web-services
