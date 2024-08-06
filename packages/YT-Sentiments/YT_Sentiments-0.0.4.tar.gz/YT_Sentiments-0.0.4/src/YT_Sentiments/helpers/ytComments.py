from googleapiclient.discovery import build
import re
import emoji
def getComments(LINK, API_KEY, LIMIT):
    """
        Takes <limit> number of comments from the specified video using the api defined in <api> and cleans the data.

        Parameters:

        video_link [string]: the full https link of the youtube video copied from the address bar
        api [string]: The youtube developer api key used to get comments from youtube
        limit [int]: The number of comments to analyze

        Returns: relevant_data [list]: a list containing all comments
    """

    youtube = build('youtube', 'v3', developerKey=API_KEY)
    # Taking input from the user form input and slicing for video id
    video_id = LINK[-11:]
    #video_id = request.form.get("link")[-11:]

    # Getting the channelId of the video uploader
    video_response = youtube.videos().list(
        part='snippet',
        id=video_id
    ).execute()

    # Splitting the response for channelID
    video_snippet = video_response['items'][0]['snippet']
    uploader_channel_id = video_snippet['channelId']

    # Fetch comments
    comments = []
    nextPageToken = None
    while len(comments) < LIMIT:
        request = youtube.commentThreads().list(
            part='snippet',
            videoId=video_id,
            maxResults=100,  # You can fetch up to 100 comments per request
            pageToken=nextPageToken
        )
        response = request.execute()
        for item in response['items']:
            comment = item['snippet']['topLevelComment']['snippet']
            # Check if the comment is not from the video uploader
            if comment['authorChannelId']['value'] != uploader_channel_id:
                comments.append(comment['textDisplay'])
        nextPageToken = response.get('nextPageToken')

        if not nextPageToken:
            break

    # remove hyperlinks
    hyperlink_pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
    # remove tags and entities
    html_pattern = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')

    threshold_ratio = 0.65

    relevant_comments = []

    # Inside loop that processes comments
    for comment_text in comments:

        comment_text = comment_text.lower().strip()
        comment_text = re.sub(html_pattern, '', comment_text)
        emojis = emoji.emoji_count(comment_text)

        # Count text characters (excluding spaces)
        text_characters = len(re.sub(r'\s', '', comment_text))

        if (any(char.isalnum() for char in comment_text)) and not hyperlink_pattern.search(comment_text):
            if emojis == 0 or (text_characters / (text_characters + emojis)) > threshold_ratio:
                relevant_comments.append(comment_text)

    return relevant_comments