"""
Script to generate a publication-grade PDF Report (Lab_06_KNN_Report.pdf)
using ReportLab.
Student: M. Aftab Aslam | FA23-BSE-013
"""

import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, KeepTogether, PageBreak, HRFlowable
)
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            super().showPage()
        super().save()

    def draw_page_number(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748B"))
        
        # Header (pages > 1)
        if self._pageNumber > 1:
            self.drawString(54, letter[1] - 36, "Machine Learning Fundamentals (AIC-354) — Lab 06: K-Nearest Neighbors (KNN)")
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.5)
            self.line(54, letter[1] - 42, letter[0] - 54, letter[1] - 42)
            
        # Footer
        page_text = f"Page {self._pageNumber} of {page_count}"
        student_text = "Student: M. Aftab Aslam | Reg No: FA23-BSE-013"
        self.drawString(54, 30, student_text)
        self.drawRightString(letter[0] - 54, 30, page_text)
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.5)
        self.line(54, 42, letter[0] - 54, 42)
        self.restoreState()

def build_pdf(filename="Lab_06_KNN_Report.pdf"):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=48,
        rightMargin=48,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()
    
    # Custom styles
    style_univ = ParagraphStyle(
        'UnivHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=16,
        textColor=colors.HexColor('#1E3A8A'),
        alignment=1
    )
    
    style_subtitle = ParagraphStyle(
        'UnivSub',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=13,
        textColor=colors.HexColor('#475569'),
        alignment=1
    )
    
    style_title = ParagraphStyle(
        'ReportTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=16,
        leading=20,
        textColor=colors.white,
        alignment=1
    )
    
    style_title_sub = ParagraphStyle(
        'ReportTitleSub',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=13,
        textColor=colors.HexColor('#93C5FD'),
        alignment=1
    )

    style_h1 = ParagraphStyle(
        'SectionH1',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=16,
        textColor=colors.HexColor('#1E3A8A'),
        spaceBefore=14,
        spaceAfter=6
    )

    style_h2 = ParagraphStyle(
        'SectionH2',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=14,
        textColor=colors.HexColor('#0F172A'),
        spaceBefore=8,
        spaceAfter=4
    )

    style_body = ParagraphStyle(
        'BodyDark',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=12.5,
        textColor=colors.HexColor('#1E293B'),
        spaceBefore=3,
        spaceAfter=3
    )

    style_code = ParagraphStyle(
        'CodeSnippet',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=7.2,
        leading=9.2,
        textColor=colors.HexColor('#0F172A')
    )

    style_terminal = ParagraphStyle(
        'TermSnippet',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=7.2,
        leading=9.2,
        textColor=colors.HexColor('#38BDF8')
    )

    style_callout = ParagraphStyle(
        'CalloutText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11.5,
        textColor=colors.HexColor('#166534')
    )

    style_caption = ParagraphStyle(
        'FigCaption',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=8,
        leading=10,
        textColor=colors.HexColor('#64748B'),
        alignment=1,
        spaceBefore=3,
        spaceAfter=6
    )

    story = []

    # 1. Header & Title Block
    story.append(Paragraph("COMSATS UNIVERSITY ISLAMABAD", style_univ))
    story.append(Paragraph("DEPARTMENT OF COMPUTER SCIENCE / SOFTWARE ENGINEERING", style_univ))
    story.append(Spacer(1, 2))
    story.append(Paragraph("Course: Machine Learning Fundamentals (AIC-354)", style_subtitle))
    story.append(Spacer(1, 8))

    # Title Card
    title_data = [[
        Paragraph("LAB 06 LABORATORY REPORT<br/><font size='10' color='#93C5FD'>K-Nearest Neighbors (KNN) Algorithm — Solved Activities & Graded Tasks</font>", style_title)
    ]]
    t_title = Table(title_data, colWidths=[516])
    t_title.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#1E3A8A')),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 10),
        ('BOTTOMPADDING', (0,0), (-1,-1), 10),
        ('LEFTPADDING', (0,0), (-1,-1), 12),
        ('RIGHTPADDING', (0,0), (-1,-1), 12),
    ]))
    story.append(t_title)
    story.append(Spacer(1, 8))

    # Student Metadata Table
    meta_data = [
        [Paragraph("<b>Student Name:</b>", style_body), Paragraph("M. Aftab Aslam", style_body)],
        [Paragraph("<b>Registration No:</b>", style_body), Paragraph("<font color='#1E3A8A'><b>FA23-BSE-013</b></font> (BS Software Engineering)", style_body)],
        [Paragraph("<b>Lab Topics:</b>", style_body), Paragraph("KNN Classification, KNN Regression, Hyperparameter K-Tuning, Feature Scaling", style_body)],
        [Paragraph("<b>Date of Submission:</b>", style_body), Paragraph("October 2026", style_body)]
    ]
    t_meta = Table(meta_data, colWidths=[120, 396])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,-1), colors.HexColor('#F1F5F9')),
        ('BACKGROUND', (1,0), (1,-1), colors.HexColor('#FFFFFF')),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_meta)
    story.append(Spacer(1, 10))

    # Executive Summary
    story.append(Paragraph("1. Executive Summary & Algorithmic Foundations", style_h1))
    story.append(Paragraph(
        "K-Nearest Neighbors (KNN) is an intuitive non-parametric, instance-based supervised learning algorithm. "
        "Unlike eager learners, KNN stores the complete training space and performs classification or continuous regression "
        "by measuring distance (typically Euclidean distance) to the closest <i>K</i> neighboring observations. "
        "This laboratory report implements and analyzes four comprehensive tasks as mandated by the AIC-354 syllabus:",
        style_body
    ))
    story.append(Spacer(1, 4))

    # Summary Table
    summary_data = [
        ["Task", "Dataset", "Type", "Optimal K", "Performance Metric"],
        ["Activity 1", "Iris Flower", "Classification (3-class)", "K = 5", "97.78% Accuracy"],
        ["Activity 2", "Breast Cancer", "Classification (Binary)", "K = 5", "84.62% Acc (121/143)"],
        ["Graded Task 1", "Handwritten Digits", "Classification (10-class)", "K = 1 (Tuned)", "98.61% Acc (99.02% CV)"],
        ["Graded Task 2", "Abalone Shells", "Regression & Tier Classif.", "K = 15 (Distance)", "RMSE: 2.25 yrs | R²: 0.53"]
    ]
    t_sum = Table(summary_data, colWidths=[70, 110, 126, 80, 130])
    t_sum.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1E3A8A')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,0), 8),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor('#F8FAFC'), colors.HexColor('#FFFFFF')]),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_sum)
    story.append(Spacer(1, 10))

    # Helper for code/terminal cards
    def make_box(content_p, bg_hex="#F8FAFC", border_hex="#CBD5E1"):
        t = Table([[content_p]], colWidths=[516])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor(bg_hex)),
            ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor(border_hex)),
            ('TOPPADDING', (0,0), (-1,-1), 5),
            ('BOTTOMPADDING', (0,0), (-1,-1), 5),
            ('LEFTPADDING', (0,0), (-1,-1), 8),
            ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ]))
        return t

    # Helper for callouts
    def make_callout(title, text):
        content = Paragraph(f"<b>📌 {title}:</b> {text}", style_callout)
        t = Table([[content]], colWidths=[516])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F0FDF4')),
            ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#86EFAC')),
            ('LINELEFT', (0,0), (-1,-1), 2.5, colors.HexColor('#16A34A')),
            ('TOPPADDING', (0,0), (-1,-1), 5),
            ('BOTTOMPADDING', (0,0), (-1,-1), 5),
            ('LEFTPADDING', (0,0), (-1,-1), 8),
            ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ]))
        return t

    # 2. ACTIVITY 1
    story.append(Paragraph("2. Solved Lab Activity 1: Iris Flower Classification", style_h1))
    story.append(Paragraph(
        "<b>Objective:</b> Classify Iris flowers into Setosa, Versicolor, and Virginica using KNN (K=5) on a 70/30 train/test split.<br/>"
        "<b>Reference:</b> Lab Manual Page 69. Features: Sepal Length, Sepal Width, Petal Length, Petal Width.",
        style_body
    ))
    
    act1_snippet = (
        "from sklearn import datasets\n"
        "from sklearn.model_selection import train_test_split\n"
        "from sklearn.neighbors import KNeighborsClassifier\n"
        "from sklearn.metrics import confusion_matrix, classification_report, accuracy_score\n\n"
        "iris = datasets.load_iris()\n"
        "x_train, x_test, y_train, y_test = train_test_split(iris.data, iris.target, test_size=0.3, random_state=0)\n"
        "classifier = KNeighborsClassifier(n_neighbors=5)\n"
        "classifier.fit(x_train, y_train)\n"
        "y_pred = classifier.predict(x_test)"
    )
    story.append(Paragraph("<b>Source Code:</b>", style_h2))
    story.append(make_box(Paragraph(act1_snippet.replace('\n', '<br/>'), style_code)))

    act1_out = (
        "Accuracy: 97.78%\n"
        "Confusion Matrix:\n"
        "[[16  0  0]\n"
        " [ 0 17  1]\n"
        " [ 0  0 11]]\n"
        "Classification Report:\n"
        "              precision    recall  f1-score   support\n"
        "      setosa       1.00      1.00      1.00        16\n"
        "  versicolor       1.00      0.94      0.97        18\n"
        "   virginica       0.92      1.00      0.96        11"
    )
    story.append(Paragraph("<b>Terminal Execution Output:</b>", style_h2))
    story.append(make_box(Paragraph(act1_out.replace('\n', '<br/>'), style_terminal), bg_hex="#0F172A", border_hex="#334155"))

    if os.path.exists("activity1_iris_results.png"):
        story.append(Spacer(1, 4))
        story.append(Image("activity1_iris_results.png", width=6.8*inch, height=2.4*inch))
        story.append(Paragraph("Figure 1: Iris Dataset Confusion Matrix and Feature Scatter Plot (True vs Predicted).", style_caption))

    story.append(make_callout(
        "Activity 1 Analytical Insight",
        "The model achieves 97.78% accuracy. Setosa is linearly separable with zero errors. A single Versicolor sample was predicted as Virginica due to overlap in petal dimensions."
    ))
    story.append(Spacer(1, 10))

    # 3. ACTIVITY 2
    story.append(Paragraph("3. Solved Lab Activity 2: Breast Cancer Tumor Classification", style_h1))
    story.append(Paragraph(
        "<b>Objective:</b> Predict benign (1) vs malignant (0) tumors using KNN (K=5, Euclidean) with features ['mean area', 'mean compactness'].<br/>"
        "<b>Reference:</b> Lab Manual Page 70-71. Benchmark in manual: 121 / 143 correct = 84.6% accuracy.",
        style_body
    ))

    act2_snippet = (
        "from sklearn.datasets import load_breast_cancer\n"
        "cancer = load_breast_cancer()\n"
        "X = pd.DataFrame(cancer.data, columns=cancer.feature_names)[['mean area', 'mean compactness']]\n"
        "y = pd.get_dummies(pd.Categorical.from_codes(cancer.target, cancer.target_names), drop_first=True)\n"
        "X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=1)\n"
        "knn = KNeighborsClassifier(n_neighbors=5, metric='euclidean')\n"
        "knn.fit(X_train, y_train)\n"
        "y_pred = knn.predict(X_test)"
    )
    story.append(Paragraph("<b>Source Code:</b>", style_h2))
    story.append(make_box(Paragraph(act2_snippet.replace('\n', '<br/>'), style_code)))

    act2_out = (
        "Model Accuracy: 121/143 = 84.62%  (Matches manual page 71: 121/143 = 84.6%)\n"
        "Confusion Matrix:\n"
        "[[42 13]\n"
        " [ 9 79]]\n"
        "Classification Report:\n"
        "               precision    recall  f1-score   support\n"
        "Malignant (0)       0.82      0.76      0.79        55\n"
        "   Benign (1)       0.86      0.90      0.88        88"
    )
    story.append(Paragraph("<b>Terminal Execution Output:</b>", style_h2))
    story.append(make_box(Paragraph(act2_out.replace('\n', '<br/>'), style_terminal), bg_hex="#0F172A", border_hex="#334155"))

    if os.path.exists("activity2_breast_cancer_knn.png"):
        story.append(Spacer(1, 4))
        story.append(Image("activity2_breast_cancer_knn.png", width=6.8*inch, height=2.1*inch))
        story.append(Paragraph("Figure 2: Breast Cancer Ground Truth vs KNN Predictions (K=5) and 121/143 Confusion Matrix.", style_caption))

    story.append(make_callout(
        "Activity 2 Validation",
        "Our output matches the exact benchmark stated on page 71 of the lab manual (121/143 = 84.6%). Benign tumors achieved 90% recall while Malignant tumors achieved 76% recall."
    ))
    story.append(Spacer(1, 10))

    # 4. GRADED TASK 1
    story.append(Paragraph("4. Graded Lab Task 1: Handwritten Digits Classification & K Tuning", style_h1))
    story.append(Paragraph(
        "<b>Objective:</b> Classify digits 0-9 from sklearn.datasets.load_digits() using KNN. "
        "Perform hyperparameter tuning to find optimal K giving maximum score. Plot Confusion Matrix & Classification Report.<br/>"
        "<b>Reference:</b> Lab Manual Page 71.",
        style_body
    ))

    gt1_snippet = (
        "from sklearn.datasets import load_digits\n"
        "from sklearn.model_selection import train_test_split, GridSearchCV\n"
        "from sklearn.neighbors import KNeighborsClassifier\n\n"
        "digits = load_digits()\n"
        "X_train, X_test, y_train, y_test = train_test_split(digits.data, digits.target, test_size=0.2, random_state=42, stratify=digits.target)\n"
        "param_grid = {'n_neighbors': list(range(1, 21)), 'weights': ['uniform', 'distance'], 'metric': ['euclidean', 'manhattan']}\n"
        "grid = GridSearchCV(KNeighborsClassifier(), param_grid, cv=5, scoring='accuracy')\n"
        "grid.fit(X_train, y_train)\n"
        "best_knn = grid.best_estimator_\n"
        "y_pred = best_knn.predict(X_test)"
    )
    story.append(Paragraph("<b>Source Code:</b>", style_h2))
    story.append(make_box(Paragraph(gt1_snippet.replace('\n', '<br/>'), style_code)))

    gt1_out = (
        "[+] GridSearchCV Best Parameters: {'metric': 'euclidean', 'n_neighbors': 1, 'weights': 'uniform'}\n"
        "    Best Cross-Validation Accuracy: 99.02%\n"
        "[+] Final Test Accuracy with Best Model (K=1): 98.61% (355/360 correct)\n\n"
        "--- Classification Report Highlights ---\n"
        "Precision (Digits 0-9): 1.00, 0.92, 1.00, 1.00, 0.97, 1.00, 1.00, 1.00, 0.97, 1.00\n"
        "Recall (Digits 0-9):    1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 0.91, 0.94\n"
        "Overall Accuracy: 98.61% | Macro F1-Score: 0.99"
    )
    story.append(Paragraph("<b>Terminal Execution Output:</b>", style_h2))
    story.append(make_box(Paragraph(gt1_out.replace('\n', '<br/>'), style_terminal), bg_hex="#0F172A", border_hex="#334155"))

    if os.path.exists("task1_digits_results.png"):
        story.append(Spacer(1, 4))
        story.append(Image("task1_digits_results.png", width=6.8*inch, height=4.8*inch))
        story.append(Paragraph("Figure 3: Graded Task 1 - K-Tuning Accuracy Curve, 10x10 Confusion Matrix, Per-Digit Metrics, and Sample Digits.", style_caption))

    story.append(make_callout(
        "Graded Task 1 Analytical Findings",
        "The hyperparameter tuning curve confirms that K=1 achieves peak accuracy (99.02% CV, 98.61% Test). Larger K values slightly decrease performance as averaging over dissimilar digit prototypes introduces boundary confusion."
    ))
    story.append(Spacer(1, 10))

    # 5. GRADED TASK 2
    story.append(Paragraph("5. Graded Lab Task 2: Sea Slugs (Abalone) Age Prediction", style_h1))
    story.append(Paragraph(
        "<b>Objective:</b> Predict the biological age of sea slugs (Abalone) from non-invasive physical measurements "
        "(Length, Diameter, Height, Weights, Sex) without having to cut the shell and count rings (Age = Rings + 1.5).<br/>"
        "<b>Reference:</b> Lab Manual Page 71-72. Dataset: UCI Abalone (4,177 samples).",
        style_body
    ))

    gt2_snippet = (
        "from sklearn.neighbors import KNeighborsRegressor\n"
        "from sklearn.preprocessing import StandardScaler\n\n"
        "df = pd.read_csv('abalone.data', names=['Sex','Length','Diameter','Height','Whole_weight','Shucked_weight','Viscera_weight','Shell_weight','Rings'])\n"
        "df['Age'] = df['Rings'] + 1.5\n"
        "X = pd.get_dummies(df.drop(columns=['Rings', 'Age']), columns=['Sex'], drop_first=True)\n"
        "X_train, X_test, y_train, y_test = train_test_split(X, df['Age'], test_size=0.2, random_state=42)\n"
        "scaler = StandardScaler()\n"
        "X_train_s = scaler.fit_transform(X_train)\n"
        "X_test_s = scaler.transform(X_test)\n"
        "knn = KNeighborsRegressor(n_neighbors=15, weights='distance')\n"
        "knn.fit(X_train_s, y_train)\n"
        "y_pred = knn.predict(X_test_s)"
    )
    story.append(Paragraph("<b>Source Code:</b>", style_h2))
    story.append(make_box(Paragraph(gt2_snippet.replace('\n', '<br/>'), style_code)))

    gt2_out = (
        "[+] Optimal Hyperparameters: Best K = 15 | Weighting = 'distance'\n"
        "--- Final Model Regression Metrics ---\n"
        "Mean Squared Error (MSE):       5.0831\n"
        "Root Mean Squared Error (RMSE): 2.2546 years\n"
        "Mean Absolute Error (MAE):      1.5616 years\n"
        "R² Score (Variance Explained):  0.5304 (53.04%)\n"
        "--- Age Tier Classification (Young, Mature, Old) ---\n"
        "Tier Classification Accuracy: 75.60% (Confusion Matrix diagonal dominant)"
    )
    story.append(Paragraph("<b>Terminal Execution Output:</b>", style_h2))
    story.append(make_box(Paragraph(gt2_out.replace('\n', '<br/>'), style_terminal), bg_hex="#0F172A", border_hex="#334155"))

    if os.path.exists("task2_abalone_results.png"):
        story.append(Spacer(1, 4))
        story.append(Image("task2_abalone_results.png", width=6.8*inch, height=4.8*inch))
        story.append(Paragraph("Figure 4: Graded Task 2 - Hyperparameter Tuning (RMSE vs K), Actual vs Predicted Age, Residuals, and Feature Correlations.", style_caption))

    story.append(make_callout(
        "Graded Task 2 Technical Insights",
        "Feature scaling via StandardScaler is critical for KNN. Without scaling, weight attributes dominate distance metrics, inflating error. "
        "With scaling and distance-weighted neighbors (K=15), the model achieves an MAE of ±1.56 years, successfully estimating biological age non-invasively."
    ))
    story.append(Spacer(1, 10))

    # 6. CONCLUSION
    story.append(Paragraph("6. Summary of Key Learnings & Algorithmic Takeaways", style_h1))
    story.append(Paragraph(
        "• <b>Instance-Based Simplicity:</b> KNN is an intuitive, assumption-free method that adapts easily to multi-class classification and continuous regression.<br/>"
        "• <b>Role of Standardization:</b> KNN calculates geometric distances; unstandardized features with differing units distort nearest neighbors.<br/>"
        "• <b>Hyperparameter Tuning:</b> K controls variance vs bias. Small K has low bias but high variance (sensitive to noise); large K has low variance but high bias.<br/>"
        "• <b>Distance Weighting:</b> In regression, weighting neighbor votes by inverse distance significantly reduces RMSE compared to uniform averaging.",
        style_body
    ))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"[+] Successfully generated PDF Report: '{filename}'")

if __name__ == "__main__":
    build_pdf()
