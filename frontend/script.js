const API_BASE = "http://127.0.0.1:8000";

const fileInput = document.getElementById("fileInput");
const uploadBtn = document.getElementById("uploadBtn");
const uploadStatus = document.getElementById("uploadStatus");

const questionInput = document.getElementById("questionInput");
const askBtn = document.getElementById("askBtn");
const answerBox = document.getElementById("answerBox");


uploadBtn.addEventListener("click", uploadFile);
askBtn.addEventListener("click", askQuestion);

questionInput.addEventListener("keydown", function (event) {
  if (event.key === "Enter") {
    askQuestion();
  }
});


async function uploadFile() {
  if (!fileInput.files.length) {
    uploadStatus.textContent = "الرجاء اختيار ملف أولًا.";
    return;
  }

  const file = fileInput.files[0];
  const formData = new FormData();
  formData.append("file", file);

  uploadStatus.textContent = "جاري رفع الملف ومعالجته...";
  answerBox.textContent = "الإجابة ستظهر هنا...";

  try {
    const response = await fetch(`${API_BASE}/upload`, {
      method: "POST",
      body: formData
    });

    const data = await response.json();

    if (!response.ok) {
      uploadStatus.textContent = data.detail || "حدث خطأ أثناء رفع الملف.";
      return;
    }

    uploadStatus.textContent = `تم رفع الملف بنجاح: ${data.filename} | عدد الأجزاء: ${data.chunks}`;
  } catch (error) {
    uploadStatus.textContent = "تعذر الاتصال بالخادم.";
    console.error(error);
  }
}


async function askQuestion() {
  const question = questionInput.value.trim();

  if (!question) {
    answerBox.textContent = "الرجاء كتابة سؤال أولًا.";
    return;
  }

  answerBox.textContent = "جاري البحث عن الإجابة...";

  try {
    const response = await fetch(`${API_BASE}/ask?q=${encodeURIComponent(question)}`);
    const data = await response.json();

    if (!response.ok) {
      answerBox.textContent = data.detail || "حدث خطأ أثناء جلب الإجابة.";
      return;
    }

    answerBox.textContent = data.answer;
  } catch (error) {
    answerBox.textContent = "تعذر الاتصال بالخادم.";
    console.error(error);
  }
}