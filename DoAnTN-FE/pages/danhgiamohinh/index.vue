<template>
    <div class="dashboard">
      <h1>Model Evaluation Dashboard</h1>
      <div class="chart-container">
        <Chart type="bar" :data="chartData" :options="chartOptions" />
      </div>
    </div>
  </template>
  
  <script setup>
  
  // Reactive data for the chart
  const chartData = ref({
    labels: ['Accuracy', 'Precision', 'Recall', 'F1 Score'],
    datasets: [
      {
        label: 'Metrics',
        backgroundColor: ['#42A5F5', '#66BB6A', '#FFA726', '#EF5350'],
        data: [], // Data will be fetched from the API
      },
    ],
  });
  
  const chartOptions = ref({
    responsive: true,
    plugins: {
      legend: {
        display: true,
        position: 'top',
      },
    },
  });
  
  // Fetch metrics from API
  const fetchMetrics = async () => {
    try {
      const response = await fetch('http://127.0.0.1:5000/model-metrics');
      const result = await response.json();
  
      if (result.status === 'success') {
        const { accuracy, precision, recall, f1_score } = result.metrics;
        chartData.value.datasets[0].data = [
          accuracy * 100,
          precision * 100,
          recall * 100,
          f1_score * 100,
        ];
      } else {
        console.error('Error fetching metrics:', result.error);
      }
    } catch (error) {
      console.error('Error fetching metrics:', error);
    }
  };
  
  onMounted(() => {
    fetchMetrics();
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
    max-width: 600px;
    margin: 0 auto;
    background: #fff;
    padding: 20px;
    border-radius: 10px;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  }
  </style>
  