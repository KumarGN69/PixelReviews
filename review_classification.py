from custom_llm import LLMModel
import pandas as pd
import os, dotenv, csv


class ReviewClassifier:
    """

    """

    def __init__(self):
        dotenv.load_dotenv()
        self.model = LLMModel()
        # self.client = self.model.getclientinterface()
        self.MODEL = os.getenv('INFERENCE_MODEL')
        self.classification_labels = ["Audio", "Watch", "Bluetooth", "Wi-Fi", "CarKit", "Other"]
        self.classification_guidelines = (
            f"Categorize the review into exactly one of labels in {self.classification_labels} "
            f"** Strictly ensuring ** : "
            f"1. No new lines or extra white spaces."
            f"2. No additional words, explanations, or qualifiers."
            f"3. When no relevant mapping to the provided labels is detected, use Other"
        )

        self.classification_task = (
            f"You are an expert in choosing the most appropriate label for classifying a given text "
            f"and do not deviate from the guidelines "
        )
        self.testCUJ_task = (
            f"You are a senior, experienced software quality analyst and tester specializing "
            f"in mobile phones and accessories. Generate clear and concise instructions to create a "
            f"test user journey using language and descriptions that a tester can easily understand and follow"
            f"that addresses the key issue described in the review"
        )
        # self.summarization_task = (
        #     f"You are a world-class expert in text summarization, with a keen ability to distill "
        #     f"complex information into its most essential elements. Your task is to analyze the "
        #     f"given review and create a summary that captures its core message and most significant "
        #     f"points in exactly two concise, meaningful, and well-crafted sentences. "
        #     f"Ensure that your summary is both comprehensive and succinct, leaving no crucial information "
        #     f"out while avoiding unnecessary details."
        #     )
        self.summarization_task = (
            f"Summarize into a ONE concise sentence that captures "
            f"the core issue being described in the review "
        )

    def saveToFile(self, sentiment: str, comment_classification: list):
        """
        """
        # print(comment_classification)
        df = pd.DataFrame(comment_classification)
        json_file_name = f"reddit_{sentiment}_review_classification.json"
        df.to_json(json_file_name, indent=4, orient="records")

        csv_file_name = f"reddit_{sentiment}_review_classification.csv"
        df.to_csv(csv_file_name, index=False, quoting=csv.QUOTE_ALL, quotechar='"')

    def classifyReview(self, comment: str, time_frame, sentiment: str, task: str):
        """
        """
        classification = {}
        model = LLMModel()
        client = model.getclientinterface()
        sentiment = sentiment
        if task == "summarize":
            summarizer = client.generate(
                model=self.MODEL,
                prompt=(
                    f"Rewrite the following comment into a single, concise sentence that captures"
                    f"the main technology issue being described. Output only one sentence."
                    f"Do not include explanations, elaborations, or multiple statements: {comment}"
                )
            )

            classification = {
                "sentiment": f"{sentiment}",
                "user_review": f"{comment}",
                "summary": f"{summarizer.response}",
                "time_frame": time_frame
            }
            return classification

        elif task == "generateTestCUJ":
            # print("test CUJ generation starting")

            testCUJ = client.generate(
                model=self.MODEL,
                prompt=f"perform the task in {self.testCUJ_task} in {comment}"
            )
            classification = {
                "sentiment": sentiment,
                # "categories": classifier.response,
                "user_review": comment,
                # "summary": summarizer.response,
                "test_user_journey": testCUJ.response
            }
            print(f"test CUJ generation :\n {testCUJ.response}")
            return classification
