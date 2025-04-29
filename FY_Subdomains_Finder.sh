#!/bin/bash

# This script installs required tools, runs the subdomain finding process, checks live subdomains, and shows step-by-step progress.

# Define the installation function for the necessary tools
install_tools() {
  echo "[*] Installing necessary tools..."
  
  # Install Go (required for the tools)
  if ! command -v go &> /dev/null
  then
      echo "[*] Go is not installed. Installing Go..."
      wget https://dl.google.com/go/go1.19.3.linux-amd64.tar.gz -P /tmp/
      sudo tar -C /usr/local -xvzf /tmp/go1.19.3.linux-amd64.tar.gz
      export PATH=$PATH:/usr/local/go/bin
      echo "[*] Go installed successfully!"
  else
      echo "[*] Go is already installed."
  fi

  # Install subfinder
  if ! command -v subfinder &> /dev/null
  then
      echo "[*] Installing subfinder..."
      go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest
  else
      echo "[*] subfinder already installed."
  fi

  # Install assetfinder
  if ! command -v assetfinder &> /dev/null
  then
      echo "[*] Installing assetfinder..."
      go install github.com/tomnomnom/assetfinder@latest
  else
      echo "[*] assetfinder already installed."
  fi

  # Install amass
  if ! command -v amass &> /dev/null
  then
      echo "[*] Installing amass..."
      go install -v github.com/owasp-amass/amass/v3/...@latest
  else
      echo "[*] amass already installed."
  fi

  # Install httpx
  if ! command -v httpx &> /dev/null
  then
      echo "[*] Installing httpx..."
      go install -v github.com/projectdiscovery/httpx/cmd/httpx@latest
  else
      echo "[*] httpx already installed."
  fi
}

# Function to find and check subdomains
find_and_check_subdomains() {
  read -p "Enter the target domain (e.g., example.com): " DOMAIN

  if [ -z "$DOMAIN" ]; then
      echo "❌ No domain entered. Exiting."
      exit 1
  fi

  TARGETNAME=$(echo "$DOMAIN" | sed 's/\./_/g')  # Replace dots with underscores for the filename
  OUTPUT_DIR="results_$TARGETNAME"
  ALL_SUBS="$OUTPUT_DIR/Final_${TARGETNAME}_AllSubdomains.txt"
  LIVE_SUBS="$OUTPUT_DIR/live_subdomains.txt"

  mkdir -p $OUTPUT_DIR

  echo "[*] Finding subdomains for: $DOMAIN..."

  # Step 1: Find subdomains with various tools
  subfinder -d $DOMAIN -silent -all -o $OUTPUT_DIR/subfinder.txt
  assetfinder --subs-only $DOMAIN > $OUTPUT_DIR/assetfinder.txt
  amass enum -passive -d $DOMAIN -o $OUTPUT_DIR/amass.txt

  echo "[*] Subdomain discovery complete. Combining and cleaning subdomains..."

  # Step 2: Combine and clean subdomains
  cat $OUTPUT_DIR/*.txt | sort -u | grep -E ".*\.$DOMAIN$" > $ALL_SUBS

  echo "[*] Total unique subdomains found: $(wc -l < $ALL_SUBS)"

  # Step 3: Check live subdomains using httpx
  echo "[*] Checking which subdomains are live..."
  httpx -silent -l $ALL_SUBS -timeout 5 -o $LIVE_SUBS

  # Displaying live subdomains
  echo "[*] Live subdomains found:"
  cat $LIVE_SUBS

  # Final output file with all subdomains (including live ones)
  echo "[*] Live subdomains saved to: $LIVE_SUBS"
}

# Main function to install tools and run the subdomain script
main() {
  install_tools
  find_and_check_subdomains
  echo "[✔] Script completed."
}

# Run the main function
main
