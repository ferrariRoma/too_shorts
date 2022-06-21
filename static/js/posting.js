let is_okay = false;

    $(document).ready(function () {
        console.log("ready!");
    });

    function is_shorts() {
        let shorts_url = $("#floatingUrl").val();
        if(shorts_url.includes("shorts")) {
            alert("shorts 영상이 맞습니다!");
            $("#image-box").empty();
            let video_url = shorts_url.split("/")[4];
            let temp_html = `<img src="http://img.youtube.com/vi/${video_url}/mqdefault.jpg"></img>`
            $("#image-box").append(temp_html);
            is_okay = true;
        }
        else if(shorts_url === "") {
            alert("shorts의 URL을 입력해주세요!!");
        }
        else {
            alert("shorts 영상이 아닙니다.")
            $("#floatingUrl").val("");
            is_okay = false;
        }
    }

    function submit_cancel() {
        location.href = "/"
    }
    function submit_complete() {
        let shorts_url = $("#floatingUrl").val();
        let description = $("#floatingDescription").val();
        let username="nggoong"
        if(is_okay){
            /* ajax요청으로 url과 description보내기 */
             $.ajax({
                    type: "POST",
                    url: "/api/posting",
                    data: {
                        'username': username,
                        "URL": shorts_url,
                        "description":description
                    },
                    success: function (response) {
                        let message = response['msg'];
                        alert(message);
                    }
                })
            location.href = "/";
        }
        else if(!is_okay) alert("shorts 영상 확인해주세요!");
        else if($("#floatingDescription").val()==="") alert("description을 작성해주세요!");

    }