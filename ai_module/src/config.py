from pathlib import Path

MODULE_ROOT = Path(__file__).resolve().parent.parent
SRC_DIR = MODULE_ROOT / "src"
DATASET_DIR = MODULE_ROOT / "dataset"
MODELS_DIR = MODULE_ROOT / "models"
REPORTS_DIR = MODULE_ROOT / "reports"
API_DIR = MODULE_ROOT / "api"
TESTS_DIR = MODULE_ROOT / "tests"
NOTEBOOKS_DIR = MODULE_ROOT / "notebooks"

for directory in [DATASET_DIR, MODELS_DIR, REPORTS_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

DATASET_CSV_PATH = DATASET_DIR / "sms_scam_dataset.csv"
RAW_TSV_PATH = DATASET_DIR / "raw" / "sms_spam_collection.tsv"
PARENT_DATA_TSV = MODULE_ROOT.parent / "data" / "sms_spam_collection.tsv"

LOGISTIC_REGRESSION_MODEL_PATH = MODELS_DIR / "logistic_regression_model.joblib"
NAIVE_BAYES_MODEL_PATH = MODELS_DIR / "naive_bayes_model.joblib"
TFIDF_VECTORIZER_PATH = MODELS_DIR / "tfidf_vectorizer.joblib"
METRICS_SUMMARY_PATH = MODELS_DIR / "metrics_summary.json"

CONFUSION_MATRIX_PATH = REPORTS_DIR / "confusion_matrix.png"
ROC_CURVE_PATH = REPORTS_DIR / "roc_curve.png"
EVALUATION_REPORT_PATH = REPORTS_DIR / "evaluation_report.md"

RANDOM_STATE = 42
TEST_SIZE = 0.20
CV_FOLDS = 5

LABEL_LEGITIMATE = 0
LABEL_SCAM = 1
LABEL_MAP = {
    LABEL_LEGITIMATE: "legitimate",
    LABEL_SCAM: "scam",
}
STRING_TO_LABEL_MAP = {
    "ham": LABEL_LEGITIMATE,
    "legitimate": LABEL_LEGITIMATE,
    "spam": LABEL_SCAM,
    "scam": LABEL_SCAM,
}

TFIDF_NGRAM_RANGE = (1, 2)
TFIDF_MAX_FEATURES = 5000
TFIDF_SUBLINEAR_TF = True
TFIDF_MIN_DF = 2

MIN_MESSAGE_LENGTH = 2
MAX_MESSAGE_LENGTH = 1000

STANDARD_DISCLAIMER = (
    "This is an automated machine learning assessment, not a guarantee that the "
    "message is fraudulent. A legitimate prediction does not prove a message is safe."
)
