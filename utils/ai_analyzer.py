import os
import glob
from typing import List, Dict, Any
from bs4 import BeautifulSoup
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()


def analyze_failures() -> None:
    """Analyze test failures using Anthropic AI"""
    report_files = glob.glob("reports/*.html")
    if not report_files:
        print("No report found")
        return

    report_file = report_files[0]
    print(f"Analyzing report: {report_file}")

    with open(report_file, 'r', encoding='utf-8') as f:
        html_content = f.read()

    soup = BeautifulSoup(html_content, 'html.parser')
    
    failed_tests: List[Dict[str, str]] = []
    for row in soup.find_all('tr', class_='failed'):
        test_name = row.find('td', class_='name')
        error_msg = row.find('td', class_='error')
        if test_name and error_msg:
            failed_tests.append({
                'test': test_name.get_text(strip=True),
                'error': error_msg.get_text(strip=True)
            })

    if not failed_tests:
        print("No failed tests found")
        return

    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print("ANTHROPIC_API_KEY not found in environment")
        return

    client = Anthropic(api_key=api_key)

    prompt = f"""Analyze the following test failures and provide:
1. Root cause analysis for each failure
2. Suggested fixes
3. Potential flakiness issues

Failed tests:
{failed_tests}

Provide concise, actionable analysis."""

    try:
        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=4096,
            messages=[{"role": "user", "content": prompt}]
        )

        analysis = message.content[0].text
        
        os.makedirs("reports", exist_ok=True)
        with open("reports/ai_report.txt", "w", encoding='utf-8') as f:
            f.write("AI Failure Analysis Report\n")
            f.write("=" * 50 + "\n\n")
            f.write(analysis)

        print("AI analysis complete. Report saved to reports/ai_report.txt")

    except Exception as e:
        print(f"Error during AI analysis: {e}")


if __name__ == "__main__":
    analyze_failures()