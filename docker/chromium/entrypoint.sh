#!/bin/bash

# Generic Chromium Container Entrypoint Script
# Provides flexible startup options for different use cases

set -e

# Default values
DISPLAY_NUM=${DISPLAY_NUM:-99}
VNC_PORT=${VNC_PORT:-5900}
DEBUG_PORT=${DEBUG_PORT:-9222}

# Function to start Xvfb (virtual display)
start_xvfb() {
    echo "Starting Xvfb on display :${DISPLAY_NUM}"
    Xvfb :${DISPLAY_NUM} -screen 0 1920x1080x24 -ac +extension GLX +render -noreset &
    export DISPLAY=:${DISPLAY_NUM}
    
    # Wait for Xvfb to start
    sleep 2
}

# Function to start VNC server
start_vnc() {
    echo "Starting VNC server on port ${VNC_PORT}"
    x11vnc -display :${DISPLAY_NUM} -nopw -listen localhost -xkb -ncache 10 -ncache_cr -forever -shared -bg
}

# Function to start window manager
start_window_manager() {
    echo "Starting Fluxbox window manager"
    fluxbox -display :${DISPLAY_NUM} &
    sleep 1
}

# Function to start Chromium in headless mode
start_chromium_headless() {
    echo "Starting Chromium in headless mode on port ${DEBUG_PORT}"
    exec chromium \
        --no-sandbox \
        --disable-dev-shm-usage \
        --disable-gpu \
        --headless \
        --remote-debugging-port=${DEBUG_PORT} \
        --remote-debugging-address=0.0.0.0 \
        --disable-background-timer-throttling \
        --disable-backgrounding-occluded-windows \
        --disable-renderer-backgrounding \
        --disable-features=TranslateUI \
        --disable-ipc-flooding-protection \
        --user-data-dir=/home/chromium/.config/chromium \
        "${@}"
}

# Function to start Chromium with GUI (requires X11 forwarding)
start_chromium_gui() {
    echo "Starting Chromium with GUI"
    start_xvfb
    start_window_manager
    
    if [ "${ENABLE_VNC}" = "true" ]; then
        start_vnc
        echo "VNC server available at localhost:${VNC_PORT}"
    fi
    
    exec chromium \
        --no-sandbox \
        --disable-dev-shm-usage \
        --disable-background-timer-throttling \
        --user-data-dir=/home/chromium/.config/chromium \
        "${@}"
}

# Function to run custom command
run_custom_command() {
    echo "Running custom command: $*"
    exec "$@"
}

# Function to run Python script
run_python() {
    if [ "${GUI_MODE}" = "true" ]; then
        start_xvfb
        start_window_manager
    fi
    
    echo "Running Python script: $*"
    exec python3 "$@"
}

# Function to run interactive shell
run_shell() {
    echo "Starting interactive shell"
    exec /bin/bash
}

# Main entrypoint logic
case "${1:-chromium}" in
    "chromium"|"headless")
        start_chromium_headless "${@:2}"
        ;;
    "gui")
        start_chromium_gui "${@:2}"
        ;;
    "python"|"py")
        run_python "${@:2}"
        ;;
    "shell"|"bash")
        run_shell
        ;;
    "vnc")
        start_xvfb
        start_window_manager
        start_vnc
        echo "VNC server started. Connect to localhost:${VNC_PORT}"
        echo "Starting Chromium..."
        start_chromium_gui "${@:2}"
        ;;
    *)
        # If it's not a recognized command, treat it as a custom command
        run_custom_command "$@"
        ;;
esac
