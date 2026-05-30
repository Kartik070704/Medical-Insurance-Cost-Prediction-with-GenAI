const form = document.querySelector("#predictionForm");
const steps = [...document.querySelectorAll(".form-step")];
const stepButtons = [...document.querySelectorAll(".step")];
const nextButtons = document.querySelectorAll("[data-next]");
const backButtons = document.querySelectorAll("[data-back]");
const birthDateInput = document.querySelector("#birth_date");
const ageInput = document.querySelector("#age");
const errorBox = document.querySelector("#formError");
let currentStep = 0;
let predictionReady = false;

function showStep(index) {
  currentStep = Math.max(0, Math.min(index, steps.length - 1));
  steps.forEach((step, stepIndex) => {
    step.classList.toggle("active", stepIndex === currentStep);
  });
  stepButtons.forEach((button, buttonIndex) => {
    button.classList.toggle("active", buttonIndex === currentStep);
    button.classList.toggle("done", buttonIndex < currentStep);
  });
}

function fieldsForStep(index) {
  return [...steps[index].querySelectorAll("input, select")];
}

function validateStep(index) {
  const fields = fieldsForStep(index);
  const invalid = fields.find((field) => !field.checkValidity());
  if (invalid) {
    invalid.reportValidity();
    return false;
  }
  return true;
}

function calculateAge(value) {
  if (!value) return "";
  const born = new Date(`${value}T00:00:00`);
  const today = new Date();
  let age = today.getFullYear() - born.getFullYear();
  const monthDifference = today.getMonth() - born.getMonth();
  if (monthDifference < 0 || (monthDifference === 0 && today.getDate() < born.getDate())) {
    age -= 1;
  }
  return age > 0 ? age : "";
}

function formPayload() {
  return Object.fromEntries(new FormData(form).entries());
}

function setLoading(isLoading) {
  const submitButton = form.querySelector('button[type="submit"]');
  submitButton.disabled = isLoading;
  submitButton.textContent = isLoading ? "Predicting..." : "Predict";
}

function updateSummary(data) {
  document.querySelector("#predictionValue").textContent = data.formatted_prediction;
  document.querySelector("#reasoningText").textContent = data.reasoning || "--";
  document.querySelector("#reasoningModel").textContent = `AI reasoning: ${data.reasoning_model || "unknown"}`;
  document.querySelector("#summaryName").textContent = data.personal.full_name || "--";
  document.querySelector("#summarySmoker").textContent = data.inputs.smoker;
  document.querySelector("#summaryBmi").textContent = data.inputs.bmi;
  document.querySelector("#summaryAge").textContent = data.inputs.age;
  document.querySelector("#summaryStorage").textContent = data.storage?.saved
    ? `Neon #${data.storage.id}`
    : data.storage?.reason || "Not saved";
}

birthDateInput.addEventListener("change", () => {
  const age = calculateAge(birthDateInput.value);
  if (age) {
    ageInput.value = age;
  }
});

nextButtons.forEach((button) => {
  button.addEventListener("click", () => {
    if (validateStep(currentStep)) {
      showStep(currentStep + 1);
    }
  });
});

backButtons.forEach((button) => {
  button.addEventListener("click", () => showStep(currentStep - 1));
});

stepButtons.forEach((button) => {
  button.addEventListener("click", () => {
    const target = Number(button.dataset.jump);
    if (target === 2 && !predictionReady) return;
    if (target <= currentStep || validateStep(currentStep)) {
      showStep(target);
    }
  });
});

form.addEventListener("reset", () => {
  setTimeout(() => {
    errorBox.textContent = "";
    predictionReady = false;
    showStep(0);
  }, 0);
});

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  errorBox.textContent = "";
  if (!validateStep(currentStep)) return;

  if (window.location.protocol === "file:") {
    errorBox.textContent = "Run the Flask server and open http://127.0.0.1:5000 to make predictions.";
    return;
  }

  setLoading(true);
  try {
    const response = await fetch("/predict", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(formPayload()),
    });
    const data = await response.json();
    if (!data.ok) {
      throw new Error(data.error || "Prediction failed");
    }
    updateSummary(data);
    predictionReady = true;
    showStep(2);
  } catch (error) {
    errorBox.textContent = error.message;
  } finally {
    setLoading(false);
  }
});

document.querySelector("#startOver").addEventListener("click", () => {
  form.reset();
  errorBox.textContent = "";
  predictionReady = false;
  showStep(0);
});

showStep(0);

if (window.location.protocol === "file:") {
  errorBox.textContent = "This page is opened directly. Use http://127.0.0.1:5000 for the working app.";
}
