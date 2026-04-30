# Повна ревізія вимог до розроблення ПЗ AutoRL Strategy Manager

Дата підготовки: 2026-04-28  
Призначення документа: внутрішнє технічне завдання на фактичну розробку програмної системи та експериментальної частини третього розділу.

---

## 0. Висновок після повторної перевірки

Попередній підхід був недостатньо глибоким, бо надто сильно зводив систему до ядра експериментів, CLI та логів. Після повторного аналізу розділів 1–2, пояснювальної записки та CSV-файлів вимог правильна постановка така:

> **Потрібно розробити локальну адаптивну інтелектуальну навчальну систему AutoRL Strategy Manager на основі навчання з підкріпленням, яка забезпечує динамічний вибір навчальних стратегій самонавчання агента, має повноцінний веб-інтерфейс для запуску й аналізу експериментів, API, сховище, журналювання, механізми відтворення запусків, тестування та експериментальну валідацію практично-наукових результатів.**

Система не повинна бути лише дослідницьким скриптом. Вона має бути практично корисним програмним засобом для ML/RL-дослідника або інженера, який:
- створює експеримент;
- вибирає сценарій середовища;
- задає набір стратегій самонавчання;
- запускає адаптивний або baseline-режим;
- спостерігає метрики через веб-інтерфейс;
- бачить активну стратегію та журнал Stay/Switch-рішень;
- порівнює стратегії;
- отримує графіки, таблиці, звіти й артефакти;
- може повторити запуск за тією самою конфігурацією та seed.

---

## 1. Використані джерела вимог

### 1.1. Основні DOCX-джерела

| Джерело | Що взято |
|---|---|
| `Розділ1-2.docx` | Основні вимоги, постановка задачі, архітектура, дані, алгоритм, сценарії, API/UI, журналювання, відтворюваність |
| `Пояснювальна_Записка(3).docx` | Тема, мета, об'єкт, предмет, наукова новизна, практичне значення, H1/H2, експериментальні серії, benchmark-и, статус гіпотез |
| `Розділ_2_фінал_UML_псевдокод_діаграмні_інструменти(3).docx` | Проєктна модель другого розділу, структура компонентів, endpoint-и, локальне розгортання |

### 1.2. CSV-джерела

| CSV | Що взято |
|---|---|
| `Вступ(3).csv` | Акцент на програмній системі, мета під 121, зв'язок новизни з tempered reward + LCB |
| `Розділ1(3).csv` | Потреба у вимогах, use case, матриці трасування, аналізі аналогів, DFD |
| `Розділ2(3).csv` | Модульний моноліт, шари, component/sequence/state diagram, алгоритмічне ядро, ER/SQL, deployment/security |
| `Розділ3(3).csv` | Структура реалізації третього розділу, UI, логи, конфіги, тести, H1/H2 як системна валідація, p-value/CI/effect size, експлуатаційна документація |
| `СтекТехнологій(3).csv` | Python 3.11 + venv, FastAPI + Uvicorn, Streamlit, SQLite, river/gymnasium/stable-baselines3/scikit-learn/numpy/pandas, logging, pytest+coverage, Git |
| `ПрикладТаблиціВимог(3).csv` | FR-01..FR-07: online/offline запуск, метаконтролер, web UI, latency ≤ 0.5s CPU, БД історії, reproducibility, CPU-only |
| `Протокол системного тестування (готовий до використання)(3).csv` | Unit, integration, system, performance, reproducibility тести |

> Примітка: частина CSV-файлів має некоректне екранування лапок, тому вони були проаналізовані за фактичним текстом рядків, а не як суворо валідні CSV-таблиці.

---

## 2. Що саме має залишитися сутністю системи

Система має залишатися саме:

> **адаптивною інтелектуальною навчальною системою на основі навчання з підкріпленням для динамічного вибору оптимальних навчальних стратегій самонавчання.**

Це означає:

1. **Адаптивна** — змінює активну стратегію самонавчання залежно від метрик і стану середовища.
2. **Інтелектуальна** — має алгоритмічний метарівень, що приймає формалізоване рішення Stay/Switch, а не працює за ручним правилом.
3. **Навчальна** — стратегії описують спосіб організації навчання/самонавчання агента: exploration, reward shaping, evaluation window, update rule, stability penalties.
4. **На основі RL** — агент/метаконтролер працює в RL-подібному контурі `state → action/strategy → reward → update/evaluation`.
5. **Для динамічного вибору стратегій** — центральний результат системи не prediction/classification сам по собі, а вибір, збереження або зміна активної навчальної стратегії.
6. **Для самонавчання** — система керує навчальним процесом агента, а не лише запускає готову модель.

---

## 3. Межі системи

### 3.1. Що система робить

Система повинна:

- приймати конфігурацію експерименту;
- запускати RL/самонавчальний експеримент;
- підтримувати портфель стратегій самонавчання;
- збирати епізодичні та агреговані метрики;
- оцінювати поточну й кандидатні стратегії;
- приймати Stay/Switch-рішення;
- журналювати причини рішень;
- підтримувати baseline-режими;
- підтримувати адаптивний режим;
- відображати результати через веб-інтерфейс;
- надавати API для програмного доступу;
- підтримувати CLI для batch/відтворюваних запусків;
- зберігати конфігурації, seed, хеші, версії бібліотек, артефакти;
- формувати звіти;
- виконувати експериментальні сценарії для третього розділу;
- забезпечувати тести і верифікацію функціональних/нефункціональних вимог.

### 3.2. Що система не повинна робити

Система не повинна:

- бути хмарною MLOps-платформою;
- вимагати GPU;
- вимагати зовнішній сервер БД;
- передавати дані в зовнішні сервіси;
- зберігати персональні дані користувачів;
- підміняти Stable-Baselines3/RLlib як універсальна RL-бібліотека;
- обмежуватися тільки CLI без web UI;
- робити висновки за одним запуском без повторів;
- приймати Switch без достатньої статистики.

---

## 4. Користувачі та сценарії роботи

### 4.1. Актори

| Актор | Роль |
|---|---|
| ML/RL-інженер або дослідник | Створює конфігурації, запускає експерименти, аналізує метрики, порівнює стратегії |
| Розробник стратегій | Додає нові стратегії самонавчання, змінює параметри метаконтролера, розширює середовища |
| Користувач системи/аналітик | Переглядає результати запусків, звіти, графіки та журнал рішень |

### 4.2. Обов'язкові use cases

| ID | Use case | Суть |
|---|---|---|
| UC-01 | Створити експеримент | Користувач задає сценарій, seed, кількість епізодів, набір стратегій, параметри метаконтролера |
| UC-02 | Запустити експеримент | Система створює run-директорію, копіює конфігурацію, запускає orchestrator |
| UC-03 | Моніторити виконання | UI показує статус, активну стратегію, reward, кількість switch/stay/fallback |
| UC-04 | Переглянути метрики | UI/API відображає reward, rolling mean, variance, utility, LCB |
| UC-05 | Переглянути журнал рішень | Користувач бачить Stay/Switch, причини, числові підстави |
| UC-06 | Порівняти стратегії | Fixed/Greedy/Drift-aware/LCB/Tempered/Adaptive порівнюються за метриками |
| UC-07 | Сформувати звіт | Система генерує markdown/html-звіт і графіки |
| UC-08 | Експортувати артефакти | Користувач завантажує metrics.csv, decisions.csv, config.yaml, plots |
| UC-09 | Повторити запуск | Система повторно виконує експеримент із тим самим seed/config_hash |
| UC-10 | Додати нову стратегію | Розробник реалізує новий клас Strategy і реєструє його у StrategyPool |
| UC-11 | Зупинити запуск | Система керовано завершує виконання і зберігає доступні логи |
| UC-12 | Перевірити конфігурацію | Система валідує YAML/JSON до старту запуску |

