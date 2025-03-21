import pandas as pd
import dotenv, os, csv
from custom_llm import LLMModel



class GenerateSearchQueries:

    def __init__(self):
        dotenv.load_dotenv()
        self.model = LLMModel()
        self.client = self.model.getclientinterface()
        self.keyphrases = (
                f"User Experience challenges"
               )
        self.search_themes =(
            f"audio quality issues ",
            f"pairing and connection issues",
            f"pairing and sync issues"
        )

    def generateQueries(self):
        df = pd.read_csv("inputfile.csv", header=0, delimiter=",")
        query = self.client.generate(
            model=self.model.MODEL_NAME,
            prompt = (
                f"You are an expert in crafting targeted Reddit search queries to extract comprehensive user feedback" 
                f"Generate a complete list of natural-language search phrases in {self.keyphrases}" 
                f"using the boolean operator AND in CAPS to combine elements from our dataset:"
                
                f"**DATASET:**"
                f" All Device Combinations (from {df['1PDevices']}, REQUIRED)"
                f"Core software User journey (from {df['UserJourney']}, REQUIRED)"
                f"Software Components (from {df['Component']}, REQUIRED)"
                f"Software Functionality (from {df['Functionality']}, REQUIRED)"
                f"All Accessory combinations  (from {df['1PAccessories']}, REQUIRED)"
                
                
                f"**STRINGENT REQUIREMENTS:**"
                f"Mandatory inclusion of User Journey "
                f"Exclude any entry with missing values (NaNs) in ANY field"
                f"Max Create 10-12 word natural phrases, not keyword lists"
                f"Blend elements contextually (e.g.,'Usage of Pixel 7 with Pixel Watch')"
                f"Output as clean text with one query per line without numbering"
                f"No markdown, numbering, bullets or special characters"
                f"**Restrict only the themes in {self.search_themes}**"
                
                f"**Example queries:**"
                f"**Pixel 9 pairing issues with Pixel Watch for themes in {self.search_themes}** "
                f"**Pixel tablet connection issues with Wifi for the themes in {self.search_themes}"
            )
        )
        search_queries = query.response.splitlines()
        queries = []
        for search_query in search_queries:
            queries.append({
                "queries": search_query
            })
            # print(search_query)

        df = pd.DataFrame(queries)
        df = df.astype(str)
        df.to_json(path_or_buf="./search_queries.json", index=False)
        df.to_csv(path_or_buf="./search_queries.csv", index=False,quoting=csv.QUOTE_ALL)
