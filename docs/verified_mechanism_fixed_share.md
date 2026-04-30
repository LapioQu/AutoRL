## Перевірений механізм: Fixed-Share для recovery shifting experts

### Що саме перевірялось

Було додано controller family `fixed_share_portfolio` у [src/autorl/application/benchmark_replay.py](/E:/dipproj/src/autorl/application/benchmark_replay.py:488) і включено в `auto_meta` у [src/autorl/application/dataset_lab.py](/E:/dipproj/src/autorl/application/dataset_lab.py:713).

Ідея механізму:

- після кожного online update невелика частка ваги `alpha` перерозподіляється між усіма експертами;
- це дає експертам, які були слабкими в поточному режимі, шанс швидко відновити вагу, якщо середовище повертається в режим, де вони знову сильні;
- тобто механізм додає **expert recovery under regime re-entry**, чого немає в звичайного Hedge без share update.

Це не лише евристика проєкту: саме такий механізм описаний у класичній лінії робіт про `tracking the best expert` для shifting environments.

### Чому це концептуально інше, ніж у поточній системі

Попередні controller-и:

- `hard_switch_lcb`
- `recent_leader_meta`
- `hedge_portfolio`

переважно реагують на вже побачений reward.

`Fixed-Share` додає окремий механізм:

- **не дати “мертвим” експертам назавжди втратити шанс повернутися**, якщо режим повториться.

Це важливо саме в recurring/non-stationary streams.

### Емпіричний результат

Порівняння зафіксовано в:

- [artifacts/concept_mechanism_check/mechanism_comparison.json](/E:/dipproj/artifacts/concept_mechanism_check/mechanism_comparison.json:1)
- [artifacts/concept_mechanism_check/fixed_share](/E:/dipproj/artifacts/concept_mechanism_check/fixed_share)
- [artifacts/concept_mechanism_check/method_compare](/E:/dipproj/artifacts/concept_mechanism_check/method_compare)

#### WaterFlow

- `hard_switch_lcb`: `+0.002097`
- `recent_leader_meta`: `-0.004819`
- `hedge_portfolio`: `-0.000186`
- `fixed_share_portfolio`: `+0.032334`

Це найсильніший позитивний результат.

Для built-in `WaterFlow` у `DatasetLabService.analyze_builtin_dataset(..., policy_name=\"auto_meta\")` після додавання `Fixed-Share`:

- adaptive score = `0.836279`
- best fixed = `0.803945`
- delta = `+0.032334`
- oracle capture = `0.461488`

Тобто система почала забирати близько `46.1%` доступного oracle gain на цьому потоці.

#### Bikes

- `hard_switch_lcb`: `+0.000823`
- `recent_leader_meta`: `+0.001728`
- `hedge_portfolio`: `-0.100351`
- `fixed_share_portfolio`: `+0.001949`

Тут `Fixed-Share` теж дає найкращий результат серед перевірених controller-ів.

#### InsectsRecurring

- `hard_switch_lcb`: `+0.005067`
- `recent_leader_meta`: `0.000000`
- `hedge_portfolio`: `0.000000`
- `fixed_share_portfolio`: `+0.001950`

Тобто механізм корисний, але не найкращий: для цього recurring classification stream кращим лишається `hard_switch_lcb`.

#### Elec2

- `hard_switch_lcb`: `+0.000154`
- `recent_leader_meta`: `+0.000640`
- `hedge_portfolio`: `-0.000927`
- `fixed_share_portfolio`: `-0.001920`

Тут `Fixed-Share` шкодить.

### Висновок

`Fixed-Share` є **реально перевіреним концептуальним механізмом**, якого системі раніше бракувало:

- він додає recovery of previously suppressed experts;
- він істотно покращує систему на частині non-stationary streams;
- найсильніше це видно на `WaterFlow`, де приріст великий і практично значущий;
- він не є універсально найкращим, тому його правильне місце не як єдиний controller, а як окрема family inside `auto_meta`.

Отже перевірений висновок не такий:

- "це теоретично могло б допомогти"

а такий:

- **додавання share-update механізму реально покращує систему на частині потоків і усуває конкретний функціональний брак: відсутність expert recovery при повторному вході в режим.**

### Джерела механізму

- Herbster, Warmuth, *Tracking the Best Expert*, Machine Learning, 1998: https://mwarmuth.bitbucket.io/pubs/J39.pdf
- JMLR summary про non-stationary two-layer online ensemble / tracking base learners: https://www.jmlr.org/papers/v26/23-1188.html