---

### 4.3. Режими виконання експериментів

Система повинна підтримувати два різні режими виконання, оскільки перші два розділи вимагають і практичного локального моніторингу через інтерфейс, і відтворюваних серій запусків для експериментальної валідації.

| Режим | Призначення | Основні дії |
|---|---|---|
| `ONLINE_MONITORING` | Практична робота через Streamlit/FastAPI | створення експерименту з UI/API, оновлення статусу, відображення поточного епізоду, активної стратегії, rolling reward, utility, LCB, журналу Stay/Switch, керована зупинка |
| `OFFLINE_BATCH` | Відтворювані серії для третього розділу | запуск YAML/JSON з CLI, запуск `suite_all.yaml`, серії seed, baseline/adaptive порівняння, агреговані таблиці, автоматичний summary-звіт |

Обидва режими повинні використовувати ті самі application services і domain core, щоб результати UI, API, CLI, SQLite, CSV і звітів мали однакову семантику.

---

## 5. Повний перелік функціональних вимог

### 5.1. Вимоги з CSV `ПрикладТаблиціВимог(3).csv`

| ID | Тип | Вимога | Пріоритет | Трасування |
|---|---|---|---|---|
| FR-01 | Функціональна | Система має підтримувати онлайн- та офлайн-режими запуску експериментів | Must | 2.2, 3.1 |
| FR-02 | Функціональна | Реалізувати метаконтролер з критерієм переключення стратегій | Must | 2.3, 3.3 |
| FR-03 | Функціональна | Надавати веб-інтерфейс для моніторингу метрик та історії рішень | Must | 2.5, 3.1 |
| FR-04 | Нефункціональна | Час прийняття рішення ≤ 0.5 с на CPU | Should | 2.5, 3.2 |
| FR-05 | Нефункціональна | Збереження історії стратегій, конфігурацій та метрик у БД | Must | 2.4, 3.1 |
| FR-06 | Нефункціональна | Відтворюваність запусків при фіксованих seeds | Must | 2.3, 3.4 |
| FR-07 | Обмеження | Робота на CPU-середовищі, відсутність залежності від GPU | Should | 2.5 |

### 5.2. Функціональні вимоги, витягнуті з розділів 1–2

| ID | Вимога | Джерело в дипломі |
|---|---|---|
| FR-08 | Приймати конфігураційний файл експерименту | 1.1, 1.3, 2.3, 2.6, 2.7 |
| FR-09 | Задавати середовище, агента, набір стратегій, кількість епізодів, evaluation window, seed | 1.3, 2.1, 2.3, 2.6 |
| FR-10 | Автоматизувати запуск експериментів із фіксованими конфігураціями | 1.3 |
| FR-11 | Запускати експеримент у Gymnasium-сумісному або іншому підтримуваному середовищі/симуляторі | 1.1.4, 2.4 |
| FR-12 | Керувати активною стратегією самонавчання | 1.1.4, 2.4, 2.5 |
| FR-13 | Підтримувати портфель стратегій самонавчання | 1.3, 2.2, 2.4 |
| FR-14 | Дозволяти додавання нових стратегій розробником | 1.3, 2.2 |
| FR-15 | Збирати епізодичні метрики під час навчання | 1.3, 2.3, 2.4 |
| FR-16 | Агрегувати метрики у вікнах оцінювання W | 1.1.2, 2.4, 2.5 |
| FR-17 | Розраховувати середню винагороду | 1.1, 2.4 |
| FR-18 | Розраховувати дисперсію/стабільність винагороди | 1.1.2, 2.4 |
| FR-19 | Розраховувати кількість перемикань | 1.1.2, 2.4 |
| FR-20 | Розраховувати час відновлення після зміни режиму | 1.1.2, 2.4 |
| FR-21 | Розраховувати функцію корисності U | 2.4 |
| FR-22 | Розраховувати LCB | 2.4, 2.5 |
| FR-23 | Ураховувати switch cost | 2.4, 2.5 |
| FR-24 | Ураховувати practical threshold delta | 2.4, 2.5 |
| FR-25 | Ураховувати tempered reward / reward shaping | 2.5, CSV Розділ2 |
| FR-26 | Формувати рішення Stay/Switch | 1.1.2, 1.3, 2.5 |
| FR-27 | Записувати причину рішення | 1.1.2, 2.5, 2.7 |
| FR-28 | Реалізувати fallback при недостатній кількості даних | 2.5 |
| FR-29 | Не перемикати стратегію на основі надто короткого або шумового фрагмента | 1.1.2, 1.1.3, 2.5 |
| FR-30 | Зберігати журнал епізодів | 1.1, 2.3, 2.7 |
| FR-31 | Зберігати журнал рішень метаконтролера | 1.1, 2.3, 2.7 |
| FR-32 | Зберігати технічний журнал помилок і службових подій | 2.7 |
| FR-33 | Формувати звітні артефакти | 1.1, 1.3, 2.7 |
| FR-34 | Надавати доступ до журналу рішень користувачу | 1.3, 2.7 |
| FR-35 | Підтримувати порівняння baseline і adaptive стратегій | 1.3, ПЗ |
| FR-36 | Підтримувати повторний запуск за збереженою конфігурацією і seed | 1.3, 1.5, 2.7 |
| FR-37 | Створювати новий запуск із посиланням на початковий при rerun | 2.7 |
| FR-38 | Підтримувати API для створення/запуску/зупинки/стану/метрик/рішень/звіту | 2.7 |
| FR-39 | Підтримувати CLI запуск з передаванням шляху до конфігурації | 2.7 |
| FR-40 | Підтримувати Streamlit web UI для перегляду запусків, метрик і рішень | 2.7, CSV Стек |
| FR-41 | Відображати список запусків | 2.7 |
| FR-42 | Відображати поточну активну стратегію | 2.7 |
| FR-43 | Відображати графік винагороди | 2.7 |
| FR-44 | Відображати кількість перемикань | 2.7 |
| FR-45 | Відображати журнал рішень | 2.7 |
| FR-46 | Експортувати CSV/JSON/Markdown/HTML артефакти | 1.3, 2.3, 2.7 |
| FR-47 | Підтримувати сценарії stationary, abrupt drift, gradual drift, noisy reward | 1.5, 2.4, 2.6 |
| FR-48 | Підтримувати серії повторів за seed 42..46 або іншим списком seed | ПЗ, 1.5, 2.6 |
| FR-49 | Підтримувати baseline fixed strategy | ПЗ, 2.6 |
| FR-50 | Підтримувати greedy/random/negative-control comparator-и для порівняння | ПЗ |
| FR-51 | Підтримувати drift-aware comparator, але не як основний механізм | ПЗ H1 |
| FR-52 | Підтримувати uncertainty/multi-objective/tempered reward shaping як перспективну лінію реалізації | ПЗ H2 |
| FR-53 | Формувати графіки: reward curve, rolling reward, strategy timeline, utility/LCB | 2.7, Розділ3 CSV |
| FR-54 | Формувати таблиці результатів, p-value, CI, effect size там, де це доречно для експериментів | Розділ3 CSV |
| FR-55 | Підтримувати експлуатаційну документацію: встановлення, запуск, конфігурація, моніторинг, аварійне відновлення | Розділ3 CSV |

---

### 5.3. Додатково формалізовані функціональні вимоги після контрольної звірки

