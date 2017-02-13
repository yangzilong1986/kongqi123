(function() {
   //Section 1 : 按下自定义按钮时执行的代码
    var gwmFtpFun= {
        exec:function(editor){
            $('.pickfiles_ckeditor_wrap input[type="file"]').trigger("click");
        }
    }
    CKEDITOR.plugins.add("gwm_ftp", {
        init: function(editor) {
            var pluginName = 'gwm_ftp';
            editor.addCommand(pluginName,gwmFtpFun);
            editor.ui.addButton(pluginName,
            {
                label: '插入图片',
                command: pluginName,
                icon: this.path + "gwm_ftp.png"//在toolbar中的图标
            });

        }

    })
})();