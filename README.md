# OSINT-MASTER

OSINT-MASTER is a Python-based command-line reconnaissance and intelligence gathering tool designed for authorized, lawful, and privacy-conscious research. It allows users to query:

- IP address reputation and geolocation data
- Social media and public profile information for a username across multiple platforms
- Domain and subdomain details, WHOIS metadata, and takeover-risk checks

The project is intended for legitimate security research, threat intelligence, and authorized assessments where you have a clear legal and operational basis to collect and analyze publicly available data.

![Description of image](./resources/osint-meme.png)
## Project Overview

This repository provides a lightweight CLI built with Python and standard HTTP requests. It helps automate common OSINT tasks and saves output to the `output/` directory.

Current capabilities include:

- IP lookups via the `ffraud` public IP intelligence API
- Username lookups across Instagram, GitHub, X (Twitter), TikTok, and LinkedIn using Apify-backed endpoints
- Domain validation plus WHOIS metadata retrieval and subdomain enumeration
- Subdomain takeover scanning using public certificate transparency and takeover-risk services

## Features

### 1. IP Lookup

Use `-i` to inspect an IP address and retrieve:

- ISP and network information
- VPN/TOR/proxy indicators
- Geo-location details
- ASN and timezone information
- Fraud score and risk indicators

### 2. Username Lookup

Use `-u` to query a username across several platforms, including:

- Instagram profile metadata and last activity
- GitHub profile details
- X/Twitter profile information
- TikTok profile statistics
- LinkedIn public profile details

### 3. Domain Enumeration

Use `-d` to inspect a domain and gather:

- WHOIS registrar and administrative information
- Domain event history
- Subdomain discovery from certificate transparency data
- Potential subdomain takeover risk findings

### 4. Output Capture

Use `-o` to save the tool output to a file in the `output/` folder.

## Repository Layout

- `src/main.py` – CLI entry point
- `src/ip_lookup.py` – IP intelligence logic
- `src/username_lookup.py` – Username intelligence logic
- `src/domain_enum.py` – Domain and subdomain enumeration logic
- `.env.example` – template for environment variables
- `requirements.txt` – Python dependencies
- `output/` – generated command output is stored here

## Prerequisites

Before using the project, make sure you have:

- Python 3.9 or newer
- `pip` for installing Python packages
- Internet access to reach the external APIs used by the tool
- Valid API tokens for the supported services if required

The project currently expects the following environment variables:

- `APIFY_APIKEY` for username lookups via Apify
- `WHOIS_APIKEY` for WHOIS API access

## Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/zakariasalhi12/OSINT-MASTER.git
   cd OSINT-MASTER
   ```

2. Create and activate a virtual environment (recommended):

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. Install required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Configure environment variables:

   Copy the example file and set your tokens:

   ```bash
   cp .env.example .env
   ```

   Then edit `.env` and add the required values:

   ```env
   APIFY_APIKEY=your_apify_token_here
   WHOIS_APIKEY=your_whois_api_key_here
   ```

5. Verify the CLI is available:

   ```bash
   python src/main.py --help
   ```

## Configuration

### Environment Variables

The tool reads values from a local `.env` file using `python-dotenv`.

| Variable | Required | Purpose |
|---|---:|---|
| `APIFY_APIKEY` | Yes for username lookups | Access to platform data providers used by the username enumeration functions |
| `WHOIS_APIKEY` | Yes for domain WHOIS checks | Authorization for WHOIS API requests |

### Output Directory

When `-o` is passed, the script saves results under:

```text
output/
```

The file name is sanitized to the base name only. For example:

```bash
python src/main.py -u johndoe -o johndoe_report.txt
```

This saves to:

```text
output/johndoe_report.txt
```

## Usage

The CLI entry point is:

```bash
python src/main.py
```

### Command Options

```text
-i "IP Address"       Search information by IP address
-u "Username"         Search information by username
-d "Domain"           Enumerate subdomains and check for takeover risks
-o "FileName"         File name to save output
--help                Display this help message
```

### Examples

#### IP lookup

```bash
python src/main.py -i 8.8.8.8
python src/main.py -i 8.8.8.8 -o google_ip.txt
```

#### Username lookup

```bash
python src/main.py -u johndoe
python src/main.py -u janedoe -o janedoe_report.txt
```

#### Domain enumeration

```bash
python src/main.py -d example.com
python src/main.py -d example.com -o example_domain.txt
```

### Example Output

```text
IP: 8.8.8.8
ISP: Google LLC
TOR: Unknown
VPN: Unknown
Proxy: Unknown