| ID | Вимога | Джерело / обґрунтування |
|---|---|---|
| FR-56 | Підтримувати два режими виконання експериментів: online-monitoring та offline-batch | 1.3, 2.7, CSV вимог |
| FR-57 | Реалізувати станову модель виконання експерименту в ExperimentOrchestrator | 2.2, 2.5, CSV Розділ2 |
| FR-58 | Підтримувати benchmark replay mode для відтворення практично-наукових H1/H2 серій | ПЗ, Розділ3 CSV |
| FR-59 | У benchmark replay mode підтримувати кандидатні моделі `river_logreg`, `river_nb`, `river_hoeffding_tree`, `windowed_rf`, `windowed_histgb` | ПЗ H1/H2 |
| FR-60 | Використовувати єдину схему метрик для UI, API, CSV, SQLite і звітів | 1.3, 1.4, 2.3, 2.7 |
| FR-61 | Використовувати стандартизований enum причин Stay/Switch/fallback у журналі рішень | 1.3, 2.5, 2.7 |

---

## 6. Нефункціональні вимоги

| ID | Вимога | Обґрунтування |
|---|---|---|
| NFR-01 | Локальне розгортання | Система проєктується як локальний програмний комплекс |
| NFR-02 | Python 3.11 + venv | Вказано в стеку і розгортанні |
| NFR-03 | CPU-сумісність, GPU не обов'язковий | Розділ 1.5, CSV вимог |
| NFR-04 | Час рішення метаконтролера ≤ 0.5 с на CPU | CSV вимог і тестовий протокол |
| NFR-05 | Пам'ять у performance-тесті ≤ 512 MB | Тестовий протокол |
| NFR-06 | Відтворюваність за seed | Розділ 1.5, 2.7 |
| NFR-07 | Збереження config snapshot | Розділ 2.3, 2.7 |
| NFR-08 | Збереження config hash | Розділ 2.7 |
| NFR-09 | Збереження версій бібліотек | Розділ 2.7 |
| NFR-10 | Збереження параметрів середовища | Розділ 2.7 |
| NFR-11 | Збереження переліку стратегій | Розділ 2.7 |
| NFR-12 | Збереження timestamps | Розділ 2.7 |
| NFR-13 | Збереження шляху до артефактів | Розділ 2.7 |
| NFR-14 | Трасованість рішення Stay/Switch | Розділ 1.4, 2.7 |
| NFR-15 | Пояснюваність рішення | Розділ 1.4, 2.5 |
| NFR-16 | Модульність | Розділ 2.2 |
| NFR-17 | Розширюваність набору стратегій | Розділ 1.3, 2.2 |
| NFR-18 | Розширюваність середовищ | Розділ 1.3 |
| NFR-19 | Надійне журналювання при помилці | Розділ 2.3, 2.7 |
| NFR-20 | Частковий журнал має зберігатися при аварійному завершенні | Розділ 2.3 |
| NFR-21 | Контроль шляхів до файлів | Розділ 2.7 |
| NFR-22 | Запис лише у logs/artifacts/data в межах робочої директорії | Розділ 2.7 |
| NFR-23 | Відсутність збереження персональних даних | Розділ 2.7 |
| NFR-24 | Відсутність обов'язкового зовнішнього сервера БД | SQLite |
| NFR-25 | Відсутність передавання даних у зовнішні сервіси | Локальний режим |
| NFR-26 | UI не повинен містити доменну логіку | Розділ 2.7 |
| NFR-27 | Application services мають бути спільними для API/CLI/UI | Розділ 2.7 |
| NFR-28 | Підтримка тестування через pytest + coverage | CSV стек, Розділ3 |
| NFR-29 | Версіонування через Git | CSV стек |
| NFR-30 | Експлуатаційна документація README | Розділ3 CSV |

---

### 6.1. Додатково формалізовані нефункціональні вимоги після контрольної звірки

| ID | Вимога | Обґрунтування |
|---|---|---|
| NFR-31 | Підсумковий науковий висновок не повинен формуватися на основі одиничного запуску | Розділ 1.5, ПЗ H1/H2 |
| NFR-32 | Підсумкові таблиці мають містити `n`, seed-и, mean, std/CI та позначення статистичної обережності | Розділ 1.5, Розділ3 CSV |
| NFR-33 | Освітній benchmark replay не повинен зберігати персональні ідентифікатори користувачів | Розділ 2.7, вимога відсутності персональних даних |
| NFR-34 | Звіти не повинні містити персональні записи або сирі навчальні траєкторії користувачів, тільки агреговані метрики | Розділ 2.7, практична безпека даних |

---

## 7. Стек технологій

| Компонент | Технологія | Обов'язковість | Коментар |
|---|---|---:|---|
| Мова | Python 3.11 | Must | Базова мова реалізації |
| Віртуальне середовище | venv | Must | Локальна ізоляція залежностей |
| IDE | VS Code | Should | Орієнтир для запуску, debug, тестів |
| API | FastAPI | Must | Локальний API-шар |
| ASGI сервер | Uvicorn | Must | Запуск FastAPI |
| Web UI | Streamlit | Must | Повноцінний локальний дашборд |
| БД | SQLite | Must | Один файл `data/autorl.db` |
| Логи | logging + JSON/CSV logger | Must | Технічні й предметні журнали |
| Артефакти | Файлова система `logs/`, `artifacts/` | Must | Звіти, графіки, конфіги |
| RL/ML | stable-baselines3 | Should | Для PPO/агентів, якщо використовується повний RL |
| RL environment API | gymnasium | Should | Для Gymnasium-сумісних середовищ |
| Stream ML | river | Should | Для потокових comparator-ів і stream-сценаріїв |
| ML baseline | scikit-learn | Should | Для baseline/comparator-моделей |
| Дані/аналіз | numpy, pandas | Must | Метрики, таблиці, агрегації |
| Графіки | matplotlib | Must | Звіти й дашборд |
| Тести | pytest | Must | Unit/integration/system |
| Coverage | coverage/pytest-cov | Should | Звіт покриття |
| Версіонування | Git | Must | Для дипломного проєкту |
| Формат конфігурацій | YAML/JSON | Must | Відтворювані запуски |
| Звіти | Markdown/HTML | Must | Для третього розділу й експорту |

---

## 8. Метод розробки

Згідно з другим розділом, процес розробки — **ітеративно-інкрементальний**.

### 8.1. Ітерації

| Ітерація | Результат |
|---|---|
| I1 | Базова структура проєкту, config service, SQLite, artifacts |
| I2 | Простий запуск експерименту, environment, metrics collector |
| I3 | StrategyPool, baseline strategies |
| I4 | Evaluator, utility, LCB, switch threshold |
| I5 | MetaController + fallback + decision log |
| I6 | CLI + FastAPI |
| I7 | Streamlit UI |
| I8 | Reports + plots + exports |
| I9 | Unit/integration/system/performance tests |
| I10 | Експериментальні сценарії + baseline comparison |
| I11 | Аналіз результатів для третього розділу |
| I12 | README, експлуатаційна документація |

### 8.2. Контрольований протокол виконання для Codex-агента

Цей підрозділ не додає нових функціональних вимог до системи, а задає порядок виконання розроблення, щоб реалізація не перетворилася на одноразову генерацію неперевіреного коду. Codex-агент повинен працювати тільки ітераціями, а кожна ітерація повинна мати код, тести або smoke-перевірку, оновлений статус вимог і короткий звіт про результат.

Перед початком реалізації агент повинен створити файл `docs/requirements_inventory.md` і перенести до нього всі вимоги з цього ТЗ за групами:

