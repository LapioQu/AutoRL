# Phase 0-7 Validation Suite

Validation suite executed on the controlled non-stationary environment to check whether the adaptive system
matches or exceeds the best fixed strategy under abrupt and gradual drift.

- n: 5
- seeds: 41, 42, 43, 44, 45
- interpretation note: this is a controlled system-validation suite, not the final benchmark replay/H1/H2 study.

## Scenario Summaries

| Scenario | Adaptive Mean | Adaptive Std | Adaptive CI95 | Best Fixed | Best Fixed Mean | Best Fixed Std | Best Fixed CI95 | Delta Mean | Delta Std | Delta CI95 | Effect Size d |
| --- | ---: | ---: | ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| abrupt_drift | 1.021324 | 0.000260 | 0.000228 | fixed_mid | 0.942297 | 0.000258 | 0.000226 | 0.079027 | 0.000003 | 0.000002 | 30822.274415 |
| gradual_drift | 1.042064 | 0.001687 | 0.001478 | fixed_mid | 0.990232 | 0.000169 | 0.000148 | 0.051832 | 0.001536 | 0.001347 | 33.735849 |

## Run Artifacts

| Scenario | Seed | Mode | Mean Reward | Experiment ID | Report Path |
| --- | ---: | --- | ---: | --- | --- |
| abrupt_drift | 41 | adaptive | 1.021618 | phase0-7-abrupt-adaptive-20260428150545-b1c23b63 | E:\dipproj\artifacts\validation_suite_0_7\abrupt_drift\seed_41\adaptive\experiments\phase0-7-abrupt-adaptive-20260428150545-b1c23b63\report.md |
| abrupt_drift | 41 | fixed_low | 0.745249 | phase0-7-abrupt-fixed-low-20260428150549-f00a9aea | E:\dipproj\artifacts\validation_suite_0_7\abrupt_drift\seed_41\fixed_low\experiments\phase0-7-abrupt-fixed-low-20260428150549-f00a9aea\report.md |
| abrupt_drift | 41 | fixed_mid | 0.942591 | phase0-7-abrupt-fixed-mid-20260428150553-a48e79bd | E:\dipproj\artifacts\validation_suite_0_7\abrupt_drift\seed_41\fixed_mid\experiments\phase0-7-abrupt-fixed-mid-20260428150553-a48e79bd\report.md |
| abrupt_drift | 41 | fixed_high | 0.722188 | phase0-7-abrupt-fixed-high-20260428150556-48c84242 | E:\dipproj\artifacts\validation_suite_0_7\abrupt_drift\seed_41\fixed_high\experiments\phase0-7-abrupt-fixed-high-20260428150556-48c84242\report.md |
| abrupt_drift | 41 | adaptive_meta_final | 0.941832 | phase0-7-abrupt-adaptive-meta-final-20260428150601-a57d1c10 | E:\dipproj\artifacts\validation_suite_0_7\abrupt_drift\seed_41\adaptive_meta_final\experiments\phase0-7-abrupt-adaptive-meta-final-20260428150601-a57d1c10\report.md |
| abrupt_drift | 42 | adaptive | 1.021256 | phase0-7-abrupt-adaptive-20260428150605-692810ce | E:\dipproj\artifacts\validation_suite_0_7\abrupt_drift\seed_42\adaptive\experiments\phase0-7-abrupt-adaptive-20260428150605-692810ce\report.md |
| abrupt_drift | 42 | fixed_low | 0.744888 | phase0-7-abrupt-fixed-low-20260428150609-7b555f0a | E:\dipproj\artifacts\validation_suite_0_7\abrupt_drift\seed_42\fixed_low\experiments\phase0-7-abrupt-fixed-low-20260428150609-7b555f0a\report.md |
| abrupt_drift | 42 | fixed_mid | 0.942226 | phase0-7-abrupt-fixed-mid-20260428150613-4821501d | E:\dipproj\artifacts\validation_suite_0_7\abrupt_drift\seed_42\fixed_mid\experiments\phase0-7-abrupt-fixed-mid-20260428150613-4821501d\report.md |
| abrupt_drift | 42 | fixed_high | 0.721880 | phase0-7-abrupt-fixed-high-20260428150617-b495241f | E:\dipproj\artifacts\validation_suite_0_7\abrupt_drift\seed_42\fixed_high\experiments\phase0-7-abrupt-fixed-high-20260428150617-b495241f\report.md |
| abrupt_drift | 42 | adaptive_meta_final | 0.941472 | phase0-7-abrupt-adaptive-meta-final-20260428150621-80d5a2c0 | E:\dipproj\artifacts\validation_suite_0_7\abrupt_drift\seed_42\adaptive_meta_final\experiments\phase0-7-abrupt-adaptive-meta-final-20260428150621-80d5a2c0\report.md |
| abrupt_drift | 43 | adaptive | 1.021044 | phase0-7-abrupt-adaptive-20260428150625-1c1925c4 | E:\dipproj\artifacts\validation_suite_0_7\abrupt_drift\seed_43\adaptive\experiments\phase0-7-abrupt-adaptive-20260428150625-1c1925c4\report.md |
| abrupt_drift | 43 | fixed_low | 0.744675 | phase0-7-abrupt-fixed-low-20260428150629-677b4a3a | E:\dipproj\artifacts\validation_suite_0_7\abrupt_drift\seed_43\fixed_low\experiments\phase0-7-abrupt-fixed-low-20260428150629-677b4a3a\report.md |
| abrupt_drift | 43 | fixed_mid | 0.942021 | phase0-7-abrupt-fixed-mid-20260428150633-33d46424 | E:\dipproj\artifacts\validation_suite_0_7\abrupt_drift\seed_43\fixed_mid\experiments\phase0-7-abrupt-fixed-mid-20260428150633-33d46424\report.md |
| abrupt_drift | 43 | fixed_high | 0.721544 | phase0-7-abrupt-fixed-high-20260428150637-e324a310 | E:\dipproj\artifacts\validation_suite_0_7\abrupt_drift\seed_43\fixed_high\experiments\phase0-7-abrupt-fixed-high-20260428150637-e324a310\report.md |
| abrupt_drift | 43 | adaptive_meta_final | 0.941257 | phase0-7-abrupt-adaptive-meta-final-20260428150641-6a69562a | E:\dipproj\artifacts\validation_suite_0_7\abrupt_drift\seed_43\adaptive_meta_final\experiments\phase0-7-abrupt-adaptive-meta-final-20260428150641-6a69562a\report.md |
| abrupt_drift | 44 | adaptive | 1.021573 | phase0-7-abrupt-adaptive-20260428150645-d1c4d1c5 | E:\dipproj\artifacts\validation_suite_0_7\abrupt_drift\seed_44\adaptive\experiments\phase0-7-abrupt-adaptive-20260428150645-d1c4d1c5\report.md |
| abrupt_drift | 44 | fixed_low | 0.745204 | phase0-7-abrupt-fixed-low-20260428150650-326d3795 | E:\dipproj\artifacts\validation_suite_0_7\abrupt_drift\seed_44\fixed_low\experiments\phase0-7-abrupt-fixed-low-20260428150650-326d3795\report.md |
| abrupt_drift | 44 | fixed_mid | 0.942546 | phase0-7-abrupt-fixed-mid-20260428150654-0ec0abac | E:\dipproj\artifacts\validation_suite_0_7\abrupt_drift\seed_44\fixed_mid\experiments\phase0-7-abrupt-fixed-mid-20260428150654-0ec0abac\report.md |
| abrupt_drift | 44 | fixed_high | 0.722149 | phase0-7-abrupt-fixed-high-20260428150658-fe90b3ce | E:\dipproj\artifacts\validation_suite_0_7\abrupt_drift\seed_44\fixed_high\experiments\phase0-7-abrupt-fixed-high-20260428150658-fe90b3ce\report.md |
| abrupt_drift | 44 | adaptive_meta_final | 0.941788 | phase0-7-abrupt-adaptive-meta-final-20260428150702-2f136fce | E:\dipproj\artifacts\validation_suite_0_7\abrupt_drift\seed_44\adaptive_meta_final\experiments\phase0-7-abrupt-adaptive-meta-final-20260428150702-2f136fce\report.md |
| abrupt_drift | 45 | adaptive | 1.021129 | phase0-7-abrupt-adaptive-20260428150706-9f1eaf67 | E:\dipproj\artifacts\validation_suite_0_7\abrupt_drift\seed_45\adaptive\experiments\phase0-7-abrupt-adaptive-20260428150706-9f1eaf67\report.md |
| abrupt_drift | 45 | fixed_low | 0.744760 | phase0-7-abrupt-fixed-low-20260428150709-0116fb77 | E:\dipproj\artifacts\validation_suite_0_7\abrupt_drift\seed_45\fixed_low\experiments\phase0-7-abrupt-fixed-low-20260428150709-0116fb77\report.md |
| abrupt_drift | 45 | fixed_mid | 0.942103 | phase0-7-abrupt-fixed-mid-20260428150712-75162a21 | E:\dipproj\artifacts\validation_suite_0_7\abrupt_drift\seed_45\fixed_mid\experiments\phase0-7-abrupt-fixed-mid-20260428150712-75162a21\report.md |
| abrupt_drift | 45 | fixed_high | 0.721677 | phase0-7-abrupt-fixed-high-20260428150715-ff70999c | E:\dipproj\artifacts\validation_suite_0_7\abrupt_drift\seed_45\fixed_high\experiments\phase0-7-abrupt-fixed-high-20260428150715-ff70999c\report.md |
| abrupt_drift | 45 | adaptive_meta_final | 0.941343 | phase0-7-abrupt-adaptive-meta-final-20260428150718-cf73a8a7 | E:\dipproj\artifacts\validation_suite_0_7\abrupt_drift\seed_45\adaptive_meta_final\experiments\phase0-7-abrupt-adaptive-meta-final-20260428150718-cf73a8a7\report.md |
| gradual_drift | 41 | adaptive | 1.043376 | phase0-7-gradual-adaptive-20260428150722-cd1290e4 | E:\dipproj\artifacts\validation_suite_0_7\gradual_drift\seed_41\adaptive\experiments\phase0-7-gradual-adaptive-20260428150722-cd1290e4\report.md |
| gradual_drift | 41 | fixed_low | 0.747331 | phase0-7-gradual-fixed-low-20260428150725-12cb7afb | E:\dipproj\artifacts\validation_suite_0_7\gradual_drift\seed_41\fixed_low\experiments\phase0-7-gradual-fixed-low-20260428150725-12cb7afb\report.md |
| gradual_drift | 41 | fixed_mid | 0.990422 | phase0-7-gradual-fixed-mid-20260428150728-b4813654 | E:\dipproj\artifacts\validation_suite_0_7\gradual_drift\seed_41\fixed_mid\experiments\phase0-7-gradual-fixed-mid-20260428150728-b4813654\report.md |
| gradual_drift | 41 | fixed_high | 0.718529 | phase0-7-gradual-fixed-high-20260428150732-23784d59 | E:\dipproj\artifacts\validation_suite_0_7\gradual_drift\seed_41\fixed_high\experiments\phase0-7-gradual-fixed-high-20260428150732-23784d59\report.md |
| gradual_drift | 41 | adaptive_meta_final | 0.989748 | phase0-7-gradual-adaptive-meta-final-20260428150735-720709b6 | E:\dipproj\artifacts\validation_suite_0_7\gradual_drift\seed_41\adaptive_meta_final\experiments\phase0-7-gradual-adaptive-meta-final-20260428150735-720709b6\report.md |
| gradual_drift | 42 | adaptive | 1.040287 | phase0-7-gradual-adaptive-20260428150738-01f9a6f7 | E:\dipproj\artifacts\validation_suite_0_7\gradual_drift\seed_42\adaptive\experiments\phase0-7-gradual-adaptive-20260428150738-01f9a6f7\report.md |
| gradual_drift | 42 | fixed_low | 0.747046 | phase0-7-gradual-fixed-low-20260428150742-3e7c2020 | E:\dipproj\artifacts\validation_suite_0_7\gradual_drift\seed_42\fixed_low\experiments\phase0-7-gradual-fixed-low-20260428150742-3e7c2020\report.md |
| gradual_drift | 42 | fixed_mid | 0.990134 | phase0-7-gradual-fixed-mid-20260428150745-fb237486 | E:\dipproj\artifacts\validation_suite_0_7\gradual_drift\seed_42\fixed_mid\experiments\phase0-7-gradual-fixed-mid-20260428150745-fb237486\report.md |
| gradual_drift | 42 | fixed_high | 0.718291 | phase0-7-gradual-fixed-high-20260428150748-ddf0575a | E:\dipproj\artifacts\validation_suite_0_7\gradual_drift\seed_42\fixed_high\experiments\phase0-7-gradual-fixed-high-20260428150748-ddf0575a\report.md |
| gradual_drift | 42 | adaptive_meta_final | 0.989464 | phase0-7-gradual-adaptive-meta-final-20260428150752-c8d62caf | E:\dipproj\artifacts\validation_suite_0_7\gradual_drift\seed_42\adaptive_meta_final\experiments\phase0-7-gradual-adaptive-meta-final-20260428150752-c8d62caf\report.md |
| gradual_drift | 43 | adaptive | 1.040151 | phase0-7-gradual-adaptive-20260428150755-e795845f | E:\dipproj\artifacts\validation_suite_0_7\gradual_drift\seed_43\adaptive\experiments\phase0-7-gradual-adaptive-20260428150755-e795845f\report.md |
| gradual_drift | 43 | fixed_low | 0.746911 | phase0-7-gradual-fixed-low-20260428150758-fdeeea77 | E:\dipproj\artifacts\validation_suite_0_7\gradual_drift\seed_43\fixed_low\experiments\phase0-7-gradual-fixed-low-20260428150758-fdeeea77\report.md |
| gradual_drift | 43 | fixed_mid | 0.990005 | phase0-7-gradual-fixed-mid-20260428150802-0add4830 | E:\dipproj\artifacts\validation_suite_0_7\gradual_drift\seed_43\fixed_mid\experiments\phase0-7-gradual-fixed-mid-20260428150802-0add4830\report.md |
| gradual_drift | 43 | fixed_high | 0.718046 | phase0-7-gradual-fixed-high-20260428150805-6bc64904 | E:\dipproj\artifacts\validation_suite_0_7\gradual_drift\seed_43\fixed_high\experiments\phase0-7-gradual-fixed-high-20260428150805-6bc64904\report.md |
| gradual_drift | 43 | adaptive_meta_final | 0.989327 | phase0-7-gradual-adaptive-meta-final-20260428150808-bc9bc075 | E:\dipproj\artifacts\validation_suite_0_7\gradual_drift\seed_43\adaptive_meta_final\experiments\phase0-7-gradual-adaptive-meta-final-20260428150808-bc9bc075\report.md |
| gradual_drift | 44 | adaptive | 1.043316 | phase0-7-gradual-adaptive-20260428150811-8f30fbc7 | E:\dipproj\artifacts\validation_suite_0_7\gradual_drift\seed_44\adaptive\experiments\phase0-7-gradual-adaptive-20260428150811-8f30fbc7\report.md |
| gradual_drift | 44 | fixed_low | 0.747270 | phase0-7-gradual-fixed-low-20260428150814-257584cc | E:\dipproj\artifacts\validation_suite_0_7\gradual_drift\seed_44\fixed_low\experiments\phase0-7-gradual-fixed-low-20260428150814-257584cc\report.md |
| gradual_drift | 44 | fixed_mid | 0.990361 | phase0-7-gradual-fixed-mid-20260428150817-58f27c70 | E:\dipproj\artifacts\validation_suite_0_7\gradual_drift\seed_44\fixed_mid\experiments\phase0-7-gradual-fixed-mid-20260428150817-58f27c70\report.md |
| gradual_drift | 44 | fixed_high | 0.718474 | phase0-7-gradual-fixed-high-20260428150821-62e42b58 | E:\dipproj\artifacts\validation_suite_0_7\gradual_drift\seed_44\fixed_high\experiments\phase0-7-gradual-fixed-high-20260428150821-62e42b58\report.md |
| gradual_drift | 44 | adaptive_meta_final | 0.989688 | phase0-7-gradual-adaptive-meta-final-20260428150824-31bab986 | E:\dipproj\artifacts\validation_suite_0_7\gradual_drift\seed_44\adaptive_meta_final\experiments\phase0-7-gradual-adaptive-meta-final-20260428150824-31bab986\report.md |
| gradual_drift | 45 | adaptive | 1.043192 | phase0-7-gradual-adaptive-20260428150827-ead5131e | E:\dipproj\artifacts\validation_suite_0_7\gradual_drift\seed_45\adaptive\experiments\phase0-7-gradual-adaptive-20260428150827-ead5131e\report.md |
| gradual_drift | 45 | fixed_low | 0.747147 | phase0-7-gradual-fixed-low-20260428150830-daf89815 | E:\dipproj\artifacts\validation_suite_0_7\gradual_drift\seed_45\fixed_low\experiments\phase0-7-gradual-fixed-low-20260428150830-daf89815\report.md |
| gradual_drift | 45 | fixed_mid | 0.990239 | phase0-7-gradual-fixed-mid-20260428150834-36e181a2 | E:\dipproj\artifacts\validation_suite_0_7\gradual_drift\seed_45\fixed_mid\experiments\phase0-7-gradual-fixed-mid-20260428150834-36e181a2\report.md |
| gradual_drift | 45 | fixed_high | 0.718325 | phase0-7-gradual-fixed-high-20260428150837-4b3146c9 | E:\dipproj\artifacts\validation_suite_0_7\gradual_drift\seed_45\fixed_high\experiments\phase0-7-gradual-fixed-high-20260428150837-4b3146c9\report.md |
| gradual_drift | 45 | adaptive_meta_final | 0.989563 | phase0-7-gradual-adaptive-meta-final-20260428150840-942b2c42 | E:\dipproj\artifacts\validation_suite_0_7\gradual_drift\seed_45\adaptive_meta_final\experiments\phase0-7-gradual-adaptive-meta-final-20260428150840-942b2c42\report.md |
