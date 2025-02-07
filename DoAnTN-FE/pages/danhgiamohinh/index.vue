<template>
  <div class="dashboard">
    <h1>Đánh giá mô hình</h1>
    <div class="chart-container">
      <Chart type="line" :data="chartData" :options="chartOptions" />
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';

const dataMetrics = {
  "metrics": {
    "accuracy": 0.8053830227743272,
    "precision": 1.0,
    "recall": 0.8053830227743272,
    "f1": 0.8922018348623854,
    "exact_match_rate": 0.8053830227743272
  },
};

const lossLogs = [
    {
        "step": 10,
        "loss": 4.7454
    },
    {
        "step": 20,
        "loss": 1.8645
    },
    {
        "step": 30,
        "loss": 1.5324
    },
    {
        "step": 40,
        "loss": 1.3632
    },
    {
        "step": 50,
        "loss": 1.2573
    },
    {
        "step": 60,
        "loss": 1.0641
    },
    {
        "step": 70,
        "loss": 1.0735
    },
    {
        "step": 80,
        "loss": 0.9567
    },
    {
        "step": 90,
        "loss": 0.9332
    },
    {
        "step": 100,
        "loss": 0.9279
    },
    {
        "step": 110,
        "loss": 0.8575
    },
    {
        "step": 120,
        "loss": 0.763
    },
    {
        "step": 130,
        "loss": 0.8043
    },
    {
        "step": 140,
        "loss": 0.7353
    },
    {
        "step": 150,
        "loss": 0.7827
    },
    {
        "step": 160,
        "loss": 0.7659
    },
    {
        "step": 170,
        "loss": 0.6828
    },
    {
        "step": 180,
        "loss": 0.72
    },
    {
        "step": 190,
        "loss": 0.6848
    },
    {
        "step": 200,
        "loss": 0.687
    },
    {
        "step": 210,
        "loss": 0.6196
    },
    {
        "step": 220,
        "loss": 0.5787
    },
    {
        "step": 230,
        "loss": 0.535
    },
    {
        "step": 240,
        "loss": 0.5497
    },
    {
        "step": 250,
        "loss": 0.5161
    },
    {
        "step": 260,
        "loss": 0.5267
    },
    {
        "step": 270,
        "loss": 0.5343
    },
    {
        "step": 280,
        "loss": 0.4624
    },
    {
        "step": 290,
        "loss": 0.5896
    },
    {
        "step": 300,
        "loss": 0.538
    },
    {
        "step": 310,
        "loss": 0.455
    },
    {
        "step": 320,
        "loss": 0.5198
    },
    {
        "step": 330,
        "loss": 0.4426
    },
    {
        "step": 340,
        "loss": 0.4051
    },
    {
        "step": 350,
        "loss": 0.3592
    },
    {
        "step": 360,
        "loss": 0.3822
    },
    {
        "step": 370,
        "loss": 0.3558
    },
    {
        "step": 380,
        "loss": 0.3279
    },
    {
        "step": 390,
        "loss": 0.3007
    },
    {
        "step": 400,
        "loss": 0.3025
    },
    {
        "step": 410,
        "loss": 0.291
    },
    {
        "step": 420,
        "loss": 0.3271
    },
    {
        "step": 430,
        "loss": 0.2845
    },
    {
        "step": 440,
        "loss": 0.2994
    },
    {
        "step": 450,
        "loss": 0.2921
    },
    {
        "step": 460,
        "loss": 0.3174
    },
    {
        "step": 470,
        "loss": 0.2879
    },
    {
        "step": 480,
        "loss": 0.2792
    },
    {
        "step": 490,
        "loss": 0.2675
    },
    {
        "step": 500,
        "loss": 0.2769
    },
    {
        "step": 510,
        "loss": 0.2766
    },
    {
        "step": 520,
        "loss": 0.2332
    },
    {
        "step": 530,
        "loss": 0.2707
    },
    {
        "step": 540,
        "loss": 0.2514
    },
    {
        "step": 550,
        "loss": 0.2343
    },
    {
        "step": 560,
        "loss": 0.2315
    },
    {
        "step": 570,
        "loss": 0.2124
    },
    {
        "step": 580,
        "loss": 0.2079
    },
    {
        "step": 590,
        "loss": 0.25
    },
    {
        "step": 600,
        "loss": 0.1961
    },
    {
        "step": 610,
        "loss": 0.2239
    },
    {
        "step": 620,
        "loss": 0.2049
    },
    {
        "step": 630,
        "loss": 0.2248
    },
    {
        "step": 640,
        "loss": 0.2126
    },
    {
        "step": 650,
        "loss": 0.2261
    },
    {
        "step": 660,
        "loss": 0.1869
    },
    {
        "step": 670,
        "loss": 0.1706
    },
    {
        "step": 680,
        "loss": 0.1499
    },
    {
        "step": 690,
        "loss": 0.1444
    },
    {
        "step": 700,
        "loss": 0.1422
    },
    {
        "step": 710,
        "loss": 0.1399
    },
    {
        "step": 720,
        "loss": 0.143
    },
    {
        "step": 730,
        "loss": 0.1329
    },
    {
        "step": 740,
        "loss": 0.1567
    },
    {
        "step": 750,
        "loss": 0.1493
    },
    {
        "step": 760,
        "loss": 0.1313
    },
    {
        "step": 770,
        "loss": 0.1386
    },
    {
        "step": 780,
        "loss": 0.1505
    },
    {
        "step": 790,
        "loss": 0.1211
    },
    {
        "step": 800,
        "loss": 0.1138
    },
    {
        "step": 810,
        "loss": 0.1239
    },
    {
        "step": 820,
        "loss": 0.114
    },
    {
        "step": 830,
        "loss": 0.1251
    },
    {
        "step": 840,
        "loss": 0.1148
    },
    {
        "step": 850,
        "loss": 0.1267
    },
    {
        "step": 860,
        "loss": 0.1094
    },
    {
        "step": 870,
        "loss": 0.135
    },
    {
        "step": 880,
        "loss": 0.1103
    },
    {
        "step": 890,
        "loss": 0.101
    },
    {
        "step": 900,
        "loss": 0.1089
    },
    {
        "step": 910,
        "loss": 0.1253
    },
    {
        "step": 920,
        "loss": 0.0932
    },
    {
        "step": 930,
        "loss": 0.1193
    },
    {
        "step": 940,
        "loss": 0.1057
    },
    {
        "step": 950,
        "loss": 0.1001
    },
    {
        "step": 960,
        "loss": 0.0881
    },
    {
        "step": 970,
        "loss": 0.0981
    },
    {
        "step": 980,
        "loss": 0.0972
    },
    {
        "step": 990,
        "loss": 0.0917
    },
    {
        "step": 1000,
        "loss": 0.1079
    },
    {
        "step": 1010,
        "loss": 0.0967
    },
    {
        "step": 1020,
        "loss": 0.074
    },
    {
        "step": 1030,
        "loss": 0.0767
    },
    {
        "step": 1040,
        "loss": 0.0776
    },
    {
        "step": 1050,
        "loss": 0.0702
    },
    {
        "step": 1060,
        "loss": 0.0698
    },
    {
        "step": 1070,
        "loss": 0.0787
    },
    {
        "step": 1080,
        "loss": 0.0661
    },
    {
        "step": 1090,
        "loss": 0.0719
    },
    {
        "step": 1100,
        "loss": 0.0789
    },
    {
        "step": 1110,
        "loss": 0.0592
    },
    {
        "step": 1120,
        "loss": 0.0653
    },
    {
        "step": 1130,
        "loss": 0.0678
    },
    {
        "step": 1140,
        "loss": 0.066
    },
    {
        "step": 1150,
        "loss": 0.0704
    },
    {
        "step": 1160,
        "loss": 0.0677
    },
    {
        "step": 1170,
        "loss": 0.0641
    },
    {
        "step": 1180,
        "loss": 0.0666
    },
    {
        "step": 1190,
        "loss": 0.0679
    },
    {
        "step": 1200,
        "loss": 0.0708
    },
    {
        "step": 1210,
        "loss": 0.0524
    },
    {
        "step": 1220,
        "loss": 0.0572
    },
    {
        "step": 1230,
        "loss": 0.0631
    },
    {
        "step": 1240,
        "loss": 0.0658
    },
    {
        "step": 1250,
        "loss": 0.0539
    },
    {
        "step": 1260,
        "loss": 0.0593
    },
    {
        "step": 1270,
        "loss": 0.0517
    },
    {
        "step": 1280,
        "loss": 0.0636
    },
    {
        "step": 1290,
        "loss": 0.0579
    },
    {
        "step": 1300,
        "loss": 0.0624
    },
    {
        "step": 1310,
        "loss": 0.0555
    },
    {
        "step": 1320,
        "loss": 0.0595
    },
    {
        "step": 1330,
        "loss": 0.0591
    },
    {
        "step": 1340,
        "loss": 0.0446
    },
    {
        "step": 1350,
        "loss": 0.0412
    },
    {
        "step": 1360,
        "loss": 0.035
    },
    {
        "step": 1370,
        "loss": 0.039
    },
    {
        "step": 1380,
        "loss": 0.0352
    },
    {
        "step": 1390,
        "loss": 0.0332
    },
    {
        "step": 1400,
        "loss": 0.0348
    },
    {
        "step": 1410,
        "loss": 0.036
    },
    {
        "step": 1420,
        "loss": 0.0381
    },
    {
        "step": 1430,
        "loss": 0.0362
    },
    {
        "step": 1440,
        "loss": 0.0338
    },
    {
        "step": 1450,
        "loss": 0.0352
    },
    {
        "step": 1460,
        "loss": 0.0384
    },
    {
        "step": 1470,
        "loss": 0.0381
    },
    {
        "step": 1480,
        "loss": 0.0354
    },
    {
        "step": 1490,
        "loss": 0.0357
    },
    {
        "step": 1500,
        "loss": 0.0362
    },
    {
        "step": 1510,
        "loss": 0.0317
    },
    {
        "step": 1520,
        "loss": 0.0347
    },
    {
        "step": 1530,
        "loss": 0.0312
    },
    {
        "step": 1540,
        "loss": 0.0373
    },
    {
        "step": 1550,
        "loss": 0.0333
    },
    {
        "step": 1560,
        "loss": 0.0339
    },
    {
        "step": 1570,
        "loss": 0.0246
    },
    {
        "step": 1580,
        "loss": 0.0311
    },
    {
        "step": 1590,
        "loss": 0.0338
    },
    {
        "step": 1600,
        "loss": 0.0306
    },
    {
        "step": 1610,
        "loss": 0.0268
    },
    {
        "step": 1620,
        "loss": 0.0294
    },
    {
        "step": 1630,
        "loss": 0.0294
    },
    {
        "step": 1640,
        "loss": 0.0285
    },
    {
        "step": 1650,
        "loss": 0.0383
    },
    {
        "step": 1660,
        "loss": 0.0281
    },
    {
        "step": 1670,
        "loss": 0.0262
    },
    {
        "step": 1680,
        "loss": 0.0233
    },
    {
        "step": 1690,
        "loss": 0.0204
    },
    {
        "step": 1700,
        "loss": 0.0175
    },
    {
        "step": 1710,
        "loss": 0.0205
    },
    {
        "step": 1720,
        "loss": 0.0231
    },
    {
        "step": 1730,
        "loss": 0.0192
    },
    {
        "step": 1740,
        "loss": 0.0194
    },
    {
        "step": 1750,
        "loss": 0.0236
    },
    {
        "step": 1760,
        "loss": 0.0193
    },
    {
        "step": 1770,
        "loss": 0.0195
    },
    {
        "step": 1780,
        "loss": 0.0196
    },
    {
        "step": 1790,
        "loss": 0.0186
    },
    {
        "step": 1800,
        "loss": 0.0199
    },
    {
        "step": 1810,
        "loss": 0.0162
    },
    {
        "step": 1820,
        "loss": 0.0167
    },
    {
        "step": 1830,
        "loss": 0.0165
    },
    {
        "step": 1840,
        "loss": 0.0178
    },
    {
        "step": 1850,
        "loss": 0.0179
    },
    {
        "step": 1860,
        "loss": 0.0212
    },
    {
        "step": 1870,
        "loss": 0.0211
    },
    {
        "step": 1880,
        "loss": 0.0185
    },
    {
        "step": 1890,
        "loss": 0.0147
    },
    {
        "step": 1900,
        "loss": 0.0162
    },
    {
        "step": 1910,
        "loss": 0.0177
    },
    {
        "step": 1920,
        "loss": 0.0213
    },
    {
        "step": 1930,
        "loss": 0.0202
    },
    {
        "step": 1940,
        "loss": 0.0163
    },
    {
        "step": 1950,
        "loss": 0.0192
    },
    {
        "step": 1960,
        "loss": 0.0185
    },
    {
        "step": 1970,
        "loss": 0.0159
    },
    {
        "step": 1980,
        "loss": 0.0181
    },
    {
        "step": 1990,
        "loss": 0.0143
    },
    {
        "step": 2000,
        "loss": 0.0154
    },
    {
        "step": 2010,
        "loss": 0.0185
    },
    {
        "step": 2020,
        "loss": 0.0112
    },
    {
        "step": 2030,
        "loss": 0.0102
    },
    {
        "step": 2040,
        "loss": 0.01
    },
    {
        "step": 2050,
        "loss": 0.0084
    },
    {
        "step": 2060,
        "loss": 0.0114
    },
    {
        "step": 2070,
        "loss": 0.0126
    },
    {
        "step": 2080,
        "loss": 0.0107
    },
    {
        "step": 2090,
        "loss": 0.0112
    },
    {
        "step": 2100,
        "loss": 0.0102
    },
    {
        "step": 2110,
        "loss": 0.0109
    },
    {
        "step": 2120,
        "loss": 0.009
    },
    {
        "step": 2130,
        "loss": 0.0108
    },
    {
        "step": 2140,
        "loss": 0.0106
    },
    {
        "step": 2150,
        "loss": 0.0107
    },
    {
        "step": 2160,
        "loss": 0.0129
    },
    {
        "step": 2170,
        "loss": 0.0117
    },
    {
        "step": 2180,
        "loss": 0.0123
    },
    {
        "step": 2190,
        "loss": 0.012
    },
    {
        "step": 2200,
        "loss": 0.0115
    },
    {
        "step": 2210,
        "loss": 0.0102
    },
    {
        "step": 2220,
        "loss": 0.0137
    },
    {
        "step": 2230,
        "loss": 0.0106
    },
    {
        "step": 2240,
        "loss": 0.0106
    },
    {
        "step": 2250,
        "loss": 0.0111
    },
    {
        "step": 2260,
        "loss": 0.0107
    },
    {
        "step": 2270,
        "loss": 0.0112
    },
    {
        "step": 2280,
        "loss": 0.0128
    },
    {
        "step": 2290,
        "loss": 0.0109
    },
    {
        "step": 2300,
        "loss": 0.0097
    },
    {
        "step": 2310,
        "loss": 0.0123
    },
    {
        "step": 2320,
        "loss": 0.0117
    },
    {
        "step": 2330,
        "loss": 0.009
    },
    {
        "step": 2340,
        "loss": 0.012
    },
    {
        "step": 2350,
        "loss": 0.0119
    },
    {
        "step": 2360,
        "loss": 0.0065
    },
    {
        "step": 2370,
        "loss": 0.0074
    },
    {
        "step": 2380,
        "loss": 0.0073
    },
    {
        "step": 2390,
        "loss": 0.0064
    },
    {
        "step": 2400,
        "loss": 0.0066
    },
    {
        "step": 2410,
        "loss": 0.0069
    },
    {
        "step": 2420,
        "loss": 0.0078
    },
    {
        "step": 2430,
        "loss": 0.0085
    },
    {
        "step": 2440,
        "loss": 0.007
    },
    {
        "step": 2450,
        "loss": 0.0092
    },
    {
        "step": 2460,
        "loss": 0.0064
    },
    {
        "step": 2470,
        "loss": 0.0053
    },
    {
        "step": 2480,
        "loss": 0.0066
    },
    {
        "step": 2490,
        "loss": 0.0069
    },
    {
        "step": 2500,
        "loss": 0.0081
    },
    {
        "step": 2510,
        "loss": 0.0065
    },
    {
        "step": 2520,
        "loss": 0.0072
    },
    {
        "step": 2530,
        "loss": 0.0059
    },
    {
        "step": 2540,
        "loss": 0.0077
    },
    {
        "step": 2550,
        "loss": 0.0061
    },
    {
        "step": 2560,
        "loss": 0.0068
    },
    {
        "step": 2570,
        "loss": 0.0065
    },
    {
        "step": 2580,
        "loss": 0.0075
    },
    {
        "step": 2590,
        "loss": 0.0081
    },
    {
        "step": 2600,
        "loss": 0.0073
    },
    {
        "step": 2610,
        "loss": 0.0068
    },
    {
        "step": 2620,
        "loss": 0.007
    },
    {
        "step": 2630,
        "loss": 0.0068
    },
    {
        "step": 2640,
        "loss": 0.0072
    },
    {
        "step": 2650,
        "loss": 0.0075
    },
    {
        "step": 2660,
        "loss": 0.0052
    },
    {
        "step": 2670,
        "loss": 0.0056
    },
    {
        "step": 2680,
        "loss": 0.0077
    },
    {
        "step": 2690,
        "loss": 0.0051
    },
    {
        "step": 2700,
        "loss": 0.0055
    },
    {
        "step": 2710,
        "loss": 0.0058
    },
    {
        "step": 2720,
        "loss": 0.0053
    },
    {
        "step": 2730,
        "loss": 0.0066
    },
    {
        "step": 2740,
        "loss": 0.0053
    },
    {
        "step": 2750,
        "loss": 0.0043
    },
    {
        "step": 2760,
        "loss": 0.0055
    },
    {
        "step": 2770,
        "loss": 0.005
    },
    {
        "step": 2780,
        "loss": 0.0052
    },
    {
        "step": 2790,
        "loss": 0.0048
    },
    {
        "step": 2800,
        "loss": 0.0048
    },
    {
        "step": 2810,
        "loss": 0.0071
    },
    {
        "step": 2820,
        "loss": 0.0045
    },
    {
        "step": 2830,
        "loss": 0.0055
    },
    {
        "step": 2840,
        "loss": 0.004
    },
    {
        "step": 2850,
        "loss": 0.006
    },
    {
        "step": 2860,
        "loss": 0.0046
    },
    {
        "step": 2870,
        "loss": 0.0049
    },
    {
        "step": 2880,
        "loss": 0.0049
    },
    {
        "step": 2890,
        "loss": 0.0046
    },
    {
        "step": 2900,
        "loss": 0.0056
    },
    {
        "step": 2910,
        "loss": 0.0049
    },
    {
        "step": 2920,
        "loss": 0.0052
    },
    {
        "step": 2930,
        "loss": 0.0057
    },
    {
        "step": 2940,
        "loss": 0.0043
    },
    {
        "step": 2950,
        "loss": 0.0052
    },
    {
        "step": 2960,
        "loss": 0.0047
    },
    {
        "step": 2970,
        "loss": 0.0046
    },
    {
        "step": 2980,
        "loss": 0.0038
    },
    {
        "step": 2990,
        "loss": 0.0042
    },
    {
        "step": 3000,
        "loss": 0.0045
    },
    {
        "step": 3010,
        "loss": 0.0052
    },
    {
        "step": 3020,
        "loss": 0.0042
    },
    {
        "step": 3030,
        "loss": 0.0042
    },
    {
        "step": 3040,
        "loss": 0.0037
    },
    {
        "step": 3050,
        "loss": 0.0042
    },
    {
        "step": 3060,
        "loss": 0.0033
    },
    {
        "step": 3070,
        "loss": 0.0038
    },
    {
        "step": 3080,
        "loss": 0.0039
    },
    {
        "step": 3090,
        "loss": 0.0038
    },
    {
        "step": 3100,
        "loss": 0.0043
    },
    {
        "step": 3110,
        "loss": 0.0047
    },
    {
        "step": 3120,
        "loss": 0.0038
    },
    {
        "step": 3130,
        "loss": 0.0037
    },
    {
        "step": 3140,
        "loss": 0.0035
    },
    {
        "step": 3150,
        "loss": 0.0034
    },
    {
        "step": 3160,
        "loss": 0.0034
    },
    {
        "step": 3170,
        "loss": 0.0035
    },
    {
        "step": 3180,
        "loss": 0.0041
    },
    {
        "step": 3190,
        "loss": 0.0033
    },
    {
        "step": 3200,
        "loss": 0.0037
    },
    {
        "step": 3210,
        "loss": 0.004
    },
    {
        "step": 3220,
        "loss": 0.0038
    },
    {
        "step": 3230,
        "loss": 0.0036
    },
    {
        "step": 3240,
        "loss": 0.0037
    },
    {
        "step": 3250,
        "loss": 0.004
    },
    {
        "step": 3260,
        "loss": 0.0045
    },
    {
        "step": 3270,
        "loss": 0.0037
    },
    {
        "step": 3280,
        "loss": 0.0042
    },
    {
        "step": 3290,
        "loss": 0.003
    },
    {
        "step": 3300,
        "loss": 0.0042
    },
    {
        "step": 3310,
        "loss": 0.0038
    },
    {
        "step": 3320,
        "loss": 0.0033
    },
    {
        "step": 3330,
        "loss": 0.0031
    },
    {
        "step": 3340,
        "loss": 0.0034
    },
    {
        "step": 3350,
        "loss": 0.0032
    }
];

