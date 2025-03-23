import pandas as pd
import dotenv, os, csv, re
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
                f" You are an expert in crafting targeted Reddit search queries to extract comprehensive user feedback. "
                f" Generate a list of search phrases using combination of {df['1PDevices']} AND {df['1PAccessories']} "
                f" ** Example Output:** "
                f" Pixel7 AND Pixel Watch"
                f" Pixel8 AND Pixel Earbuds"
            )
            # prompt=(
            #     f"You are an expert in crafting targeted Reddit search queries to extract comprehensive user feedback. "
            #     f"Generate a complete list of natural-language search phrases in {self.keyphrases} "
            #     f"using the boolean operator AND in CAPS to combine elements from our dataset: "
            #
            #     f"DATASET: "
            #     f"All Device Combinations (from {df['1PDevices']}, REQUIRED) "
            #     f"Core software User journey (from {df['UserJourney']}, REQUIRED) "
            #     f"Software Components (from {df['Component']}, REQUIRED) "
            #     f"Software Functionality (from {df['Functionality']}, REQUIRED) "
            #     f"All Accessory combinations (from {df['1PAccessories']}, REQUIRED) "
            #
            #     f"STRINGENT REQUIREMENTS: "
            #     f"Mandatory inclusion of User Journey. "
            #     f"Exclude any entry with missing values (NaNs) in ANY field. "
            #     f"Create NOT MORE than 10 word natural phrases "
            #     f"Blend elements contextually (e.g., 'Usage of Pixel 7 with Pixel Watch'). "
            #     f"Output as clean text with one query per line without numbering or special characters. "
            #     # f"Output ONE query per line "
            #     # f"DO NOT ADD numbering, bullets or special characters. "
            #     f"Restrict only to the themes in {self.search_themes}. "
            #
            #     f"Example output: "
            #     f"Pixel 8 usage experiences related to audio quality problems with Pixel Earbuds\n"
            #     f"Connection issues faced while using Pixel 9A with Bluetooth accessories\n"
            #     f"Pairing troubles experienced on Pixel Fold when connected to Pixel Watch\n"
            # )

        )
        search_queries = query.response.splitlines()
        # print(search_queries)
        queries = [
            {"queries": re.sub(r'\d+', '', search_query).replace('"', '').replace('.', '')}
            for search_query in search_queries
        ]
        cleaned_queries =[{"queries": ' '.join(query['queries'].split())} for query in queries]
        # for query in queries:
        #     print(type(query['queries']))
        #     query = ' '.join(query['queries'].split())
        #     cleaned_queries.append({
        #         "queries": query
        #     })
        print(cleaned_queries)
        df = pd.DataFrame(cleaned_queries)
        df = df.astype(str)
        df.to_json(path_or_buf="./search_queries.json", index=False)
        df.to_csv(path_or_buf="./search_queries.csv", index=False,quoting=csv.QUOTE_MINIMAL, escapechar='\\' )
