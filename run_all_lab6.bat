@echo off
echo ===================================================
echo   RUNNING ALL LAB 06 TASKS AND GENERATING REPORTS
echo   Student: M. Aftab Aslam ^| FA23-BSE-013
echo ===================================================

echo [1/6] Running Activity 1 (Iris Flower KNN)...
python activity1_iris_knn.py

echo [2/6] Running Activity 2 (Breast Cancer KNN)...
python activity2_breast_cancer_knn.py

echo [3/6] Running Graded Task 1 (Digits KNN and K-Tuning)...
python task1_digits_knn.py

echo [4/6] Running Graded Task 2 (Abalone Sea Slugs Age Prediction)...
python task2_abalone_knn.py

echo [5/6] Generating Lab 06 Word Report (.docx)...
python generate_lab6_docx_and_pdf.py

echo [6/6] Generating Lab 06 PDF Report (.pdf)...
python generate_lab6_pdf.py

echo ===================================================
echo   ALL LAB 06 TASKS COMPLETED SUCCESSFULLY!
echo   Reports generated:
echo     - Lab_06_KNN_Report.docx
echo     - Lab_06_KNN_Report.pdf
echo     - Lab_06_KNN_Report.md
echo ===================================================
pause
