#  YT comments Analyzer 

### Description
A python package that allows you to perform sentiment analysis of comments on any Youtube video. 

- using Google API Client Library to interact with the YouTube Data API to fetch video comments.

- using regex to filter out hyperlinks, html tags and entities. Sentences with more than 65% composition of emojis are discarded.

- using VADER, a rule based model specifically fine tuned for analyzing sentiments in social media texts

### Issues
for optimization purposes, the number of comments you recievce per API call is set to 100. (The maximum). This can lead to issues where the number of comments you actually recieve is more than you have specified. 

>#### Why this package?
> Youtube has very few, unintuitive filters for their comments. You often have to scroll very far to see negative comments. (this is important for product review videos) Also, since the dislike count has been removed since 2021, you cannot effectively view how well someone's video is doing. With this package you can retrieve up to 12000 comments and separate them into positive, neutral, and negative categories for further analysis.
### Installation

To install the current release

```
$ pip install YT_Sentiment
```
*Try your first YT_Sentiment program*

```
$ python
```
```python
>>> from YT_Sentiments.sentiment import analyzer
>>> obj = analyzer("API_KEY", "VIDEO_LINK", 100)
>>> obj.get_analysis()
>>> <class 'list'>
```

# YT_Sentiments Documentation

## `analyzer` Class

The `analyzer` class is designed to extract comments from a specified YouTube video and perform sentiment analysis on them. The comments are categorized as positive, negative, or neutral based on their sentiment polarity.

### Methods

#### `__init__(self, api, video_link, limit=600)`

Initializes the `analyzer` object with the provided YouTube API key, video link, and a limit on the number of comments to analyze.

**Parameters:**
- `api` (str): YouTube v3 developer API key used to access the YouTube Data API.
- `video_link` (str): Full HTTPS link of the YouTube video from which comments are to be fetched.
- `limit` (int): Upper bound on the number of comments to retrieve and analyze. Default is 600.

**Attributes:**
- `LINK` (str): Stores the YouTube video link.
- `LIMIT` (int): Stores the maximum number of comments to fetch.
- `API_KEY` (str): Stores the YouTube API key.
- `positive` (list): Stores comments classified as positive.
- `negative` (list): Stores comments classified as negative.
- `neutral` (list): Stores comments classified as neutral.
- `polarityList` (list): Stores the sentiment polarity scores of all comments.

#### `get_analysis(self)`

Returns a comprehensive analysis of the comments.

**Returns:**
- `list`: A list containing the positive, negative, neutral comments, and the polarity scores of each comment in the following format: `[positive_list, negative_list, neutral_list, polarity_list[dict]]`.

#### `get_positive(self)`

Returns a list of all positive comments.

**Returns:**
- `list`: A list containing all positive comments.

#### `get_negative(self)`

Returns a list of all negative comments.

**Returns:**
- `list`: A list containing all negative comments.

#### `get_neutral(self)`

Returns a list of all neutral comments.

**Returns:**
- `list`: A list containing all neutral comments.

#### `get_polarity(self)`

Returns a list of all sentiment polarity scores.

**Returns:**
- `list`: A list of dictionaries containing the polarity scores for each comment. Each dictionary has keys `neg`, `neu`, `pos`, and `compound`.

## Helper Functions

### `getSentimentScore(comment)`

Analyzes the sentiment of a single comment and returns its polarity scores.

**Parameters:**
- `comment` (str): The comment text to be analyzed.

**Returns:**
- `dict`: A dictionary containing the sentiment polarity scores with keys `neg` (negative), `neu` (neutral), `pos` (positive), and `compound` (overall sentiment score).

### `getComments(LINK, API_KEY, LIMIT)`

Fetches and cleans a specified number of comments from a YouTube video.

**Parameters:**
- `LINK` (str): The full HTTPS link of the YouTube video.
- `API_KEY` (str): YouTube developer API key for accessing the YouTube Data API.
- `LIMIT` (int): The maximum number of comments to fetch.

**Returns:**
- `list`: A list of relevant, cleaned comments.

**Note:**
The function removes comments with hyperlinks, HTML tags, or those containing a disproportionate number of emojis. It also excludes comments from the video uploader.

### License
[MIT License](LICENSE)

