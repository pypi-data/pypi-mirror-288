from pykit import validation
from pykit.condition import ComparisonCondition, ComparisonMark
from pykit.expectation import ListExpectation
from pykit.expectation.errors import (
    ExpectationError,
    UnsupportedExpectationTypeError,
)


def test_count():
    expectation: ListExpectation = ListExpectation(count=ComparisonCondition(
        mark=ComparisonMark.MoreEqual,
        value=3,
    ))

    validation.expect(
        expectation.check,
        ExpectationError,
        [1, 2],
    )
    expectation.check([1, 2, 3])
    expectation.check([1, 2, 3, 4])


def test_unsupported_type():
    expectation: ListExpectation = ListExpectation(count=ComparisonCondition(
        mark=ComparisonMark.MoreEqual,
        value=2,
    ))

    validation.expect(
        expectation.check,
        UnsupportedExpectationTypeError,
        # only list should be expected as a target
        2,
    )
