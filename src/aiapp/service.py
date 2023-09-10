from ai.pipeline import MedQAPipeline

pipeline = MedQAPipeline()


async def qa(question: str | list[str]):
    return await pipeline(question)
