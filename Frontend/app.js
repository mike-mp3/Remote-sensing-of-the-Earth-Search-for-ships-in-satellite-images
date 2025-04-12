// Страница регистрации
if (document.getElementById("signupForm")) {
    document.getElementById("signupForm").addEventListener("submit", function(e) {
      e.preventDefault();
      const email = document.getElementById("email").value;
      const password = document.getElementById("password").value;
  
      // Сохраняем email для подтверждения
      localStorage.setItem("userEmail", email);
      
      // В реальном приложении здесь отправка кода на email
      alert(`Код подтверждения отправлен на ${email} (в реальном приложении)`);
      
      // Переход на страницу подтверждения
      window.location.href = "verify.html";
    });
  }
  
  // Страница подтверждения
  if (document.getElementById("verifyForm")) {
    // Показываем email пользователя
    document.getElementById("userEmail").textContent = localStorage.getItem("userEmail");
  
    document.getElementById("verifyForm").addEventListener("submit", function(e) {
      e.preventDefault();
      const code = document.getElementById("code").value;
  
      // Проверка кода (в реальном приложении — запрос к серверу)
      if (code === "123456") { // Пример кода
        alert("Email подтверждён! Регистрация завершена.");
        window.location.href = "/"; // Перенаправление на главную
      } else {
        alert("Неверный код. Попробуйте снова.");
      }
    });
  }

  // Функция для "отправки" данных на сервер (эмуляция)
async function checkEmailExists(email) {
    // В реальном проекте здесь будет fetch-запрос к API
    console.log("Проверяем email на сервере...");
    
    // Имитация ответа сервера
    const fakeUsers = [
      { email: "test@example.com" },
      { email: "user@gmail.com" }
    ];
    
    const userExists = fakeUsers.some(user => user.email === email);
    
    return new Promise((resolve) => {
      setTimeout(() => {
        resolve({
          status: userExists ? 400 : 200, // 400 = email занят, 200 = свободен
          message: userExists ? "Email уже используется" : "Email свободен"
        });
      }, 1000); // Имитация задержки сети
    });
  }
  
  // Страница регистрации
  if (document.getElementById("signupForm")) {
    document.getElementById("signupForm").addEventListener("submit", async function(e) {
      e.preventDefault();
      const email = document.getElementById("email").value;
      const password = document.getElementById("password").value;
  
      // Проверяем email
      const response = await checkEmailExists(email);
      
      if (response.status === 400) {
        alert("Ошибка: " + response.message);
        return;
      }
  
      // Если email свободен — сохраняем и переходим дальше
      localStorage.setItem("userEmail", email);
      alert("Код подтверждения отправлен на " + email);
      window.location.href = "verify.html";
    });
  }
  
  // Страница подтверждения (без изменений)
  if (document.getElementById("verifyForm")) {
    document.getElementById("userEmail").textContent = localStorage.getItem("userEmail");
    
    document.getElementById("verifyForm").addEventListener("submit", function(e) {
      e.preventDefault();
      const code = document.getElementById("code").value;
      
      if (code === "123456") {
        alert("Регистрация завершена!");
        window.location.href = "/";
      } else {
        alert("Неверный код. Попробуйте снова.");
      }
    });
  }