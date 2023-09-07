from ai.pipeline import MedQAPipeline
from asgiref.sync import sync_to_async

pipeline = MedQAPipeline()


async def qa(question: str):
    return await sync_to_async(pipeline)(question)
