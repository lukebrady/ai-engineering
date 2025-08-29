# Generic Chromium Docker Container
# Provides headless Chromium browser with automation tools
FROM alpine:3.19

LABEL maintainer="AI Engineering Team"
LABEL description="Generic Chromium container for web automation and scraping"
LABEL version="1.0.0"

# Set timezone
ENV TZ=UTC

# Create non-root user for security
RUN addgroup -g 1001 -S chromium && \
    adduser -u 1001 -S chromium -G chromium -h /home/chromium -s /bin/sh

# Install system dependencies
RUN apk add --no-cache \
    # Core dependencies
    wget \
    curl \
    unzip \
    ca-certificates \
    ttf-liberation \
    # Chromium and dependencies
    chromium \
    # Additional tools for web automation
    xvfb \
    x11vnc \
    fluxbox \
    # Python for potential scripting
    python3 \
    py3-pip \
    # Bash for entrypoint script
    bash


# Set up Chrome/Chromium directories and permissions
RUN mkdir -p /home/chromium/.config/chromium \
    && mkdir -p /home/chromium/Downloads \
    && mkdir -p /tmp/.X11-unix \
    && chmod 1777 /tmp/.X11-unix \
    && chown -R chromium:chromium /home/chromium

# Environment variables for Chromium
ENV DISPLAY=:99
ENV CHROME_BIN=/usr/bin/chromium
ENV CHROMIUM_FLAGS="--no-sandbox --disable-dev-shm-usage --disable-gpu --headless --remote-debugging-port=9222 --remote-debugging-address=0.0.0.0"

# Expose debugging port
EXPOSE 9222

# Copy entrypoint script
COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

# Switch to non-root user
USER chromium
WORKDIR /home/chromium

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:9222/json || exit 1

# Default entrypoint
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]

# Default command - run headless chromium
CMD ["chromium"]