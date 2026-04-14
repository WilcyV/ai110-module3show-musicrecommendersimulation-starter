# Reflection — VibeFinder 1.0

## Profile Comparisons

### High-Energy Pop vs. Chill Lofi
These are nearly opposite profiles in every dimension. The pop profile targets energy ~0.85, danceability ~0.88, and acousticness ~0.05; the lofi profile targets energy ~0.25, danceability ~0.55, and acousticness ~0.80. The results reflect this cleanly — the pop profile returns uptempo radio hits while the lofi profile returns ambient Chillhop tracks. What's interesting is that both profiles return a "perfect" or near-perfect score for their #1 result (pop: 6.853, lofi: 7.0), yet these are completely different songs. This makes sense: the scoring system is relative to the user, not absolute. A score of 7.0 just means "this song matches your profile as closely as possible given our dataset."

### Deep Intense Rock vs. Hype Hip-Hop
Both profiles want high energy (~0.90) and low valence (~0.30), but they differ in genre and danceability. The rock profile returns classic and alternative rock, while the hip-hop profile returns trap and rap. The interesting observation is that without the genre match, these profiles would likely overlap — many hip-hop and rock tracks share similar energy and valence. This shows that genre is doing a lot of heavy lifting in separating these two profiles.

### Romantic R&B vs. Edge Case (High Energy + Sad)
The R&B profile is internally consistent and the system handles it well. The edge-case profile is deliberately conflicted. The R&B user gets Frank Ocean and Childish Gambino — exactly right. The edge-case user gets "Save Your Tears" as #1 (medium energy, sad pop), which is a reasonable compromise but not fully satisfying for either preference. The system cannot hold two contradictory preferences in tension and simply awards points for both, meaning the song that hits genre + mood wins even if its energy is wrong. A real system might ask the user to clarify, or weight preferences by explicitly stated importance.

---

## Personal Reflection

**Biggest learning moment:** The genre dominance problem. I set the genre weight to +2.0 thinking it was "reasonable," but after running the experiments I realized it almost always controls the outcome. A song with a genre match and mediocre everything else will beat a song without a genre match but perfect energy, valence, and danceability. This taught me that weight design is genuinely hard — intuition is not enough. You need to actually run the numbers and test edge cases to see how weights interact.

**How AI tools helped — and when I checked them:** AI was most helpful for structuring the scoring logic quickly and generating the 50-song dataset in valid CSV format in one shot. I did have to verify the logic for the "no mutation" requirement — my first instinct was to sort the original list in place with `.sort()`, which would have modified the caller's data. Thinking through the `sorted()` vs `.sort()` distinction was an important correctness check that the AI framed well but I needed to verify in my own code.

**What surprised me about simple algorithms:** The fact that a system with just 6 weighted rules and 50 songs produces recommendations that "feel" like real music suggestions was surprising. When the Chill Lofi profile returns Lofi Study Beat and Coffee Shop Vibes — that's genuinely what I would put on a quiet study session. The algorithm isn't smart; it's just matching numbers. But because those numbers encode something real about acoustic characteristics, the output feels intelligent. This was my first concrete experience of the gap between "this is just arithmetic" and "this feels like AI."

**What I'd try next:** I'd add a diversity penalty to prevent the same artist from appearing multiple times in the top 5 (Chillhop appears 4 times in the lofi profile's top results). I'd also experiment with using cosine similarity across all numerical features at once rather than summing individual proximity scores — this would treat the song's attributes as a vector and find songs geometrically close to the user's preference vector, which is closer to how real recommendation engines work.
