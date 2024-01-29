""" Copyright (c) . All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation
and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote products derived from this software without 
specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED 
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY 
DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS 
OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING 
NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

import numbers

import numpy as np


def fit_and_score(estimator, train_ds, validation_ds, scorer, parameters,
                  fit_params):
    if parameters is not None:
        estimator.set_params(**parameters)
    x_train, y_train = train_ds
    estimator.fit(x_train, y_train, **fit_params)
    x_test, y_test = validation_ds
    test_scores = _score(estimator, x_test, y_test, scorer)

    return [test_scores]

def fit(estimator, train_ds, scorer, parameters, fit_params):
    if parameters is not None:
        estimator.set_params(**parameters)
    x_train, y_train = train_ds
    estimator.fit(x_train, y_train, **fit_params)
    return estimator

def score_func(estimator, validation_ds, scorer):
    x_test, y_test = validation_ds
    test_scores = _score(estimator, x_test, y_test, scorer)

    return [test_scores]

def _score(estimator, x, y, scorers):
    """Return a dict of scores"""
    scores = {}

    for name, scorer in scorers.items():
        score = scorer(estimator, x, y)
        scores[name] = score
    return scores


def validate_score(score, name):
    if not isinstance(score, numbers.Number) and \
            not (isinstance(score, np.ndarray) and len(score.shape) == 0):
        raise ValueError("scoring must return a number, got %s (%s) "
                         "instead. (scorer=%s)"
                         % (str(score), type(score), name))
    return score


def aggregate_score_dicts(scores):
    """Aggregate the results of each scorer
    Example
    -------
    >>> scores = [{'a': 1, 'b':10}, {'a': 2, 'b':2}, {'a': 3, 'b':3},
    ...           {'a': 10, 'b': 10}]
    >>> aggregate_score_dicts(scores)
    {'a': array([1, 2, 3, 10]),
     'b': array([10, 2, 3, 10])}
    """
    return {key: np.asarray([score[key] for score in scores])
            for key in scores[0]}


def check_scorer(estimator, scorer):
    if scorer is None:
        if hasattr(estimator, 'score'):
            def _passthrough_scorer(estimator, *args, **kwargs):
                """Function that wraps estimator.score"""
                return estimator.score(*args, **kwargs)
            return _passthrough_scorer
        else:
            raise TypeError(
                "If a scorer is None, the estimator passed should have a "
                "'score' method. The estimator %r does not." % estimator)
    elif callable(scorer):
        return scorer
    raise ValueError("Invalid scorer %r" % scorer)
