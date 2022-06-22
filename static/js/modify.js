// 수정기능
function modify_posting(posting_number) {
    let new_URL = $('#floatingUrl').val();
    let new_desc =$('#floatingDescription').val();
    $.ajax({
        type: "POST",
        url: "/api/modify",
        data: {
            "posting_number":posting_number,
            "URL": new_URL,
            "desc": new_desc
        },
        success: function (response) {
            location.href = "/";
        }
    })
}


