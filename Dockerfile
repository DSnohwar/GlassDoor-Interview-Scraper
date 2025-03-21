# Use the official Streamlit base image
FROM streamlit/streamlit:latest

# Install system dependencies
RUN apt-get update && apt-get install -y \
	wget \
	unzip \
	gnupg \
	xvfb \
	x11-utils \
	x11vnc \
	&& wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
	&& echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list \
	&& apt-get update \
	&& apt-get install -y google-chrome-stable \
	&& rm -rf /var/lib/apt/lists/*

# Install ChromeDriver (matching Chrome version)
RUN CHROME_VERSION=$(google-chrome --version | awk '{print $3}' | cut -d '.' -f1) \
	&& wget -q "https://chromedriver.storage.googleapis.com/$(curl -s "https://chromedriver.storage.googleapis.com/LATEST_RELEASE_$CHROME_VERSION")/chromedriver_linux64.zip" \
	&& unzip chromedriver_linux64.zip \
	&& mv chromedriver /usr/bin/chromedriver \
	&& chmod +x /usr/bin/chromedriver \
	&& rm chromedriver_linux64.zip

# Copy application code
COPY . /app
WORKDIR /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose Streamlit port
EXPOSE 8501

# Start Xvfb before running Streamlit
CMD ["sh", "-c", "Xvfb :99 -screen 0 1920x1080x24 & streamlit run app.py"]