- use cases `UC-01..UC-12`;
- функціональні вимоги `FR-01..FR-61`;
- нефункціональні вимоги `NFR-01..NFR-34`;
- UI acceptance criteria;
- API endpoints;
- CLI commands;
- SQLite tables;
- required artifacts;
- required experiments `SE/EXP`;
- documentation artifacts `DOC-01..DOC-10`.

Для кожної вимоги у `docs/requirements_inventory.md` має бути статус:

```text
not_started / in_progress / implemented / tested / deferred
```

Правила виконання:

- не переходити до наступної фази без перевірок поточної фази;
- не позначати Must-вимогу як `deferred` без окремого пояснення;
- після кожної фази оновлювати `docs/requirements_inventory.md`;
- доменну логіку не розміщувати у Streamlit або FastAPI handlers;
- UI, API і CLI мають викликати application services;
- підсумкові наукові висновки формувати тільки з фактично виконаних експериментів і збережених артефактів;
- система має залишатися адаптивною інтелектуальною навчальною системою для динамічного вибору навчальних стратегій самонавчання, а не загальним ML-runner або CLI-скриптом.

Формат звіту після кожної фази:

```text
1. Що реалізовано.
2. Які файли створено або змінено.
3. Які тести додано.
4. Які команди перевірки запущено.
5. Результат перевірок.
6. Які вимоги оновлено в docs/requirements_inventory.md.
7. Що залишається на наступну фазу.
```

### 8.3. Фазовий план контрольованої реалізації

Фазовий план деталізує ітеративно-інкрементальний процес із підрозділу 8.1 і використовується як інструкція для Codex-агента. Кожна фаза має завершуватися перевіркою.

| Фаза | Зміст робіт | Мінімальна перевірка |
|---|---|---|
| 0 | Аудит ТЗ, `docs/requirements_inventory.md`, структура проєкту, `pyproject.toml` або `requirements.txt`, базовий README, каркас `src/autorl` і `tests` | `pytest`, імпорт пакета без помилок |
| 1 | Доменні сутності, конфігурації YAML/JSON, валідація, `config_hash`, приклади конфігурацій для основних сценаріїв | unit-тести config validation і hash stability |
| 2 | Контрольоване навчальне RL/Gymnasium-подібне середовище: stationary, abrupt_drift, gradual_drift, noisy_reward, fallback; recurring — реалізувати або явно позначити як deferred/Could | тести seed-відтворюваності й режимів drift/noise |
| 3 | `LearningStrategy`, StrategyPool, Fixed, GreedyReward, DriftAware, LCBConservative, TemperedReward, AdaptiveMeta; MetricsCollector і rolling/window aggregation | unit-тести стратегій і метрик |
| 4 | Evaluator і MetaController: utility, LCB, switch criterion, fallback, `DecisionReason` | тести utility, LCB, Stay/Switch/fallback, latency smoke-test |
| 5 | SQLite/file storage, artifacts root, PathGuard, metrics/window_metrics/decisions/events/config/versions | integration-тести запису, читання й часткових логів при помилці |
| 6 | ExperimentOrchestrator, CLI `run/list/report/rerun/validate-config`, перший end-to-end запуск | e2e-тести stationary, abrupt_drift, reproducibility, CLI smoke-tests |
| 6.5 | Benchmark replay mode: `BenchmarkReplayRunner`, `DatasetAdapter`, `CandidateModelRegistry`, H1/H2 candidate registry | unit-тест registry, smoke-тест benchmark replay, перевірка агрегованого звіту без персональних даних |
| 7 | Reports і plots: `report.md`/HTML, reward curve, strategy timeline, utility/LCB, summary tables, CSV/JSON export | integration-тест генерації звіту й наявності файлів |
| 8 | FastAPI backend: health, scenarios, strategies, experiments, start/stop/status/metrics/decisions/report/rerun/compare | API tests через TestClient |
| 9 | Streamlit UI: створення експерименту, моніторинг, метрики, strategy timeline, журнал рішень, порівняння, звіти, відтворюваність | UI smoke-test і `docs/ui_acceptance_checklist.md` |
| 10 | Експериментальні серії: stationary, abrupt drift, gradual drift, noisy reward, tempered reward, H1 control, reproducibility, fallback, baseline comparison | усі запуски мають config, seed, metrics, decisions, plots, report, artifact path |
| 11 | Requirements traceability, test protocol, DOC-01..DOC-10, README, operation manual, фінальні перевірки | повний pytest, CLI/API/UI smoke, performance/memory checks |

У Фазі 11 файл `docs/requirements_traceability.md` має містити трасування не лише FR/NFR, а всіх груп вимог: UC, FR, NFR, UI-AC, API endpoints, CLI commands, SQLite tables, artifacts, SE, EXP і DOC. Для кожного елемента має бути вказано: компонент, тест або перевірка, артефакт результату, статус.

Для benchmark replay mode обов'язково передбачити кандидатні моделі, якщо вони заявлені в науковій частині роботи:

```text
river_logreg
river_nb
river_hoeffding_tree
windowed_rf
windowed_histgb
```

Для H1/H2-профілів конфігурацій необхідно підготувати окремі профілі або YAML-файли:

```text
h1_drift_aware_v1
h1_drift_aware_v2
h2_search
h2_refined_drift_stable
h2_refined_correctness_balanced
h2_tempered_drift
h2_tempered_correctness
adaptive_meta_final
```

Benchmark replay mode має бути доступний щонайменше через CLI, а результати benchmark replay мають відображатися у UI на сторінці порівняння або звітів. Якщо API endpoint для benchmark replay не реалізується окремо, це має бути зафіксовано в `docs/requirements_inventory.md`.

Усі endpoint-и FastAPI мають відповідати таблиці API з цього ТЗ. Якщо додаються альтернативні endpoint-и, сумісні endpoint-и з ТЗ усе одно мають залишатися доступними. Для керування виконанням експерименту обов'язково підтримати `POST /experiments/{id}/start` і `POST /experiments/{id}/stop`.

Після реалізації Streamlit UI необхідно створити `docs/ui_acceptance_checklist.md` і перевірити UI-AC-01..UI-AC-08. Фаза UI не вважається завершеною, якщо користувач не може без редагування коду створити експеримент, запустити його, побачити reward/utility/LCB, переглянути active strategy timeline, відкрити Stay/Switch-журнал, порівняти baseline/adaptive режими, експортувати звіт і повторити запуск із попередньої конфігурації.

Фінальні експериментальні результати повинні містити не лише одиничні значення, а й `n`, список seed, mean, std, confidence interval або інший обґрунтований інтервал невизначеності, effect size там, де порівняння коректне, p-value тільки там, де статистичний тест методично доречний, і обмеження інтерпретації.

Фаза 10 не вважається завершеною, доки в `docs/requirements_inventory.md` усі `SE-01..SE-07` і `EXP-01..EXP-05` не мають статусу `implemented` або `tested`, а для кожного експерименту не вказано шлях до config, metrics, decisions, plots і report.

---

## 9. Архітектура

Система реалізується як **модульний моноліт із шаровою структурою**.

### 9.1. Шари

| Шар | Призначення | Компоненти |
|---|---|---|
| Presentation | Засоби взаємодії користувача | FastAPI, Streamlit, CLI |
| Application | Координація сценаріїв | ExperimentOrchestrator, ConfigService, ExperimentService, ReportService |
| Domain | Предметна логіка | MetaController, StrategyPool, Evaluator, MetricsCollector, Agent/Environment Adapter |
| Infrastructure | Збереження та інтеграції | SQLite, JSON/CSV logger, ArtifactStore, Gymnasium/SB3/river adapters |

### 9.2. Вимога до залежностей

Правильний напрям залежностей:

`Presentation → Application → Domain`  
`Application → Infrastructure`  
`Domain` не повинен залежати від Streamlit, FastAPI, SQLite.

