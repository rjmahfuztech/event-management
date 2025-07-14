// For dashboard chart
Chart.register(ChartDataLabels);

// Events Per Month Chart
new Chart(document.getElementById("eventsPerMonthChart"), {
  type: "bar",
  data: {
    labels: months,
    datasets: [
      {
        label: "Events",
        data: eventsCount,
        backgroundColor: "rgba(59, 130, 246, 0.6)",
        borderColor: "rgba(59, 130, 246, 1)",
        borderWidth: 1,
      },
    ],
  },
  options: {
    responsive: true,
    maintainAspectRatio: false,
    scales: { y: { beginAtZero: true } },
  },
});

// generate unique color for each category
const generateColors = (count) => {
  const colors = [];
  for (let i = 0; i < count; i++) {
    const hue = ((i * 360) / count) % 360;
    colors.push(`hsl(${hue}, 70%, 70% )`);
  }
  return colors;
};

// Events By Category Chart
new Chart(document.getElementById("eventsByCategoryChart"), {
  type: "doughnut",
  data: {
    labels: categories,
    datasets: [
      {
        label: "Events",
        data: categoryCount,
        backgroundColor: generateColors(categories.length),
        borderColor: "#fff",
        borderWidth: 1,
      },
    ],
  },
  options: {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: "bottom",
      },
    },
  },
});
