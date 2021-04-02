        $("#comment_form").submit(function(){
            // 判断是否为空
            $("#comment_error").text('');
            if(CKEDITOR.instances["id_text"].document.getBody().getText().trim()==''){
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
                success: function(data){
                    console.log(data);
                    if(data['status']=="SUCCESS"){
                        if($('#reply_comment_id').val()=='0'){
                            // 插入评论
                            var comment_html = '<div id="root_' + data['pk'] + '" class="comment"><span>' + data['username'] + '</span><span> (' + data['comment_time'] + ')：</span><div id="comment_' + data['pk'] + '">' + data['text'] + '</div><a href="javascript:reply(' + data['pk'] + ');">回复</a></div>';
                            $("#comment_list").prepend(comment_html);
                        }else{
                            // 插入回复
                            var reply_html ='<div class="reply"><span>' + data['username'] + '</span><span> (' + data['comment_time'] + ')</span><span> 回复 </span><span>' + data['reply_to'] + '：</span><div id="comment_' + data['pk'] + '">' + data['text'] + '</div><a href="javascript:reply(' + data['pk'] + ');">回复</a></div>';
                            $("#root_" + data['root_pk']).append(reply_html);
                        }

                        // 清空编辑框的内容
                        CKEDITOR.instances['id_text'].setData('');
                        $('#reply_content_container').hide();
                        $('#reply_comment_id').val('0');
                        $('#no_comment').remove();
                    }else{
                        // 显示错误信息
                        $("#comment_error").text(data['message']);
                    }
                },
                error: function(xhr){
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


function reply(reply_comment_id) {
    $("#reply_comment_id").val(reply_comment_id);
    var html = $('#comment_' + reply_comment_id).html()
    $('#reply_content').html(html);
    $('#reply_content_container').show()

    $("html").animate({scrollTop: $("#comment_form").offset().top - 60}, 300, function () {
        CKEDITOR.instances['id_text'].focus()
    })
}