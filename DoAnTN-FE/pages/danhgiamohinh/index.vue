<template>
  <div class="dashboard">
    <h1>Đánh giá mô hình</h1>
    <div class="chart-container">
      <Chart type="line" :data="chartData" :options="chartOptions" />
    </div>
  </div>
</template>

<script setup>

const dataMetrics = [
    {
        "run_index": 0,
        "parameters": {
            "learning_rate": 2e-05,
            "num_train_epochs": 3,
            "per_device_train_batch_size": 4,
            "weight_decay": 0.01,
            "gradient_accumulation_steps": 2
        },
        "metrics": {
            "eval_loss": 0.43777841329574585,
            "eval_start_accuracy": 0.9257375381485249,
            "eval_end_accuracy": 0.8860630722278738,
            "eval_precision": 0.7980157842500407,
            "eval_recall": 0.811889196260301,
            "eval_f1": 0.7943056523632034,
            "eval_runtime": 5.4978,
            "eval_samples_per_second": 178.8,
            "eval_steps_per_second": 44.745,
            "epoch": 2.986449864498645
        },
        "model_path": "./phobert-qa-search/run_0_20250110_082602"
    },
    {
        "run_index": 1,
        "parameters": {
            "learning_rate": 2e-05,
            "num_train_epochs": 3,
            "per_device_train_batch_size": 4,
            "weight_decay": 0.02,
            "gradient_accumulation_steps": 2
        },
        "metrics": {
            "eval_loss": 0.3858720064163208,
            "eval_start_accuracy": 0.9267548321464903,
            "eval_end_accuracy": 0.8972533062054934,
            "eval_precision": 0.8273661131578552,
            "eval_recall": 0.8336147473155668,
            "eval_f1": 0.8216677666554844,
            "eval_runtime": 5.5765,
            "eval_samples_per_second": 176.275,
            "eval_steps_per_second": 44.113,
            "epoch": 2.986449864498645
        },
        "model_path": "./phobert-qa-search/run_1_20250110_082921"
    },
    {
        "run_index": 2,
        "parameters": {
            "learning_rate": 2e-05,
            "num_train_epochs": 3,
            "per_device_train_batch_size": 8,
            "weight_decay": 0.01,
            "gradient_accumulation_steps": 2
        },
        "metrics": {
            "eval_loss": 0.745593249797821,
            "eval_start_accuracy": 0.8708036622583927,
            "eval_end_accuracy": 0.7731434384537131,
            "eval_precision": 0.7354886026130711,
            "eval_recall": 0.7628505425721311,
            "eval_f1": 0.7304942111332965,
            "eval_runtime": 4.6274,
            "eval_samples_per_second": 212.429,
            "eval_steps_per_second": 26.581,
            "epoch": 2.972972972972973
        },
        "model_path": "./phobert-qa-search/run_2_20250110_083217"
    },
    {
        "run_index": 3,
        "parameters": {
            "learning_rate": 2e-05,
            "num_train_epochs": 3,
            "per_device_train_batch_size": 8,
            "weight_decay": 0.02,
            "gradient_accumulation_steps": 2
        },
        "metrics": {
            "eval_loss": 0.7618352770805359,
            "eval_start_accuracy": 0.861648016276704,
            "eval_end_accuracy": 0.7619532044760936,
            "eval_precision": 0.704888669291571,
            "eval_recall": 0.7293392213278899,
            "eval_f1": 0.698259344778434,
            "eval_runtime": 4.4378,
            "eval_samples_per_second": 221.505,
            "eval_steps_per_second": 27.716,
            "epoch": 2.972972972972973
        },
        "model_path": "./phobert-qa-search/run_3_20250110_083637"
    },
    {
        "run_index": 4,
        "parameters": {
            "learning_rate": 2e-05,
            "num_train_epochs": 4,
            "per_device_train_batch_size": 4,
            "weight_decay": 0.01,
            "gradient_accumulation_steps": 2
        },
        "metrics": {
            "eval_loss": 0.2804967761039734,
            "eval_start_accuracy": 0.9542217700915565,
            "eval_end_accuracy": 0.9379450661241099,
            "eval_precision": 0.8885103196348951,
            "eval_recall": 0.9060642999008253,
            "eval_f1": 0.8922582412556681,
            "eval_runtime": 6.2616,
            "eval_samples_per_second": 156.988,
            "eval_steps_per_second": 39.287,
            "epoch": 3.9810298102981028
        },
        "model_path": "./phobert-qa-search/run_4_20250110_084104"
    },
    {
        "run_index": 5,
        "parameters": {
            "learning_rate": 2e-05,
            "num_train_epochs": 4,
            "per_device_train_batch_size": 4,
            "weight_decay": 0.02,
            "gradient_accumulation_steps": 2
        },
        "metrics": {
            "eval_loss": 0.27332890033721924,
            "eval_start_accuracy": 0.9582909460834181,
            "eval_end_accuracy": 0.9572736520854527,
            "eval_precision": 0.8968115935593113,
            "eval_recall": 0.9052628379604656,
            "eval_f1": 0.8963403230230105,
            "eval_runtime": 5.0854,
            "eval_samples_per_second": 193.299,
            "eval_steps_per_second": 48.374,
            "epoch": 3.9810298102981028
        },
        "model_path": "./phobert-qa-search/run_5_20250110_084755"
    },
    {
        "run_index": 6,
        "parameters": {
            "learning_rate": 2e-05,
            "num_train_epochs": 4,
            "per_device_train_batch_size": 8,
            "weight_decay": 0.01,
            "gradient_accumulation_steps": 2
        },
        "metrics": {
            "eval_loss": 0.4665208160877228,
            "eval_start_accuracy": 0.9186164801627671,
            "eval_end_accuracy": 0.8880976602238047,
            "eval_precision": 0.8514812867968813,
            "eval_recall": 0.8643598054512126,
            "eval_f1": 0.848670481897467,
            "eval_runtime": 4.5092,
            "eval_samples_per_second": 217.998,
            "eval_steps_per_second": 27.277,
            "epoch": 3.962162162162162
        },
        "model_path": "./phobert-qa-search/run_6_20250110_085358"
    },
    {
        "run_index": 7,
        "parameters": {
            "learning_rate": 2e-05,
            "num_train_epochs": 4,
            "per_device_train_batch_size": 8,
            "weight_decay": 0.02,
            "gradient_accumulation_steps": 2
        },
        "metrics": {
            "eval_loss": 0.47441136837005615,
            "eval_start_accuracy": 0.9155645981688708,
            "eval_end_accuracy": 0.8819938962360122,
            "eval_precision": 0.8386563917055195,
            "eval_recall": 0.8395221233738142,
            "eval_f1": 0.8294772943739819,
            "eval_runtime": 4.5058,
            "eval_samples_per_second": 218.164,
            "eval_steps_per_second": 27.298,
            "epoch": 3.962162162162162
        },
        "model_path": "./phobert-qa-search/run_7_20250110_085920"
    },
    {
        "run_index": 8,
        "parameters": {
            "learning_rate": 3e-05,
            "num_train_epochs": 3,
            "per_device_train_batch_size": 4,
            "weight_decay": 0.01,
            "gradient_accumulation_steps": 2
        },
        "metrics": {
            "eval_loss": 0.2557419240474701,
            "eval_start_accuracy": 0.9511698880976602,
            "eval_end_accuracy": 0.9501525940996948,
            "eval_precision": 0.8926121941221911,
            "eval_recall": 0.902960858254242,
            "eval_f1": 0.8855924262263422,
            "eval_runtime": 5.5383,
            "eval_samples_per_second": 177.492,
            "eval_steps_per_second": 44.418,
            "epoch": 2.986449864498645
        },
        "model_path": "./phobert-qa-search/run_8_20250110_090615"
    },
    {
        "run_index": 9,
        "parameters": {
            "learning_rate": 3e-05,
            "num_train_epochs": 3,
            "per_device_train_batch_size": 4,
            "weight_decay": 0.02,
            "gradient_accumulation_steps": 2
        },
        "metrics": {
            "eval_loss": 0.29058638215065,
            "eval_start_accuracy": 0.9542217700915565,
            "eval_end_accuracy": 0.9257375381485249,
            "eval_precision": 0.8893757898996913,
            "eval_recall": 0.8896530813756129,
            "eval_f1": 0.8843439193519408,
            "eval_runtime": 5.3798,
            "eval_samples_per_second": 182.72,
            "eval_steps_per_second": 45.727,
            "epoch": 2.986449864498645
        },
        "model_path": "./phobert-qa-search/run_9_20250110_090904"
    },
    {
        "run_index": 10,
        "parameters": {
            "learning_rate": 3e-05,
            "num_train_epochs": 3,
            "per_device_train_batch_size": 8,
            "weight_decay": 0.01,
            "gradient_accumulation_steps": 2
        },
        "metrics": {
            "eval_loss": 0.48867931962013245,
            "eval_start_accuracy": 0.9175991861648016,
            "eval_end_accuracy": 0.8769074262461851,
            "eval_precision": 0.8261851730386884,
            "eval_recall": 0.8403702477562452,
            "eval_f1": 0.823193086069902,
            "eval_runtime": 4.2702,
            "eval_samples_per_second": 230.199,
            "eval_steps_per_second": 28.804,
            "epoch": 2.972972972972973
        },
        "model_path": "./phobert-qa-search/run_10_20250110_091133"
    },
    {
        "run_index": 11,
        "parameters": {
            "learning_rate": 3e-05,
            "num_train_epochs": 3,
            "per_device_train_batch_size": 8,
            "weight_decay": 0.02,
            "gradient_accumulation_steps": 2
        },
        "metrics": {
            "eval_loss": 0.47919905185699463,
            "eval_start_accuracy": 0.9165818921668362,
            "eval_end_accuracy": 0.8748728382502543,
            "eval_precision": 0.8222033203331267,
            "eval_recall": 0.8377600754004801,
            "eval_f1": 0.8195473117907127,
            "eval_runtime": 4.4667,
            "eval_samples_per_second": 220.073,
            "eval_steps_per_second": 27.537,
            "epoch": 2.972972972972973
        },
        "model_path": "./phobert-qa-search/run_11_20250110_091344"
    },
    {
        "run_index": 12,
        "parameters": {
            "learning_rate": 3e-05,
            "num_train_epochs": 4,
            "per_device_train_batch_size": 4,
            "weight_decay": 0.01,
            "gradient_accumulation_steps": 2
        },
        "metrics": {
            "eval_loss": 0.17788897454738617,
            "eval_start_accuracy": 0.9745676500508647,
            "eval_end_accuracy": 0.9613428280773143,
            "eval_precision": 0.9317962462357041,
            "eval_recall": 0.9377153577144528,
            "eval_f1": 0.9309757011631494,
            "eval_runtime": 4.9079,
            "eval_samples_per_second": 200.289,
            "eval_steps_per_second": 50.123,
            "epoch": 3.9810298102981028
        },
        "model_path": "./phobert-qa-search/run_12_20250110_091559"
    },
    {
        "run_index": 13,
        "parameters": {
            "learning_rate": 3e-05,
            "num_train_epochs": 4,
            "per_device_train_batch_size": 4,
            "weight_decay": 0.02,
            "gradient_accumulation_steps": 2
        },
        "metrics": {
            "eval_loss": 0.18079493939876556,
            "eval_start_accuracy": 0.9745676500508647,
            "eval_end_accuracy": 0.9725330620549338,
            "eval_precision": 0.9323604089509293,
            "eval_recall": 0.938770904064729,
            "eval_f1": 0.9315024611672611,
            "eval_runtime": 5.3877,
            "eval_samples_per_second": 182.453,
            "eval_steps_per_second": 45.66,
            "epoch": 3.9810298102981028
        },
        "model_path": "./phobert-qa-search/run_13_20250110_091940"
    },
    {
        "run_index": 14,
        "parameters": {
            "learning_rate": 3e-05,
            "num_train_epochs": 4,
            "per_device_train_batch_size": 8,
            "weight_decay": 0.01,
            "gradient_accumulation_steps": 2
        },
        "metrics": {
            "eval_loss": 0.320600301027298,
            "eval_start_accuracy": 0.9501525940996948,
            "eval_end_accuracy": 0.940996948118006,
            "eval_precision": 0.8915123134456373,
            "eval_recall": 0.8947206056669468,
            "eval_f1": 0.8873074922373478,
            "eval_runtime": 4.4721,
            "eval_samples_per_second": 219.806,
            "eval_steps_per_second": 27.504,
            "epoch": 3.962162162162162
        },
        "model_path": "./phobert-qa-search/run_14_20250110_092525"
    },
    {
        "run_index": 15,
        "parameters": {
            "learning_rate": 3e-05,
            "num_train_epochs": 4,
            "per_device_train_batch_size": 8,
            "weight_decay": 0.02,
            "gradient_accumulation_steps": 2
        },
        "metrics": {
            "eval_loss": 0.3634004592895508,
            "eval_start_accuracy": 0.9399796541200407,
            "eval_end_accuracy": 0.9175991861648016,
            "eval_precision": 0.8655618701585502,
            "eval_recall": 0.8725182710617118,
            "eval_f1": 0.8632819428477646,
            "eval_runtime": 5.4119,
            "eval_samples_per_second": 181.635,
            "eval_steps_per_second": 22.727,
            "epoch": 3.962162162162162
        },
        "model_path": "./phobert-qa-search/run_15_20250110_092820"
    }
]

