from __future__ import annotations

from dataclasses import dataclass
from typing import Any


APP_TITLE = "FinAccess 2024 Capstone Portfolio"
APP_SUBTITLE = "Predicting Financial Access Profiles in Kenya Using FinAccess 2024"
OWNER_NAME = "Jesse Mutiga"
OWNER_TITLE = "PRINCE2 Agile Project Manager and Business Analyst"

CONTACT = {
    "phone": "+254-720-176-766",
    "email": "jessemutiga2003@live.com",
}

PROFESSIONAL_SUMMARY = (
    "Certified PRINCE2 Agile Practitioner Project Manager and Business Analyst with over 6 years of "
    "experience eliciting, analyzing, and documenting business requirements to deliver technical solutions "
    "aligned with business objectives. Skilled in bridging the gap between business users and IT teams, "
    "developing test plans and training materials, and supporting end users through implementation. "
    "Proven ability to deliver scalable, user-centric solutions in fast-paced Agile environments across "
    "banking, insurance, and digital channels."
)

HOME_INTRO = (
    "Jesse Mutiga is a working professional in project delivery and business analysis who is also completing a "
    "Master’s in Data Science. This portfolio app was designed to present that combined profile clearly, with a "
    "capstone project that connects structured delivery, analytics, and real-world financial services context."
)

ACADEMIC_BACKGROUND = [
    "Master’s in Data Science, Eastern University",
    "Bachelor’s in Economics and Statistics, Kenyatta University",
    "Diploma in Information Technology, KCA University",
]

CAREER_ASPIRATIONS = [
    "Continue building at the intersection of project delivery, business analysis, and applied data science.",
    "Use analytics and machine learning to support practical decision-making in financial services and digital transformation.",
    "Lead delivery of user-centric, well-governed solutions that connect business goals with strong technical execution.",
]

PROFESSIONAL_INTERESTS = [
    "Financial services transformation and digital banking",
    "Applied machine learning for practical business problems",
    "Financial inclusion and data-informed product strategy",
    "AML, compliance, and risk-focused delivery programs",
    "Bridging business stakeholders and technical teams in Agile environments",
]

CORE_SKILLS = [
    "Project Management (PRINCE2 Agile)",
    "Requirements Elicitation, Prioritization, and Documentation",
    "Business Process Analysis and Optimization",
    "Bridging Business and Technical Stakeholders",
    "Mobile and Digital Banking Solutions",
    "Cloud Platforms (Azure)",
    "Agile and Scrum Environments",
    "UAT Planning, Execution, and Defect Management",
    "Requirements Traceability and Change Control",
    "End User Support and Training Materials Development",
]

WORK_HISTORY = [
    {
        "organization": "NCBA",
        "role": "Business Analyst & Project Manager",
        "period": "",
        "start": "2022-11-01",
        "end": None,
        "highlights": [
            "Delivered a 5-phase enterprise AML Program across Kenya, Uganda, Rwanda, and Tanzania, now in production with over 80 strategic changes implemented.",
            "Played a key role in the AIG Insurance merger with NCBA, leading AML solution design for insurance products and redefining customer onboarding journeys.",
            "Translated AML policy requirements into technical specifications and facilitated communication between business stakeholders and IT teams.",
            "Developed BRDs, functional specifications, and user stories for AML modules such as real-time PEP screening, GoAML reporting, and customer risk classification.",
            "Prepared UAT plans and scripts, executed test cases, logged defects, and supported issue resolution before go-live.",
            "Coordinated cross-functional delivery teams and chaired regional stakeholder workshops.",
            "Created user guides and training decks for branch operations and compliance officers.",
            "Prepared C-level dashboards and program status reports.",
            "Spearheaded Agile transformation within compliance delivery projects.",
        ],
    },
    {
        "organization": "Stanbic Bank",
        "role": "Business Analyst",
        "period": "",
        "start": "2020-10-01",
        "end": "2022-09-30",
        "highlights": [
            "Worked on digital channels such as the Chama App and enterprise data solutions like Azure Data Warehouse and Amazon Data Lake.",
            "Extracted requirements through interviews, workshops, and use cases.",
            "Led data-centric initiatives including a master data management platform for unified access to over 40 application databases.",
            "Spearheaded data quality initiatives.",
            "Contributed to UAT planning and execution.",
            "Managed minor changes through structured change control.",
            "Facilitated brainstorming sessions with SMEs.",
            "Chaired daily and weekly stakeholder meetings.",
        ],
    },
    {
        "organization": "Tezza Business Solutions",
        "role": "Junior Business Analyst and Junior Data Scientist",
        "period": "",
        "start": "2018-02-01",
        "end": "2020-10-31",
        "highlights": [
            "Directed development of a resource capacity planning tool.",
            "Engineered a proof-of-concept NLP solution to detect negative sentiment in customer feedback.",
        ],
    },
    {
        "organization": "Tezza Business Solutions",
        "role": "Change Management Intern",
        "period": "",
        "start": "2015-08-01",
        "end": "2017-07-31",
        "highlights": [
            "Conducted ERP gap analysis at Kenya Public Service Commission.",
        ],
    },
]

