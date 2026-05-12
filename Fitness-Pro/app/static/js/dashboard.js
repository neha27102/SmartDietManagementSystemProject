function makeChart(id, label, rows, color) {
  const ctx = document.getElementById(id);
  if (!ctx) return;
  new Chart(ctx, {
    type: "line",
    data: {
      labels: rows.map((row) => row.date),
      datasets: [{
        label,
        data: rows.map((row) => row.value),
        borderColor: color,
        backgroundColor: `${color}33`,
        borderWidth: 3,
        tension: 0.35,
        fill: true
      }]
    },
    options: {
      responsive: true,
      plugins: { legend: { display: false } },
      scales: { x: { grid: { display: false } }, y: { grid: { color: "rgba(148,163,184,.15)" } } }
    }
  });
}

fetch("/dashboard/api/summary")
  .then((res) => res.json())
  .then((data) => {
    makeChart("bmiChart", "BMI", data.bmi, "#2dd4bf");
    makeChart("weightChart", "Weight", data.weight, "#f97316");
    makeChart("calorieChart", "Calories", data.calories, "#60a5fa");
    const completion = document.getElementById("goalCompletion");
    if (completion) completion.textContent = `${data.goal_completion}%`;
  });