Geolocation Informations:
Country: United States
City: Mountain View
Latitude: 37.3860
Longitude: -122.0838
ASN: AS15169
Timezone: America/Los_Angeles
```

## Operational Notes

- This tool relies on third-party APIs and services; availability and output quality may vary depending on the provider.
- Some lookups can be slow because they query several independent services.
- Results should be treated as investigative leads, not definitive proof of identity, ownership, or malicious behavior.
- Always verify any intelligence gathered using additional data sources and lawful investigative procedures.

## Ethical and Legal Use Guidelines

This tool is intended for legitimate, authorized, and transparent use only. It must not be used for harassment, stalking, privacy violations, unauthorized access, or deceptive conduct.

### You must not use this tool to:

- Harass, intimidate, or target individuals or groups
- Collect or expose personal information without a valid legal basis
- Circumvent access restrictions, rate limits, or platform terms of service
- Conduct unauthorized reconnaissance against third parties
- Obtain or disseminate sensitive data without explicit authorization
- Perform illegal surveillance, blackmail, identity theft, or fraud

### Before using the tool, ensure that you:

- Have a legitimate and lawful reason to perform the research
- Have authorization from the relevant parties when required
- Comply with all applicable laws, regulations, and contractual obligations
- Respect local privacy laws, platform terms, and data protection regulations
- Avoid collecting or storing unnecessary personal data

### Important warnings

- Publicly available data does not automatically equal lawful or ethical permission to use it.
- Some jurisdictions impose strict rules around personal data collection, profiling, and automated scraping.
- Even when information is visible on public platforms, using it for doxxing, stalking, or exploitation may be illegal and harmful.
- The project maintainers are not responsible for misuse or unlawful activity performed with this tool.

### Recommended use cases

This tool may be appropriate for:

- Authorized security research
- Compliance reviews and internal risk assessments
- Threat-intelligence exploration with explicit permission
- Legitimate OSINT investigations under applicable legal frameworks
- Research on public infrastructure and domain ownership with proper authorization

## Security and Responsible Use

Use this project responsibly and in compliance with the law. If you are conducting work on a third-party system, verify that:

- You have written authorization, where applicable
- Your testing is within the scope of the engagement
- You are not violating platform policies or local law
- You minimize the risk of exposing sensitive information

## Known limitations

- The tool depends on external services, including `ffraud.com`, `who.is`, `crt.sh`, Canopy Stack, and Apify actors. Availability, response formats, authentication requirements, and provider-side rate limits or quotas are outside this project’s control.
- API credentials must be supplied through environment variables for the services that require them. In particular, username lookups depend on an Apify API key, while WHOIS lookups require a WHOIS API key. Missing, invalid, expired, or exhausted credentials can cause lookups to fail.
- A username lookup runs scrapers for Instagram, TikTok, GitHub, X, and LinkedIn. This can be slow, can fail independently for individual platforms, and may incur provider usage charges. The LinkedIn scraper is configured for a paid profile-details mode (`$4 per 1k` in the provider request).
- Network requests have a 120-second timeout, but the tool does not implement retries, backoff, or provider-specific throttling. Repeated requests may therefore hit upstream limits or remain unavailable until the provider recovers.
- Results are limited to information returned by the upstream providers. Private, deleted, blocked, newly changed, or unavailable profiles may be reported as missing or `Unknown`; returned data should not be treated as complete or authoritative.
- Domain enumeration is not exhaustive: it discovers names present in `crt.sh` certificate-transparency records, resolves hosts through the local DNS resolver, and checks takeover signals through Canopy Stack. It may miss domains without certificates, DNS records, or provider coverage, and DNS resolution is not guaranteed to reflect all addresses.
- The project does not define or enforce a universal API rate limit. Users are responsible for complying with each data source’s terms of service, acceptable-use rules, and applicable law.

## Troubleshooting

### Common issues

#### `ModuleNotFoundError`

Install dependencies:

```bash
pip install -r requirements.txt
```

#### Missing environment variables

Ensure `.env` exists and contains valid values:

```bash
cp .env.example .env
```

Then populate the required keys.

#### API requests fail

Check:

- Your internet connection
- API token validity
- Rate limits or provider restrictions
- Whether the target is reachable and valid


## Contributing

Contributions are welcome if they improve security, documentation, maintainability, or usability while preserving the ethical and lawful use of the project. All contributors should follow responsible research practices and avoid enabling misuse.

## Disclaimer

OSINT-MASTER is a research and investigation tool. It does not guarantee the accuracy, completeness, legality, or appropriateness of third-party data. Use it only in compliance with applicable law, policy, and professional standards.