// Colors for different metrics
const metricColors = {
  eval_loss: '#42A5F5',
  eval_start_accuracy: '#66BB6A',
  eval_end_accuracy: '#FFA726',
  eval_precision: '#EF5350',
  eval_recall: '#AB47BC',
  eval_f1: '#26C6DA'
}

// Function to format metric name for display
const formatMetricName = (metric) => {
  return metric
    .replace('eval_', '')
    .split('_')
    .map(word => word.charAt(0).toUpperCase() + word.slice(1))
    .join(' ')
}

// Computed chart data
const chartData = computed(() => {
  // Get labels (run indexes)
  const labels = dataMetrics.map(run => `Run ${run.run_index}`)
  
  // Get metrics we want to display
  const metricsToShow = ['eval_loss', 'eval_start_accuracy', 'eval_end_accuracy', 
                        'eval_precision', 'eval_recall', 'eval_f1']
  
  // Create datasets
  const datasets = metricsToShow.map(metric => ({
    label: formatMetricName(metric),
    borderColor: metricColors[metric],
    backgroundColor: metricColors[metric],
    data: dataMetrics.map(run => {
      const value = run.metrics[metric]
      // Convert to percentage except for loss
      return metric === 'eval_loss' ? value : value * 100
    }),
    yAxisID: metric === 'eval_loss' ? 'loss' : 'percentage'
  }))

  return {
    labels,
    datasets
  }
})

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
          const runIndex = context.dataIndex;
          const run = dataMetrics[runIndex];
          const value = context.raw.toFixed(2);
          const metric = context.dataset.label;
          
          let tooltipLines = [
            `${metric}: ${value}${metric === 'Loss' ? '' : '%'}`,
            '',
            'Parameters:',
            `Learning Rate: ${run.parameters.learning_rate}`,
            `Epochs: ${run.parameters.num_train_epochs}`,
            `Batch Size: ${run.parameters.per_device_train_batch_size}`,
            `Weight Decay: ${run.parameters.weight_decay}`,
            `Gradient Steps: ${run.parameters.gradient_accumulation_steps}`
          ];
          
          return tooltipLines;
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