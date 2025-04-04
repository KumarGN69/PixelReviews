from sentence_transformers import SentenceTransformer, util
import pandas as pd
import re, os, csv


#----------------reading the extracted posts into a dataframe---------------------------------------


#----------------combining the title and review text into a single text-----------------------------
# df["combined_reviews"] = df['post_title'].astype(str).str.cat(df['self_text'].astype(str), na_rep='')

class CategoryClassifier:

    def __init__(self):
        pass

    def clean_text(self, text):
        text = str(text).lower()
        text = re.sub(r'\W+', ' ', text)  # Remove punctuation
        return text

    #----------------defining themes-------------------------------------------------------------------
    def get_themes(self):
        return [
            'Ease of functionality',
            'User Experience',
            'App difficult to use',
            'Notification issues',
            'Software updates',
            'Audio quality issues',
            'Video quality Issues',
            'Connection Issues',
            'Pairing Issues',
            'Sync issues',
            'Voice Commands',
            'Android Auto Issues',
            'Bluetooth Issues',
            'Wifi Issues',
            'Price related',
        ]

    #----------------creating embeddings for review and the themes-------------------------------------
    def get_sentencetransformer_model(self):
        return SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

    def get_theme_embeddgings(self, themes):
        theme_embedding =  self.get_sentencetransformer_model().encode(themes)
        # print(f"theme_embedding: {theme_embedding}")
        return theme_embedding

    def encode_review(self, review):
        encoded_review = self.get_sentencetransformer_model().encode(review)
        # print(f"review embedding: {encoded_review}")
        return encoded_review

    def find_similarity(self, review, theme_embedding):
        review_embedding = self.encode_review(review)
        similarities = util.pytorch_cos_sim(review_embedding, theme_embedding)
        theme= self.get_themes()[similarities.argmax().item()]
        # print(theme)
        return theme

    #---------------find similarity and theme--------------------------------------------------------
    # Convert 'cleaned_reviews' column to a list and classify themes
    def generate_theme_mappings(self,sentiment):
        df = pd.read_csv(f"./reddit_{sentiment}_review_classification.csv")
        # del (df['user_review'])
        # print(df)
        df['user_review'] = df['user_review'].astype(str)
        df['cleaned_reviews'] = df['user_review'].apply(self.clean_text)
        df['Issue Category'] = [self.find_similarity(review, self.get_theme_embeddgings(self.get_themes())) for review in
                          df['cleaned_reviews']]
        del (df['cleaned_reviews'])
        df.to_csv(path_or_buf=f'./classified_{sentiment}_posts.csv', index=False, quoting=csv.QUOTE_ALL, quotechar='"')


# if __name__ == "__main__":
#     theme_categorizer = CategoryClassifier()
#     for item in ["negative"]:
#         theme_categorizer.generate_theme_mappings(sentiment=item)
