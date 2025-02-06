<template>
  <div class="dashboard">
    <h1>Đánh giá mô hình</h1>
    <div class="chart-container">
      <Chart type="line" :data="chartData" :options="chartOptions" />
    </div>
  </div>
</template>

<script setup>

const dataMetrics = {
  "metrics": {
        "accuracy": 0.8053830227743272,
        "precision": 1.0,
        "recall": 0.8053830227743272,
        "f1": 0.8922018348623854,
        "exact_match_rate": 0.8053830227743272
    },
}

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