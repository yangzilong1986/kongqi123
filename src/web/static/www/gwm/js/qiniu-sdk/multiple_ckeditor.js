$(function() {
    /**
     * 多文件上传工具
     */
    var Q2_ckeditor = new QiniuJsSDK();
    var uploader2_ckeditor = Q2_ckeditor.uploader({
        runtimes: 'html5,flash,html4',
        browse_button: 'pickfiles_ckeditor',
        container: 'container_ckeditor',
        drop_element: 'container_ckeditor',
        max_file_size: '5mb',
        flash_swf_url: 'js/plupload/Moxie.swf',
        dragdrop: true,
        chunk_size: '4mb',
        uptoken_url: $('#uptoken_url_ckeditor').val(),
        domain: $('#domain_ckeditor').val(),
        auto_start: true,
        unique_names:false,
        save_key:false,
        init: {
            'BeforeUpload': function(up, file) {
              // 每个文件上传前,处理相关的事情
                /*图片上传加载中*/
                var loadingImgFtp=[];
                loadingImgFtp.push('<div class="loading-wrap">');
                loadingImgFtp.push('    <div class="anim-loading">');
                loadingImgFtp.push('        <i></i>');
                loadingImgFtp.push('        <i></i>');
                loadingImgFtp.push('        <i></i>');
                loadingImgFtp.push('    </div>');
                loadingImgFtp.push('    <div class="loading-txt">别着急，正在努力上传中……</div>');
                loadingImgFtp.push('</div>');
                if($('#loadingImgFtp').length==0){
                    popnormal({
                        //"eventEle":".js_popnormal",//点击事件元素（不定义：立即弹出）
                        "popconTpl":loadingImgFtp.join(''),
                        "popId":"loadingImgFtp"
                    });
                }
            },
            'UploadComplete': function() {
                //队列文件处理完毕后,处理相关的事情
                $('#loadingImgFtp').remove();
            },
            'FileUploaded': function(up, file, info) {
                // 每个文件上传成功后,处理相关的事情
                var domain = up.getOption('domain');
                var res = jQuery.parseJSON(info);
                // var sourceLink = domain + res.key; 获取上传成功后的文件的Url
                //AJAX 获取图片的URL
                var sourceLink = '';
                var thumbLink = '';
                var liElement = '';
                $.ajax({
                    type: "GET",
                    url: '/upload/getUrl?key=' + res['key']+'&size='+$("#multiple_size_ckeditor").val(),
                    dataType:"json",
                    async:false,
                    success:function(result){
                        sourceLink = result['url'];
                        thumbLink = result['thumb_url'];
                        var cellimgH=$('.cell .btn-ftp1').outerHeight();
                        liElement = '<img src="'+sourceLink+'" key="'+res['key']+'">';

                    }
                });
                $("#result_ckeditor").append(liElement);
                $(document.getElementById('gwm_ckeditor_iframe').contentWindow.document.body).append(liElement);
                //刷新keys input框的内容
                refreshKeys_ckeditor();
            },
            'Error': function(up, err, errTip) {
                if (err.status == 413) {
                    poperror({
                        "popconMsg":"文件超过1M",
                        "popId":"poperror"
                    });
                } else if (err.status==403) {
                    poperror({
                        "popconMsg":"图片文件格式错误",
                        "popId":"poperror"
                    });
                }
            },
            'Key': function(up, file) {
                // 若想在前端对每个文件的key进行个性化处理，可以配置该函数
                // 该配置必须要在 unique_names: false , save_key: false 时才生效
                var key = "";
                // do something with key here
                //ajax 生成key
                $.ajax({
                    type: "GET",
                    url: $('#get_key_url_ckeditor').val(),
                    dataType:"json",
                    async:false,
                    success:function(result){
                        key = result['key'];
                        return key;
                    }
                });
                return key
            }
        }
    });

});

/**
 * 刷新keys隐藏节点的值
 */
var refreshKeys_ckeditor = function() {
    var keys = [];
    $("#result_ckeditor img").each(function(){
        var key = $(this).attr('key');
        if (key!='') {
            keys.push(key)
        }
    });
    $(".multiple_field_name_ckeditor").val(keys.join(','));

};

