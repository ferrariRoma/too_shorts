function logout() {
  $.removeCookie("mytoken");
  alert("로그아웃 되었습니다.");
  window.location.href = "/";
}