EDUCATION = [
    "Master’s in Data Science, Eastern University",
    "Bachelor’s in Economics and Statistics, Kenyatta University",
    "Diploma in Information Technology, KCA University",
]

CERTIFICATIONS = [
    "PRINCE2 Agile Foundation Certificate in Agile Project Management",
    "Agile Foundations",
    "Microsoft Copilot AI: Crafting Effective Prompts for Microsoft 365",
    "Data Science Certificate from Strathmore University",
    "ITIL 4 Foundation",
    "Datagear AML",
]

ACCOMPLISHMENTS = [
    "Delivered NCBA’s group-wide AML transformation program across 4 countries with 80+ AML controls.",
    "Consolidated AML operations into a centralized DG AML platform.",
    "Resolved 100% of AML audit findings on time.",
    "Delivered over 80 group-wide and country initiatives.",
    "Implemented bulk PesaLink transactions.",
    "Spearheaded a $1M bank-wide data repository project on Azure.",
    "Achieved major efficiency improvements through automation of KYC data retrieval, card PIN issuance, onboarding, and regulatory reporting ETL processes.",
]

PROJECT_CARDS = [
    {
        "title": "FinAccess 2024 Capstone",
        "tag": "Applied Data Science Capstone",
        "summary": "A machine learning portfolio project that predicts an adult respondent’s current financial access profile in Kenya using interpretable survey features from FinAccess 2024.",
        "status": "Featured project",
    },
    {
        "title": "AML Transformation Program",
        "tag": "Program Delivery / Business Analysis",
        "summary": "Enterprise AML transformation work delivered across multiple countries, covering policy translation, solution design, UAT, stakeholder coordination, and production rollout.",
        "status": "Professional delivery work",
    },
    {
        "title": "Chama App / Digital Banking Work",
        "tag": "Digital Channels",
        "summary": "Business analysis support for digital banking experiences, channel requirements, use cases, and stakeholder-driven product improvement work.",
        "status": "Portfolio summary",
    },
    {
        "title": "Azure / Data Platform Initiatives",
        "tag": "Data & Cloud",
        "summary": "Data platform and repository initiatives focused on quality, accessibility, and enterprise use across financial services environments.",
        "status": "Portfolio summary",
    },
]

CAPSTONE_OVERVIEW = {
    "title": "Predicting Financial Access Profiles in Kenya Using FinAccess 2024",
    "problem": (
        "The project asks a practical question: based on a small set of demographic, household, and digital-access factors, "
        "can we predict whether an adult in Kenya is currently excluded from formal financial rails, uses mobile money only, or is banked?"
    ),
    "why_it_matters": (
        "Financial access is tied to day-to-day resilience, payments, savings, and participation in the broader economy. "
        "Using Kenya’s FinAccess 2024 survey makes the project relevant to a real national context rather than a toy dataset."
    ),
    "target_classes": ["Excluded", "Mobile money only", "Banked"],
    "modeling_approach": [
        "Use the FinAccess 2024 public survey for Kenya.",
        "Focus the main analysis on adults aged 18 and above.",
        "Limit the model to a small set of interpretable predictors rather than the full survey file.",
        "Avoid leakage by excluding target-defining fields such as current mobile money use and current bank use from the predictors.",
        "Handle known nonresponse codes like 98 and 99 as missing values before preprocessing.",
        "Impute numeric features with the median and categorical features with the most frequent value in the preprocessing pipeline.",
        "Compare several beginner-friendly models and retain a tuned Gradient Boosting model as the strongest current option.",
    ],
    "results_summary": [
        "Current strongest model: tuned Gradient Boosting.",
        "Current reported macro F1: 0.5939.",
        "Current reported balanced accuracy: 0.5658.",
        "Evaluation emphasis includes macro F1, balanced accuracy, class-level recall, confusion matrix review, subgroup summaries, and permutation importance.",
    ],
    "limitations": [
        "This project predicts current financial access profile, not future wealth, default risk, or long-term outcomes.",
        "The Banked class may include some dual users who also use mobile money.",
        "The results are predictive rather than causal, so they should not be interpreted as proof that a feature causes an outcome.",
        "This is an educational capstone tool and should not be used as a production decision-making system.",
    ],
}

CAPSTONE_METRICS = {
    "dataset_responses": "20,871 survey responses",
    "dataset_fields": "3,816 fields",
    "main_sample": "Adults 18+",
    "cleaned_rows": "20,862 cleaned rows",
    "adult_rows": "19,741 adult rows",
    "best_model": "Tuned Gradient Boosting",
    "macro_f1": 0.5939,
    "balanced_accuracy": 0.5658,
}

