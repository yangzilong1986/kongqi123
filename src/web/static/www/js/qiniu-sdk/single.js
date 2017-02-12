$(function(){
    /**
     * 单文件上传工具
     */
    var uploaderSingle = Qiniu.uploader({
        runtimes: 'html5,flash,html4',
        browse_button: 'single_pickfiles',
        container: 'single_container',
        drop_element: 'single_container',
        max_file_size: '5mb',
        flash_swf_url: 'js/plupload/Moxie.swf',
        dragdrop: true,
        chunk_size: '4mb',
        uptoken_url: $('#single_uptoken_url').val(),
        domain: $('#domain').val(),
        auto_start: true,
        unique_names:false,
        save_key:false,
        init: {
            'FileUploaded': function(up, file, info) {               
                $(".single-del-btn").click();
                // 每个文件上传成功后,处理相关的事情
                var domain = up.getOption('domain');
                var res = jQuery.parseJSON(info);
                console.log(res);
                // var sourceLink = domain + res.key; 获取上传成功后的文件的Url
                //AJAX 获取图片的URL
                var sourceLink = '';
                $.ajax({
                    type: "GET",
                    url: '/upload/getUrl?key=' + res['key']+'&size='+$("#single_size").val(),
                    dataType:"json",
                    async:false,
                    success:function(result){
                        sourceLink = result['url'];
                    }
                });
                var liElement = '<img class="single_pickfiles "  key="'+res['key']+'" src="'+sourceLink+'" /><span class="radiushaed"></span> '
                $(".single_img_box").html(liElement);
                $("#single_key").val(res['key']);
                $("#single_key").trigger("change");

                //裁剪预览 start
                var previewFun=function(sourceLink,key){
                    this.sourceLink=sourceLink;
                    this.key=key;
                    this.previewClass="preview-head";
                    this.ajaxsave='/upload/crop/';
                    this.eventEle=$('#single_pickfiles').closest('.user_head');
                    this.init();

                }
                previewFun.prototype={
                    init:function(){
                        var TfThis=this;
                        var ftpvalue='<p class="poploadbox"><img src="http://s2.wealinkcdn.com/pc/images/default/landing.gif" width="160"  alt=""></p>';
                        TfThis.setPreviewTplFun(ftpvalue);    
                        //裁剪
                        var dataimg=new Image();
                        dataimg.src=this.sourceLink;
                        $(dataimg).load(function(){                     
                            var ftpvalue=TfThis.jcropImgTpl(TfThis.sourceLink);
                            TfThis.setPreviewTplFun(ftpvalue);
                            if($(TfThis.eventEle).attr("mobileftp")=="true"){
                                TfThis.mobilejcropImgFun();
                            }else{
                                TfThis.jcropImgFun();                                 
                            }                            
                            $("#single_pickfiles_preview .js_file_txt").val(TfThis.sourceLink);                                             
                        });
                    },
                    setPreviewTplFun:function(args){
                        var TfThis=this;
                        var winW=$(window).width();
                        var winH=$(window).height();
                        var ftpvalue=args;
                        if($("#single_pickfiles_preview").length>0){
                            $("#single_pickfiles_preview .pop-main").html(ftpvalue);                                                       
                        }else{
                            var previewTpl=this.previewTpl(ftpvalue);
                            $("body").append(previewTpl);
                        }
                        var popW=$("#single_pickfiles_preview .pop").width();
                        var popH=$("#single_pickfiles_preview .pop").height();
                        $(".pagewrap").css({"width":winW+"px","height":winH+"px","overflow":"hidden"});//mobile 页面100% set
                        $("#single_pickfiles_preview .pop").css({"margin": "-"+(popH/2)+"px 0 0 -"+(popW/2)+"px"});
                         $("body").on('click', "#single_pickfiles_preview .close", function(event) {
                                //默认裁剪
                                $('#single_pickfiles_preview .js_ajaxsave_btn').trigger('click');
                                //删除
                                $("#single_pickfiles_preview").remove();
                                $(".pagewrap").css({"width":"","height":"","overflow":""});//mobile 页面100% cancel                                
                        });                        

                    },                     
                    previewTpl:function(args){
                        var TfThis=this;
                        var html = [];
                        html.push(''); 
                        //裁剪层
                        if($(this.eventEle).attr("mobileftp")=="true"){
                        html.push('<div id="single_pickfiles_preview" class="jcroppop side_pop" style="display:block;">');                            
                        }else{
                        html.push('<div id="single_pickfiles_preview" class="jcroppop popUp" style="display:block;">');
                        }
                        html.push('    <div id="gmask"></div>');
                        html.push('    <div class="pop">');
                        html.push('    <div class="pop-wrap">');
                        html.push('        <span class="close close2"></span>');
                        html.push('        <div class="pop-main">');
                        html.push(args);
                        html.push('        </div>');        
                        html.push('    </div>');     
                        html.push('    </div>');      
                        html.push('</div>'); 
                        return html.join('');                                                
                    },
                    jcropImgTpl:function(args){
                        var html = [];
                        html.push('');
                        html.push('<div class="jcrop_wrap">');        
                        html.push('          <img src="'+args+'" class="target" alt="[Jcrop Example]" />');
                        html.push('          <div class="preview-pane" >');
                        html.push('            <div class="preview-container '+this.previewClass+'">');
                        html.push('              <img src="'+args+'"  class="jcrop-preview" alt="Preview" />');
                        html.push('            </div>'); 
                        html.push('          <div class="save_btn_box"><input class="js_ajaxsave_btn"  type="button" value="裁剪"></div>');            
                        html.push('          </div>');

                        html.push('          <div class="clear"></div>');
                        //图片裁剪表单
                        html.push('<form action="'+this.ajaxsave+'" id="single_pickfiles_preview_form" class="hidden">');
                        html.push('    <label>key <input type="hidden"  class="key" name="key" value="'+this.key+'" /></label>');
                        html.push('    <label>X1 <input type="hidden" size="4" class="x1" name="x1" /></label>');
                        html.push('    <label>Y1 <input type="hidden" size="4" class="y1" name="y1" /></label>');
                        html.push('    <label>W <input type="hidden" size="4" class="w" name="w" /></label>');
                        html.push('    <label>H <input type="hidden" size="4" class="h" name="h" /></label>');
              
                        html.push('</form>');  
                        html.push('</div>'); 
                        if($(this.eventEle).attr("mobileftp")=="true"){
                        html.push('<div class="jcrop_pop_action ">');
                        html.push('    <div class="pop_action">');
                        html.push('        <a class="btn btn-orange btn-s2 pop_comfirm" href="javascript:;" ><i class="ico ico-sure"></i>选  取</a>');
                        //html.push('        <a class="btn btn-green btn-s2 pop_cancel" href="javascript:;" ><i class="ico ico-cancel"></i>取  消 </a>');
                        html.push('    </div>');
                        html.push('</div>');
                        }     
                        return html.join('');  
                    },
                    jcropImgFun:function(){
                        var jcroppopid="#single_pickfiles_preview";
                        // Create variables (in this scope) to hold the API and image size
                        var jcrop_api,
                            boundx,
                            boundy,

                            // Grab some information about the preview pane
                              $preview = $(jcroppopid+' .preview-pane'),
                              $pcnt = $(jcroppopid+' .preview-pane .preview-container'),
                              $pimg = $(jcroppopid+' .preview-pane .preview-container img'),
                              $orimg =$(jcroppopid+" .target");
                              xsize = $pcnt.width(),
                              ysize = $pcnt.height();

                        jQuery(function($){            
                            var orx=$orimg.width();
                            var ory=$orimg.height();
                            
                            var zx=(xsize*ory)/ysize;
                            var zy=(ysize*orx)/xsize; 
                            var orw=orx;
                            var orh=ory;
                            if(ysize>=ory){
                                $(jcroppopid+' .pop .jcrop_wrap').height(ysize+56);
                                orh=ysize+56;
                            }
                            $(jcroppopid+' .jcrop_wrap').css({"padding-right": (xsize+50)});
                            $(jcroppopid+' .preview-pane').css({"right": -(xsize+50)});
                            var popw=(orw+100+xsize+50);
                            var poph=(orh+100);
                            $(jcroppopid+' .pop').css({"margin": "-"+(poph/2)+"px 0 0 -"+(popw/2)+"px"});  

                            if(zx<=orx){
                                var inty1=0;      
                                var intx1=(orx-zx)/2;                            
                                var intw=zx;                    
                            }else{
                                var intw=zy;                
                                var inty1=(ory-zy)/2;
                                var intx1=0;
                            }
                            $orimg.Jcrop({
                              onChange: updatePreview,
                              onSelect: updatePreview,
                              aspectRatio: xsize / ysize
                            },function(){
                              // Use the API to get the real image size
                              var bounds = this.getBounds();
                              boundx = bounds[0];
                              boundy = bounds[1];
                              // Store the API in the jcrop_api variable
                              jcrop_api = this;

                              // Move the preview into the jcrop container for css positioning
                              $preview.appendTo(jcrop_api.ui.holder);
                              jcrop_api.setSelect([intx1,inty1,intx1+intw]);
                            });


                        });
                        function updatePreview(c){
                          if (parseInt(c.w) > 0){
                            var rx = xsize / c.w;
                            var ry = ysize / c.h;
                            $pimg.css({
                              width: Math.round(rx * boundx) + 'px',
                              height: Math.round(ry * boundy) + 'px',
                              marginLeft: '-' + Math.round(rx * c.x) + 'px',
                              marginTop: '-' + Math.round(ry * c.y) + 'px'
                            });
                            showCoords(c);
                          }
                        };
                        function showCoords(c){
                            $(jcroppopid+' .x1').val(c.x);
                            $(jcroppopid+' .y1').val(c.y);
                            $(jcroppopid+' .w').val(c.w);
                            $(jcroppopid+' .h').val(c.h);
                        };           
                        this.ajaxsaveFun();
                    },
                    mobilejcropImgFun:function(){
                        var headerH=$(".header").height();
                            headerH=0;
                        if(headerH==null){
                            headerH=0;
                        }
                        var actionH=$(".jcrop_pop_action").height();
                        var winW=$(window).width();
                        var winH=$(window).height();
                        var rateWin; 
                        /*mobile*/
                        var jcroppopid="#single_pickfiles_preview";
                        // Create variables (in this scope) to hold the API and image size
                        var jcrop_api,
                            boundx,
                            boundy,
                            // Grab some information about the preview pane
                              $preview = $(jcroppopid+' .preview-pane'),
                              $pcnt = $(jcroppopid+' .preview-pane .preview-container'),
                              $pimg = $(jcroppopid+' .preview-pane .preview-container img'),
                              $orimg =$(jcroppopid+" .target");
                              xsize = $pcnt.width(),
                              ysize = $pcnt.height();                 
                        jQuery(function($){    
                            var orimgW=$orimg.width();
                            var orimgH=$orimg.height();                
                            var maxW=winW;
                            var maxH=winH-headerH-actionH;

                            var orx=$orimg.width();
                            var ory=$orimg.height();

                            var zx=(xsize*ory)/ysize;
                            var zy=(ysize*orx)/xsize; 
                            var orw=orx;
                            var orh=ory;
                            if(ysize>=ory){
                                $(jcroppopid+' .pop .jcrop_wrap').height(ysize+56);
                                orh=ysize+56;
                            }
                            /*mobile 显示 start*/
                            var targetSmaxW=maxH*orimgW/orimgH;
                            var targetSmaxH=maxW*orimgH/orimgW;
                            if(targetSmaxW>maxW){
                                $(jcroppopid+' .target').css({"width": maxW+"px"});
                                $(jcroppopid+' .jcrop_wrap').css({"padding-top": (maxH-targetSmaxH)/2+"px"});
                                rateWin=orimgW/maxW;                    
                            }
                            if(targetSmaxH>maxH){
                                $(jcroppopid+' .target').css({"height": maxH+"px"});
                                $(jcroppopid+' .jcrop_wrap').css({"padding-left": (maxW-targetSmaxW)/2+"px"});
                                rateWin=orimgH/maxH;
                            }
                            $(jcroppopid+' .pop').css({"top":headerH+"px","left":"0px","margin":"0px","width":winW+"px","height":maxH+"px"});
                             /*mobile 显示 end*/
                            if(zx<=orx){
                                var inty1=0;      
                                var intx1=(orx-zx)/2;                            
                                var intw=zx;                    
                            }else{
                                var intw=zy;                
                                var inty1=(ory-zy)/2;
                                var intx1=0;
                            }
                            var w_intx1=intx1/rateWin;
                            var w_inty1=inty1/rateWin;
                            var w_intw=intw/rateWin;
                            $orimg.Jcrop({
                              onChange: updatePreview,
                              onSelect: updatePreview,
                              aspectRatio: xsize / ysize
                            },function(){
                              // Use the API to get the real image size
                              var bounds = this.getBounds();
                              boundx = bounds[0];
                              boundy = bounds[1];
                              // Store the API in the jcrop_api variable
                              jcrop_api = this;

                              // Move the preview into the jcrop container for css positioning
                              $preview.appendTo(jcrop_api.ui.holder);
                              jcrop_api.setSelect([w_intx1,w_inty1,w_intx1+w_intw]);
                            });

                            $(".pop_comfirm").on('click', function(event) {
                               $(jcroppopid+' .js_ajaxsave_btn').trigger('click');
                            });
                            $(".pop_cancel").on('click', function(event) {
                               $(jcroppopid+' .close').trigger('click');
                            });
                        });
                        function updatePreview(c){
                          if (parseInt(c.w) > 0){
                            var rx = xsize / c.w;
                            var ry = ysize / c.h;
                            $pimg.css({
                              width: Math.round(rx * boundx) + 'px',
                              height: Math.round(ry * boundy) + 'px',
                              marginLeft: '-' + Math.round(rx * c.x) + 'px',
                              marginTop: '-' + Math.round(ry * c.y) + 'px'
                            });
                            showCoords(c);
                          }
                        };
                        function showCoords(c){
                            $(jcroppopid+' .x1').val(c.x*rateWin);
                            $(jcroppopid+' .y1').val(c.y*rateWin);
                            $(jcroppopid+' .w').val(c.w*rateWin);
                            $(jcroppopid+' .h').val(c.h*rateWin);
                        };           
                        this.ajaxsaveFun();
                    },
                    ajaxsaveFun:function(){
                        var TfThis=this;
                        $("body").on('click','.js_ajaxsave_btn',function(event) {
                            var curbtn = $(this);
                            $("#single_pickfiles_preview_form").on('submit',function(event) { 
                                 //倒数
                                /*curbtn.attr("disabled", "disabled");
                                curbtn.val("处理中...");*/
                                $("#single_pickfiles_preview").remove();                                                                            
                                var ftpvalue='<p class="poploadbox"><img src="http://s2.wealinkcdn.com/pc/images/default/landing.gif" width="160"  alt=""></p>';
                                TfThis.setPreviewTplFun(ftpvalue);
                                $.ajax({
                                    url: TfThis.ajaxsave,
                                    type: 'POST',
                                    data:$(this).serialize(),
                                    dataType: 'json',
                                    success: function(data){
                                        if(data.status){  
                                            // key 回填
                                            var keypath=$("#single_result #single_key").val();
                                                keypath=keypath.substring(0,keypath.lastIndexOf('/')+1);
                                            var newkey=data.url;
                                                newkey=newkey.substring(newkey.lastIndexOf('/')+1);
                                                newkey=keypath+newkey;
                                            $("#single_result #single_key").val(newkey);
                                            //图片 回填                  
                                            $(".single_img_box img.single_pickfiles").attr("src",data.url);                                            
                                            $("#single_pickfiles_preview").remove();                                                                            
                                            popsucc({
                                                "popconMsg":"上传成功",//成功Msg
                                                "popId":"single_pickfiles_preview"
                                            });    

                                        }else{ 
                                            curbtn.removeAttr("disabled");
                                            curbtn.val("确定");                                     
                                        }  
                                        $(".pagewrap").css({"width":"","height":"","overflow":""});//mobile 页面100% cancel  
                                    }
                                });
                               return false;
                            });
                           $("#single_pickfiles_preview_form").submit();     
                        });
                    },
                    discount:function(i,fun){
                           //倒数
                        var dis = i;
                        function _discount(){
                            fun(dis);
                            if(dis>0){
                                setTimeout(_discount,1000);
                            }
                            dis--;
                        }
                        _discount();
                    }
                }
                new previewFun(sourceLink,res['key']);
                //裁剪预览 end
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
                    url: $('#single_get_key_url').val(),
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