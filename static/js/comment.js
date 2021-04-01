$("#comment_form").submit(function () {
    // 判断是否为空
    $("#comment_error").text('');
    if (CKEDITOR.instances["id_text"].document.getBody().getText().trim() == '') {
        $("#comment_error").text('评论内容不能为空');
        return false;
    }

    // 更新数据到textarea
    CKEDITOR.instances['id_text'].updateElement();

    // 异步提交
    $.ajax({
        url: "/comment/update_comment",
        type: 'POST',
        data: $(this).serialize(),
        cache: false,
        success: function (data) {
            console.log(data);
            if (data['status'] == "SUCCESS") {
                // 插入数据
                var comment_html = '<div>' + data['username'] +
                    ' (' + data['comment_time'] + ')：' +
                    data['text'] + '</div>';
                $("#comment_list").prepend(comment_html);
                // 清空编辑框的内容
                CKEDITOR.instances['id_text'].setData('');
            } else {
                // 显示错误信息
                $("#comment_error").text(data['message']);
            }
        },
        error: function (xhr) {
            console.log(xhr);
        }
    });
    return false;
});

function likeChange(obj, content_type, object_id) {
    console.log(content_type);
    console.log(object_id);
    var is_like = obj.getElementsByClassName('active').length == 0
    $.ajax({
        url: "/like/like_change",
        type: 'GET',
        data: {
            content_type: content_type,
            object_id: object_id,
            is_like: is_like
        },
        cache: false,
        success: function (data) {
            console.log(data);
        },
        error: function (xhr) {
        }
    })
}