---

### 9.3. Станова модель ExperimentOrchestrator

ExperimentOrchestrator повинен реалізувати явну станову модель виконання експерименту, щоб відповідати проєктній моделі другого розділу і забезпечити тестованість кожного переходу.

Обов'язкові стани:

```text
CREATED / IDLE
VALIDATING_CONFIG
INITIALIZING
COLLECTING
EVALUATING
SWITCHING
STABLE
LOGGING
STOPPING
COMPLETED
FAILED
```

Мінімальна модель, яку потрібно показати в тексті третього розділу:

```text
Idle → Collecting → Evaluating → Switching/Stable → Logging → Completed
```

Обов'язкова поведінка:
- у `VALIDATING_CONFIG` перевіряються конфігурація, шляхи, seed, набір стратегій і параметри метаконтролера;
- у `COLLECTING` збираються епізодичні метрики;
- у `EVALUATING` агрегуються метрики за вікном `W`;
- у `SWITCHING` активна стратегія змінюється тільки після виконання критерію;
- у `STABLE` явно фіксується рішення `Stay`;
- у `LOGGING` записуються метрики, рішення, службові події та артефакти;
- у `FAILED` зберігаються часткові журнали й причина помилки.

---

## 10. Рекомендована структура проєкту

```text
autorl_strategy_manager/
  README.md
  pyproject.toml або requirements.txt
  .gitignore

  configs/
    stationary_adaptive.yaml
    stationary_fixed.yaml
    abrupt_drift_adaptive.yaml
    gradual_drift_adaptive.yaml
    noisy_reward_lcb.yaml
    fallback_insufficient_data.yaml
    reproducibility_seed_42.yaml
    suite_all.yaml

  data/
    autorl.db

  logs/

  artifacts/

  src/
    autorl/
      __init__.py

      presentation/
        api/
          main.py
          routes_experiments.py
          routes_metrics.py
          routes_reports.py
          schemas.py
        ui/
          dashboard.py
          pages/
            01_create_experiment.py
            02_monitor.py
            03_metrics.py
            04_decisions.py
            05_compare.py
            06_reports.py
        cli.py

      application/
        experiment_orchestrator.py
        experiment_service.py
        config_service.py
        report_service.py
        comparison_service.py
        rerun_service.py

      domain/
        entities.py
        learning_strategy.py
        strategy_pool.py
        strategies/
          fixed.py
          greedy.py
          drift_aware.py
          lcb_conservative.py
          tempered_reward.py
          adaptive_meta.py
        metrics_collector.py
        evaluator.py
        meta_controller.py
        reward_shaping.py
        fallback.py

      environments/
        adaptive_learning_env.py
        nonstationary_bandit_env.py
        scenario_factory.py
        gym_adapter.py

      infrastructure/
        sqlite_repository.py
        storage_schema.sql
        artifact_store.py
        json_csv_logger.py
        versioning.py
        path_guard.py
        event_logger.py

      experiments/
        scenario_runner.py
        suite_runner.py
        baselines.py
        statistical_analysis.py

      reporting/
        plots.py
        markdown_report.py
        html_report.py
        exporters.py

  tests/
    unit/
    integration/
    system/
    performance/
    reproducibility/
```

---

### 10.1. Додаткові обов'язкові модулі та конфігурації

До наведеної структури потрібно додати такі елементи, щоб покрити пропущені вимоги контрольної звірки:

```text
configs/
  h1_drift_aware_v1.yaml
  h1_drift_aware_v2.yaml
  h2_search.yaml
  h2_tempered_drift.yaml
  adaptive_meta_final.yaml

src/autorl/application/
  run_mode_service.py

src/autorl/domain/
  decision_reason.py
  metric_schema.py

src/autorl/experiments/
  benchmark_replay_runner.py
  dataset_adapter.py
  candidate_model_registry.py
  experiment_profiles.py
```

`run_mode_service.py` відповідає за `ONLINE_MONITORING` і `OFFLINE_BATCH`; `decision_reason.py` уніфікує причини Stay/Switch/fallback; `metric_schema.py` забезпечує єдині назви метрик; benchmark-модулі потрібні для відтворення H1/H2-профілів і практично-наукових результатів.

---

## 11. Доменна модель

### 11.1. Основні сутності

| Сутність | Поля/зміст |
|---|---|
| Experiment | id, name, scenario, status, seed, config_hash, timestamps, artifact_path |
| Config | environment, agent, strategies, W, beta, lambda, delta, switch_cost, seeds |
| Strategy | id, name, type, exploration, reward_mode, eval_mode, params |
| Metric | episode, reward, duration, variance, rolling_mean, strategy_id |
| Decision | episode, current_strategy, candidate, current_lcb, candidate_lcb, delta, switch_cost, result, reason |
| Artifact | experiment_id, type, path, checksum, created_at |
| Report | experiment summary, metrics summary, decisions, plots, conclusions |

### 11.2. LearningStrategy

Кожна стратегія самонавчання має бути окремим об'єктом, а не рядком у конфігурації.

Обов'язкові атрибути:

```text
strategy_id
name
strategy_type
algorithm_mode
exploration_mode
reward_mode
evaluation_mode
update_rule
parameters
description
```

---

## 12. Портфель стратегій самонавчання

| Стратегія | Роль |
|---|---|
| Fixed Learning Strategy | Базова стратегія без перемикання |
| Greedy Reward Strategy | Comparator за rolling reward |
| Random Switch / Negative Control | Негативний контроль, якщо реалізується |
| Drift-Aware Strategy | Comparator для H1, але не основа реалізації |
| LCB Conservative Strategy | Консервативний стабілізаційний механізм |
| Tempered Reward Strategy | Інженерний напрям H2 |
| Adaptive Meta Strategy | Основна стратегія системи: utility + LCB + threshold + switch cost + fallback |

Важливо: H1 не можна подавати як доведений основний механізм. З пояснювальної записки: H1 не підтверджена і не рекомендована як базовий механізм. H2 не доведена формально при n=5, але приймається як перспективна інженерна лінія; найкращий практичний компроміс — tempered/drift-aware reward shaping.

---

### 12.1. Кандидатні моделі для benchmark replay

Для системного контуру навчальні стратегії залишаються об'єктами `LearningStrategy`. Для практично-наукового benchmark replay додатково потрібен реєстр кандидатних моделей/дій, що відповідає H1/H2-серіям пояснювальної записки.

```text
river_logreg
river_nb
river_hoeffding_tree
windowed_rf
windowed_histgb
```

Ці моделі не замінюють портфель навчальних стратегій у продукті. Вони використовуються як кандидатні механізми в replay-профілях, щоб відтворити порівняння H1/H2 і отримати обережні практично-наукові висновки.

---

## 13. Алгоритмічне ядро

### 13.1. Вхідні дані MetaController

```text
current_strategy
candidate_strategies
metrics_window W
utility_weights w1..w4
beta
lambda
delta
switch_cost
min_samples
environment_state / drift indicators
```

### 13.2. Вихідні дані

```text
decision = Stay або Switch
selected_strategy
reason
current_utility
candidate_utility
current_lcb
candidate_lcb
advantage
threshold
used_metrics
```

### 13.3. Utility

```text
U(gᵢ, W) = w1 * Rmean - w2 * Var - w3 * Ccomp - w4 * Csw
```

### 13.4. LCB

```text
LCB(gᵢ) = μ(Uᵢ) - λ * σ(Uᵢ)
```

### 13.5. Switch criterion

```text
Switch, якщо LCB(candidate) - LCB(current) > δ + Cswitch
інакше Stay
```

### 13.6. Fallback