// Colors for different metrics
const metricColors = {
  accuracy: '#42A5F5',
  precision: '#66BB6A',
  recall: '#FFA726',
  f1: '#EF5350',
  exact_match_rate: '#AB47BC'
};

// Function to format metric name for display
const formatMetricName = (metric) => {
  return metric
    .replace('_', ' ')
    .split(' ')
    .map(word => word.charAt(0).toUpperCase() + word.slice(1))
    .join(' ');
};

// Computed chart data
const chartData = computed(() => {
  // Get labels (steps from lossLogs)
  const labels = lossLogs.map(log => `Step ${log.step}`);

  // Create datasets for loss
  const lossDataset = {
    label: 'Loss',
    borderColor: '#EF5350',
    backgroundColor: '#EF5350',
    data: lossLogs.map(log => log.loss),
    yAxisID: 'loss',
  };

  // Create datasets for metrics (accuracy, precision, recall, etc.)
  const metricsToShow = ['accuracy', 'precision', 'recall', 'f1', 'exact_match_rate'];

  const metricDatasets = metricsToShow.map(metric => ({
    label: formatMetricName(metric),
    borderColor: metricColors[metric],
    backgroundColor: metricColors[metric],
    data: Array(lossLogs.length).fill(dataMetrics.metrics[metric] * 100), // Set the value to be constant across steps
    yAxisID: 'percentage'
  }));

  return {
    labels,
    datasets: [lossDataset, ...metricDatasets] // Combine both loss and metrics datasets
  };
});

// Chart options
const chartOptions = ref({
  responsive: true,
  plugins: {
    legend: {
      display: true,
      position: 'top',
    },
    tooltip: {
      callbacks: {
        label: function(context) {
          const value = context.raw.toFixed(2);
          const metric = context.dataset.label;
          return `${metric}: ${value}${metric === 'Loss' ? '' : '%'}`;
        }
      }
    }
  },
  scales: {
    percentage: {
      type: 'linear',
      display: true,
      position: 'left',
      min: 0,
      max: 100,
      ticks: {
        callback: function(value) {
          return value + '%';
        }
      }
    },
    loss: {
      type: 'linear',
      display: true,
      position: 'right',
      min: 0,
      grid: {
        drawOnChartArea: false
      }
    }
  }
});

onMounted(() => {
  // Component is mounted
});
</script>

<style scoped>
.dashboard {
  font-family: Arial, sans-serif;
  background-color: #f9f9f9;
  text-align: center;
  padding: 20px;
}

h1 {
  margin-bottom: 20px;
  color: #333;
}

.chart-container {
  max-width: 1200px;
  margin: 0 auto;
  background: #fff;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}
</style>
