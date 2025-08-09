from simple_.config import RAGConfig
from simple_.rag_pipeline import RAGPipeline
from dotenv import load_dotenv
import os
load_dotenv()
class SampleModel:
    def __init__(self, api_key: str = None):
        self.api_key = os.getenv("OPENAI_API_KEY") 
        print(self.api_key)
        print("SampleModel initialized with API key:", self.api_key)
        self.rag = None
        self.document_loaded = False

    def load_document(self, file_path: str) -> None:
        """Load and process a document (PDF URL or local path)"""
        config = RAGConfig(
            # openai_api_key=self.api_key,
            chunk_size=1000,
            chunk_overlap=200,
            batch_size=8,
            max_threads=4,
            similarity_threshold=0.7,
            save_dir="./documents"
        )
        self.rag = RAGPipeline(config)
        try:
            print("Loading document from:", file_path)
            self.rag.load_document(file_path)
            self.document_loaded = True
            print("Document loaded and processed.")
        except Exception as e:
            print(f"Error loading document: {e}")
            self.document_loaded = False

    def inference(self, question):
        """
        Answer a question or a batch of questions using the loaded document.
        Accepts a single string or a list of strings.
        Returns a single answer or a list of answers.
        """
        if not self.rag or not self.document_loaded:
            print("No document loaded. Please load a document first.")
            return "No document loaded."
        import asyncio
        try:
            if isinstance(question, str):
                questions = [question]
                single = True
            elif isinstance(question, list):
                questions = question
                single = False
            else:
                raise ValueError("Input must be a string or a list of strings.")

            async def ask():
                results = await self.rag.ask_questions(questions)
                return [r['answer'] for r in results] if results else ["No answer."]

            answers = asyncio.run(ask())
            if single:
                print("Inference made with question:", question)
                return answers[0]
            else:
                print(f"Inference made with batch of {len(questions)} questions.")
                return answers
        except Exception as e:
            print(f"Error during inference: {e}")
            return f"Error: {e}"


if __name__ == "__main__":
    import json
    api_key = input("Enter your OpenAI API key: ").strip()
    pdf_url = input("Enter PDF URL or file path: ").strip()
    print("Enter your questions (one per line). Enter an empty line to finish:")
    questions = []
    while True:
        q = input()
        if not q.strip():
            break
        questions.append(q.strip())

    if not questions:
        print("No questions provided. Exiting.")
        exit(0)

    model = SampleModel(api_key=api_key)
    model.load_document(pdf_url)
    answers = model.inference(questions)
    print("\nAnswers:")
    for i, (q, a) in enumerate(zip(questions, answers), 1):
        print(f"Q{i}: {q}\nA{i}: {a}\n")

    # Save to answers.json
    output = [{"question": q, "answer": a} for q, a in zip(questions, answers)]
    with open("answers.json", "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    print("All answers saved to answers.json")