Fallback спрацьовує, якщо:
- кількість даних < min_samples;
- немає валідних метрик;
- кандидатна стратегія невалідна;
- variance занадто висока;
- advantage не перевищує threshold;
- сталася помилка середовища.

У fallback система зберігає поточну стратегію і записує причину.

---

### 13.7. Стандартизовані причини Stay/Switch/fallback

Журнал рішень, API, UI та звіти повинні використовувати один enum причин. Це потрібно для пояснюваності, трасування і порівнянності результатів.

```text
SWITCH_THRESHOLD_MET
STAY_NO_CANDIDATE_ADVANTAGE
STAY_HIGH_VARIANCE
STAY_INSUFFICIENT_SAMPLES
STAY_SWITCH_COST_TOO_HIGH
STAY_INVALID_CANDIDATE
STAY_MISSING_METRICS
STAY_SAFE_MODE_AFTER_ERROR
FALLBACK_INSUFFICIENT_DATA
FALLBACK_ENVIRONMENT_ERROR
FALLBACK_CONFIG_INTEGRITY_ERROR
```

---

## 14. Середовища та експериментальні сценарії

### 14.1. Обов'язкові режими середовища

| Сценарій | Мета | Очікувана поведінка |
|---|---|---|
| Stationary baseline | Контроль без зміни середовища | Не повинно бути частих зайвих перемикань |
| Abrupt drift | Різка зміна reward/динаміки | Система має перейти після накопичення доказів |
| Gradual drift | Поступова деградація/зміна | Система має реагувати без надмірних switch |
| Noisy reward | Висока дисперсія reward | LCB має зменшити реакцію на шум |
| Fallback insufficient data | Недостатньо епізодів | Stay + reason |
| Reproducibility | Повтор запуску | Той самий config_hash/seed, відтворювані логи |

### 14.2. Потрібні benchmark-и / набори для наукової частини

З пояснювальної записки:

| Benchmark | Роль |
|---|---|
| ASSISTments Skill Builder | Освітній потоковий benchmark; важливий для збереження навчального контексту |
| Elec2 | Drift-heavy benchmark, спільний для H1/H2 |
| OpenML-CC18 / kr-vs-kp | Batch-задача для H1 |
| UCI Adult | Табличний benchmark для H2 |
| UCI Bank Marketing | Табличний benchmark для H2 |

Для повної системи достатньо мати два рівні експериментів:
1. **Вбудоване контрольоване середовище** для системних сценаріїв UI/API.
2. **Benchmark replay mode** для відтворення практично-наукових результатів із H1/H2.

---

### 14.3. Benchmark replay mode

Контрольовані сценарії `stationary`, `abrupt drift`, `gradual drift` і `noisy reward` перевіряють працездатність системного контуру. Окремо потрібен `benchmark replay mode`, який перевіряє практично-наукову частину: чи придатний підхід для реальних або наближених до реальних потокових/табличних задач.

Обов'язкові компоненти:
- `BenchmarkReplayRunner`;
- `DatasetAdapter`;
- `BenchmarkConfig`;
- `CandidateModelRegistry`;
- профілі H1/H2;
- агрегований summary-звіт із кількістю повторів, seed-ами, mean/std/CI.

У разі використання освітніх benchmark-даних система повинна працювати тільки з публічними або анонімізованими записами, не імпортувати персональні ідентифікатори користувачів і не виводити сирі навчальні траєкторії у звіти.

---

## 15. Експерименти, які треба виконати

### 15.1. Системні експерименти для перевірки ПЗ

| ID | Експеримент | Що доводить |
|---|---|---|
| SE-01 | Stationary: Fixed vs Greedy vs LCB vs Adaptive | Adaptive/LCB не перемикає без підстав |
| SE-02 | Abrupt drift | Adaptive реагує на реальну зміну |
| SE-03 | Gradual drift | Adaptive не реагує надто рано |
| SE-04 | Noisy reward | LCB зменшує false switches |
| SE-05 | Fallback | Недостатні дані не дають Switch |
| SE-06 | Rerun | Відтворюваність за seed |
| SE-07 | UI workflow | Користувач може створити, запустити, проаналізувати, експортувати |

### 15.2. Практично-наукові експерименти

| ID | Експеримент | Повтори | Метрики |
|---|---|---:|---|
| EXP-01 | Global baseline suite | 5 | accuracy/prequential accuracy, balanced accuracy, fit time |
| EXP-02 | H1 v2 drift-aware contextual selection | 5 | prequential accuracy, switch regret, stability variance, total switches, mean reward |
| EXP-03 | H2 search | 5 | prequential accuracy, OOD accuracy, reward variance, convergence step, uncertainty, compute cost |
| EXP-04 | H2 tempered | 5 | ті самі метрики + практичний компроміс |
| EXP-05 | Adaptive Meta Strategy vs fixed/greedy/drift-aware/lcb/tempered | 5 | reward, utility, LCB, switches, false switches, recovery time |

### 15.3. H1/H2 профілі конфігурації

| ID | Профіль | Статус | Реалізаційне призначення |
|---|---|---|---|
| EXP-PROFILE-01 | `h1_drift_aware_v1` | контрольний/історичний | Перевірка базового drift-aware reward |
| EXP-PROFILE-02 | `h1_drift_aware_v2` | comparator | Drift-aware reward із regret/cost/drift bonus |
| EXP-PROFILE-03 | `h2_search` | дослідницький | Пошук multi-objective reward-конструкцій |
| EXP-PROFILE-04 | `h2_refined_drift_stable` | comparator | Зниження reward variance при drift-aware логіці |
| EXP-PROFILE-05 | `h2_refined_correctness_balanced` | comparator | Стабілізована correctness-aware версія |
| EXP-PROFILE-06 | `h2_tempered_drift` | перспективний | Найкращий практичний компроміс для реалізації |
| EXP-PROFILE-07 | `h2_tempered_correctness` | comparator | Tempered correctness-aware shaping |
| EXP-PROFILE-08 | `adaptive_meta_final` | основний продукт | Utility + LCB + tempered reward + switch cost + fallback |

Остаточна реалізація системи не повинна дорівнювати H1 або H2 окремо. Вона має бути програмним контуром, який використовує результати H1/H2 для стабільнішого вибору навчальних стратегій.

### 15.4. Правило доказовості результатів

Підсумкові висновки третього розділу не можна формувати з одиничного успішного запуску. Звіт повинен розрізняти:
- одиничний технічний запуск;
- серію запусків;
- baseline comparison;
- benchmark replay;
- статистично обережний висновок;
- practically valuable, але формально не доведений результат.

Для підсумкових таблиць обов'язково вказувати `n`, seed-и, mean, std/CI, а також обмеження інтерпретації.

### 15.5. Наукова інтерпретація

Очікувані висновки не повинні бути перебільшені:

- H1 не подається як підтверджена.
- H1 використовується як comparator/контроль, який показує обмеження простого drift-aware підходу.
- H2 не подається як формально доведена при n=5.
- H2/tempered reward використовується як перспективна інженерна лінія.
- Наукова новизна формулюється навколо:
  - стратегії самонавчання як окремого об'єкта оцінювання і зміни;
  - критерію доцільності зміни, що враховує покращення, надійність, стабільність і switch cost;
  - відтворюваного програмного контуру для аналізу умов, за яких перемикання обґрунтоване.

---

## 16. Метрики результатів

### 16.1. Технічні метрики

| Метрика | Призначення |
|---|---|
| latency_ms_decision | Перевірка ≤ 0.5 с |
| memory_mb | Перевірка ≤ 512 MB |
| run_duration | Тривалість запуску |
| db_write_success | Збереження в БД |
| artifact_count | Повнота артефактів |
| config_hash_match | Відтворюваність |
| tests_passed | Якість реалізації |

