
class SampleModel:
    def __init__(self, api_key: str = None):
        self.api_key = api_key
        print("SampleModel initialized with API key:")


    def load_document(self, file_path: str) -> None:
        print("Document loaded from:", file_path)
        return None
    
    def inference(self, question: str) -> str:
        print("Inference made with question:", question)
        return "Sample response to the question."