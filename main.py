
#----------------------installed packages
import dask
from dask import delayed, compute
from dask.distributed import Client
import dotenv
import pandas as pd
#------------------------standard packages with python--------------------
import multiprocessing, time, json, os


#------------------------custom classes and packages-----------
from reddit_handler import RedditHandler
from sentiment_analyzer import SentimentAnalyzer
from review_classification import ReviewClassifier
from generate_query import GenerateSearchQueries
from category_classifier import CategoryClassifier

#------------------------configuration to force dask scheduler to use full parallel processing -----------------
dask.config.set({"distributed.scheduler.worker-ttl":None})
num_workers = multiprocessing.cpu_count()
print(num_workers)

#------------------------create a classifier instance---------------
classifier = ReviewClassifier()

#------------------------functions needed preprocessing-------------
# function for parallel processing of classification tasks
def classify_reviews(review: str, sentiment: str, task:str):
    return classifier.classifyReview(sentiment=sentiment, comment=review,task=task)

#------------------------MAIN function------------------------------
if __name__ == "__main__":
    dotenv.load_dotenv()
    # -----------------generate search queries----------------------------------------------
    # start = time.time()
    # query_generator = GenerateSearchQueries()
    # query_generator.generateQueries()
    # end = time.time()
    # print(f"time taken for generating queries", end - start)
    # ----------------------------------------------------------------

    # # ----------------fetch reddit posts------------------------------------------------
    # start = time.time()
    # df = pd.read_csv(f"./search_queries.csv")
    # queries = [df['queries'][record] for record in range(0, df['queries'].size)]
    #
    # # create Reddit handler and fetch reviews
    # reddit = RedditHandler(queries=queries)
    #
    # # fetch posts from reddit for generated search strings
    # reddit.fetch_posts()
    # end = time.time()
    # print(f"time taken for fetching posts", end - start)
    # #----------------------------------------------------------------
    # #
    # # ---------------analyze sentiments -------------------------------------------------
    # start = time.time()
    # print(f"Starting Sentiment analysis")
    # posts = pd.read_csv('./all_posts.csv')
    # sentiments = SentimentAnalyzer()
    # sentiments.assessSentiments(reviews=posts)
    # # print the sentiment analysis summary
    # print(
    #     f"Positive: {sentiments.positive_sentiments}, Negative:{sentiments.negative_sentiments}, "
    #     f" Neutral: {sentiments.neutral_sentiments}, Unclassified: {sentiments.unclassified_sentiments}")
    # end = time.time()
    # print(f"time taken for sentiment analysis", end - start)
    #-----------------------------------------------------------------



    #---------------classify into labels-------------------------------------------------
    # print(f"Starting classification of reviews into different categories")
    # multiprocessing.freeze_support()
    # # start the classification process
    # start = time.time()
    # for sentiment in ['positive','negative','neutral']:
    #     #--------------read the sentiment files-------------------
    #     df = pd.read_csv(f"./reddit_{sentiment}_reviews.csv")
    #     df = df.astype(str)
    #     queries = [df['user_review'][record] for record in range(0, df['user_review'].size)]
    #
    #     #--------------Use Dask `delayed` to create lazy computations---------
    #     client = Client(n_workers=int(num_workers/2), processes=True,
    #                     threads_per_worker=1)  # Adjust workers based on CPU cores
    #     print(client.dashboard_link)
    #
    #     #-------------parallel processing -------------------------
    #     tasks = [delayed(classify_reviews)(review=query, sentiment=sentiment, task="summarize") for query in queries]
    #     results = compute(*tasks)
    #     #-----------------save the classifications into csv and json files--------------------
    #     classifier.saveToFile(sentiment=sentiment, comment_classification=results)
    #     #----------------close the client for parallel processing----------------
    #     client.close()
    # end = time.time()
    #
    # print(f"time taken classifying reviews :", end - start)

 #---------------categorizing themes -------------------------------------------------
    start = time.time()
    print(f"Starting theme categorization")
    theme_categorizer = CategoryClassifier()
    for item in ['positive','negative','neutral']:
        theme_categorizer.generate_theme_mappings(sentiment=item)
    end = time.time()
    print(f"time taken for theme categorization", end - start)