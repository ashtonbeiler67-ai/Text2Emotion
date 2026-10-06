#----------Emotion analysis bank------------------------------------------
GENERAL_CONTEXTS = ["Happiness", "Sadness", "Anger", "Fear", "Disgust"]

THRESHOLD = 5

HAPPY_KEYWORDS = ["happy", "joy", "love", "great", "awesome", "excited",
                  "smile", "fun", "amazing", "glad", "wonderful", "yay"]
SADNESS_KEYWORDS = ["sad", "cry", "crying", "lonely", "miss", "lost",
                    "tears", "heartbroken", "sorry", "gloomy", "alone", "hurt"]
ANGER_KEYWORDS = ["angry", "mad", "hate", "furious", "annoyed", "rage",
                  "unfair", "worst", "stupid", "ridiculous", "outraged", "ugh"]
FEAR_KEYWORDS = ["scared", "afraid", "fear", "worried", "nervous", "anxious",
                 "terrified", "panic", "danger", "scary", "dread", "yikes"]
DISGUST_KEYWORDS = ["gross", "disgusting", "nasty", "eww", "yuck", "rotten",
                    "vile", "filthy", "smelly", "awful", "cringe", "sick"]
#-------------------------------------------------------------------
def convert_to_sequence(text):
    sequence = text.split()
    return sequence

def total_for_word(word, sequence):
    count = 0
    for item in sequence:
        if item == word:
            count += 1
    return count

def evaluate_context(context_sequence, post_sequence):
    total = 0
    for word in context_sequence:
        total += total_for_word(word, post_sequence) 
    return total
#-----------------Emotion Analysis--------------------------------------
def analyze_text(post_sequence):
    happy = evaluate_context(HAPPY_KEYWORDS, post_sequence)
    sadness = evaluate_context(SADNESS_KEYWORDS, post_sequence)
    anger = evaluate_context(ANGER_KEYWORDS, post_sequence)
    fear = evaluate_context(FEAR_KEYWORDS, post_sequence)
    disgust = evaluate_context(DISGUST_KEYWORDS, post_sequence)
    mostly = []
    if post_sequence:
        if happy / len(post_sequence) * 100 >= THRESHOLD:
            mostly.append(GENERAL_CONTEXTS[0])
        if sadness / len(post_sequence) * 100 >= THRESHOLD:
            mostly.append(GENERAL_CONTEXTS[1])
        if anger / len(post_sequence) * 100 >= THRESHOLD:
            mostly.append(GENERAL_CONTEXTS[2])
        if fear / len(post_sequence) * 100 >= THRESHOLD:
            mostly.append(GENERAL_CONTEXTS[3])
        if disgust / len(post_sequence) * 100 >= THRESHOLD:
            mostly.append(GENERAL_CONTEXTS[4])

    print("Analysis complete!")
    print("Happiness:", happy)
    print("Sadness:", sadness)
    print("Anger:", anger)
    print("Fear:", fear)
    print("Disgust:", disgust)
    print("This post contains mostly:", ", ".join(mostly) if mostly else "Neutral")
#---------------Post Labeling--------------------------------------------
def main():
    post = input("Enter a post: ")
    if len(post) == 0 or post.isspace():
        print("Nothing to analyze.")
        return
    post_sequence = convert_to_sequence(post)
    analyze_text(post_sequence)
    scan_post(post_sequence)
#---------------Common Links--------------------------------------------
MENTION_SYMBOL = "@"
LINK_START = "https://"
VIDEO_LINK = "https://feta.tv/watch/"
#---------------Is Mention----------------------------------------------
def is_mention(word):
    if len(word) > 1 and word[0] == MENTION_SYMBOL:
        return True
    else:
        return False

def get_username(word):
    if is_mention(word):
        return word[1:]
    else:
        return None
#----------------Is Link----------------------------------------------
def is_link(word):
    start = word[0:8]
    if start == LINK_START:
        return True
    else:
        return False
#----------------Video Link Analysis------------------------------------
def get_video_id(link):
    if is_link(link):
        if link.startswith(VIDEO_LINK):
            vid_id = link.split("/")[-1]
            return vid_id
        else:
            return ""
    else:
        return  ""
#-------------------------------------------------------------------------
def report_list(label, items):
    if len(items) == 0:
        print(label + ": none")
    else:
        print(label + ":", ", ".join(items))
#---------------Mention, Link, and Video Scanning Function------------------------------------
def scan_post(post_sequence):
    mentions = []
    links = []
    videos = []
    for word in post_sequence:
        if is_mention(word):
            username = get_username(word)
            if username not in mentions:
                mentions.append(username)
        elif is_link(word):
            links.append(word)
            vid_id = get_video_id(word)
            if vid_id != "":
                videos.append(vid_id)
    print("-" * 30)
    print("Scan complete!")
    report_list("Mentions", mentions)
    report_list("Links", links)
    report_list("Videos", videos)
    print("-" * 30)
    return mentions, links, videos
#-------------------------------------------------------------------------
main()