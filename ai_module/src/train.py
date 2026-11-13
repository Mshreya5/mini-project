import json
import logging
from pathlib import Path
from typing import Dict, Tuple

import joblib
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_curve
from sklearn.model_selection import StratifiedKFold, cross_validate, train_test_split
from sklearn.naive_bayes import MultinomialNB

from ai_module.src.config import (
    CONFUSION_MATRIX_PATH,
    CV_FOLDS,
    EVALUATION_REPORT_PATH,
    LOGISTIC_REGRESSION_MODEL_PATH,
    METRICS_SUMMARY_PATH,
    MODELS_DIR,
    NAIVE_BAYES_MODEL_PATH,
    RANDOM_STATE,
    REPORTS_DIR,
    ROC_CURVE_PATH,
    TEST_SIZE,
    TFIDF_VECTORIZER_PATH,
)
from ai_module.src.data_loader import load_prepared_dataset
from ai_module.src.evaluate import (
    compute_classification_metrics,
    generate_markdown_report,
    plot_confusion_matrices,
    plot_roc_curves,
)
from ai_module.src.preprocessing import create_tfidf_vectorizer

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)


def split_data(
    df: pd.DataFrame,
) -> Tuple[pd.Series, pd.Series, pd.Series, pd.Series]:
    X = df["message"]
    y = df["label"]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=TEST_SIZE,
        stratify=y,
        random_state=RANDOM_STATE,
    )
    logger.info(
        f"Stratified split completed: {len(X_train)} train samples, {len(X_test)} test samples."
    )
    return X_train, X_test, y_train, y_test


def run_training_pipeline() -> Dict[str, object]:
    logger.info("Loading prepared scam message dataset...")
    df = load_prepared_dataset()

    X_train, X_test, y_train, y_test = split_data(df)

    logger.info("Fitting TF-IDF Vectorizer strictly on the training partition...")
    vectorizer = create_tfidf_vectorizer()
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)

    TFIDF_VECTORIZER_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(vectorizer, TFIDF_VECTORIZER_PATH)
    logger.info(f"Fitted TF-IDF Vectorizer serialized to {TFIDF_VECTORIZER_PATH}")

    models = {
        "Logistic Regression": LogisticRegression(
            class_weight="balanced",
            max_iter=1000,
            random_state=RANDOM_STATE,
        ),
        "Multinomial Naive Bayes": MultinomialNB(
            alpha=0.1,
        ),
    }

    results: Dict[str, Dict[str, object]] = {}
    roc_plot_data: Dict[str, Tuple[np.ndarray, np.ndarray, float]] = {}
    cv = StratifiedKFold(n_splits=CV_FOLDS, shuffle=True, random_state=RANDOM_STATE)

    for name, model in models.items():
        logger.info(f"--- Training & Evaluating: {name} ---")

        cv_scores = cross_validate(
            model,
            X_train_vec,
            y_train,
            cv=cv,
            scoring=["accuracy", "f1_macro"],
            return_train_score=False,
        )
        mean_cv_acc = round(float(np.mean(cv_scores["test_accuracy"])), 4)
        mean_cv_f1 = round(float(np.mean(cv_scores["test_f1_macro"])), 4)
        logger.info(f"{name} 5-Fold CV Accuracy: {mean_cv_acc:.4f}, Macro-F1: {mean_cv_f1:.4f}")

        model.fit(X_train_vec, y_train)

        y_pred = model.predict(X_test_vec)
        y_proba = model.predict_proba(X_test_vec)[:, 1]

        metrics = compute_classification_metrics(y_test.values, y_pred, y_proba)
        metrics["cv_mean_accuracy"] = mean_cv_acc
        metrics["cv_mean_macro_f1"] = mean_cv_f1

        results[name] = metrics

        fpr, tpr, _ = roc_curve(y_test, y_proba)
        roc_plot_data[name] = (fpr, tpr, metrics["roc_auc"])

    joblib.dump(models["Logistic Regression"], LOGISTIC_REGRESSION_MODEL_PATH)
    logger.info(f"Saved Logistic Regression model to {LOGISTIC_REGRESSION_MODEL_PATH}")

    joblib.dump(models["Multinomial Naive Bayes"], NAIVE_BAYES_MODEL_PATH)
    logger.info(f"Saved Multinomial Naive Bayes model to {NAIVE_BAYES_MODEL_PATH}")

    with open(METRICS_SUMMARY_PATH, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    logger.info(f"Saved evaluation metrics to {METRICS_SUMMARY_PATH}")

    plot_confusion_matrices(results, CONFUSION_MATRIX_PATH)
    plot_roc_curves(roc_plot_data, ROC_CURVE_PATH)
    generate_markdown_report(results, EVALUATION_REPORT_PATH)

    logger.info("Model training, evaluation, and reporting pipeline completed successfully.")
    return results


if __name__ == "__main__":
    run_training_pipeline()
