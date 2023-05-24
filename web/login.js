










async function login(name, password) {
    return await eel.login(name, password)();
  }


async function isadmin(username,password){
  return await eel.isadmin(username,password)();
}

  let customerId;
  let form = document.querySelector("form");
  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    let formdata = new FormData(form);
    let username = formdata.get("username");
    let password = formdata.get("password");
    let isAdmin = await isadmin(username,password)
    if(isAdmin){
      window.location.href = "Admin.html";
      return
    }
    let error = document.querySelector(".error");
    let isSuccess = await login(username, password);
    if (isSuccess) {
      window.location.href = "MainPage.html";
      customerId = await eel.getCustomerId(username)()
      localStorage.setItem('customerId',customerId)
    } else {
      error.style.opacity = 1;
      form.querySelector('input[name="username"]').value = "";
      form.querySelector('input[name="password"]').value = "";
    }
  });

