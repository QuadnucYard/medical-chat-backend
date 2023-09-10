from __future__ import annotations

import asyncio
from dataclasses import dataclass
from pprint import pprint
from typing import TYPE_CHECKING, overload

from .config import settings
from .logging import logger

logger.info("Start pipeline")

from .kgqa.answer import Answer, AnswerResult

if TYPE_CHECKING:
    from .slu.detector import DetectResult


@dataclass
class PipelineResult:
    detection: DetectResult
    answer: list[AnswerResult]
    fallback_answer: str | None = None


class MedQAPipeline:
    def __init__(self) -> None:
        logger.info("Init MedQAPipeline")
        logger.info("Loading model async.")
        self.load_model_task = asyncio.ensure_future(self._load_model())
        self.answerer = Answer()
        logger.info("OK.")

    async def _load_model(self):
        from .slu.detector import JointIntentSlotDetector

        self.detector = JointIntentSlotDetector.from_pretrained(
            model_path=settings.MODEL_PATH,
            tokenizer_path=settings.TOKENIZER_PATH,
            intent_label_path=settings.INTENT_LABEL_PATH,
            slot_label_path=settings.SLOT_LABEL_PATH,
        )
        logger.info("Model loading done")

    def create_answer(self, res: DetectResult):
        if not res.slots:
            return "您的问题并不明确，请换个问法再说一遍，谢谢。"
        return [self.answerer.create_answer(res.intent, r.text) for r in res.slots]

    async def pipeline(self, question: str) -> PipelineResult:
        await self.load_model_task
        res = self.detector.detect(question)
        logger.info(res)
        answers = [self.answerer.create_answer(res.intent, r.text) for r in res.slots]
        logger.info(answers)  # 如果为空，考虑加一个
        return PipelineResult(res, answers, None if answers else self.answerer.get_answer_none())

    @overload
    async def __call__(self, question: str) -> PipelineResult:
        ...

    @overload
    async def __call__(self, question: list[str]) -> list[PipelineResult]:
        ...

    async def __call__(self, question: str | list[str]):
        if isinstance(question, list):
            return await asyncio.gather(*list(map(self.pipeline, question)))
        return await self.pipeline(question)


async def main():
    pipeline = MedQAPipeline()
    while True:
        text = input("input: ")
        pprint(await pipeline(text), width=120)


if __name__ == "__main__":
    asyncio.run(main())
