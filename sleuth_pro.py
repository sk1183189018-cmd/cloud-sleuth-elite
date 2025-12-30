import os
import requests
import threading
import time
from datetime import datetime
from fpdf import FPDF

# --- CONFIG ---
TOKEN = "7763707184:AAEe8Ozx_V1b6A6pNvyeSfMRpZbtFN5nzsU"
CHAT_ID = "7072808951"

def send_telegram_msg(message):
    try:
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        requests.post(url, data={"chat_id": CHAT_ID, "text": message})
    except: pass

# --- EXPLOIT FINDER ENGINE ---

def find_exploits(service_name):
    """यह फंक्शन इंटरनेट से उस सर्विस के लिए तैयार हैकिंग कोड खोजता है"""
    print(f"[!] Searching Exploits for: {service_name}")
    # Google Dork for Exploit-DB and GitHub
    query = f"{service_name} exploit site:exploit-db.com OR site:github.com"
    search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
    return search_url

def deep_scan_with_exploits(target):
    print(f"\n[!] Mission Started: {target}")
    
    # 1. Nmap Service Detection
    print("[+] Detecting Services...")
    nmap_raw = os.popen(f"nmap -sV -Pn --top-ports 10 {target}").read()
    
    # सर्विस के नाम निकालना (जैसे Apache 2.4.41)
    exploits_found = []
    lines = nmap_raw.split('\n')
    for line in lines:
        if "open" in line and "  " in line:
            service = line.split("  ")[-1].strip()
            if service:
                link = find_exploits(service)
                exploits_found.append(f"Service: {service}\nExploit Link: {link}")

    # 2. Nikto Scan
    print("[+] Searching Vulnerabilities...")
    nikto_raw = os.popen(f"nikto -h {target} -Tuning 1").read()

    return nmap_raw, exploits_found, nikto_raw

def generate_pro_report(target, nmap, exploits, nikto):
    pdf = FPDF()
    pdf.add_page()
    
    # Professional Header
    pdf.set_font("Arial", 'B', 20)
    pdf.set_text_color(255, 0, 0)
    pdf.cell(200, 15, txt="CRITICAL SECURITY AUDIT", ln=True, align='C')
    pdf.set_text_color(0, 0, 0)
    
    # Exploit Section (सबसे ऊपर)
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, txt="🔥 READY-TO-USE EXPLOITS FOUND:", ln=True)
    pdf.set_font("Arial", size=9)
    pdf.set_text_color(0, 0, 255)
    for ex in exploits:
        pdf.multi_cell(0, 7, txt=ex)
    pdf.set_text_color(0, 0, 0)
    
    # Nmap & Nikto Details
    pdf.ln(5)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, txt="Full Service Analysis:", ln=True)
    pdf.set_font("Arial", size=8)
    pdf.multi_cell(0, 4, txt=nmap)
    
    fname = f"Exploit_Report_{target}.pdf"
    pdf.output(fname)
    return fname

# --- MAIN RUNNER ---
if __name__ == "__main__":
    target = input("Enter Target to Exploit: ")
    send_telegram_msg(f"⚡ Elite Exploit Search Started for: {target}")
    
    nmap, exploits, nikto = deep_scan_with_exploits(target)
    report = generate_pro_report(target, nmap, exploits, nikto)
    
    from requests import post
    with open(report, "rb") as f:
        post(f"https://api.telegram.org/bot{TOKEN}/sendDocument", 
             data={"chat_id": CHAT_ID}, files={"document": f})
    
    send_telegram_msg(f"✅ Mission Finished. Check the PDF for Exploit Scripts!")
