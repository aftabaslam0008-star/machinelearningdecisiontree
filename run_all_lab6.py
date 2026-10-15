"""
Master runner script for Lab 06: K-Nearest Neighbors (KNN).
Executes all 4 tasks and generates reports.
Student: M. Aftab Aslam | FA23-BSE-013
"""

import subprocess
import sys
import time

scripts = [
    ("Activity 1: Iris Flower KNN", "activity1_iris_knn.py"),
    ("Activity 2: Breast Cancer KNN", "activity2_breast_cancer_knn.py"),
    ("Graded Task 1: Digits KNN Classification & K-Tuning", "task1_digits_knn.py"),
    ("Graded Task 2: Abalone Sea Slugs Age Prediction", "task2_abalone_knn.py"),
    ("Report Generator (.docx)", "generate_lab6_docx_and_pdf.py"),
    ("Report Generator (.pdf)", "generate_lab6_pdf.py")
]

print("=" * 70)
print("  MASTER RUNNER: LAB 06 (K-NEAREST NEIGHBORS ALGORITHM)  ")
print("  Student: M. Aftab Aslam | Registration No: FA23-BSE-013")
print("=" * 70)

start_time = time.time()
for idx, (title, script_name) in enumerate(scripts, 1):
    print(f"\n[{idx}/{len(scripts)}] Executing {title} ({script_name})...")
    res = subprocess.run([sys.executable, script_name])
    if res.returncode != 0:
        print(f"[-] Error: {script_name} failed with return code {res.returncode}")
        sys.exit(res.returncode)

elapsed = time.time() - start_time
print("\n" + "=" * 70)
print(f"  ALL LAB 06 TASKS EXECUTED SUCCESSFULLY IN {elapsed:.1f} SECONDS!")
print("  Generated Files:")
print("    - activity1_iris_results.png")
print("    - activity2_breast_cancer_knn.png")
print("    - task1_digits_results.png")
print("    - task2_abalone_results.png")
print("    - Lab_06_KNN_Report.docx (Complete Word Submission)")
print("    - Lab_06_KNN_Report.pdf  (Complete PDF Submission)")
print("    - Lab_06_KNN_Report.md   (Markdown Report)")
print("=" * 70)
