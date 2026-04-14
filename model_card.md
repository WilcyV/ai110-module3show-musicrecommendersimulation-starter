# Model Card — VibeFinder 1.0

## Model Name
**VibeFinder 1.0** — a content-based music recommendation simulator.

---

## Goal / Task
VibeFinder predicts which songs from a catalog a user will enjoy, given their stated musical preferences (genre, mood, energy level, and other audio attributes). The system ranks every song in the dataset by a weighted relevance score and returns the top-K recommendations with human-readable explanations.

---

## Data Used

| Property | Detail |
|---|---|
| Dataset size | 50 songs |
| Source | Manually curated; attributes inspired by Spotify Audio Features API |
| Genres covered | Pop, Rock, Metal, Hip-Hop, Electronic, R&B, Lofi, Classical, Country, Latin |
| Numerical features | `energy` (0–1), `valence` (0–1), `danceability` (0–1), `acousticness` (0–1), `tempo_bpm` |
| Categorical features | `genre`, `mood` |

**Data limitations:**
- Only 50 songs — far too small for real-world use.
- Pop is overrepresented (~20% of catalog). Users who prefer pop have more variety; niche genre users (Latin, Classical) have very few genre matches to work with.
- Attributes were assigned manually, not extracted by audio analysis tools — they reflect judgment, not measurement.
- No time dimension: release year, trends, or seasonal listening patterns are ignored.

---

## Algorithm Summary

VibeFinder uses **content-based filtering**: it compares a user's taste profile directly against each song's attributes.

**Scoring a single song:**
1. Award +2.0 points if the song's genre matches the user's favorite genre.
2. Award +1.0 point if the song's mood matches the user's favorite mood.
3. Award up to +1.5 points for energy closeness: the nearer the song's energy is to the user's target, the more points.
4. Award up to +1.0 for valence (happiness) closeness.
5. Award up to +0.75 for danceability closeness.
6. Award up to +0.75 for acousticness closeness.
7. Sum all points. Maximum possible score = 7.0.

**Ranking:** All 50 songs are scored, then sorted highest-to-lowest. The top-K are returned.

No machine learning, no training data, no user history. The system is fully explainable — every recommendation comes with a reasons list showing exactly where each point came from.

---

## Observed Behavior and Biases

**1. Genre dominance — filter bubbles.**  
The +2.0 genre bonus is the single largest score component. A song with a genre match starts with a ~29% advantage. In practice this means users almost always get back songs in their stated genre, regardless of whether non-genre songs might actually be a better energy or mood fit. This is a classic **filter bubble**: the system reinforces existing preferences rather than surfacing discovery.

**2. Pop over-representation.**  
~20% of the catalog is pop. A pop user has 10 genre matches to rank, while a Classical user has only 3. Pop users receive more meaningful differentiation among their top results; Classical users quickly exhaust genre matches and the rankings become dominated by numerical similarity, occasionally pulling in stylistically unrelated songs with low energy.

**3. Conflicting preferences produce ambiguous results.**  
The edge-case profile (high energy + sad mood) reveals that the system cannot resolve contradictions. It awards full genre and mood bonuses, but the energy bonus is capped — so a medium-energy song that hits genre + mood often beats a high-energy song that hits genre only. The "right" answer is genuinely ambiguous, and the system has no way to learn which preference should take priority.

**4. Tempo is unused.**  
The `tempo_bpm` column is loaded but never scored. Users who care deeply about tempo (e.g., runners who need exactly 170 BPM) get no benefit from this data.

---

## Evaluation Process

Six user profiles were tested:

| Profile | Top Result | Surprise? |
|---|---|---|
| High-Energy Pop | Blinding Lights (The Weeknd) | No — strong genre + mood + energy alignment |
| Chill Lofi | Lofi Study Beat (Chillhop) | No — perfect 7.0 score |
| Deep Intense Rock | Seven Nation Army (White Stripes) | Slight — expected Enter Sandman (Metal) to score higher |
| Romantic R&B | Thinking About You (Frank Ocean) | No |
| Hype Hip-Hop | SICKO MODE (Travis Scott) | No |
| Edge Case (High Energy + Sad) | Save Your Tears (The Weeknd) | Yes — lower energy won because genre + mood = +3.0 |

**Weight-shift experiment:** Doubling energy weight (energy-first mode) slightly reordered Chill Lofi results but did not change the #1 result, suggesting energy proximity is already well-tuned for that profile.

**Genre-first mode experiment:** Tripling the genre weight locked in only genre-matching songs in the top 3 for every profile, confirming that genre weight is already the dominant factor even at 2.0.

---

## Intended Use

- **Educational simulation** of how content-based filtering works.
- Demonstrating trade-offs between explainability and accuracy.
- A starting point for adding collaborative filtering, user history, or ML components.

## Non-Intended Use

- Production music recommendations (dataset too small, attributes manually assigned).
- Making editorial or commercial decisions about songs or artists.
- Any use case requiring real-time data or user privacy considerations.

---

## Ideas for Improvement

1. **Add tempo scoring.** Use the existing `tempo_bpm` data with a proximity formula (e.g., reward songs within ±10 BPM of a target).
2. **Expand and balance the dataset.** Add 200+ songs with equal representation across all genres to reduce pop over-representation.
3. **Introduce a diversity penalty.** If 3 of the top 5 results are from the same artist, apply a -0.5 penalty per duplicate artist to increase variety.
4. **Learn weights from feedback.** Instead of fixed weights, allow the system to adjust them based on thumbs-up/thumbs-down signals using a simple gradient update.
5. **Hybrid filtering.** Combine content scores with a simple collaborative layer: find users with similar profiles and boost songs they rated highly.
