from ai.kg.detector import JointIntentSlotDetector
from ..config import settings

if __name__ == "__main__":
    detector = JointIntentSlotDetector.from_pretrained(
        model_path=settings.MODEL_PATH,
        tokenizer_path=settings.TOKENIZER_PATH,
        intent_label_path=settings.INTENT_LABEL_PATH,
        slot_label_path=settings.SLOT_LABEL_PATH,
    )

    while True:
        text = input("input: ")
        print(detector.detect(text))
