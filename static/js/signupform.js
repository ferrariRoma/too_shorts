const userid = document.querySelector(".userid");
const userpw = document.querySelector(".userpw");
const usercheckedpw = document.querySelector(".usercheckedpw");
const usernick = document.querySelector(".usernick");
const signup__btn = document.querySelector("#signup__btn");

function activeBtn() {
  switch (
    !(userid.value && userpw.value && usercheckedpw.value && usernick.value)
  ) {
    case true:
      signup__btn.disabled = true;
      break;
    case false:
      signup__btn.disabled = false;
      break;
  }
}
userid.addEventListener("keyup", activeBtn);
userpw.addEventListener("keyup", activeBtn);
usercheckedpw.addEventListener("keyup", activeBtn);
usernick.addEventListener("keyup", activeBtn);