### 16.2. RL/експериментальні метрики

| Метрика | Призначення |
|---|---|
| mean_reward | Основна винагорода |
| cumulative_reward | Сумарна винагорода |
| reward_variance | Стабільність |
| reward_std | Розкид |
| rolling_reward | Динаміка |
| utility | Багатокритеріальна корисність |
| LCB | Консервативна оцінка |
| total_switches | Кількість перемикань |
| stay_count | Кількість Stay |
| switch_count | Кількість Switch |
| fallback_count | Кількість fallback |
| false_switches | Зайві перемикання |
| recovery_time | Відновлення після drift |
| switch_regret | Шкода від перемикань |
| stability_variance | Стабільність роботи |
| convergence_step | Швидкість збіжності |
| mean_uncertainty | Невизначеність |
| mean_compute_cost | Обчислювальна вартість |
| effect_size | Практична значущість |
| confidence_interval | Довірчий інтервал |
| p_value | Статистична оцінка, якщо коректна для серії |

---

### 16.3. Єдина схема метрик

Одна й та сама метрика не повинна мати різні назви або різну семантику в UI, API, SQLite, CSV і звітах. Для цього потрібно реалізувати `MetricSchema`, `WindowMetricSchema` і `DecisionSchema`.

Рекомендовані канонічні назви:
- `reward_mean`, а не одночасно `avg_reward`, `mean_reward`, `Rmean`;
- `reward_variance`, а не неузгоджені `Var`, `variance`, `std_reward` без пояснення;
- `utility`, `lcb`, `switch_cost`, `decision`, `decision_reason`;
- `episode`, `strategy_id`, `scenario`, `seed`, `config_hash`.

---

## 17. Web UI: обов'язковий склад

Streamlit UI має бути повноцінним інтерфейсом, а не другорядним переглядачем CSV.

### 17.1. Сторінки

| Сторінка | Функції |
|---|---|
| Dashboard / Overview | Кількість експериментів, останні запуски, статуси, доступні сценарії |
| Create Experiment | Форма конфігурації експерименту |
| Run Monitor | Статус, поточний епізод, активна стратегія, reward, switch/stay/fallback |
| Metrics | Reward curve, rolling mean, variance, utility, LCB |
| Strategy Timeline | Активна стратегія за епізодами |
| Decisions | Таблиця Stay/Switch із причинами |
| Compare Strategies | Порівняння fixed/greedy/drift-aware/lcb/tempered/adaptive |
| Reports | Перегляд/експорт report.md/html, csv, json, plots |
| Reproducibility | seed, config_hash, versions, rerun |
| Settings / Config validation | Перевірка YAML/JSON, параметри системи |

### 17.2. UI-компоненти

- selectbox сценаріїв;
- multiselect стратегій;
- numeric inputs для episodes/W/beta/lambda/delta/switch_cost;
- status indicators;
- charts;
- tables;
- download buttons;
- rerun button;
- config preview;
- validation messages.

---

### 17.3. Acceptance criteria для практичної цінності UI

| ID | Вимога | Пріоритет | Acceptance criteria |
|---|---|---:|---|
| UI-AC-01 | Користувач може створити експеримент без редагування коду | Must | Через форму UI |
| UI-AC-02 | Користувач може запустити експеримент і бачити статус | Must | Status panel оновлюється |
| UI-AC-03 | Користувач бачить reward/utility/LCB графіки | Must | Мінімум 3 графіки |
| UI-AC-04 | Користувач бачить active strategy timeline | Must | Окремий графік або таблиця |
| UI-AC-05 | Користувач бачить Stay/Switch журнал із причинами | Must | Таблиця decisions |
| UI-AC-06 | Користувач може порівняти baseline/adaptive | Must | Compare page |
| UI-AC-07 | Користувач може експортувати звіт і CSV | Must | Download buttons |
| UI-AC-08 | Користувач може повторити запуск із попередньої конфігурації | Must | Rerun button |

---

## 18. API

| Method | Endpoint | Призначення |
|---|---|---|
| POST | `/experiments` | Створення експерименту |
| POST | `/experiments/{id}/start` | Запуск |
| POST | `/experiments/{id}/stop` | Зупинка |
| GET | `/experiments` | Список експериментів |
| GET | `/experiments/{id}` | Деталі |
| GET | `/experiments/{id}/status` | Статус і активна стратегія |
| GET | `/experiments/{id}/metrics` | Метрики |
| GET | `/experiments/{id}/decisions` | Журнал рішень |
| GET | `/experiments/{id}/report` | Звіт |
| POST | `/experiments/{id}/rerun` | Повтор запуску |
| GET | `/scenarios` | Доступні сценарії |
| GET | `/strategies` | Доступні стратегії |
| GET | `/compare` | Порівняння результатів |

---

## 19. CLI

```bash
autorl validate-config --config configs/stationary_adaptive.yaml
autorl run --config configs/abrupt_drift_adaptive.yaml
autorl run-suite --config configs/suite_all.yaml
autorl list
autorl status --experiment-id EXP_ID
autorl report --experiment-id EXP_ID
autorl rerun --experiment-id EXP_ID
autorl export --experiment-id EXP_ID --format zip
```

---

## 20. Сховище даних

### 20.1. SQLite tables

| Таблиця | Призначення |
|---|---|
| experiments | Запуски |
| configs | Snapshot конфігурацій |
| strategies | Стратегії |
| episode_metrics | Метрики епізодів |
| window_metrics | Агреговані метрики |
| decisions | Stay/Switch-рішення |
| artifacts | Файли |
| events | Технічні події |
| errors | Помилки |
| reruns | Зв'язок повторних запусків |

### 20.2. Артефакти запуску

```text
artifacts/
  EXP_ID/
    config.yaml
    config_hash.txt
    versions.json
    environment.json
    metrics.csv
    window_metrics.csv
    decisions.csv
    events.log
    report.md
    report.html
    plots/
      reward_curve.png
      rolling_reward.png
      strategy_timeline.png
      utility_lcb.png
      comparison.png
```

---

### 20.3. Обмеження щодо даних і безпеки benchmark replay

- Усі шляхи артефактів мають бути всередині дозволених директорій `data/`, `logs/`, `artifacts/`.
- `PathGuard` повинен блокувати запис у довільні системні шляхи.
- Якщо використовується ASSISTments або інший освітній benchmark, `DatasetAdapter` не повинен імпортувати персональні ідентифікатори користувачів.
- `ReportService` експортує тільки агреговані метрики, таблиці й графіки, без персональних записів або сирих навчальних траєкторій.

---

## 21. Тестування

### 21.1. Тести з CSV протоколу

| Тип | Сценарій | Очікуваний результат | Метрика |
|---|---|---|---|
| Unit | `test_lcb_criterion()` | Коректний розрахунок нижньої межі | `abs(calc - expected) < 1e-5` |
| Unit | `test_tempered_reward()` | Коректне змішування базової та shaped винагороди | `0 <= reward <= 1` |
| Integration | `test_full_pipeline()` | Запуск → метрики → рішення → БД | `0 exceptions`, `decisions.count >= 1` |
| System | `POST /api/experiment` | Створення експерименту | `status_code == 201`, `id > 0` |
| Performance | 1000 кроків оцінки | Час рішення ≤ 0.5 с, пам'ять ≤ 512 MB | `latency_ms`, `memory_mb` |
| Reproducibility | 5 запусків seed 42–46 | Розкид метрик ≤ 5% | `std_dev / mean < 0.05` |

