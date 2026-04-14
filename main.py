"""
main.py — Entry point for VibeFinder 1.0.

Run with:  python -m src.main
"""

from src.recommender import load_songs, recommend_songs, recommend_songs_mode


# ---------------------------------------------------------------------------
# User Profiles
# ---------------------------------------------------------------------------

PROFILES = {
    "High-Energy Pop": {
        "favorite_genre":       "pop",
        "favorite_mood":        "happy",
        "target_energy":        0.85,
        "target_valence":       0.80,
        "target_danceability":  0.88,
        "target_acousticness":  0.05,
    },
    "Chill Lofi": {
        "favorite_genre":       "lofi",
        "favorite_mood":        "calm",
        "target_energy":        0.25,
        "target_valence":       0.55,
        "target_danceability":  0.55,
        "target_acousticness":  0.80,
    },
    "Deep Intense Rock": {
        "favorite_genre":       "rock",
        "favorite_mood":        "intense",
        "target_energy":        0.90,
        "target_valence":       0.35,
        "target_danceability":  0.55,
        "target_acousticness":  0.05,
    },
    "Romantic R&B": {
        "favorite_genre":       "rnb",
        "favorite_mood":        "romantic",
        "target_energy":        0.45,
        "target_valence":       0.70,
        "target_danceability":  0.65,
        "target_acousticness":  0.25,
    },
    "Hype Hip-Hop": {
        "favorite_genre":       "hiphop",
        "favorite_mood":        "intense",
        "target_energy":        0.90,
        "target_valence":       0.30,
        "target_danceability":  0.85,
        "target_acousticness":  0.03,
    },
    # Adversarial / edge-case profile: conflicting high energy + sad mood
    "Edge Case (High Energy + Sad)": {
        "favorite_genre":       "pop",
        "favorite_mood":        "sad",
        "target_energy":        0.90,
        "target_valence":       0.20,
        "target_danceability":  0.60,
        "target_acousticness":  0.10,
    },
}


# ---------------------------------------------------------------------------
# Display Helpers
# ---------------------------------------------------------------------------

SEPARATOR = "─" * 62

def print_header(title: str) -> None:
    """Print a section header."""
    print(f"\n{'═' * 62}")
    print(f"  🎵  {title}")
    print(f"{'═' * 62}")


def print_recommendations(recs: list[dict], top_k: int = 5) -> None:
    """Pretty-print a ranked list of recommendations."""
    for rank, song in enumerate(recs[:top_k], start=1):
        print(f"\n  #{rank}  {song['title']}  —  {song['artist']}")
        print(f"       Genre: {song['genre'].title()} | Mood: {song['mood'].title()} | "
              f"Energy: {song['energy']}")
        print(f"       Score: {song['score']}")
        print(f"       Why:   {' | '.join(song['reasons'])}")
        print(f"       {SEPARATOR}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    songs = load_songs()
    print(f"\nLoaded songs: {len(songs)}")

    # ── Run each profile ──────────────────────────────────────────────────
    for profile_name, prefs in PROFILES.items():
        print_header(f"Profile: {profile_name}")
        recs = recommend_songs(prefs, songs, k=5)
        print_recommendations(recs)

    # ── Mode comparison (High-Energy Pop) ─────────────────────────────────
    print_header("Mode Comparison — 'High-Energy Pop' profile")
    for mode in ["default", "genre_first", "energy_first"]:
        print(f"\n  ◆ Mode: {mode.upper()}")
        recs = recommend_songs_mode(PROFILES["High-Energy Pop"], songs, k=3, mode=mode)
        for rank, song in enumerate(recs, 1):
            print(f"    #{rank} {song['title']} (score: {song['score']})")

    # ── Weight-shift experiment ────────────────────────────────────────────
    print_header("Experiment — Energy-first mode vs Default (Chill Lofi profile)")
    prefs = PROFILES["Chill Lofi"]
    print("\n  Default weights:")
    for r, s in enumerate(recommend_songs(prefs, songs, k=3), 1):
        print(f"    #{r} {s['title']} — score {s['score']}")
    print("\n  Energy-first mode:")
    for r, s in enumerate(recommend_songs_mode(prefs, songs, k=3, mode="energy_first"), 1):
        print(f"    #{r} {s['title']} — score {s['score']}")


if __name__ == "__main__":
    main()
