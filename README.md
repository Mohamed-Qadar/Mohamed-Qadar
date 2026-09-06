\documentclass[a4paper,10pt]{article}

% =========================================================
% PACKAGES
% =========================================================

\usepackage[T1]{fontenc}
\usepackage[utf8]{inputenc}
\usepackage{lmodern}

\usepackage[
    a4paper,
    left=1.35cm,
    right=1.35cm,
    top=1.10cm,
    bottom=1.10cm
]{geometry}

\usepackage{xcolor}
\usepackage{enumitem}
\usepackage{titlesec}
\usepackage{tabularx}
\usepackage{array}
\usepackage[hidelinks]{hyperref}
\usepackage{fontawesome5}
\usepackage{microtype}

% =========================================================
% GENERAL FORMATTING
% =========================================================

\pagestyle{empty}

\setlength{\parindent}{0pt}
\setlength{\parskip}{0pt}
\setlength{\tabcolsep}{0pt}

\definecolor{darkblue}{RGB}{22,55,92}

\hypersetup{
    colorlinks=true,
    urlcolor=darkblue,
    linkcolor=darkblue
}

\urlstyle{same}

% =========================================================
% SECTION FORMAT
% =========================================================

\titleformat{\section}
{\large\bfseries}
{}
{0pt}
{}
[\vspace{-1mm}\titlerule]

\titlespacing*{\section}
{0pt}
{8pt}
{4pt}

% =========================================================
% CUSTOM COMMANDS
% =========================================================

