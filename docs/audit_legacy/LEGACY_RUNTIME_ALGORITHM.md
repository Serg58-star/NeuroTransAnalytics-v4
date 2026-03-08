# Legacy Runtime Algorithm

## 1. System Overview

The legacy Visual Reaction Time (СЗР) testing system is a Delphi-based Windows application consisting of three sequential testing batteries:

1. **Simple Visual Reaction Time (PZR / Tst1)**: Evaluates baseline sensory-motor transmission (V1 pathway).
2. **Color Reaction Time (Tst2)**: Evaluates acetylcholine-dominant differentiation (ΔV4 pathway). Subject reacts exclusively to red stimuli among distractors.
3. **Shift Reaction Time (Tst3)**: Evaluates dopamine-dominant motion detection (ΔV5/MT pathway). Subject reacts to sudden spatial displacement of a stimulus among static circles.

The system enforces highly deterministic experimental conditions, dictating identical pseudo-random stimulus parameters (position, color, pre-stimulus intervals) across all subjects, ensuring strict reproducability.

## 2. Runtime State Machine

The core execution flow of the application follows a rigid state machine:

```
[INIT]
  |-- Load subject demographic data (from `users.xlsx/mdb`)
  v
[LOAD_CONFIG]
  |-- Parse `config.ini` for Test parameters (Timers, rotations, sequences)
  |-- Load deterministic test matrix (Color, Position, PSI)
  v
[WARMUP]
  |-- Execute 3 non-scored trials (NoUchtPOKAZ_COUNT = 3).
  |-- Results are discarded (not saved to `boxbase`).
  v
[TRIAL_LOOP] (For trial = 1 to 36)
  |
  |--> [WAIT_PSI]
  |      |-- Hold blank/neutral screen for prescribed Pre-Stimulus Interval (e.g. 1045ms).
  |      v
  |--> [SHOW_STIMULUS / START_TIMER]
  |      |-- Render visual stimuli (Color Tst: flashed array; Shift Tst: displacement).
  |      |-- Begin millisecond hardware/OS timer.
  |      v
  |--> [WAIT_RESPONSE]
  |      |-- Monitor hardware interrupts (mouse/keyboard).
  |      |-- Break on input OR timeout (`MaxRedLight` = 2000ms).
  |      v
  |--> [REGISTER_RESPONSE]
  |      |-- Calculate RT = InputTime - StimulusTime.
  |      |-- Categorize: Validity vs. Early (< `MinRedLight`) vs. Late (> `MaxRedLight`).
  |      v
  |--> [OUTLIER_EVALUATION]
  |      |-- Append valid RT to rolling stats.
  |      |-- Calculate sample Coefficient of Variation (CV).
  |      |-- If CV > target (15-20%), flag trial as invalid, queue repeat trial.
  |      |-- Loop continues until 36 strictly valid responses are captured.
  |      v
  |--> [NEXT_TRIAL]
         |-- Advance configuration index.
  v
[END_TEST]
  |-- Compute aggregate statistics (Mean, SD).
  |-- Pack data vector and flush to `boxbase` repository.
```

## 3. Stimulus Generation

Stimuli are rigidly pre-configured per trial step (1-36).

* **Target Size**: Fixed at 7 cm diameter on screen.
* **Positions**: Left, Center, Right. (Tst1 uses horizontal midline. Tst2/Tst3 form a triangle: left/right bottom corners + center top edge).
* **Colors**: Red (`К`), Green (`Ж`), Blue (`С`).
* **Color Test Pattern (Tst2)**: Sequences of colored circles are flashed (e.g., "ЖЖС ЖСЖ"). Target is always the Red (`К`) appearance.
* **Shift Test Pattern (Tst3)**: Arrays denote background configurations. The target dynamically "shifts" 50ms toward the midline and returns. Indices indicate moving target (0=None, 1=Left, 2=Center, 3=Right).

## 4. Timing System

Configuration is driven by values present in `config_timing_parameters.md` and hardcoded limits:

* **Pre-Stimulus Interval (PSI)**: Extracted directly from the design matrix (ranging ~800ms to 2800ms). It is the deterministic delay between the readiness state and stimulus onset.
* **`MinRedLight`**: `135` ms. Any response under this latency is logged as a premature reaction (`RANO_POKAZ`).
* **`MaxRedLight`**: `2000` ms. A timeout. The stimulus extinguishes, logged as omission/late (`POZDNO_POKAZ`).
* **`ROTATE_PERIOD`**: `400` ms. Used in Tst2/Tst3 as the flashing or state-rotation period for complex stimulus arrays.

## 5. Response Handling

* Input is registered via system API hooks (KeyDown/MouseDown intercepts).
* If `Reaction Time (RT) < MinRedLight (135ms)`: Trial is discarded from the main sequence, `RANO_POKAZ_N` counter is incremented.
* If `Reaction Time (RT) > MaxRedLight (2000ms)`: Trial is discarded from the main sequence, `POZDNO_POKAZ_N` counter is incremented.
* Valid RTs (`135 <= RT <= 2000`) proceed to outlier evaluation.

