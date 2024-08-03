"""Acquisition function wrappers."""

from baybe.acquisition.acqfs import (
    ExpectedImprovement,
    LogExpectedImprovement,
    PosteriorMean,
    PosteriorStandardDeviation,
    ProbabilityOfImprovement,
    UpperConfidenceBound,
    qExpectedImprovement,
    qKnowledgeGradient,
    qLogExpectedImprovement,
    qLogNoisyExpectedImprovement,
    qNegIntegratedPosteriorVariance,
    qNoisyExpectedImprovement,
    qProbabilityOfImprovement,
    qSimpleRegret,
    qUpperConfidenceBound,
)

PM = PosteriorMean
PSTD = PosteriorStandardDeviation
qSR = qSimpleRegret
EI = ExpectedImprovement
qEI = qExpectedImprovement
qKG = qKnowledgeGradient
LogEI = LogExpectedImprovement
qLogEI = qLogExpectedImprovement
qNEI = qNoisyExpectedImprovement
qNIPV = qNegIntegratedPosteriorVariance
qLogNEI = qLogNoisyExpectedImprovement
PI = ProbabilityOfImprovement
qPI = qProbabilityOfImprovement
UCB = UpperConfidenceBound
qUCB = qUpperConfidenceBound

__all__ = [
    ######################### Acquisition functions
    # Knowledge Gradient
    "qKnowledgeGradient",
    # Posterior Statistics
    "PosteriorMean",
    "PosteriorStandardDeviation",
    # Simple Regret
    "qSimpleRegret",
    # Expected Improvement
    "ExpectedImprovement",
    "qExpectedImprovement",
    "LogExpectedImprovement",
    "qLogExpectedImprovement",
    "qNoisyExpectedImprovement",
    "qNegIntegratedPosteriorVariance",
    "qLogNoisyExpectedImprovement",
    # Probability of Improvement
    "ProbabilityOfImprovement",
    "qProbabilityOfImprovement",
    # Upper Confidence Bound
    "UpperConfidenceBound",
    "qUpperConfidenceBound",
    ######################### Abbreviations
    # Knowledge Gradient
    "qKG",
    # Posterior Statistics
    "PM",
    "PSTD",
    # Simple Regret
    "qSR",
    # Expected Improvement
    "EI",
    "qEI",
    "LogEI",
    "qLogEI",
    "qNEI",
    "qNIPV",
    "qLogNEI",
    # Probability of Improvement
    "PI",
    "qPI",
    # Upper Confidence Bound
    "UCB",
    "qUCB",
]
