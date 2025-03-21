# Use the official Streamlit base image
FROM streamlit/streamlit:latest

# Install system dependencies
RUN apt-get update && apt-get install -y \
	wget \
	unzip \
	gnupg \
	&& wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
	&& sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list' \
	&& apt-get update \
	&& apt-get install -y google-chrome-stable \
	&& rm -rf /var/lib/apt/lists/*

# Install ChromeDriver
RUN wget -q https://chromedriver.storage.googleapis.com/$(curl -s https://chromedriver.storage.googleapis.com/LATEST_RELEASE)/chromedriver_linux64.zip \
	&& unzip chromedriver_linux64.zip \
	&& mv chromedriver /usr/bin/chromedriver \
	&& chmod +x /usr/bin/chromedriver \
	&& rm chromedriver_linux64.zip

# Copy your app code
COPY . /app
WORKDIR /app

# Install Python dependencies
RUN pip install -r requirements.txt

# Expose the Streamlit port
EXPOSE 8501

# Run the app
CMD ["streamlit", "run", "app.py"]