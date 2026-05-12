function mealTemplate(meal) {
  const icons = { breakfast: "sunrise", lunch: "sun", dinner: "moon", snack: "apple" };
  const proteinWidth = Math.min(meal.protein * 2, 100);
  const carbWidth = Math.min(meal.carbs, 100);
  const fatWidth = Math.min(meal.fats * 3, 100);
  return `
    <div class="meal-top">
      <div class="meal-icon"><i data-lucide="${icons[meal.meal_type] || "utensils"}"></i></div>
      <div><span>${meal.meal_type[0].toUpperCase() + meal.meal_type.slice(1)}</span><h3>${meal.food.name}</h3></div>
    </div>
    <p>${meal.food.cuisine} &middot; ${meal.food.ingredients.join(", ")}</p>
    <div class="macro-row"><b>${meal.calories} kcal</b><b>${meal.protein}g P</b><b>${meal.carbs}g C</b><b>${meal.fats}g F</b></div>
    <div class="macro-bars">
      <div><span>Protein</span><em style="--value: ${proteinWidth}%"></em></div>
      <div><span>Carbs</span><em style="--value: ${carbWidth}%"></em></div>
      <div><span>Fats</span><em style="--value: ${fatWidth}%"></em></div>
    </div>
    <div class="card-actions"><button class="icon-btn replace-meal" aria-label="Replace meal"><i data-lucide="refresh-cw"></i></button></div>
  `;
}

document.addEventListener("click", async (event) => {
  const button = event.target.closest(".replace-meal");
  if (!button) return;
  const card = button.closest(".meal-card");
  const response = await fetch(`/diet/api/meals/${card.dataset.mealId}/replace`, { method: "POST" });
  const meal = await response.json();
  card.innerHTML = mealTemplate(meal);
  if (window.lucide) lucide.createIcons();
});

document.getElementById("regeneratePlan")?.addEventListener("click", async () => {
  const response = await fetch("/diet/api/regenerate", { method: "POST" });
  const plan = await response.json();
  const grid = document.getElementById("mealGrid");
  grid.innerHTML = plan.meals.map((meal) => `<article class="meal-card" data-meal-id="${meal.id}">${mealTemplate(meal)}</article>`).join("");
  if (window.lucide) lucide.createIcons();
});
