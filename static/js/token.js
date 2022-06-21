// login handler
function login() {
  $.ajax({
    type: "POST",
    url: "/api/login",
    data: { id_give: $(".userid").val(), pw_give: $(".userpw").val() },
    success: function (response) {
      if (response["result"] == "success") {
        $.cookie("mytoken", response["token"]);
        alert("로그인 완료!");
        window.location.href = "/";
      } else {
        alert(response["msg"]);
      }
    },
  });
}

// sign up handler
function register() {
  $.ajax({
    type: "POST",
    url: "/api/register",
    data: {
      id_give: $(".userid").val(),
      pw_give: $(".userpw").val(),
      checked_pw_give: $(".usercheckedpw").val(),
      nickname_give: $(".usernick").val(),
    },
    success: function (response) {
      if (response["result"] == "success") {
        alert("회원가입이 완료되었습니다.");
        window.location.href = "/login";
      } else {
        alert(response["msg"]);
      }
    },
  });
}
