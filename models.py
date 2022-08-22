from typing import List

from pydantic import BaseModel


class Problem(BaseModel):
    contestId: int | None
    index: str | None
    name: str | None
    rating: int | None
    tags: List[str] | None


class ProblemResult(BaseModel):
    problems: List[Problem] | None


class Submission(BaseModel):
    problem: Problem | None


class GeneralResponse(BaseModel):
    status: str | None
    result: ProblemResult | List[Submission] | None
