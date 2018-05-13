## Results

0. [Info](#0-info)
1. [Baseline](#1-baseline)
2. [Baseline translation](#2-translation-baseline)
3. [Back-Forward Translation](#3-back-forward-translation)
4. [Transfer learning](#4-transfer-learning)


### 0. Info

1. bleu is nltk-bleu

2. one batch per step is viewed

3. batch_size is 4096

### 1. Baseline

#### hebrew-english

##### single-random-reference mode

results on new test ~ 29K

10K steps, 4096 batch_size:

train_size | bleu
---------- | ----
236K(0.8) | 0.63
88K(0.3) | 0.59
50K(0.17) | 0.51
29K(0.1) | 0.44
3K(0.01) | 0.05


50K train_size(~ 12 steps/epoch):

steps, K | bleu
---------|-----
10 | 51
11 | 51.9
13 | 52.3
18 | 52.4


236K train size(~ 58 steps/epoch)

steps, K | bleu
---------|-----
2 | 33
4 | 53
7 | 60
10 | 63.5
15 | 66
17 | 66.7
19 | 67
21 | 67.3
22 | 67.6
23 | 67.8

##### all-reference mode

236K train size:

results on new dev ~ 29K:

steps | bleu
------|-----
11K | 60.04
12K | 60.77
13K | 61.05
14K | 61.53
15K | 61.99
16K | 62.34
17K | 62.29
18K | 62.85
19K | 62.6
20K | 62.92

results on old dev ~ 4K:

he-en

steps | bleu
------|-----
11K | 56.29
12K | 57.45
13K | 57.76
14K | 57.74
15K | 58.69
16K | 58.93
17K | 58.91
18K | 59.52
19K | 58.97
20K | 59.14


en-he

steps | bleu
------|-----
4K | 61.07
5K | 66.86
6K | 68.86
7K | 70.81
8K | 71.06
9K | 73.22
10K | 73.71
11K | 74.29
12K | 74.99
13K | 75.27
14K | 75.77

![100__test4000](https://trello-attachments.s3.amazonaws.com/5a8c674b302a8b5b2f0d9cd8/5aa70addb0e4401313478392/0991d054934a1bae91db7ad40d5dbb58/100__test4000.png)

results on old test ~ 1K:

steps | bleu
------|-----
11К | 53.10
12К | 48.07
13K | 51.84
14K | 45.06
15K | 43.86
16K | 48.39
17K | 48.29
18K | 48.79
19K | 52.30
20K | 46.69

### 2. Translation baseline
Results on 3k test set 
#### english-russian
Training curves
![epochs.png](https://trello-attachments.s3.amazonaws.com/5a8c674b302a8b5b2f0d9cd8/5aa6fec0cca08f5bd69bec27/8d59947189cbbd534afae99deee216a3/epochs.png) 
![passes.png](https://trello-attachments.s3.amazonaws.com/5a8c674b302a8b5b2f0d9cd8/5aa6fec0cca08f5bd69bec27/beadeadda57b8f69eeee01312daa3b11/passes_(1).png) 
Training size
![all.png](https://trello-attachments.s3.amazonaws.com/5a8c674b302a8b5b2f0d9cd8/5aa6fec0cca08f5bd69bec27/dc23060666ca539893b7b28d2a046dc4/all.png) 
### 3. Back-Forward Translation


results he-en on new test 29K:

setup | bleu
------|-----
100% train | 67.80
10% train | 42.26
10% train + 90% forward translated | 38.46
10% train + 90% back translated | 33.28
10% train + 10% forward translated | 42.40
10% train + 10% back translated | 44.33
10% train + 10% back weight translated | 44.55

![he-en_10__test](https://trello-attachments.s3.amazonaws.com/5a8c674b302a8b5b2f0d9cd8/5aa70addb0e4401313478392/f1e26c2b989e085e15439f453cde786c/he-en_10__test.png)

results en-he on old dev 4K:

setup | bleu
------|-----
100% train | 75.77
10% train | 45.89
10% train + 10% forward translated | 46.33
10% train + 10% back translated | 47.05

![en-he_10__test](https://trello-attachments.s3.amazonaws.com/5a8c674b302a8b5b2f0d9cd8/5aa70addb0e4401313478392/2ca7457d6589cdfde94a588e633c2421/en-he_10__test.png)

results en-ru on 15K test:

setup | bleu cased
------|-----
100K train | 14.87
200K train | 16.35
100K train + 100K back translated | 16.39

![en-ru_10__test](https://trello-attachments.s3.amazonaws.com/5a8c674b302a8b5b2f0d9cd8/5aa70addb0e4401313478392/26fd0adabf7d09d89c9969ef8cdbf093/en-ru_test.png)

results en-ru on 15K test:

setup | bleu cased
------|-----
100K train | 14.87
100K train + 100K back translated | 16.39
100K train + 300K back translated | 18.12
100K train + 860K back translated | 18.35
100K train + 860K back translated 32K dict | 19.11

results ru-en on 15K test:

setup | bleu cased
------|-----
100K train | 17.96
100K train + 100K back translated | 20.29

### Joint training

results en-ru on 15K test:

setup | bleu cased
------|-----
100K train, iter 0 | 14.87
100K train + 100K back translated, iter 1 | 16.39
100K train + 100K back translated, iter 2 | 16.73

![en-ru_10__test](https://trello-attachments.s3.amazonaws.com/5a8c674b302a8b5b2f0d9cd8/5aa70addb0e4401313478392/d0f0b6295e9dd5761fbbcd1d26be4c41/en-ru_jt_test.png)

### Many to One (from Zero-shot)

results on 15K test:

setup | bleu cased
------|-----
100K en-ru | 14.87
100K en-ru + 100K de-ru | 15.38
100K train + 100K back translated | 16.08

![en-ru_de-ru__test](https://trello-attachments.s3.amazonaws.com/5a8c674b302a8b5b2f0d9cd8/5aa70addb0e4401313478392/e205d5899a22662011f1f85b6bc65ec9/en-ru_mto_test.png)

### 4. Transfer learning

![en-ru_bleu_translation](https://github.com/awant/lowResourceNMT/blob/master/en-ru_approx_bleu_scores.png)

|             |                                                                                                                                                                     Sentences                                                                                                                                                                     |
|-------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------:|
| orig sent   | Traditionally, the Arabs have worshiped and appreciated hunt with hunting birds (using saker falcons for hunting houbara bustard).                                                                                                                                                                                                                |
| ref tr      | Особым почетом и показателем престижности у арабов традиционно считается охота с ловчими птицами (с соколами-балобанами на дроф-красоток).                                                                                                                                                                                                        |
| small tr    | Традиционно, арабы поклоняются и переживают охотник птицам (используя сакерные муки для охоты на охотохарактеризованных кусках).                                                                                                                                                                                                                  |
| transfer tr | Традиционно арабы поклонялись и ценили охоту птиц охоты (с использованием saker falcons для охоты на бухте хоubara).                                                                                                                                                                                                                              |
|             |                                                                                                                                                                                                                                                                                                                                                   |
| orig sent   | Also, with this technology, user-friendly scanning can be easily integrated into existing browser-based business applications, streamlining the capture and classification of paper documents.                                                                                                                                                    |
| ref tr      | Кроме того, данная технология помогает без лишних сложностей интегрировать удобные функции сканирования в имеющиеся бизнес-приложения на основе браузера, чтобы ускорить процессы сканирования и документооборота.                                                                                                                                |
| small tr    | Кроме того, с помощью этой технологии, удобное сканирование может быть интегрированно в существующее приложения для бизнеса, упрощение оптимизации и классификации документов.                                                                                                                                                                    |
| transfer tr | Кроме того, с помощью этой технологии пользователь может быть легко встроен в существующие бизнес-приложения на базе браузеров, что упрощает процесс улавливания и классификации бумажных документов.                                                                                                                                             |
|             |                                                                                                                                                                                                                                                                                                                                                   |
| orig sent   | We don't deal with newspapers, TV-channels or information agencies about low price of placement of customers' paid materials - this is not our profile.                                                                                                                                                                                           |
| ref tr      | Мы не договариваемся с газетами, телеканалами, информационными агентствами о низкой цене размещения платных материалов про компанию заказчика - это не наш профиль (тем более это не PR, а всего лишь распределение маркетингового бюджета в СМИ, только вместо рекламных макетов выходят хвалебные статьи или сюжеты, которым мало кто поверит). |
| small tr    | Мы не имеем отношения с газетами, телевизорами или информационными агентствами о низких ценах написания московских материалов - это не наш профиль.                                                                                                                                                                                               |
| transfer tr | Мы не имеем дело с газетами, телеканалами или информационными агентствами о низкой цене размещения оплачиваемых материалов клиентов - это не наш профиль.                                                                                                                                                                                         |
|             |                                                                                                                                                                                                                                                                                                                                                   |
| orig sent   | Microsoft offers the software for use in a variety of devices, including set-top boxes and handhelds.                                                                                                                                                                                                                                             |
| ref tr      | Microsoft предлагает ПО для самых разнообразных устройств, включая ТВ-приставки и карманные ПК.                                                                                                                                                                                                                                                   |
| small tr    | Microsoft предлагает программное обеспечение для использования в различных устройствах, в том числе базовых ящиков и карманов.                                                                                                                                                                                                                    |
| transfer tr | Microsoft предлагает программное обеспечение для использования в различных устройствах, включая коробки с set-top и карманные КПК.                                                                                                                                                                                                                |
|             |                                                                                                                                                                                                                                                                                                                                                   |
| orig sent   | The return of Silvio Berlusconi, a self-declared European "advocate" for Mr. Putin and his gang, can only make things worse.                                                                                                                                                                                                                      |
| ref tr      | Ситуация усугубляется возвращением к власти Сильвио Берлускони, который сам вызвался быть "адвокатом" Путина и его клики в Европе.                                                                                                                                                                                                                |
| small tr    | Возвращение Силвии Берлуи, самоуверенный европейский "адвокат" для г-на Путина и его ганга, может только усугубиться.                                                                                                                                                                                                                             |
| transfer tr | Возвращение Силвии Берлукона, самопровозглашенного европейского "адвоката" для Путина и его банды, может только усложнить ситуацию.                                                                                                                                                                                                               |
