"""
tests/test_recommender.py — Unit tests for VibeFinder 1.0.

Run with:  python -m pytest tests/ -v
"""

import pytest
from src.recommender import load_songs, score_song, recommend_songs


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

POP_HAPPY_USER = {
    "favorite_genre":       "pop",
    "favorite_mood":        "happy",
    "target_energy":        0.80,
    "target_valence":       0.80,
    "target_danceability":  0.85,
    "target_acousticness":  0.05,
}

ROCK_INTENSE_USER = {
    "favorite_genre":       "rock",
    "favorite_mood":        "intense",
    "target_energy":        0.90,
    "target_valence":       0.30,
    "target_danceability":  0.55,
    "target_acousticness":  0.05,
}

SAMPLE_SONG_POP = {
    "title": "Test Pop Song",
    "artist": "Test Artist",
    "genre": "pop",
    "mood": "happy",
    "energy": 0.80,
    "tempo_bpm": 120,
    "valence": 0.80,
    "danceability": 0.85,
    "acousticness": 0.05,
}

SAMPLE_SONG_ROCK = {
    "title": "Test Rock Song",
    "artist": "Test Artist",
    "genre": "rock",
    "mood": "intense",
    "energy": 0.90,
    "tempo_bpm": 130,
    "valence": 0.30,
    "danceability": 0.55,
    "acousticness": 0.05,
}


# ---------------------------------------------------------------------------
# load_songs tests
# ---------------------------------------------------------------------------

def test_load_songs_returns_list():
    songs = load_songs()
    assert isinstance(songs, list)


def test_load_songs_not_empty():
    songs = load_songs()
    assert len(songs) > 0


def test_load_songs_have_required_keys():
    songs = load_songs()
    required_keys = {"title", "artist", "genre", "mood", "energy",
                     "tempo_bpm", "valence", "danceability", "acousticness"}
    for song in songs:
        assert required_keys.issubset(song.keys()), f"Song missing keys: {song}"


def test_load_songs_numeric_fields_are_numbers():
    songs = load_songs()
    for song in songs:
        assert isinstance(song["energy"], float)
        assert isinstance(song["valence"], float)
        assert isinstance(song["danceability"], float)
        assert isinstance(song["tempo_bpm"], int)


# ---------------------------------------------------------------------------
# score_song tests
# ---------------------------------------------------------------------------

def test_score_song_returns_tuple():
    result = score_song(POP_HAPPY_USER, SAMPLE_SONG_POP)
    assert isinstance(result, tuple)
    assert len(result) == 2


def test_score_song_genre_match_gives_higher_score():
    score_match, _ = score_song(POP_HAPPY_USER, SAMPLE_SONG_POP)
    score_no_match, _ = score_song(POP_HAPPY_USER, SAMPLE_SONG_ROCK)
    assert score_match > score_no_match


def test_score_song_mood_match_contributes_to_score():
    happy_song = dict(SAMPLE_SONG_POP)
    sad_song = dict(SAMPLE_SONG_POP, mood="sad")
    score_happy, _ = score_song(POP_HAPPY_USER, happy_song)
    score_sad, _ = score_song(POP_HAPPY_USER, sad_song)
    assert score_happy > score_sad


def test_score_song_reasons_is_list_of_strings():
    _, reasons = score_song(POP_HAPPY_USER, SAMPLE_SONG_POP)
    assert isinstance(reasons, list)
    assert all(isinstance(r, str) for r in reasons)


def test_score_song_reasons_mention_genre_when_matched():
    _, reasons = score_song(POP_HAPPY_USER, SAMPLE_SONG_POP)
    assert any("genre match" in r for r in reasons)


def test_score_song_reasons_mention_mood_when_matched():
    _, reasons = score_song(POP_HAPPY_USER, SAMPLE_SONG_POP)
    assert any("mood match" in r for r in reasons)


def test_score_song_energy_proximity_rewards_closeness():
    close_song = dict(SAMPLE_SONG_POP, energy=0.80, genre="jazz", mood="dark")
    far_song   = dict(SAMPLE_SONG_POP, energy=0.10, genre="jazz", mood="dark")
    score_close, _ = score_song(POP_HAPPY_USER, close_song)
    score_far, _   = score_song(POP_HAPPY_USER, far_song)
    assert score_close > score_far


def test_score_song_is_non_negative():
    songs = load_songs()
    for song in songs:
        score, _ = score_song(POP_HAPPY_USER, song)
        assert score >= 0


# ---------------------------------------------------------------------------
# recommend_songs tests
# ---------------------------------------------------------------------------

def test_recommend_songs_returns_list():
    songs = load_songs()
    recs = recommend_songs(POP_HAPPY_USER, songs, k=5)
    assert isinstance(recs, list)


def test_recommend_songs_respects_k():
    songs = load_songs()
    for k in [1, 3, 5, 10]:
        recs = recommend_songs(POP_HAPPY_USER, songs, k=k)
        assert len(recs) == k


def test_recommend_songs_sorted_descending():
    songs = load_songs()
    recs = recommend_songs(POP_HAPPY_USER, songs, k=10)
    scores = [r["score"] for r in recs]
    assert scores == sorted(scores, reverse=True)


def test_recommend_songs_does_not_mutate_original():
    songs = load_songs()
    original_count = len(songs)
    recommend_songs(POP_HAPPY_USER, songs, k=5)
    assert len(songs) == original_count
    assert "score" not in songs[0]


def test_recommend_songs_results_have_score_and_reasons():
    songs = load_songs()
    recs = recommend_songs(POP_HAPPY_USER, songs, k=3)
    for rec in recs:
        assert "score" in rec
        assert "reasons" in rec


def test_recommend_different_profiles_give_different_results():
    songs = load_songs()
    pop_recs  = recommend_songs(POP_HAPPY_USER, songs, k=1)
    rock_recs = recommend_songs(ROCK_INTENSE_USER, songs, k=1)
    assert pop_recs[0]["title"] != rock_recs[0]["title"]
