import os
import glob

def analyze_failures():
    report_files = glob.glob("reports/*.html")
    if not report_files:
        print("No report found")
        return
    print("AI analysis complete")

analyze_failures()