DEFAULT_MODEL_COMPARISON_ROWS = [
    {
        "Model": "Multinomial Logistic Regression",
        "Status": "Compared in notebook",
        "Macro F1": None,
        "Balanced Accuracy": None,
        "Notes": "Baseline linear classifier; connect artifact CSV for exact metrics.",
    },
    {
        "Model": "Class-weighted Logistic Regression",
        "Status": "Compared in notebook",
        "Macro F1": None,
        "Balanced Accuracy": None,
        "Notes": "Used to address class imbalance; exact metrics expected from saved artifacts.",
    },
    {
        "Model": "Random Forest",
        "Status": "Compared in notebook",
        "Macro F1": None,
        "Balanced Accuracy": None,
        "Notes": "Flexible tree baseline; exact metrics expected from saved artifacts.",
    },
    {
        "Model": "Class-weighted Random Forest",
        "Status": "Compared in notebook",
        "Macro F1": None,
        "Balanced Accuracy": None,
        "Notes": "Class-weighted variant; exact metrics expected from saved artifacts.",
    },
    {
        "Model": "Gradient Boosting (tuned)",
        "Status": "Best current model",
        "Macro F1": 0.5939,
        "Balanced Accuracy": 0.5658,
        "Notes": "Current strongest option according to the approved proposal and notebook outputs.",
    },
]

DEFAULT_METADATA: dict[str, Any] = {
    "placeholder_note": (
        "This fallback metadata supports the fresh app in stub mode. For final artifact-backed prediction, replace it with your "
        "saved feature_metadata.json so the app uses the exact training-time category codes."
    ),
    "fields": {
        "county": {
            "label": "County",
            "options": [
                {"label": name, "value": name}
                for name in [
                    "Mombasa", "Kwale", "Kilifi", "Tana River", "Lamu", "Taita Taveta", "Garissa", "Wajir", "Mandera",
                    "Marsabit", "Isiolo", "Meru", "Tharaka-Nithi", "Embu", "Kitui", "Machakos", "Makueni", "Nyandarua",
                    "Nyeri", "Kirinyaga", "Murang'a", "Kiambu", "Turkana", "West Pokot", "Samburu", "Trans Nzoia",
                    "Uasin Gishu", "Elgeyo Marakwet", "Nandi", "Baringo", "Laikipia", "Nakuru", "Narok", "Kajiado",
                    "Kericho", "Bomet", "Kakamega", "Vihiga", "Bungoma", "Busia", "Siaya", "Kisumu", "Homa Bay",
                    "Migori", "Kisii", "Nyamira", "Nairobi",
                ]
            ],
        },
        "sex": {
            "label": "Sex",
            "options": [
                {"label": "Male", "value": 1},
                {"label": "Female", "value": 2},
            ],
        },
        "education": {
            "label": "Education",
            "options": [
                {"label": "None", "value": 1},
                {"label": "Some primary", "value": 2},
                {"label": "Primary completed", "value": 3},
                {"label": "Some secondary", "value": 4},
                {"label": "Secondary completed", "value": 5},
                {"label": "Some technical", "value": 6},
                {"label": "Completed technical", "value": 7},
                {"label": "Some university", "value": 8},
                {"label": "University completed", "value": 9},
                {"label": "Other", "value": 10},
            ],
        },
        "marital_status": {
            "label": "Marital status",
            "options": [
                {"label": "Single / Never married", "value": 1},
                {"label": "Married / Living with partner", "value": 2},
                {"label": "Divorced / Separated", "value": 3},
                {"label": "Widowed", "value": 4},
            ],
        },
        "livelihood": {
            "label": "Livelihood",
            "options": [
                {"label": "Farming / livestock / fishing", "value": 1},
                {"label": "Formal employment", "value": 2},
                {"label": "Casual or seasonal work", "value": 3},
                {"label": "Own business / self-employed", "value": 4},
                {"label": "Support, transfers, or assistance", "value": 5},
                {"label": "Rent, pension, investments, or other income", "value": 6},
            ],
            "is_grouped_placeholder": True,
        },
        "can_access_internet": {
            "label": "Internet access",
            "options": [
                {"label": "No internet access", "value": 0.0},
                {"label": "Can access internet", "value": 1.0},
            ],
        },
        "internet_frequency": {
            "label": "Internet frequency",
            "options": [
                {"label": "Daily", "value": 1},
                {"label": "Weekly", "value": 2},
                {"label": "Monthly", "value": 3},
                {"label": "Less often", "value": 4},
                {"label": "Never", "value": 5},
            ],
        },
        "financial_health": {
            "label": "Financial health",
            "options": [
                {"label": "High", "value": 1},
                {"label": "Medium", "value": 2},
                {"label": "Low", "value": 3},
            ],
        },
    },
}

MODEL_FEATURE_ORDER = [
    "county",
    "sex",
    "age_years",
    "household_size",
    "education",
    "marital_status",
    "children_in_household",
    "livelihood",
    "can_access_internet",
    "internet_frequency",
    "financial_health",
]

CLASS_ORDER = ["Excluded", "Mobile money only", "Banked"]

NUMERIC_BOUNDS = {
    "age_years": {"min": 18, "max": 105, "label": "Age"},
    "household_size": {"min": 1, "max": 20, "label": "Household size"},
    "children_in_household": {"min": 0, "max": 19, "label": "Number of children in household"},
}
