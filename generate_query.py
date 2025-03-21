import pandas as pd
import dotenv, os, csv
from custom_llm import LLMModel



class GenerateSearchQueries:

    def __init__(self):
        dotenv.load_dotenv()
        self.model = LLMModel()
        self.client = self.model.getclientinterface()
        self.keyphrases = (
                f"Pixel vs iPhone comparison"
                f"Challenges switching from iPhone to Pixel"
                f"Pixel ecosystem advantages over iPhone ecosystem"
                f"Google ecosystem vs Apple ecosystem"
                f"Pixel features compared to iPhone features"
                f"Pixel ecosystem vs iPhone ecosystem user reviews"
               )
        self.search_themes =(
            f"audio quality issues while using headsets"
            f"video quality issues when using bluetooth or wifi"
            f"application issues when doing conference calls"
        )

    def generateQueries(self):
        df = pd.read_csv("inputfile.csv", header=0, delimiter=",")
        query = self.client.generate(
            model=self.model.MODEL_NAME,
            prompt = (
                f"You are an expert in crafting targeted Reddit search queries to extract comprehensive user feedback" 
                f"comparing Google and Apple products. Generate a complete list of natural-language search phrases" 
                f"using the BOOLEAN OPERATOR AND in CAPS to combine elements from our dataset:"
                
                f"Device Combinations (from {df['1P Devices  Combination']}, REQUIRED)"
                f"Core software app User Pain Points (from {df['Critical User Journey Problem area']}, REQUIRED)"
                f"Software Components (from {df['Component']}, REQUIRED)"
                f"Software Functionality (from {df['Functionality']}, REQUIRED)"
                f"Comparison of Google Pixel products AND Apple iPhone products (REQUIRED)"
                
                f"STRINGENT REQUIREMENTS:"
                
                f"Mandatory inclusion of Critical User Journey Problem area"
                f"Exclude any entry with missing values (NaNs) in ANY field"
                f"Create 20-30 word natural phrases, not keyword lists"
                f"Blend elements contextually (e.g., '[Google Device] AND [Apple Device] comparison for [Problem] during"
                f"Feature] usage due to [Component]')"
                f"Output as clean text with one query per line without numbering"
                f"No markdown, numbering, bullets or special characters"
                f"Include ONLY Apple product(s) for comparison, excluding other competitors"
                f"**Restrict only the themes in {self.search_themes}**"
                
                f"**Example structures using the BOOLEAN OPERATOR AND and the key phrases in {self.keyphrases}**:"
                
                f"Pixel phone AND iPhone audio quality comparison for [Device Combination] when [Problem] occurs"
                f"[Problem] in Google ecosystem AND Apple ecosystem affecting [Functionality] on [Device Combination]"
                f"[Component] issues on Pixel devices AND iPhones impacting [Functionality] for [Device Combination]"
            )
        )
        search_queries = query.response.splitlines()
        queries = []
        for search_query in search_queries:
            queries.append({
                "queries": search_query
            })
            print(search_query)

        df = pd.DataFrame(queries)
        df = df.astype(str)
        df.to_json(path_or_buf="./search_queries.json", index=False)
        df.to_csv(path_or_buf="./search_queries.csv", index=False,quoting=csv.QUOTE_ALL)
