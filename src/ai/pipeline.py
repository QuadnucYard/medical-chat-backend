from .config import settings
from .kgqa.answer import Answer
from .slu.detector import DetectResult, JointIntentSlotDetector


class MedQAPipeline:
    def __init__(self) -> None:
        self.detector = JointIntentSlotDetector.from_pretrained(
            model_path=settings.MODEL_PATH,
            tokenizer_path=settings.TOKENIZER_PATH,
            intent_label_path=settings.INTENT_LABEL_PATH,
            slot_label_path=settings.SLOT_LABEL_PATH,
        )
        self.answerer = Answer()
        self.slot_label: list[list[str]]

    def identify_question_entity(self, q: DetectResult) -> tuple[str, str] | None:
        entity: str | None = None
        question_type: str | None = None
        if q.slots.__contains__("disease"):
            entity = q.slots["disease"][0]
        elif q.slots.__contains__("symptom"):
            entity = q.slots["symptom"][0]
        question_type = q.intent
        return None if not question_type or not entity else (question_type, entity)

    def __call__(self, question: str):
        res = self.detector.detect(question)
        print(res)
        qe = self.identify_question_entity(res[:-1])
        self.slot_label = res[-1]
        if not qe:
            return "您的问题并不明确，请换个问法再说一遍，谢谢。"
        return self.answerer.create_answer(*qe)

    def entity_position(self):
        start = []
        end = []
        for label, i in enumerate(self.slot_label[0]):
            if label == "B_disease" or label == "B_symptom" or label == "B_secsymptom":
                start.append(i)
            elif label == "I_disease" or label == "I_symptom" or label == "I_secsymptom":
                if self.slot_label[0][i + 1] not in ["I_disease", "I_symptom", "I_secsymptom"]:
                    end.append(i)
        position = []
        for i in range(len(start)):
            position.append(
                {"slot": self.slot_label[0][start[i][2:]], "start": start[i], "end": end[i]}
            )
        return position


if __name__ == "__main__":
    pipeline = MedQAPipeline()
    while True:
        text = input("input: ")
        print(pipeline(text))
