const userid = document.querySelector(".userid");
const userpw = document.querySelector(".userpw");
const login__btn = document.querySelector("#login__btn");

function activeBtn() {
  switch (!(userid.value && userpw.value)) {
    case true:
      login__btn.disabled = true;
      break;
    case false:
      login__btn.disabled = false;
      break;
  }
}
userid.addEventListener("keyup", activeBtn);
userpw.addEventListener("keyup", activeBtn);
