$(function() {
    /**
     * 多文件上传工具
     */
    var Q2 = new QiniuJsSDK();
    var uploader2 = Q2.uploader({
        runtimes: 'html5,flash,html4',
        browse_button: 'pickfiles',
        container: 'container',
        drop_element: 'container',
        max_file_size: '5mb',
        flash_swf_url: 'js/plupload/Moxie.swf',
        dragdrop: true,
        chunk_size: '4mb',
        uptoken_url: $('#uptoken_url').val(),
        domain: $('#domain').val(),
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
                console.log(res);
                // var sourceLink = domain + res.key; 获取上传成功后的文件的Url
                //AJAX 获取图片的URL
                var sourceLink = '';
                var thumbLink = '';
                var liElement = '';
                $.ajax({
                    type: "GET",
                    url: '/upload/getUrl?key=' + res['key']+'&size='+$("#multiple_size").val(),
                    dataType:"json",
                    async:false,
                    success:function(result){
                        sourceLink = result['url'];
                        thumbLink = result['thumb_url'];
                        var cellimgH=$('.cell .btn-ftp1').outerHeight();
                        liElement = '<div class="cell"><div class="cell-img " style="height:'+cellimgH+'px"><a href="'+sourceLink+'" class="fancybox cell_li" rel="gallery" title="">'+ ' <img src="'+thumbLink+'" key="'+res['key']+'"></a></div><div class="cell-del"><a href="javascript:;" class="del-btn"><i class="ico ico-del"></i><span class="txt-del">删除</span></a></div></div>';

                    }
                });
                $("#result").append(liElement);

                if(isExitsFunction('imgShow')){
                   imgShow();
                }
                //刷新keys input框的内容
                refreshKeys();
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
                    url: $('#get_key_url').val(),
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
    /**
     * 删除图片按钮
     */
    $(document).on('click', '.del-btn', function() {
        $(this).parent().parent().remove();
        refreshKeys();
    });
});

/**
 * 刷新keys隐藏节点的值
 */
var refreshKeys = function() {
    var keys = [];
    $("#result .cell-img img").each(function(){
        var key = $(this).attr('key');
        if (key!='') {
            keys.push(key)
        }
    });
    $(".multiple_field_name").val(keys.join(','));

};

