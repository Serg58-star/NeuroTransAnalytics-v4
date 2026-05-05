# Stage G — Legacy Stimulus Ecology Investigation Report

This document answers the core functional questions regarding the legacy stimulus environment. The analysis was conducted against the historical empirical dataset to inform the architecture constraints for **Stimulus Generator v5** and **Phase F2**.

---

## Вопрос 1: Как устроена стимульная среда legacy-протокола?

The legacy system utilized all 27 mathematical permutations of context triples but distributed them with severe bias.

- **Domination:** The environment was heavily saturated with Blue (С) and Green (Ж) elements. The top 5 triples (СЖС, ЖСЖ, ССЖ, ЖЖС, КЖС) accounted for over 50% of the entire visual sequence.
- **Red Scarcity:** Triples heavily featuring Red (ККК, КСС, КЖК) appeared less than 1% of the time, making Red stimuli pop out structurally rather than functioning as neutral noise.
- **Complexity:** The environment maintained a high baseline of spectral noise. 77.6% of generated triples had High complexity (heterogeneous colors), and 0% were monochromatic (AAA type).

---

## Вопрос 2: Как legacy-протокол стимулирует зрительные каналы?

The baseline masking sequences overloaded the lateral channels while systematically under-utilizing the central contrast channel.

- **Channel Means:** P-channel ($\text{mean} = 6.51$), K-channel ($\text{mean} = 6.75$), R-channel ($\text{mean} = 2.83$).
- **Unequal Targeting:** Target detection (Red signal) was inherently preceded by a structurally distinct channel load ($P=18.0, K=20.0$) compared to Shift detection ($P=21.0, K=21.0$). The legacy protocol involuntarily pre-conditioned patients with different sensory loads depending on the upcoming explicit target type.

---

## Вопрос 3: Формирует ли протокол адаптационную динамику?

**Yes.** The protocol exhibited massive "channel inertia" rather than random sequence behavior.

- **State Transition:**
  - A Blue-dominant triple had a $77.3\%$ probability of being followed by another Blue-dominant triple.
  - A Green-dominant triple had a $76.2\%$ probability of repeating.
- **Consequence:** The legacy environment created long un-interrupted sequences of unilateral channel activation, forcibly inducing sensory adaptation and suppression rather than maintaining neutral baseline readiness.
- **Slow Waves:** A moving average analysis over a 12-stimulus window confirmed non-stationary drift across the block, meaning the baseline difficulty drifted independently of patient state.

---

## Вопрос 4: Как формируется когнитивная нагрузка?

Cognitive load in the legacy architecture was completely entangled with temporal variables.

- **PSI-Context Coupling:** Spearman $\rho(\text{PSI}, \text{Total Masking Load}) = 0.998$. The length of the Pre-Stimulus Interval directly determined the total number of masking elements.
- **Consequence for v5:** Slower reaction-time readiness (linked to longer PSI) was involuntarily paired with massive accumulated sensory noise (P-load and K-load). This confirms that "baseline recovery" in the legacy system was structurally impossible because longer wait times equaled monotonically heavier channel exhaustion.

---

## Архитектурный вывод для Generator v5 и Phase F2

The execution of Tasks A-J confirms that the legacy generator was highly non-orthogonal. It mapped the patient's state onto three massive contextual clusters:

1. **Cluster 0 (39%):** High masking saturation with long PSI intervals.
2. **Cluster 1 (33%):** Brief periods of high complexity structural noise with short PSI.
3. **Cluster 2 (28%):** Lower complexity, high visual contrast sequences.

**Mandate for v5:**

1. The new Stimulus Generator **must mathematically decouple** PSI duration from Masking Volume.
2. Channel load (P, K, R) must be explicitly managed, not left to artifactual distribution that clusters Blue/Green to the detriment of Red.
3. If sequence inertia (sticky channel states) is required for adaptation stress, it must be an explicit, controllable meta-parameter (`adaptation_run_length`), not a hidden Markov drift.