\newcommand{\cvEntry}[4]{
\begin{tabularx}{\textwidth}{@{}X r@{}}
    \textbf{#1} & \textit{#4} \\
    \textit{#2} & #3
\end{tabularx}
\vspace{0.8mm}
}

\newcommand{\cvProject}[3]{
\begin{tabularx}{\textwidth}{@{}X r@{}}
    \textbf{#1} & #3 \\
    \textit{#2} & 
\end{tabularx}
\vspace{-1mm}
}

\newcommand{\bulletListStart}{
\begin{itemize}[
    leftmargin=4.5mm,
    itemsep=1.1mm,
    topsep=1mm,
    parsep=0pt
]
}

\newcommand{\bulletListEnd}{
\end{itemize}
}

% =========================================================
% DOCUMENT
% =========================================================

\begin{document}

% =========================================================
% HEADER
% =========================================================

\begin{center}

{\LARGE\textbf{Mohamed Ibrahim Abdi}}\\[1.8mm]

{\large\textbf{Computer Engineer | Artificial Intelligence, NLP \& Research}}\\[2.5mm]

\small
\faEnvelope\ \href{mailto:mohamedqadar280@gmail.com}{mohamedqadar280@gmail.com}
\quad | \quad
\faWhatsapp\ +90 553 171 4783
\quad | \quad
\faPhone\ 0611354800
\\[1.5mm]

\faLinkedin\ \href{https://tr.linkedin.com/in/mohamed-ibrahim-abdi-572475232}{LinkedIn}
\quad | \quad
\faGithub\ \href{https://github.com/Mohamed-Qadar}{GitHub}
\quad | \quad
\faGraduationCap\ \href{https://scholar.google.com/citations?user=0yqZjd4AAAAJ&hl=en}{Google Scholar}
\quad | \quad
\faDatabase\ \href{https://www.kaggle.com/mohamedibrahimabdi/datasets}{Kaggle}
\quad | \quad
\faIdCard\ \href{https://orcid.org/0009-0002-7874-8740}{ORCID}

\end{center}

\vspace{-2mm}

% =========================================================
% OBJECTIVE
% =========================================================

\section{OBJECTIVE}

\small
Computer Engineer with an M.Sc. from Fırat University and a B.Sc. from Karadeniz Technical University, with research interests in Natural Language Processing, transformer-based models, low-resource language processing, and Computer Vision. Research experience includes Automatic Question Generation, biomedical NLP, Somali-language text classification, deepfake detection, and autonomous-driving computer vision. Experienced in dataset development, model training, experimental evaluation, and conducting research from problem formulation and methodology development to scientific publication.

% =========================================================
% EDUCATION
% =========================================================

\section{Education}

\cvEntry
{Fırat University}
{M.Sc. in Computer Engineering}
{Elazığ, Türkiye}
{June 2026}

\vspace{0.5mm}
\textbf{Master's Thesis:} Automatic Question Generation from Educational Materials Using a T5-Based Natural Language Processing Approach\\
Research focused on transformer-based automatic question generation, model training and evaluation, and the application of NLP to educational and low-resource language environments.

\vspace{2mm}

\cvEntry
{Karadeniz Technical University}
{B.Sc. in Computer Engineering}
{Trabzon, Türkiye}
{July 2024}

% =========================================================
% UNDERGRADUATE PROJECT
% =========================================================

\subsection*{Undergraduate Project}

\cvProject
{GSM-Based Location Tracking Application}
{GSM Modules \textbar\ Embedded Systems \textbar\ Software Design \textbar\ System Integration}
{}

\bulletListStart
\item Developed a real-time location tracking system as a senior design (capstone) project at Karadeniz Technical University (KTU).
\item Designed and implemented the overall system architecture, integrating GSM hardware with software components.
\item Contributed to system development, testing, and integration throughout the project lifecycle.
\item Took an active role in technical development and project coordination within a student team.
\bulletListEnd

% =========================================================
% RESEARCH EXPERIENCE
% =========================================================

\section{Research Experience}

\cvProject
{TÜBİTAK-Funded Research Project -- Project No. 124E787}
{Lane Marking Estimation on Unmarked Straight Roads for Autonomous Driving}
{2025--2026}

\bulletListStart
\item Contributed to a TÜBİTAK-funded computer-vision research project focused on lane estimation and drivable-area understanding for autonomous-driving applications.
\item Participated in dataset preparation, image annotation, algorithm development, experimental evaluation, and analysis of computer-vision approaches.
\item Worked collaboratively within a four-member research team representing Munzur University, Fırat University, and Yeditepe University.
\item Contributed to research activities leading to journal manuscripts on lane-line estimation and drivable-area segmentation.
\bulletListEnd

\vspace{1mm}
\textbf{Research Team:}

\vspace{0.8mm}
\textbf{Gürkan Doğan}$^1$, \textbf{Mohamed Ibrahim Abdi}$^2$, \textbf{Berkin Yılmaz}$^3$, \textbf{Burhan Ergen}$^4$

\vspace{1mm}
{\footnotesize
$^1$ Computer Engineering Department, Engineering Faculty, Munzur University, Tunceli, Türkiye\\
$^{2,4}$ Computer Engineering Department, Engineering Faculty, Fırat University, Elazığ, Türkiye\\
$^3$ Computer Engineering Department, Engineering Faculty, Yeditepe University, Istanbul, Türkiye
}

\vspace{1mm}
{\footnotesize
\textbf{Research Team Contacts:}\\
\href{mailto:gurkandogan@munzur.edu.tr}{gurkandogan@munzur.edu.tr} \quad | \quad \href{mailto:berkinyilmaz6223@gmail.com}{berkinyilmaz6223@gmail.com} \quad | \quad \href{mailto:bergen@firat.edu.tr}{bergen@firat.edu.tr}
}

% =========================================================
% PROFESSIONAL EXPERIENCE
% =========================================================

\section{Professional Experience}

\cvEntry
{Elasoft}
{Software Developer Intern}
{Trabzon, Türkiye}
{Jan 2024 -- May 2024}

\bulletListStart
\item Developed backend functionality for a real-estate management platform using \textbf{C\#, ASP.NET Core 8, Dapper, and Microsoft SQL Server}.
\item Worked on a three-interface application consisting of administrator, real-estate agent, and end-user components connected through RESTful APIs.
\item Integrated \textbf{SignalR} to support real-time messaging between platform users.
\item Contributed to frontend development using HTML, CSS, JavaScript, and Bootstrap, while working primarily on backend implementation.
\bulletListEnd

\vspace{1mm}

\cvEntry
{Online Programming Instructor}
{Volunteer}
{Remote}
{Dec 2024 -- May 2025}

\bulletListStart
\item Delivered introductory Python programming and applied data-science sessions for beginner learners.
\item Taught supervised machine-learning concepts including k-NN, SVM, logistic regression, decision trees, random forests, and Naive Bayes.
\item Introduced artificial neural networks, activation functions, classification methods, and practical machine-learning workflows.
\item Prepared hands-on exercises and mini-projects to support practical understanding of programming and data analysis.
\bulletListEnd

% =========================================================
% RELEVANT BSC COURSEWORK
% =========================================================

\section{Relevant B.Sc. Coursework -- Computer Engineering}

\small
\begin{itemize}[leftmargin=4.5mm, itemsep=1.2mm, topsep=1mm]
\item \textbf{Computer Science \& Programming:} Data Structures, Algorithms, Object-Oriented Programming, Programming Languages, Automata Theory, Discrete Mathematics
\item \textbf{Computer Systems \& Hardware:} Computer Architecture, Microprocessors, Digital Design, Digital Design Laboratory, Electric Circuits, Electronic Circuits, Electronic Laboratory, Computer Organization Laboratory, Hardware Description Languages
\item \textbf{Software, Databases \& Networks:} Operating Systems, Database Management, Computer Networks, Computer Networks Laboratory, System Programming, Computer Network Programming, Web Programming, Windows Programming, Parallel Computers
\item \textbf{Data, Mathematics \& Signal Foundations:} Probability and Statistics, Engineering Mathematics, Differential Equations, Numerical Analysis, Signals and Systems, Data Mining
\item \textbf{Applied Computer Engineering:} Computer Graphics, Medical Imaging Systems, Robot Technologies, Engineering Design
\item \textbf{Data Protection:} Protection of Personal Data
\end{itemize}

% =========================================================
% NLP & COMPUTER VISION PROJECTS
% =========================================================

\section{NLP \& Computer Vision Projects}

\cvProject
{Somali News Classification Dataset (SNCD)}
{Low-Resource NLP \textbar\ Dataset Development \textbar\ Text Classification}
{\href{https://github.com/Mohamed-Qadar/Somali-News-Classification-Dataset}{GitHub}}

\bulletListStart
\item Created a balanced Somali-language dataset containing \textbf{21,020 news headlines} across four equally represented categories: Politics, World, Sports, and Economy.
\item Collected and structured data from multiple Somali news and institutional sources, including text, class labels, source information, and article references.
\item Designed the dataset to support reproducible machine-learning and NLP research for an under-resourced language.
\item Used the dataset in Somali-language text-classification research comparing classical machine-learning approaches.
\bulletListEnd

\vspace{1mm}

\cvProject
{Biomedical Question Generation with Transformer Models}
{FLAN-T5 \textbar\ Generative NLP \textbar\ Low-Resource Biomedical QA}
{\href{https://github.com/Mohamed-Qadar}{GitHub}}

\bulletListStart
\item Investigated instruction-tuned transformer models for generative biomedical question answering in low-resource settings.
\item Performed data preprocessing, model experimentation, question generation, and evaluation of biomedical QA outputs.
\item Presented related research at the \textit{International Informatics Congress 2026}.
\bulletListEnd

\vspace{1mm}

\cvProject
{Deepfake Video Detection}
{ResNeXt50 \textbar\ LSTM \textbar\ Deep Learning \textbar\ Video Analysis}
{\href{https://github.com/Mohamed-Qadar}{GitHub}}

\bulletListStart
\item Developed and investigated a hybrid deep-learning approach combining \textbf{ResNeXt50} for spatial feature extraction with \textbf{LSTM} for temporal modelling of video sequences.
\item Applied the architecture to deepfake-video detection and contributed to the corresponding peer-reviewed publication.
\bulletListEnd

\vspace{1mm}

\cvProject
{Somali-Language Text Summarization}
{Natural Language Processing \textbar\ Extractive \& Abstractive Summarization}
{\href{https://github.com/Mohamed-Qadar}{GitHub}}

\bulletListStart
\item Designed and evaluated extractive and abstractive methods for automatic summarization of Somali-language text.
\item Explored NLP methods for a language with limited labelled datasets and computational resources.
\bulletListEnd

\vspace{1mm}

\cvProject
{Text Extraction from Images Using Hybrid Deep Learning}
{Computer Vision \textbar\ OCR \textbar\ CNN}
{\href{https://github.com/Mohamed-Qadar}{GitHub}}

\bulletListStart
\item Investigated a hybrid approach combining convolutional neural networks and OCR-based components for extracting text from complex visual scenes.
\bulletListEnd

\vspace{1mm}

\cvProject
{Human Bone Fracture Classification (HBFMID)}
{Medical Imaging \textbar\ CNN \textbar\ Deep Learning}
{\href{https://github.com/Mohamed-Qadar}{GitHub}}

\bulletListStart
\item Developed a CNN-based image-classification workflow for identifying different fracture categories using the Human Bone Fractures Multi-modal Image Dataset.
\bulletListEnd

% =========================================================
% PUBLICATIONS & RESEARCH MANUSCRIPTS
% =========================================================

\section{Publications \& Research Manuscripts}

\small

\textbf{Peer-Reviewed Journal Articles}
\begin{enumerate}[leftmargin=5mm, itemsep=1.5mm, topsep=1mm]
\item \textbf{Mohamad Ibrahim}, Burhan Ergen. ``Facial Expression Based Emotion Recognition.'' \textit{Journal of Electrical Engineering and Computer (JEECOM)}, 2025.\\
\href{https://doi.org/10.33650/jeecom.v7i1.11069}{doi:10.33650/jeecom.v7i1.11069}
\item Nurcan Yardımcı, \textbf{Mohamed Ibrahim Abdi}, Burhan Ergen. ``Hibrit ResNeXt ve LSTM Mimarisi Kullanılarak Deepfake Video Algılama.'' \textit{Politeknik Dergisi}, 2025.\\
\href{https://doi.org/10.2339/politeknik.1721371}{doi:10.2339/politeknik.1721371}
\end{enumerate}

\textbf{Conference Papers}
\begin{enumerate}[leftmargin=5mm, itemsep=1.5mm, topsep=1mm]
\item \textbf{Abdi, M. I.}, Ergen, B. ``Classification of Somali News Headlines Using Classical Machine Learning.'' \textit{9th International Mediterranean Scientific Research Congress}, Adana, Türkiye, 29--30 April 2026. \textit{[Full-text/proceedings link]}
\item \textbf{Abdi, M. I.}, Ergen, B. ``Instruction-Tuned FLAN-T5 for Generative Biomedical QA in Low-Resource Settings.'' \textit{International Informatics Congress 2026}, Batman, Türkiye, 29 April--1 May 2026. \textit{[Proceedings link]}
\end{enumerate}

\textbf{Manuscripts Under Review}
\begin{itemize}[leftmargin=5mm, itemsep=1.2mm, topsep=1mm]
\item \textbf{Abdi, M. I.}, Ergen, B. ``Multilingual Transformer Models for Medical Question Generation in Low-Resource Turkish Clinical Texts.'' \textit{Balkan Journal of Electrical and Computer Engineering}.
\item Doğan, G., \textbf{Abdi, M. I.}, Yılmaz, B., Ergen, B. ``A New Convolutional Neural Network-Based Approach for Lane Line Estimation Leveraging Selective Kernel-Based Cross Feature Fusion.'' \textit{Engineering Applications of Artificial Intelligence}.
\item Doğan, G., \textbf{Abdi, M. I.}, Yılmaz, B., Ergen, B. ``A New Lightweight Network for Drivable Area Segmentation and Heuristic Lane Boundary Estimation on Unmarked Roads.'' \textit{Neurocomputing}.
\item \textbf{Abdi, M. I.}, Yardımcı, N., Ergen, B. ``Hybrid BERT-LSTM Model for Turkish Fake News Detection.'' \textit{Gazi University Journal of Science}.
\end{itemize}

% =========================================================
% TECHNICAL & RESEARCH SKILLS
% =========================================================

\section{Technical \& Research Skills}

\small
\begin{tabularx}{\textwidth}{@{}>{\bfseries}p{4cm} X@{}}
Programming & Python, C\#, C, C++, JavaScript, TypeScript \\[1.3mm]
AI / Machine Learning & Natural Language Processing, Transformer Models, Deep Learning, Computer Vision, Text Classification, Question Generation, Sequence Modelling \\[1.3mm]
AI Frameworks \& Libraries & Hugging Face Transformers, Scikit-learn, TensorFlow, Keras, NumPy, Pandas, Matplotlib \\[1.3mm]
Model Evaluation & BLEU, ROUGE, METEOR, BERTScore, classification metrics, experimental comparison \\[1.3mm]
Backend \& APIs & ASP.NET Core, Django, Node.js, REST APIs, SignalR, Dapper \\[1.3mm]
Databases & Microsoft SQL Server, PostgreSQL, relational database modelling, SQL \\[1.3mm]
Computer Engineering & Computer Architecture, Microprocessors, Digital Systems, Embedded Systems, Computer Networks, Parallel Computing, Signals and Systems \\[1.3mm]
Research & Dataset preparation, data annotation, model training, model evaluation, literature review, experiment design, academic writing, reproducible research \\[1.3mm]
Development Tools & Git, GitHub, Docker, Docker Compose, Jupyter/Colab, Visual Studio, VS Code, Postman, LaTeX, Overleaf \\
\end{tabularx}

% =========================================================
% LANGUAGES
% =========================================================

\section{Languages}

\small
\textbf{Somali:} Native
\quad | \quad
\textbf{English:} Excellent
\quad | \quad
\textbf{Turkish:} Excellent
\quad | \quad
\textbf{Arabic:} Good

% =========================================================
% REFERENCES
% =========================================================

\section{References}

\small
\begin{enumerate}[leftmargin=5mm, itemsep=2.5mm, topsep=1.5mm]
\item \textbf{Prof. Dr. Abdullahi Abdi Omar}\\
Lecturer, Somali National University\\
Email: \href{mailto:qadhyan@gmail.com}{qadhyan@gmail.com} \quad | \quad Phone: +2525615589934\\
\textit{Relationship: Academic Mentor}

\item \textbf{Prof. Dr. Burhan Ergen}\\
Director, Institute of Natural and Applied Sciences, Fırat University\\
Email: \href{mailto:bergen@firat.edu.tr}{bergen@firat.edu.tr} \quad | \quad Phone: 0(424)-237 00 00 (6316)\\
\textit{Relationship: M.Sc. Supervisor and Research Collaborator}

\item \textbf{Eng. Abdullahi Ibrahim Abdi}\\
Chief Technical Officer, Blue Sky Energy, Somalia; Lecturer, Somali National University\\
Email: \href{mailto:hilaac115@gmail.com}{hilaac115@gmail.com} \quad | \quad Phone: +27630293263\\
\textit{Relationship: Collaborator for Software Development Projects}

\item \textbf{Prof. Dr. Bekir Dizdaroğlu}\\
Vice Chair, Department of Computer Engineering, Karadeniz Technical University\\
Email: \href{mailto:bekir@ktu.edu.tr}{bekir@ktu.edu.tr} \quad | \quad Phone: +90 462 377 3167\\
\textit{Relationship: B.Sc. Supervisor}

\item \textbf{Prof. Dr. Cemal Köse}\\
Lecturer, Karadeniz Technical University\\
Email: \href{mailto:ckose@ktu.edu.tr}{ckose@ktu.edu.tr} \quad | \quad Phone: +904623773167\\
\textit{Relationship: Collaborator for Network and Internet Project}

\item \textbf{Dr. Gürkan Doğan}\\
Department of Computer Engineering, Faculty of Engineering, Munzur University, Tunceli, Türkiye\\
Email: \href{mailto:gurkandogan@munzur.edu.tr}{gurkandogan@munzur.edu.tr}\\
\textit{Relationship: Research Collaborator, TÜBİTAK Project No. 124E787}
\end{enumerate}

\end{document}