### 21.2. Додаткові обов'язкові тести

| Тип | Тест |
|---|---|
| Unit | config validation |
| Unit | utility calculation |
| Unit | switch threshold |
| Unit | fallback insufficient samples |
| Unit | path guard |
| Integration | artifact creation |
| Integration | report generation |
| Integration | UI reads data without domain logic |
| System | stationary scenario |
| System | abrupt drift scenario |
| System | gradual drift scenario |
| System | noisy reward scenario |
| UI smoke | Streamlit dashboard opens and displays experiments |
| API | all endpoints return expected schemas |
| Failure | environment error saves partial logs |

---

### 21.6. Розмежування системної та практично-наукової валідації

Результати третього розділу повинні бути поділені на дві групи.

| Тип валідації | Що доводить | Приклади результатів |
|---|---|---|
| Системна валідація ПЗ | Програмна система працює як продукт | UI створює запуск, API повертає дані, CLI виконує suite, SQLite/logs заповнюються, fallback і rerun працюють, performance-тести проходять |
| Практично-наукова валідація підходу | Підхід має дослідницьку цінність | baseline comparison, H1 як negative/comparator, H2 tempered як перспективний напрям, adaptive_meta_final, effect size/CI/p-value там, де це коректно |

---

### 21.7. Фінальні gates перевірки реалізації

Перед використанням результатів у третьому розділі необхідно виконати фінальний набір перевірок:

- `pytest` для всіх unit/integration/system tests;
- coverage-звіт, якщо підключено `pytest-cov`;
- CLI smoke-run для запуску експерименту, формування звіту й повторного запуску;
- API smoke-run для `/health`, створення експерименту, статусу, метрик, рішень і звіту;
- UI smoke-run для Streamlit-додатка;
- перевірка online-monitoring режиму через UI/API;
- перевірка offline-batch режиму через CLI або run-suite;
- performance test для decision latency ≤ 0.5 с на CPU;
- memory smoke-test або зафіксоване наближення, що типовий сценарій не перевищує 512 MB;
- перевірка, що жоден науковий висновок не сформовано без фактичного запуску й артефактів;
- перевірка, що `docs/requirements_inventory.md` не містить незакритих Must-вимог без пояснення.

---

## 22. Документація

Для повного виконання третього розділу потрібні не тільки код і README, а й інженерні артефакти, які або входять до основного тексту, або розміщуються в додатках.

| ID | Артефакт | Призначення |
|---|---|---|
| DOC-01 | Use Case Diagram | Показати взаємодію користувача, дослідника та розробника стратегій із системою |
| DOC-02 | DFD Level 0 | Показати потоки `config → orchestrator → metrics → controller → logs/reports` |
| DOC-03 | Component Diagram | Показати Presentation/Application/Domain/Infrastructure |
| DOC-04 | Sequence Diagram Stay/Switch | Показати послідовність збору метрик, оцінювання і рішення |
| DOC-05 | State Machine Diagram | Показати стани експерименту |
| DOC-06 | ER Diagram або SQL schema | Показати `experiments/configs/strategies/metrics/decisions/artifacts` |
| DOC-07 | Deployment Diagram | Показати локальне розгортання: VS Code, venv, FastAPI, Streamlit, SQLite |
| DOC-08 | Матриця трасування вимог | Зв'язати вимоги з компонентами, тестами й результатами |
| DOC-09 | MoSCoW-таблиця вимог | Зафіксувати пріоритети Must/Should/Could/Won't |
| DOC-10 | Експлуатаційна інструкція | Встановлення, запуск, конфігурація, моніторинг, аварійне відновлення |


Має бути:

- README.md;
- інструкція встановлення;
- інструкція запуску API;
- інструкція запуску Streamlit;
- інструкція CLI;
- опис конфігурацій;
- опис сценаріїв;
- опис артефактів;
- інструкція повторного запуску;
- аварійне відновлення після помилки;
- приклади команд;
- список залежностей.

---

## 23. Матеріали для третього розділу

Після реалізації треба отримати:

| Матеріал | Для якого підрозділу |
|---|---|
| Структура проєкту | 3.1 / 3.3 |
| Таблиця стеку | 3.2 |
| Скріншоти UI | 3.1, 3.6, 3.9 |
| Приклади конфігів | 3.4 |
| SQL/ER або таблиця БД | 3.4 |
| Псевдокод/фрагмент MetaController | 3.5 |
| Таблиця API | 3.6 |
| Таблиця CLI | 3.6 |
| Тест-кейси | 3.7 |
| Pytest/coverage results | 3.7 |
| Експериментальні сценарії | 3.8 |
| Таблиці результатів | 3.9 |
| Графіки reward/LCB/strategy timeline | 3.9 |
| Журнал Stay/Switch | 3.9 |
| CI/p-value/effect size, якщо коректно | 3.9 |
| Таблиця відповідності вимогам | 3.10 |
| Обмеження | 3.11 |
| README/експлуатаційна документація | Додатки / 3.5 |

---

## 24. Критерії готовності системи

Система може вважатися готовою для написання третього розділу, якщо виконано:

- [ ] є робочий Streamlit UI;
- [ ] є FastAPI API;
- [ ] є CLI;
- [ ] є SQLite БД;
- [ ] є configs для всіх сценаріїв;
- [ ] є StrategyPool;
- [ ] є MetaController;
- [ ] є utility + LCB + switch criterion;
- [ ] є tempered reward;
- [ ] є fallback;
- [ ] є logging technical/domain;
- [ ] є artifacts directory;
- [ ] є reports;
- [ ] є plots;
- [ ] є rerun;
- [ ] є tests;
- [ ] проходить performance ≤ 0.5s decision;
- [ ] підтверджено CPU-only режим;
- [ ] підтверджено відсутність персональних даних;
- [ ] виконано stationary, abrupt, gradual, noisy, fallback, reproducibility;
- [ ] виконано baseline/adaptive comparison;
- [ ] отримано таблиці й графіки для третього розділу;
- [ ] сформовано README.

- [ ] створено й оновлено `docs/requirements_inventory.md`;
- [ ] усі Must-вимоги мають статус `implemented` або `tested`;
- [ ] створено `docs/ui_acceptance_checklist.md`;
- [ ] UI-AC-01..UI-AC-08 виконані;
- [ ] реалізовано або обґрунтовано відкладено recurring scenario;
- [ ] benchmark replay має H1/H2 candidate registry;
- [ ] створено H1/H2 YAML-профілі: `h1_drift_aware_v1`, `h1_drift_aware_v2`, `h2_search`, `h2_refined_drift_stable`, `h2_refined_correctness_balanced`, `h2_tempered_drift`, `h2_tempered_correctness`, `adaptive_meta_final`;
- [ ] експериментальні таблиці містять `n`, seed, mean, std/CI та обмеження інтерпретації;
- [ ] кожен практично-науковий висновок у звітах має посилання на фактичний run/artifact path;
- [ ] виконано CLI/API/UI smoke-перевірки;
- [ ] створено DOC-01..DOC-10 або їх Markdown/Mermaid-еквіваленти;

---

## 25. Остаточне ТЗ одним реченням

Розробити локальну програмну систему **AutoRL Strategy Manager** як адаптивну інтелектуальну навчальну систему на основі RL-підходу, що через веб-інтерфейс, API та CLI дозволяє запускати відтворювані експерименти самонавчання агента, динамічно вибирати навчальні стратегії за критерієм utility/LCB/tempered reward/switch cost, журналювати причини Stay/Switch-рішень, порівнювати baseline та adaptive режими, формувати звіти й забезпечувати практично-наукові результати для підтвердження меж застосування і наукової новизни роботи.