## 6. Result Recording

The output format maps directly to the `boxbase` fields indicating a flat vector insertion upon test completion:

* `TstX_1` through `TstX_36`: The 36 valid reaction times chronologically.
* `RANO_POKAZ_X` (Early count).
* `POZDNO_POKAZ_X` (Late/Omission count).
* `result_X`: The calculated mean of the 36 trials.
* `SrKvadrOtkl_X`: The calculated Standard Deviation (SD) of the 36 trials.

## 7. Outlier Handling (CV Stabilization)

A unique aspect of the legacy system is its dynamic CV-capping loop.
Rather than removing outliers post-hoc, the runtime evaluates the Coefficient of Variation, `CV = (SD / Mean) * 100`, continuously.
If a newly captured RT causes the sample CV to exceed the programmed tolerance (historically 15% - 20%), the reaction is discarded. To ensure the database array has exactly 36 responses, the identical trial configuration (same position, color, PSI) is queued as a repeat trial, effectively extending the physical length of the session until 36 "stable" normative reactions are captured.

## 8. Formal Algorithm (Pseudocode)

```pascal
procedure RunVisualTest(TestType: Integer);
var
  TrialIndex: Integer;
  ValidTrialsCaptured: Integer;
  Config: TrialConfig;
  RT: Integer;
  EarlyCount, LateCount: Integer;
  RTArray: Array[1..36] of Integer;
begin
  ValidTrialsCaptured := 0;
  EarlyCount := 0;
  LateCount := 0;
  
  // Warmup Phase
  for TrialIndex := 1 to 3 do
  begin
    Config := LoadWarmupConfig(TestType, TrialIndex);
    Wait(Config.PSI);
    DrawStimulus(Config);
    WaitForReaction(); // Result discarded
  end;

  // Main Scoring Phase
  TrialIndex := 1;
  while ValidTrialsCaptured < 36 do
  begin
    Config := LoadTrialConfig(TestType, TrialIndex); // Design Matrix Rule
    
    ClearScreen();
    Wait(Config.PSI);
    
    DrawStimulus(Config);
    StartHardwareTimer();
    
    // Polling loop
    RT := 0;
    while (TimerValue() <= MaxRedLight) do
    begin
        if InputDetected() then
        begin
            RT := TimerValue();
            break;
        end;
    end;
    
    // Evaluation Logic
    if (RT = 0) or (RT > MaxRedLight) then // Timeout
    begin
        LateCount := LateCount + 1;
        // Trial failed, must repeat
    end
    else if (RT < MinRedLight) then // Premature ( < 135 ms)
    begin
        EarlyCount := EarlyCount + 1;
        // Trial failed, must repeat
    end
    else
    begin
        // Provisional validity
        TestArray := Append(RTArray, RT);
        CurrentCV := CalculateCV[TestArray];
        
        if (CurrentCV > CV_THRESHOLD) then
        begin
            // Outlier rejection. 
            // Do not permanently save RT. 
            // Loop repeats this TrialIndex to re-roll.
        end
        else
        begin
            // Strictly Valid
            ValidTrialsCaptured := ValidTrialsCaptured + 1;
            RTArray[ValidTrialsCaptured] := RT;
            TrialIndex := TrialIndex + 1; // Advance configuration matrix
        end;
    end;
  end;
  
  // Terminal calculation
  MeanRT := CalculateMean(RTArray);
  SDRT := CalculateSD(RTArray);
  
  // Emit to database
  WriteToBoxBase(TestType, RTArray, MeanRT, SDRT, EarlyCount, LateCount);
end;
```

---

## 9. Verification Assertions

1️⃣ **Какие элементы алгоритма подтверждены документами:**

* The rigid use of exactly 36 valid indices per test (`POKAZ_COUNT = 36`).
* The exact thresholds for premature/late hits (`MinRedLight = 135`, `MaxRedLight = 2000`).
* The use of fixed configuration sequences controlling fields 1 through 36 per test type including Pos, Color, PSI, and Distractor sequences.
* The discard of 3 unrecorded warmup sequences (`NoUchtPOKAZ_COUNT = 3`).
* The target calculation fields (`TstX_1..36`, `result_X`, `SrKvadrOtkl_X`).

2️⃣ **Какие элементы реконструированы косвенно:**

* The exact step-by-step looping logic for handling the CV repeats. While `Appendix_A` explicitly describes the *policy* ("unending tests providing repeat trials in same positions with same specs until variance bounds are satisfied"), the exact point in the while-loop where the repeat trigger is hooked was mapped conceptually into the pseudocode.
* The API timer polling logic (Delphi `GetTickCount` / event handlers are typical, reconstructed as conceptual `InputDetected()`).

3️⃣ **Какие элементы остаются неизвестными:**

* The precise, bitwise PRNG seeding formula originally used to choose the 3 warmup scenarios out of the "10 preconfigured variants".
* The exact mathematical floating-point rounding behaviour used in the legacy Delphi `CalculateCV` threshold gating compared to Python 3.11 `float` capabilities.
