DROP VIEW IF EXISTS reactions_view;
CREATE VIEW reactions_view AS
WITH
unpivoted_tst1 AS (
    SELECT trial_id, subject_id, 1 AS stimulus_index, tst1_1 AS rt, 'simple' AS test_type FROM trials UNION ALL
    SELECT trial_id, subject_id, 2 AS stimulus_index, tst1_2 AS rt, 'simple' AS test_type FROM trials UNION ALL
    SELECT trial_id, subject_id, 3 AS stimulus_index, tst1_3 AS rt, 'simple' AS test_type FROM trials UNION ALL
    SELECT trial_id, subject_id, 4 AS stimulus_index, tst1_4 AS rt, 'simple' AS test_type FROM trials UNION ALL
    SELECT trial_id, subject_id, 5 AS stimulus_index, tst1_5 AS rt, 'simple' AS test_type FROM trials UNION ALL
    SELECT trial_id, subject_id, 6 AS stimulus_index, tst1_6 AS rt, 'simple' AS test_type FROM trials UNION ALL
    SELECT trial_id, subject_id, 7 AS stimulus_index, tst1_7 AS rt, 'simple' AS test_type FROM trials UNION ALL
    SELECT trial_id, subject_id, 8 AS stimulus_index, tst1_8 AS rt, 'simple' AS test_type FROM trials UNION ALL
    SELECT trial_id, subject_id, 9 AS stimulus_index, tst1_9 AS rt, 'simple' AS test_type FROM trials UNION ALL
    SELECT trial_id, subject_id, 10 AS stimulus_index, tst1_10 AS rt, 'simple' AS test_type FROM trials UNION ALL
    SELECT trial_id, subject_id, 11 AS stimulus_index, tst1_11 AS rt, 'simple' AS test_type FROM trials UNION ALL
    SELECT trial_id, subject_id, 12 AS stimulus_index, tst1_12 AS rt, 'simple' AS test_type FROM trials UNION ALL
    SELECT trial_id, subject_id, 13 AS stimulus_index, tst1_13 AS rt, 'simple' AS test_type FROM trials UNION ALL
    SELECT trial_id, subject_id, 14 AS stimulus_index, tst1_14 AS rt, 'simple' AS test_type FROM trials UNION ALL
    SELECT trial_id, subject_id, 15 AS stimulus_index, tst1_15 AS rt, 'simple' AS test_type FROM trials UNION ALL
    SELECT trial_id, subject_id, 16 AS stimulus_index, tst1_16 AS rt, 'simple' AS test_type FROM trials UNION ALL
    SELECT trial_id, subject_id, 17 AS stimulus_index, tst1_17 AS rt, 'simple' AS test_type FROM trials UNION ALL
    SELECT trial_id, subject_id, 18 AS stimulus_index, tst1_18 AS rt, 'simple' AS test_type FROM trials UNION ALL
    SELECT trial_id, subject_id, 19 AS stimulus_index, tst1_19 AS rt, 'simple' AS test_type FROM trials UNION ALL
    SELECT trial_id, subject_id, 20 AS stimulus_index, tst1_20 AS rt, 'simple' AS test_type FROM trials UNION ALL
    SELECT trial_id, subject_id, 21 AS stimulus_index, tst1_21 AS rt, 'simple' AS test_type FROM trials UNION ALL
    SELECT trial_id, subject_id, 22 AS stimulus_index, tst1_22 AS rt, 'simple' AS test_type FROM trials UNION ALL
    SELECT trial_id, subject_id, 23 AS stimulus_index, tst1_23 AS rt, 'simple' AS test_type FROM trials UNION ALL
    SELECT trial_id, subject_id, 24 AS stimulus_index, tst1_24 AS rt, 'simple' AS test_type FROM trials UNION ALL
    SELECT trial_id, subject_id, 25 AS stimulus_index, tst1_25 AS rt, 'simple' AS test_type FROM trials UNION ALL
    SELECT trial_id, subject_id, 26 AS stimulus_index, tst1_26 AS rt, 'simple' AS test_type FROM trials UNION ALL
    SELECT trial_id, subject_id, 27 AS stimulus_index, tst1_27 AS rt, 'simple' AS test_type FROM trials UNION ALL
    SELECT trial_id, subject_id, 28 AS stimulus_index, tst1_28 AS rt, 'simple' AS test_type FROM trials UNION ALL
    SELECT trial_id, subject_id, 29 AS stimulus_index, tst1_29 AS rt, 'simple' AS test_type FROM trials UNION ALL
    SELECT trial_id, subject_id, 30 AS stimulus_index, tst1_30 AS rt, 'simple' AS test_type FROM trials UNION ALL
    SELECT trial_id, subject_id, 31 AS stimulus_index, tst1_31 AS rt, 'simple' AS test_type FROM trials UNION ALL
    SELECT trial_id, subject_id, 32 AS stimulus_index, tst1_32 AS rt, 'simple' AS test_type FROM trials UNION ALL
    SELECT trial_id, subject_id, 33 AS stimulus_index, tst1_33 AS rt, 'simple' AS test_type FROM trials UNION ALL
    SELECT trial_id, subject_id, 34 AS stimulus_index, tst1_34 AS rt, 'simple' AS test_type FROM trials UNION ALL
    SELECT trial_id, subject_id, 35 AS stimulus_index, tst1_35 AS rt, 'simple' AS test_type FROM trials UNION ALL
    SELECT trial_id, subject_id, 36 AS stimulus_index, tst1_36 AS rt, 'simple' AS test_type FROM trials
),
reactions_tst1 AS (
    SELECT u.trial_id, u.subject_id, u.test_type, u.stimulus_index, u.rt, m.position AS field, m.psi_ms AS psi, m.color 
    FROM unpivoted_tst1 u 
    JOIN metadata_simple m ON u.stimulus_index = m.stimulus_id 
    WHERE u.rt IS NOT NULL AND u.rt > 0
),
unpivoted_tst2 AS (
    SELECT trial_id, subject_id, 1 AS stimulus_index, tst2_1 AS rt, 'shift' AS test_type FROM trials UNION ALL
    SELECT trial_id, subject_id, 2 AS stimulus_index, tst2_2 AS rt, 'shift' AS test_type FROM trials UNION ALL
    SELECT trial_id, subject_id, 3 AS stimulus_index, tst2_3 AS rt, 'shift' AS test_type FROM trials UNION ALL
    SELECT trial_id, subject_id, 4 AS stimulus_index, tst2_4 AS rt, 'shift' AS test_type FROM trials UNION ALL
    SELECT trial_id, subject_id, 5 AS stimulus_index, tst2_5 AS rt, 'shift' AS test_type FROM trials UNION ALL
    SELECT trial_id, subject_id, 6 AS stimulus_index, tst2_6 AS rt, 'shift' AS test_type FROM trials UNION ALL
    SELECT trial_id, subject_id, 7 AS stimulus_index, tst2_7 AS rt, 'shift' AS test_type FROM trials UNION ALL
    SELECT trial_id, subject_id, 8 AS stimulus_index, tst2_8 AS rt, 'shift' AS test_type FROM trials UNION ALL
    SELECT trial_id, subject_id, 9 AS stimulus_index, tst2_9 AS rt, 'shift' AS test_type FROM trials UNION ALL
    SELECT trial_id, subject_id, 10 AS stimulus_index, tst2_10 AS rt, 'shift' AS test_type FROM trials UNION ALL
    SELECT trial_id, subject_id, 11 AS stimulus_index, tst2_11 AS rt, 'shift' AS test_type FROM trials UNION ALL
    SELECT trial_id, subject_id, 12 AS stimulus_index, tst2_12 AS rt, 'shift' AS test_type FROM trials UNION ALL
    SELECT trial_id, subject_id, 13 AS stimulus_index, tst2_13 AS rt, 'shift' AS test_type FROM trials UNION ALL
    SELECT trial_id, subject_id, 14 AS stimulus_index, tst2_14 AS rt, 'shift' AS test_type FROM trials UNION ALL
    SELECT trial_id, subject_id, 15 AS stimulus_index, tst2_15 AS rt, 'shift' AS test_type FROM trials UNION ALL
    SELECT trial_id, subject_id, 16 AS stimulus_index, tst2_16 AS rt, 'shift' AS test_type FROM trials UNION ALL
    SELECT trial_id, subject_id, 17 AS stimulus_index, tst2_17 AS rt, 'shift' AS test_type FROM trials UNION ALL
    SELECT trial_id, subject_id, 18 AS stimulus_index, tst2_18 AS rt, 'shift' AS test_type FROM trials UNION ALL
    SELECT trial_id, subject_id, 19 AS stimulus_index, tst2_19 AS rt, 'shift' AS test_type FROM trials UNION ALL
    SELECT trial_id, subject_id, 20 AS stimulus_index, tst2_20 AS rt, 'shift' AS test_type FROM trials UNION ALL
    SELECT trial_id, subject_id, 21 AS stimulus_index, tst2_21 AS rt, 'shift' AS test_type FROM trials UNION ALL
    SELECT trial_id, subject_id, 22 AS stimulus_index, tst2_22 AS rt, 'shift' AS test_type FROM trials UNION ALL
    SELECT trial_id, subject_id, 23 AS stimulus_index, tst2_23 AS rt, 'shift' AS test_type FROM trials UNION ALL
    SELECT trial_id, subject_id, 24 AS stimulus_index, tst2_24 AS rt, 'shift' AS test_type FROM trials UNION ALL
    SELECT trial_id, subject_id, 25 AS stimulus_index, tst2_25 AS rt, 'shift' AS test_type FROM trials UNION ALL
    SELECT trial_id, subject_id, 26 AS stimulus_index, tst2_26 AS rt, 'shift' AS test_type FROM trials UNION ALL
    SELECT trial_id, subject_id, 27 AS stimulus_index, tst2_27 AS rt, 'shift' AS test_type FROM trials UNION ALL
    SELECT trial_id, subject_id, 28 AS stimulus_index, tst2_28 AS rt, 'shift' AS test_type FROM trials UNION ALL
    SELECT trial_id, subject_id, 29 AS stimulus_index, tst2_29 AS rt, 'shift' AS test_type FROM trials UNION ALL
    SELECT trial_id, subject_id, 30 AS stimulus_index, tst2_30 AS rt, 'shift' AS test_type FROM trials UNION ALL
    SELECT trial_id, subject_id, 31 AS stimulus_index, tst2_31 AS rt, 'shift' AS test_type FROM trials UNION ALL
    SELECT trial_id, subject_id, 32 AS stimulus_index, tst2_32 AS rt, 'shift' AS test_type FROM trials UNION ALL
    SELECT trial_id, subject_id, 33 AS stimulus_index, tst2_33 AS rt, 'shift' AS test_type FROM trials UNION ALL
    SELECT trial_id, subject_id, 34 AS stimulus_index, tst2_34 AS rt, 'shift' AS test_type FROM trials UNION ALL
    SELECT trial_id, subject_id, 35 AS stimulus_index, tst2_35 AS rt, 'shift' AS test_type FROM trials UNION ALL
    SELECT trial_id, subject_id, 36 AS stimulus_index, tst2_36 AS rt, 'shift' AS test_type FROM trials
),
reactions_tst2 AS (
    SELECT u.trial_id, u.subject_id, u.test_type, u.stimulus_index, u.rt, m.position AS field, m.psi_ms AS psi, m.color 
    FROM unpivoted_tst2 u 
    JOIN metadata_shift m ON u.stimulus_index = m.stimulus_id 
    WHERE u.rt IS NOT NULL AND u.rt > 0
),
unpivoted_tst3 AS (
    SELECT trial_id, subject_id, 1 AS stimulus_index, tst3_1 AS rt, 'color' AS test_type FROM trials UNION ALL
    SELECT trial_id, subject_id, 2 AS stimulus_index, tst3_2 AS rt, 'color' AS test_type FROM trials UNION ALL
    SELECT trial_id, subject_id, 3 AS stimulus_index, tst3_3 AS rt, 'color' AS test_type FROM trials UNION ALL
    SELECT trial_id, subject_id, 4 AS stimulus_index, tst3_4 AS rt, 'color' AS test_type FROM trials UNION ALL
    SELECT trial_id, subject_id, 5 AS stimulus_index, tst3_5 AS rt, 'color' AS test_type FROM trials UNION ALL
    SELECT trial_id, subject_id, 6 AS stimulus_index, tst3_6 AS rt, 'color' AS test_type FROM trials UNION ALL
    SELECT trial_id, subject_id, 7 AS stimulus_index, tst3_7 AS rt, 'color' AS test_type FROM trials UNION ALL
    SELECT trial_id, subject_id, 8 AS stimulus_index, tst3_8 AS rt, 'color' AS test_type FROM trials UNION ALL
    SELECT trial_id, subject_id, 9 AS stimulus_index, tst3_9 AS rt, 'color' AS test_type FROM trials UNION ALL
    SELECT trial_id, subject_id, 10 AS stimulus_index, tst3_10 AS rt, 'color' AS test_type FROM trials UNION ALL
    SELECT trial_id, subject_id, 11 AS stimulus_index, tst3_11 AS rt, 'color' AS test_type FROM trials UNION ALL
    SELECT trial_id, subject_id, 12 AS stimulus_index, tst3_12 AS rt, 'color' AS test_type FROM trials UNION ALL
    SELECT trial_id, subject_id, 13 AS stimulus_index, tst3_13 AS rt, 'color' AS test_type FROM trials UNION ALL
    SELECT trial_id, subject_id, 14 AS stimulus_index, tst3_14 AS rt, 'color' AS test_type FROM trials UNION ALL
    SELECT trial_id, subject_id, 15 AS stimulus_index, tst3_15 AS rt, 'color' AS test_type FROM trials UNION ALL
    SELECT trial_id, subject_id, 16 AS stimulus_index, tst3_16 AS rt, 'color' AS test_type FROM trials UNION ALL
    SELECT trial_id, subject_id, 17 AS stimulus_index, tst3_17 AS rt, 'color' AS test_type FROM trials UNION ALL
    SELECT trial_id, subject_id, 18 AS stimulus_index, tst3_18 AS rt, 'color' AS test_type FROM trials UNION ALL
    SELECT trial_id, subject_id, 19 AS stimulus_index, tst3_19 AS rt, 'color' AS test_type FROM trials UNION ALL
    SELECT trial_id, subject_id, 20 AS stimulus_index, tst3_20 AS rt, 'color' AS test_type FROM trials UNION ALL
    SELECT trial_id, subject_id, 21 AS stimulus_index, tst3_21 AS rt, 'color' AS test_type FROM trials UNION ALL
    SELECT trial_id, subject_id, 22 AS stimulus_index, tst3_22 AS rt, 'color' AS test_type FROM trials UNION ALL
    SELECT trial_id, subject_id, 23 AS stimulus_index, tst3_23 AS rt, 'color' AS test_type FROM trials UNION ALL
    SELECT trial_id, subject_id, 24 AS stimulus_index, tst3_24 AS rt, 'color' AS test_type FROM trials UNION ALL
    SELECT trial_id, subject_id, 25 AS stimulus_index, tst3_25 AS rt, 'color' AS test_type FROM trials UNION ALL
    SELECT trial_id, subject_id, 26 AS stimulus_index, tst3_26 AS rt, 'color' AS test_type FROM trials UNION ALL
    SELECT trial_id, subject_id, 27 AS stimulus_index, tst3_27 AS rt, 'color' AS test_type FROM trials UNION ALL
    SELECT trial_id, subject_id, 28 AS stimulus_index, tst3_28 AS rt, 'color' AS test_type FROM trials UNION ALL
    SELECT trial_id, subject_id, 29 AS stimulus_index, tst3_29 AS rt, 'color' AS test_type FROM trials UNION ALL
    SELECT trial_id, subject_id, 30 AS stimulus_index, tst3_30 AS rt, 'color' AS test_type FROM trials UNION ALL
    SELECT trial_id, subject_id, 31 AS stimulus_index, tst3_31 AS rt, 'color' AS test_type FROM trials UNION ALL
    SELECT trial_id, subject_id, 32 AS stimulus_index, tst3_32 AS rt, 'color' AS test_type FROM trials UNION ALL
    SELECT trial_id, subject_id, 33 AS stimulus_index, tst3_33 AS rt, 'color' AS test_type FROM trials UNION ALL
    SELECT trial_id, subject_id, 34 AS stimulus_index, tst3_34 AS rt, 'color' AS test_type FROM trials UNION ALL
    SELECT trial_id, subject_id, 35 AS stimulus_index, tst3_35 AS rt, 'color' AS test_type FROM trials UNION ALL
    SELECT trial_id, subject_id, 36 AS stimulus_index, tst3_36 AS rt, 'color' AS test_type FROM trials
),
reactions_tst3 AS (
    SELECT u.trial_id, u.subject_id, u.test_type, u.stimulus_index, u.rt, m.position AS field, m.psi_ms AS psi, m.color 
    FROM unpivoted_tst3 u 
    JOIN metadata_color_red m ON u.stimulus_index = m.stimulus_id 
    WHERE u.rt IS NOT NULL AND u.rt > 0
)
SELECT * FROM reactions_tst1 UNION ALL SELECT * FROM reactions_tst2 UNION ALL SELECT * FROM reactions_tst3;
