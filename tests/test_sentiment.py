from sentiment_analysis import analyze_sentiment


def test_analyze_sentiment_basic():
    reviews = [
        "I absolutely loved this film, it was fantastic and inspiring!",
        "It was okay, not great but not terrible either.",
        "I hated the pacing and the acting was awful.",
    ]
    sentiments, positive, neutral, negative, scores, pos_kw, neg_kw = analyze_sentiment(reviews)

    assert sentiments["positive"] == 1
    assert sentiments["neutral"] == 1
    assert sentiments["negative"] == 1
    assert len(scores) == 3
    # Ensure keywords extraction returns tuples
    assert isinstance(pos_kw, list)
    assert isinstance(neg_kw, list)
