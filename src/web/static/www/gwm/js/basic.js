$(document).ready(function() {
     //锚点定位动画
     scrollToFun();
     //a代理
     jsAagentfun();
     //select,radio,checkbox 设置默认选择值
     selvalueFun();
     //placeholder
     placeholderFun();

     //AJAX 请求刚开始时执行
/*  $(document).ajaxStart(function() {
        var poploadingtxt='<img src="'+bascstatic+'pc/images/default/landing.gif" width="160"  alt="">'
        popnormal({
            "popconMsg":poploadingtxt,//可选项
            "popId":"poploading"//弹出层id 默认为popnormal,（可自定义）
        });
    });
    $(document).ajaxSuccess(function() {
        $("#poploading").remove();
    }); */


    //页面初始化
    pageInit();
    $("body").resize(function(){
        pageInit();
    });
    //form reset
    formReset();
    //select_checkbox 左右选择 组件
    new selectCheckboxFun();
    //模拟Select
    proxySelectFun();
    //模拟 radio checkbox  样式  注意label 的for属性 与  radio checkbox  一一对应；
    proxyInput();
    //省略符
    ellipsisText();

    //左边导航
    navlistFun();
    //偶数行加class even;
    evenClassFun();
    //父亲焦点样式
    pFocus();
});
//父亲焦点样式
function pFocus(){
    $('body').on('focus', '.js-pfocus .form-control', function(event) {
        event.preventDefault();
        /* Act on the event */
        var pEle=$(this).closest('.js-pfocus');
        $(pEle).addClass('focus');
    });
    $('body').on('blur', '.js-pfocus .form-control', function(event) {
        event.preventDefault();
        /* Act on the event */
        var pEle=$(this).closest('.js-pfocus');
        $(pEle).removeClass('focus');
    });
}
//左边导航
function navlistFun(){
    $('body').on('click', '.nav-list .has-child .nav-one', function(event){
        event.preventDefault();
        var eleP=$(this).closest('.li');
        $('.nav-two',eleP).stop().slideToggle(100);
        $(eleP).toggleClass('down');
    });
 }
//ajax 表单验证
//serviceValidateFun('#publish_position_form');
function serviceValidateFun(formId){
    $('body').off('blur',formId+' .js_validate');
    $('body').on('blur',formId+' .js_validate',function(event){
            var formEle=$(this);
            var eleWrap=$(this).closest('.ele-wrap');
            var ajaxUrl=$(formId).attr("ajaxUrl");
            var dataName=$(this).attr("name");
            var pFocusEle=$(this).closest('.form-control-ele');

            var dataVal=$(this).val();
            var dataObj={}
            dataObj[dataName]=dataVal;
            $.ajax({
                url: ajaxUrl,
                type: 'GET',
                dataType: 'json',
                data:dataObj,
                success: function(data){
                    $('p.error',eleWrap).remove();
                    $(formEle).removeClass('error');
                    if(!data.status){
                        $(formEle).addClass('error');
                        $(pFocusEle).addClass('error');
                        var errorHtml=[];
                        errorHtml.push('<p class="error">'+data.message+'</p>');
                        $(eleWrap).append(errorHtml.join(''));
                    }
                }
            })
    });
    $('body').off('focus',formId+' .js_validate');
    $('body').on('focus',formId+' .js_validate',function(event){
        var formEle=$(this);
        var pFocusEle=$(this).closest('.form-control-ele');

        var eleWrap=$(this).closest('.ele-wrap');
        $('p.error',eleWrap).remove();
        $(formEle).removeClass('error');

        $(pFocusEle).removeClass('error');
    });
}

//省略符
function ellipsisText(){
    $(".js_ellipsis").each(function(index, el) {
        var row=parseInt($(this).attr('ellipsis_row'));
        var eleH=$(this).height();
        var lineH=parseInt($(this).css("line-height"));
        var limtH=lineH*row;
        if(eleH>limtH){
            $(this).addClass('text-ellipsis');
            $(this).css({'height':limtH+'px','overflow':'hidden'});
        }
    });
}

if(!window['console'] || !window['console']['log']){
    window.console={
            log:function(){

            }
        }
}

//页面初始化
function pageInit(){
    var winH=$(window).height();
    var boydH=$("body").height();
    /*footer始终在页面底部 start*/
    var footerH=$(".footer").length>0 ? $(".footer").outerHeight() : 0;
    if($(".footer").length>0){
        if(boydH<=winH){
            $(".footer").css({"position": "fixed","bottom":"0px","left":"0px;"});
            $(".footer-wrap").css({'height':footerH+'px'});
            $('body').css({'min-height':winH+'px'});
        }else{
            $(".footer").css({"position": "","bottom":"","left":""});
            $(".footer-wrap").css({'height':''});
            $('body').css({'min-height':''});
        }
    }
    /*footer始终在页面底部 end*/

    //除首页外 768高度适应处理
    if(winH<=768){
        $("body").addClass("body-768");
    }else{
        $("body").removeClass("body-768");
    }
    if($('.page-main').hasClass('body_bg')){
        $('body').addClass('body-bg');
    }else{
        $('.footer-wrap').addClass('body-bg');
    }
    //头部动画处理
    headFun();
}
//头部动画处理 start
function headFun(){
    var hLeft=$('.header-left').outerWidth();
    var hRight=$('.header-right').outerWidth();
    var hWrapW=$('.header .wrap').outerWidth()-parseInt($('.header .wrap').css('padding-left'))-parseInt($('.header .wrap').css('padding-right'));
    var hCenterW=hWrapW-hLeft-hRight-10;
    $('.header-center').css({'width':hCenterW+'px'});
    var goTopLmit=$(window).height();

    var headAnim= $('.header-wrap').hasClass('head-anim') ? true :false;
    var animTopLmit=$('.header-wrap').outerHeight()-$('.header').outerHeight();
    if(headAnim){
        var hCenterMar=hLeft+parseInt($('.header').css('padding-left'))+parseInt($('.header .wrap').css('padding-left'));
        $('.header-center').css({'margin-left':hCenterMar+'px'});
        $('.header-wrap').data('headAnimState','up');
        $('.header-wrap').css({'height':$('.header-wrap').outerHeight()+'px'});
    }
    //scroll
    $(window).on('scroll',function(event) {
        var curT=$(this).scrollTop();
        //回到顶部
        if(curT>goTopLmit){
            $('.js_go_top').removeClass('hidden');
        }else{
            $('.js_go_top').addClass('hidden');
        }
        if(headAnim){
            if(curT>=animTopLmit){
                if($('.header-wrap').data('headAnimState')!='down'){
                    $('.header-wrap').data('headAnimState','down');
                    $('.header-wrap').removeClass('head-anim');
                    $('.header-center').css({'margin-left':''});
                    animCss3Fun({
                      "animObj":".gwm-logo",//动画对象 class
                      "animOption":"slideInDown"
                    });
                    animCss3Fun({
                      "animObj":".gwm-weixin",//动画对象 class
                      "animOption":"slideInDown"
                    });
                }
            }else{
                if($('.header-wrap').data('headAnimState')!='up'){
                    $('.header-wrap').data('headAnimState','up');
                    $('.header-wrap').addClass('head-anim');
                    $('.header-center').css({'margin-left':hCenterMar+'px'});
               }

            }
        }
    });
    $('.js_go_top').on('click',  function(event) {
        $("html,body").stop().animate({scrollTop: 0}, 300);
    });

}
//头部动画处理 end

//form reset
function formReset(){
    $("form").on("reset",function(){
        $("input.form-control",$(this)).attr("value","");
        $('select.form-control option',$(this)).removeAttr("selected");
    })
}

//偶数行加class even;
function evenClassFun(){
    $(".evenParent").each(function(index, el) {
        var evenCell=$(this).attr("even_cell");
        $(evenCell+':odd',$(this)).addClass('even');
    });
}

//a代理
var jsAagentfun=function(){
    $(".js_agent").each(function(index, el) {
        var agenttag=$(this).attr("agenttag");
        $("body").off('click', ".js_agent "+agenttag);
         $("body").on('click', ".js_agent "+agenttag, function(event) {
            if($(event.target)[0].tagName!="A"&&$(event.target)[0].tagName!="INPUT"&&$(event.target)[0].tagName!="LABEL"){
                var agentUrl=$(this).attr("agenturl");
                var  agentTarget=$(this).attr("agenttarget");
                if(agentUrl!=""&&!agentUrl!=undefined){
                    if(agentTarget=="_blank"){
                        window.open(agentUrl);
                    }else{
                        location.href=agentUrl;
                    }
                }
            }
         });
    });

}
//锚点定位动画
function scrollToFun(agrs) {
    $("body").on('click','.js_goto',function(event) {
        var gotodata=$(this).attr("gotodata");
        if($('.head-h').length>0){
            $("html,body").stop().animate({scrollTop: $(gotodata).offset().top-120}, 300);
        }else{
            $("html,body").stop().animate({scrollTop: $(gotodata).offset().top}, 300);
        }
    });
}

// 弹出层
var popFun= function(){
    this.animateTime=350;
    this.popDataId=null;
}
popFun.prototype={
    init:function(args){

        var TfThis=this;
        if(args.popDataId!=undefined){
            this.popDataId=args.popDataId;
        }else{
            this.popDataId=args.popId;
        }

        if(args.eventEle!=undefined){
            $(document).on('click',args.eventEle,((function(TfThis) {
                return function(event) {
                    event.preventDefault();
                    //关闭 所有层
                    if($('.popUp').length>0){
                        $('.popUp').each(function(){
                            $('.close',$(this)).trigger('click');
                        })
                    }

                    args.eventEle=$(this);
                    var curPop=null;
                    if(args.creatType!=undefined){
                        if(args.creatType[0]==1){
                            $("body").append(TfThis.pops1(args));
                            //取消滚动冒泡事件
                            $('.popUp').preventScroll();
                            curPop=$("#"+TfThis.popDataId);
                            //兼容  单数据源 对 1个模板1个位置
                            if(args.popTplId!=undefined&&args.data!=undefined){
                                //兼容  单数据源 对 1个模板1个位置
                                multipleTpl({
                                    "data": args.data,
                                    "sourcetpl":args.popTplId,//1个模板
                                    "insertsit": "#"+TfThis.popDataId+" .pops1_con",//1个位置
                                    "insertmethod": "html"
                                });
                            }
                            TfThis.popStyleFun(args,curPop);
                            if(args.popCallbackFun){
                                args.popCallbackFun(args,TfThis,$(this));
                            }

                        }
                    }else{
                        var curPop=null;
                        if(TfThis.popDataId!=undefined){
                            curPop=$("#"+TfThis.popDataId);
                        }else{
                            curPop=$($(this).attr("pop-data"));
                        }
                        if(curPop.length>0){
                            TfThis.popStyleFun(args,curPop);
                            if(args.popCallbackFun){
                                args.popCallbackFun(args,TfThis,$(this));
                            }
                        }
                        //取消滚动冒泡事件
                        $('.popUp').preventScroll();

                    }
                }
            })(this)));
        }
        if(args.showPop!=undefined){
            //关闭 所有层
            if($('.popUp').length>0){
                $('.popUp').each(function(){
                    $('.close',$(this)).trigger('click');
                })
            }

            var curPop=null;
            switch(args.showPop){
                case true:
                    curPop=$("#"+this.popDataId);

                    break;
                default:

                    curPop=$(args.showPop);
            }

            if(args.creatType!=undefined){
                if(args.creatType[0]==1){
                    $("body").append(TfThis.pops1(args));
                    //取消滚动冒泡事件
                    $('.popUp').preventScroll();
                    curPop=$("#"+this.popDataId);
                    //兼容  单数据源 对 1个模板1个位置
                    if(args.popTplId!=undefined&&args.data!=undefined){
                        //兼容  单数据源 对 1个模板1个位置
                        multipleTpl({
                            "data": args.data,
                            "sourcetpl":args.popTplId,//1个模板
                            "insertsit": "#"+this.popDataId+" .pops1_con",//1个位置
                            "insertmethod": "html"
                        });
                    }
                    TfThis.popStyleFun(args,curPop);
                    if(args.popCallbackFun){
                        args.popCallbackFun(args,TfThis);
                    }

                }
            }else{
                if(curPop.length>0){
                    this.popStyleFun(args,curPop);
                    if(args.popCallbackFun){
                        args.popCallbackFun(args,TfThis,$(this));
                    }
                }
                //取消滚动冒泡事件
                $('.popUp').preventScroll();

            }
        }
    },
    popStyleFun:function(args,curPop){
        var animateTime=this.animateTime;
            var curPop=curPop;
            curPop.css({"display":"block"});
            var popWH={
                W:$(".pop",curPop).width(),
                H:$(".pop",curPop).height()
            }

            switch (args.popStyle){
                case "zoom":
                    $(".pop",curPop).css({"opacity": 0,"left":"50%","top":"50%","width":"0px","height":"0px"});
                    $(".pop",curPop).addClass('over-hidden');
                    $(".pop",curPop).stop().animate({
                        "opacity": 1,
                        "width":popWH.W+"px",
                        "height":popWH.H+"px",
                        "margin": "-"+(popWH.H/2)+"px 0 0 -"+(popWH.W/2)+"px"
                    },animateTime, function() {

                        /*close*/
                        $(".close",curPop).on('click',function(event) {
                            $(".pop",curPop).stop().animate({
                                "opacity": 0,
                                "width":"0px",
                                "height":"0px",
                                "margin": "0px 0 0 0px"
                                },
                                animateTime, function() {
                                if(args.creatType!=undefined){
                                    if(args.creatType[0]==1){
                                        curPop.remove();
                                    }
                                }else{
                                    curPop.css({"display":"none"});
                                    $(".pop",curPop).removeClass('over-hidden');
                                    $(".pop",curPop).css({"opacity": 0,"left":"50%","top":"50%","width":popWH.W+"px","height":popWH.H+"px"});
                                }
                            });

                        });
                        $(".pop_action a,.pop_action input",curPop).on('click', function(event) {
                            var actionColse=$(this).attr("actionColse");

                            switch(actionColse){
                                case "false":

                                break;
                                case "true":
                                    $(".close",curPop).trigger("click");
                                break;
                                default:
                                    $(".close",curPop).trigger("click");
                            }
                        });
                    });

                  break;
                case "fade":
                    $(".pop",curPop).css({"opacity": 0,"left":"50%","top":"50%","margin": "-"+(popWH.H/2)+"px 0 0 -"+(popWH.W/2)+"px"});
                    $(".pop",curPop).stop().animate({
                        "opacity": 1
                    },animateTime, function() {
                        $("body").addClass("popbody");
                        /*close*/
                        $(".close",curPop).on('click',function(event) {
                            $(".pop",curPop).stop().animate({
                                "opacity": 0
                                },
                                0, function() {
                                $("body").removeClass("popbody");
                                if(args.creatType!=undefined){
                                    if(args.creatType[0]==1){
                                        curPop.remove();
                                    }
                                }else{
                                    curPop.css({"display":"none"});
                                }
                            });
                        });
                        //自动关闭
                        if(args.closeAuto){
                            setTimeout(function(){
                                if(curPop.length>0){
                                    $(".close",curPop).trigger("click");
                                }
                            },3000);
                        }
                        //成功自动关闭
                        if(args.creatType!=undefined){
                            if(args.creatType[0]==1){
                                if(args.creatType[1].conMsg[0]==1){
                                    setTimeout(function(){
                                        if(curPop.length>0){
                                            //$(".close",curPop).trigger("click");
                                        }
                                    },3000);
                                }
                            }
                        }
                        $(".pop_action a,.pop_action input",curPop).on('click', function(event) {
                            var actionColse=$(this).attr("actionColse");
                            switch(actionColse){
                                case "false":
                                break;
                                case "true":
                                    $(".close",curPop).trigger("click");
                                break;
                                default:
                                    $(".close",curPop).trigger("click");
                                ;
                            }
                        });
                    });
                  break;
                default:
                    $(".pop",curPop).css({"opacity": 1,"left":"50%","top":"50%","margin": "-"+(popWH.H/2)+"px 0 0 -"+(popWH.W/2)+"px"});
                    $(".pop",curPop).stop().animate({
                        "opacity": 1
                    },animateTime, function() {

                    });
            }
    },
    pops1:function(args){
        var curDomArgs=args.creatType[1];

        var pops1html = [];
        pops1html.push('');
        pops1html.push('<div id="'+this.popDataId+'" class="popUp"  >');
        pops1html.push('    <div id="gmask"></div>');
    if(curDomArgs.popSize!=undefined){
        pops1html.push('    <div class="pop '+curDomArgs.popSize+' pops1">');
    }else{
        pops1html.push('    <div class="pop mid pops1">');
    }
        pops1html.push('    <div class="pop-wrap">');
    if(curDomArgs.headTitle!=undefined){
        pops1html.push('        <span class="close"></span>');
    }else{
        pops1html.push('        <span class="close close2"></span>');
    }

    if(curDomArgs.headTitle!=undefined){
        pops1html.push('        <div class="pop_head">');
    if(curDomArgs.headRight!=undefined){
        pops1html.push('            <div class="poph_right">'+curDomArgs.headRight+'</div>');
    }
        pops1html.push('            <h3>'+curDomArgs.headTitle+'</h3>');
    if(curDomArgs.headRight!=undefined){
        pops1html.push('            <div class="sub">'+curDomArgs.headTitleSub+'</div>');
    }
        pops1html.push('        </div>');
    }
        pops1html.push('        <div class="pop_body">');
    if(curDomArgs.headTitle==undefined){
        pops1html.push('        <div class="pops1_con no-head">');
    }else{
        pops1html.push('            <div class="pops1_con">');
    }
    if(curDomArgs.conMsg!=undefined){
        switch(curDomArgs.conMsg[0]){
            case 0:
            pops1html.push(curDomArgs.conMsg[1]);
            break;
            case 1:
            pops1html.push('                <div class="pop_tips_wrap"><div class="pop_tips_info"><i class="ico ico-tips-succ"></i>'+curDomArgs.conMsg[1]+'</div></div>');
            break;
            case 2:
            pops1html.push('                <div class="pop_tips_wrap"><div class="pop_tips_info" ><i class="ico ico-tips-error"></i>'+curDomArgs.conMsg[1]+'</div></div>');
            break;
            case 3:
            pops1html.push('                <div class="pop_tips_wrap"><div class="pop_tips_info"><i class="ico ico-tips-warning"></i>'+curDomArgs.conMsg[1]+'</div></div>');
            break;
        }
    }
        pops1html.push('            </div>');
    if(curDomArgs.popAction!=undefined){
        pops1html.push('            <div class="pop_action">');
        for(var i=0;i<curDomArgs.popAction.length;i++){
            var curAction=curDomArgs.popAction[i];
        pops1html.push('                <a  ');
        if(curAction.actionClass){
        pops1html.push('class="'+curAction.actionClass+'"');
        }else{
            switch(i){
                case 0:
        pops1html.push('class="btn btn-primary"');
                break;
                case 1:
        pops1html.push('class="btn btn-default"');
                break;
                default:
        pops1html.push('class="btn btn-primary"');

            }
        }
        if(curAction.actionHref){
        pops1html.push('href="'+curAction.actionHref+'"');
        }else{
        pops1html.push('href="javascript:;"');
        }
        if(curAction.actionId!=undefined){
        pops1html.push('id="'+curAction.actionId+'"');
        }
        if(curAction.actionColse!=undefined){
        pops1html.push('actionColse="'+curAction.actionColse+'"');
        }
        if(curAction.onclick!=undefined){
            pops1html.push('onclick="'+curAction.onclick+'"');
        }
        pops1html.push('>'+curAction.actionTxt+'</a>');
        }
        pops1html.push('            </div>');
    }
        pops1html.push('        </div>');
        pops1html.push('    </div> ');
        pops1html.push('    </div> ');
        pops1html.push('</div>');
        return pops1html.join('');
    }

}
//普通弹出层
/*

<!-- 普通模板 start -->
<div id="normalbox" class="js_hidetpl_box">
    普通内容Tpl{{title}}

    <!-- 按钮区 a,input 标签 默认自带关闭该层功能 如果设置 actionColse="false" 则不关闭该层 start-->
    <div class="pop_action">
        <a href="javascript:;" class="btn btn-green2" actionColse="false" >提交</a>
        <a href="javascript:;" class="btn btn-gray"  >取消</a>
        <a class="link" href="javascript:;">修改信息</a>
    </div>
    <!-- 按钮区 end-->
</div>
<!-- 普通模板 end -->
<a href="javascript:;"   class="js_popnormal">普通</a>
<script type="text/javascript">
var data1 = {title: "My New Posffsst", body: "This is my first post!"};
popnormal({
    "data":data1,//使用 handlebars 带数据的内容模板id  的 数据  //可选项
    "popTplId":"#normalbox",//内容模板id
    //"popconMsg":"popconMsg普通内容",//可选项
    "eventEle":".js_popnormal",//点击事件元素（不定义：立即弹出）
    "popId":"popnormal",//弹出层id 默认为popnormal,（可自定义）
    "headTitle":"普通标题",//普通标题
    "popSize":"",//控制大小样式 //可选项
    //"popAction":[{"actionTxt":"提  交","actionId":"js_report_submit","actionClass":"btn btn-info","actionColse":false},{"actionTxt":"取  消","actionColse":true},{"actionTxt":"修改信息"}],//按钮区
    "popCallbackFun":function(args,TfThis){//popCallbackFun 可选项
        //console.log(args);//层的相关参数
        //var curpopid = "#" + args.popId;
        //$(curpopid+" .close").trigger('click');//关闭该层
        //$(curpopid+" .close").on('click', function(event) {
            //关闭层做的操作
        //});
    }

});
//$("#popnormal .close").trigger("click");//关闭层
//$("#popnormal .close").on('click', function(event) {
//    //关闭层做的操作
//});
</script>
*/
var popnormal=function(args){
    var popTpl;

    if(args.popconMsg!=undefined){
        if(args.popAction){
            popTpl='<div class="pop_tips_msg">'+args.popconMsg+'</div>';
        }else{
            popTpl='<div class="pop_tips_msg_noaction">'+args.popconMsg+'</div>';
        }
    }
    if(args.popTplId!=undefined){
        popTpl=$(args.popTplId).html();
        var data=args.data;
    }
    if(args.popconTpl!=undefined){
        popTpl=args.popconTpl;
    }
    var popDataId;
    if(args.popId==undefined){
        popDataId="popnormal";
    }else{
        popDataId=args.popId;
    }
    var popCallbackFun;
    if(args.popCallbackFun){
        popCallbackFun=args.popCallbackFun;
    }
    var popAction;
    if(args.popAction){
        popAction=args.popAction;
    }
    var popSize;
    if(args.popSize){
        popSize=args.popSize;
    }
    var closeAuto;
    if(args.closeAuto){
        closeAuto=args.closeAuto;
    }
    if(args.eventEle==undefined){
        new popFun().init({
            "popTplId":args.popTplId,
            "data":data,
            "popStyle":"fade",
            "popDataId":popDataId,
            "popId":popDataId,
            "creatType":[1,{
                "popSize":popSize,
                "headTitle":args.headTitle,
                "conMsg":[0,popTpl],
                "popAction":popAction
            }],
            "showPop":true,
            "closeAuto":closeAuto,
            "popCallbackFun":popCallbackFun
        });
    }else{
        new popFun().init({
            "popTplId":args.popTplId,
            "data":data,
            "eventEle":args.eventEle,
            "popStyle":"fade",
            "popDataId":popDataId,
            "popId":popDataId,
            "creatType":[1,{
                "popSize":popSize,
                "headTitle":args.headTitle,
                "conMsg":[0,popTpl],
                "popAction":popAction
            }],
            "closeAuto":closeAuto,
            "popCallbackFun":popCallbackFun
        });
    }

}
//弹出层成功
/*
<!-- 几秒后自动关闭该层 -->
<a href="javascript:;"   class="js_popsucc">成功</a>
<script type="text/javascript">
popsucc({
    "popconMsg":"成功",//成功Msg
    "eventEle":".js_popsucc",//点击事件元素（不定义：立即弹出）
    "popId":"popsucc",//弹出层id 默认为ppopsucc,（可自定义）
    "headTitle":"成功",//成功标题
    "popCallbackFun":function(args,TfThis){//popCallbackFun 可选项
        //console.log(args);//层的相关参数
        //var curpopid = "#" + args.popId;
        //$(curpopid+" .close").trigger('click');//关闭该层
        //$(curpopid+" .close").on('click', function(event) {
            //关闭层做的操作
        //});
    }
});
//$("#popsucc .close").trigger("click");//关闭层
//$("#popsucc .close").on('click', function(event) {
//    //关闭层做的操作
//});
</script>
*/
var popsucc=function(args){
    var popTpl=args.popconMsg;
    var popDataId;
    if(args.popId==undefined){
        popDataId="popsucc";
    }else{
        popDataId=args.popId;
    }
    var popCallbackFun;
    if(args.popCallbackFun){
        popCallbackFun=args.popCallbackFun;
    }
    var closeAuto;
    if(args.closeAuto){
        closeAuto=args.closeAuto;
    }
    if(args.eventEle==undefined){
        new popFun().init({
            "popStyle":"fade",
            "popDataId":popDataId,
            "popId":popDataId,
            "creatType":[1,{
                "popSize":"mid popsucc",
                "headTitle":args.headTitle,
                "conMsg":[1,popTpl]
            }],
            "showPop":true,
            "closeAuto":closeAuto,
            "popCallbackFun":popCallbackFun
        });
    }else{
        new popFun().init({
            "eventEle":args.eventEle,
            "popStyle":"fade",
            "popDataId":popDataId,
            "popId":popDataId,
            "creatType":[1,{
                "popSize":"mid popsucc",
                "headTitle":args.headTitle,
                "conMsg":[1,popTpl]
            }],
            "closeAuto":closeAuto,
            "popCallbackFun":popCallbackFun
        });
    }

}
//弹出层失败
/*
<!-- 点击确认按钮关闭该层 -->
<a href="javascript:;"   class="js_poperror">失败</a>
<script type="text/javascript">
poperror({
    "popconMsg":"失败",
    "eventEle":".js_poperror",//点击事件元素（不定义：立即弹出）
    "popId":"poperror",//弹出层id 默认为poperror,（可自定义）
    "headTitle":"失败",//失败标题
    "popCallbackFun":function(args,TfThis){//popCallbackFun 可选项
        //console.log(args);//层的相关参数
        //var curpopid = "#" + args.popId;
        //$(curpopid+" .close").trigger('click');//关闭该层
        //$(curpopid+" .close").on('click', function(event) {
            //关闭层做的操作
        //});
    }
});
//$("#poperror .close").trigger("click");//关闭层
//$("#poperror .close").on('click', function(event) {
//    //关闭层做的操作
//});
</script>
*/
var poperror=function(args){
    var popTpl=args.popconMsg;
    var popDataId;
    if(args.popId==undefined){
        popDataId="poperror";
    }else{
        popDataId=args.popId;
    }
    var popCallbackFun;
    if(args.popCallbackFun){
        popCallbackFun=args.popCallbackFun;
    }
    var popSize;
    if(args.popSize){
        popSize=args.popSize;
    }
    var closeAuto;
    if(args.closeAuto){
        closeAuto=args.closeAuto;
    }
    if(args.eventEle==undefined){
        new popFun().init({
            "popStyle":"fade",
            "popDataId":popDataId,
            "popId":popDataId,
            "creatType":[1,{
                "popSize":"mid poperror",
                "headTitle":args.headTitle,
                "conMsg":[2,popTpl]/*,
                "popAction":[{"actionTxt":"确  认"}]*/
            }],
            "showPop":true,
            "closeAuto":closeAuto,
            "popCallbackFun":popCallbackFun
        });
    }else{
        new popFun().init({
            "eventEle":args.eventEle,
            "popStyle":"fade",
            "popDataId":popDataId,
            "popId":popDataId,
            "creatType":[1,{
                "popSize":"mid poperror",
                "headTitle":args.headTitle,
                "conMsg":[2,popTpl]/*,
                "popAction":[{"actionTxt":"确  认"}]*/
            }],
            "closeAuto":closeAuto,
            "popCallbackFun":popCallbackFun
        });
    }
}
// 弹出层 end



//倒数
function discount(i,fun){
    var dis = i;
    var clear='true';
    function _discount(){
        clear= fun(dis);
        if(dis>0&& clear!='false'){
            setTimeout(_discount,1000);
        }
        dis--;
    }
    _discount();
}

//form 控件选中
//SELECT,radio:selectValue="2";
//checkbox: selectValue="2,3"
/*selvalueFun({"parentEle":});*/
var selvalueFun=function(args){
    var curparentEle="";
    if(args!=undefined){
        curparentEle=args.parentEle;
    }
    $(curparentEle+" :input").each(function(index, el) {
        if($(this).attr("selectValue")!=undefined&&$(this).attr("selectValue")!=""){
            var selectValue=$(this).attr("selectValue");
            var curOjbTagName=$(this)[0].tagName;
                if($(this).closest('form').length==1){
                    var curformEle =$(this).closest('form');
                }
            switch(curOjbTagName){
                case "INPUT":
                    var curOjbType=$(this).attr("type");
                    switch(curOjbType){
                        case "checkbox":
                            var checkboxName=$(this).attr("name");
                            var selectedValueArray = selectValue.split(",");
                            for(var i=0;i<selectedValueArray.length;i++){
                                if(curformEle!=undefined){
                                    $('[name="'+checkboxName+'"][value="'+selectedValueArray[i]+'"]',$(curformEle)).prop('checked',true);
                                }else{
                                    $(curparentEle+' [name="'+checkboxName+'"][value="'+selectedValueArray[i]+'"]').prop('checked',true);
                                }
                            }
                        break;
                        case "radio":
                            var radioName=$(this).attr("name");
                            if(curformEle!=undefined){
                                $(curparentEle+' [name="'+radioName+'"][value="'+selectValue+'"]',$(curformEle)).prop('checked',true);
                            }else{
                                $(curparentEle+' [name="'+radioName+'"][value="'+selectValue+'"]').prop('checked',true);
                            }
                        break;
                    }
                break;
                case "SELECT":
                    $('option[value="'+selectValue+'"]',$(this)).prop('selected',true);
                    /*if($(this).attr("selectxt")!=undefined){
                        $('option[value="'+selectValue+'"]',$(this)).attr('selected', true); //设置Select的Text值为jQuery的项选中
                    }*/
                break;

            }
        }
    });
    $("body").off('change', ":input");
    $("body").on('change', ":input", function(event) {
            var curOjbTagName=$(this)[0].tagName;
                if($(this).closest('form').length==1){
                    var curformEle =$(this).closest('form');
                }
            switch(curOjbTagName){
                case "INPUTss":
                    var curOjbType=$(this).attr("type");
                    switch(curOjbType){
                        //selectValue="2,3"
                        case "checkbox":
                            var checkboxName=$(this).attr("name");
                            var cursleval=[];
                            if(curformEle!=undefined){
                                var checkboxArray=$('[name="'+checkboxName+'"]',$(curformEle));
                            }else{
                                var checkboxArray=$(curparentEle+' [name="'+checkboxName+'"]');
                            }
                            if(typeof($(checkboxArray[0]).attr("selectValue"))!="undefined"){
                                if(curformEle!=undefined){
                                    var checkedArray=$('[name="'+checkboxName+'"]:checked',$(curformEle));
                                }else{
                                    var checkedArray=$(curparentEle+' [name="'+checkboxName+'"]:checked');
                                }
                                //selectValue set;
                                for(var i=0; i<checkedArray.length;i++){
                                    cursleval.push($(checkedArray[i]).val());
                                }
                                cursleval=cursleval.join(",");
                                $(checkboxArray[0]).attr("selectValue",cursleval);
                            }
                        break;
                        case "radio":
                            var radioName=$(this).attr("name");
                            var cursleval=[];
                            if(curformEle!=undefined){
                                var radioArray=$('[name="'+radioName+'"]',$(curformEle));
                            }else{
                                var radioArray=$(curparentEle+' [name="'+radioName+'"]');

                            }
                            if(typeof($(radioArray[0]).attr("selectValue"))!="undefined"){
                                if(curformEle!=undefined){
                                    var checkedArray=$('[name="'+radioName+'"]:checked',$(curformEle));
                                }else{
                                    var checkedArray=$(curparentEle+' [name="'+radioName+'"]:checked');
                                }
                                //selectValue set;
                                cursleval=$(checkedArray).val();
                                $(radioArray[0]).attr("selectValue",cursleval);
                            }
                        break;
                    }
                break;
                case "SELECT":
                    if(typeof($(this).attr("selectValue"))!="undefined"){
                        $(this).attr("selectValue",$(this).val());

                    }
                break;

            }
    });
}
/*selectValue
selectxt*/


/*handlebars生成模板 start*/
/*
var data1 = {title: "My New Posffsst", body: "This is my first post!"};
var data2=[
{"title":"ccc1","body":"1","center":"center1","bottom":"bottom1"},
{"title":"ccc2","body":"21","center":"center2","bottom":"bottom2"},
{"title":"ccc3","body":"31","center":"center3","bottom":"bottom3"}
]
// 单数据源 对 1个模板1个位置
creathtmlTpl({
    "data":data1,//数据
    "sourcetpl":"#entry-template1",//模板
    "insertsit":"#temp1",//插入位置的元素
    "insertmethod":"append"//插入方式
})
//insertmethod：append[不定义默认append],before,after;
*/
var creathtmlTpl=function(args){
    var source   = $(args.sourcetpl).html();
    var template = Handlebars.compile(source);
    var data =args.data;

    if(data instanceof Array){
        var html = "";
        for (var i = 0; i < data.length; i++) {
            var curhtml= template(data[i]);
            html=html+curhtml;
        }
    }else{
        var html = template(data);
    }
    var curInsertMethod;
    if(args.insertmethod!=undefined){
        curInsertMethod=args.insertmethod;
    }else{
        curInsertMethod="append";
    }
    $(args.insertsit)[curInsertMethod](html);
}

/*
//单数据源 对多个模板，多个位置
multipleTpl({
    "data":data2,
    "sourcetpl":["#entry-template1","#entry-template2"],//多个模板
    "insertsit":["#temp2","#temp3"],//多个位置 与模板一样对应
    "insertmethod":["before","after"],//多个插入方式与模板一样对应
    //"insertmethod":"append",//都是一个插入方式
    "CallbackFun":function(args){
        console.log("CallbackFun 1条数据对多个模板，多个位置");//回调函数
    }
});
//兼容  单数据源 对 1个模板1个位置
multipleTpl({
    "data":data1,
    "sourcetpl":"#entry-template1",//1个模板
    "insertsit":"#temp1",//1个位置
    "insertmethod":"append",//1个插入方式
    "CallbackFun":function(args){
        console.log("CallbackFun:兼容  1条数据对 1个模板1个位置");//回调函数
    }
});
//insertmethod：append[不定义默认append],before,after;
*/
var multipleTpl=function(args){

    if(args.sourcetpl instanceof Array){
        for (var i = 0; i < args.sourcetpl.length; i++) {
            var curInsertMethod="";
            if(args.insertmethod!=undefined){
                if(args.insertmethod instanceof Array){
                    curInsertMethod=args.insertmethod[i];
                }else{
                    curInsertMethod=args.insertmethod;
                }
            }else{
                curInsertMethod="append";
            }
            creathtmlTpl({
                "data":args.data,
                "sourcetpl":args.sourcetpl[i],
                "insertsit":args.insertsit[i],
                "insertmethod":curInsertMethod
            })

        }
    }else{
        var curInsertMethod="";
        if(args.insertmethod!=undefined){
            curInsertMethod=args.insertmethod;
        }else{
            curInsertMethod="append";
        }
        creathtmlTpl({
            "data":args.data,
            "sourcetpl":args.sourcetpl,
            "insertsit":args.insertsit,
            "insertmethod":curInsertMethod
        })
    }
    if(args.CallbackFun){
        args.CallbackFun(args);
    }
}
/*handlebars生成模板 end*/
//serialize字符串转json
var strToObj=function (str){
    str = str.replace(/&/g,"','");
    str = str.replace(/=/g,"':'");
    str = "({'"+str +"'})";
    obj = eval(str);
    return obj;
}



/*兼容placeholder*/
function placeholderFun(){
        //判断浏览器是否支持placeholder属性
    var supportPlaceholder='placeholder'in document.createElement('input');
    if(!supportPlaceholder){
        $('[placeholder]').focus(function() {
          var input = $(this);
          if (input.val() == input.attr('placeholder')) {
            input.val('');
            input.removeClass('placeholder');
          }
        }).blur(function() {
          var input = $(this);
          if (input.val() == '' || input.val() == input.attr('placeholder')) {
            input.addClass('placeholder');
            input.val(input.attr('placeholder'));
          }
        });
        $('[placeholder]').each(function(index, el) {
          var input = $(this);
          if (input.val() == '' || input.val() == input.attr('placeholder')) {
            input.addClass('placeholder');
            input.val(input.attr('placeholder'));
          }
        });
        $('[placeholder]').parents('form').submit(function() {
          $(this).find('[placeholder]').each(function() {
            var input = $(this);
            if (input.val() == input.attr('placeholder')) {
              input.val('');
            }
          })
        });
    }

}

/*ajax 搜索提示*/
function ajaxSearchFun(args){
    var curEventEle=null;
    $(args.eventEle).on("keyup",function(event){
      curEventEle=$(this);
      if(!$(this).data("oldval")){
        $(this).data("oldval","");
      }
      if($(this).val()!=$(this).data("oldval")){
        $(this).data("oldval",$(this).val());
        clearTimeout($(this).data("timeoutkey"));
        var timeoutKey = setTimeout(function(t){
          return function(){
            var ajaxType= args.ajaxType ? args.ajaxType :'GET';
            var ajaxDataType= args.ajaxDataType ? args.ajaxDataType :"json";
            var postDataObj={"kw":$(t).val()};
            if(args.postDataObj){
                postDataObj= args.postDataObj.call(null)
            }
            $.ajax({
              url:args.promptUrl,
              type:ajaxType,
              dataType:ajaxDataType,
              data:postDataObj,
              success:function(data){
                if(args.ajaxSuccessCall!=undefined){
                    var SuccessCall=eval(args.ajaxSuccessCall);
                    SuccessCall.call(null,{"eventEle":curEventEle,"data":data,'t':t,'FunArgs':args});//当前函数名
                }else{
                    if(data.data!=undefined && data.data.length>0){
                      var searchResultDiv = $("#searchResultDiv");
                      searchResultDiv.css({
                        left:$(t).offset().left+"px",
                        top:($(t).offset().top+$(t).outerHeight())+"px",
                        width:parseInt($(t).outerWidth()+2)+"px"
                      })
                      searchResultDiv.show();
                      searchResultDiv.html("");
                      //数据
                      var curdata=data.data;
                      if  (curdata.length != false) {
                          ga('send','event','index','ajax_complete');
                      }
                      for(var i=0;i<curdata.length;i++){
                        searchResultDiv.append($("<div class='searchResultItem' onclick=\"ga('send','event','index','search_result')\">"+curdata[i]+"</div>"));
                      }
                      searchResultDiv.data("linksearch",$(t));
                    }
                }
              }
            })
          }
        }(this),10);
        $(this).data("timeoutkey",timeoutKey);
      }else{
        var d = 0;
        switch(event.which){
          case 38:
            d--;
            var currentIdx = 0;
            break;
          case 40:
            d++;
            var currentIdx = -1;
            break;
          case 13:
            clearTimeout($(this).data("timeoutkey"));
            $("#searchResultDiv").data("linksearch",$(this));
                searchSelect();
                return true;
            }

            var all = 0;
            $("#searchResultDiv").find(".searchResultItem").each(function(idx,ele){
              if($(ele).hasClass("cur")){
                currentIdx = idx;
                $(ele).removeClass("cur");
              }
              all++;
            });
            if(all!=0){
              currentIdx+=d;
              currentIdx%=all;
            }
            if(d!=0){
                $("#searchResultDiv .searchResultItem:eq("+currentIdx+")").addClass('cur');
            }


      }
    })
    $(args.eventEle).on("blur",function(event){
      clearTimeout($(this).data("timeoutkey"));
      if($(this).data("cancelblur")!="true"){
        $("#searchResultDiv").hide();
        $("#searchResultDiv").data("linksearch",null);
      }
    })
    $("<div id='searchResultDiv' style='position:absolute;border:1px solid #f0f1f6;display:none'></div>").appendTo("body");
    $("#searchResultDiv").on("mouseover",".searchResultItem",function(){
      //$(this).closest("#searchResultDiv").find(".searchResultItem").removeClass('cur');
      //$(this).addClass('cur');
      $("#searchResultDiv").data("linksearch").data("cancelblur","true");
    });
    $("#searchResultDiv").on("mouseout",".searchResultItem",function(){
      var linkSearch = $("#searchResultDiv").data("linksearch");
      if(linkSearch!=null){
        $("#searchResultDiv").data("linksearch").data("cancelblur","false");
      }
    })
    $("#searchResultDiv").on("click",".searchResultItem",function(){
        $(this).closest("#searchResultDiv").find(".searchResultItem").removeClass('cur');
        $(this).addClass('cur');
        searchSelect();
    });
    function searchSelect(){
      var linkSearch = $("#searchResultDiv").data("linksearch");
      if(linkSearch!=null){
          linkSearch.data("cancelblur","false");
          linkSearch.trigger('blur');
          if($("#searchResultDiv .cur").length!=0){
              if(args.onconfirmFun!=undefined){
                var confirmCall=eval(args.onconfirmFun);
                confirmCall.call(null,{"eventEle":curEventEle});//当前函数名
              }else{
                linkSearch.val($("#searchResultDiv .cur").html());
              }
          }
      }
      if(args.searchCallback!=undefined){
        var searchCall=eval(args.searchCallback);
        searchCall.call(null,{"eventEle":curEventEle,"postData":linkSearch.val()});//当前函数名
      }
    }
  }

//ajax 搜索提示 data
//data： {"data":["php\u4e2d\u7ea7\u7a0b\u5e8f\u5458","php\u540e\u53f0\u5de5\u7a0b\u5e08","php\u5f00\u53d1\u5de5\u7a0b\u5e08","php\u7a0b\u5e8f\u5458","php\u9ad8\u7ea7\u7a0b\u5e8f\u5458"],"status":1}

// 调用
//ajaxSearchFun({
//  "eventEle":".ajaxSearch",
//  "promptUrl":"select_ajax_test2.json",
//  "searchCallback":function(args){
//      //{"eventEle":"eventEle","postData":"postData"}
//      console.log(args);
//      $.ajax({
//          url:"select_ajax_test2-2.json",
//          type:"POST",
//          data:args.postData,
//          success:function(data){
//            console.log("搜索结果:"+args.postData);
//            console.log(args.eventEle);
//          }
//      });
//  }
//});


//select_checkbox 左右选择 组件
function selectCheckboxFun(){
    this.selAdd();
    this.selRemove();
    this.selCheckbox();
}
selectCheckboxFun.prototype={
    eleP:null,
    selAdd:function(){
        var _this=this;
        $('body').off('click','.sel_add');
        $('body').on('click','.sel_add',function(){
            _this.eleP=$(this).closest('.select_checkbox');
            var selTextarea=$('.sel_textarea .form-control',_this.eleP);
            var addVal=$(selTextarea).val();
            var addName=$(selTextarea).attr('addName');
            if(addVal.length>0){
                addVal=addVal.split('\n');
                console.log(addVal);
                for(var i=0; i<addVal.length; i++){
                    $('.sel_checkbox',_this.eleP).prepend(_this.htmlTplFun({'addVal':addVal[i],'addName':addName}));
                }
                //var scrollH=$('.sel_checkbox',_this.eleP)[0].scrollHeight;
                //$('.sel_checkbox',_this.eleP).stop().animate({scrollTop: scrollH}, 300);
                $(selTextarea).val('');
            }else{
                alert('请先填写左测内容');
            }
        });
    },
    htmlTplFun:function(args){
        var html=[];
        html.push('');
        html.push('<div class="sel_checkbox_li cur">');
        html.push(args.addVal);
        html.push('<span class="h0hidden"><input type="checkbox" name="'+args.addName+'" checked="checked" value="'+args.addVal+'"></span>');
        html.push('</div>');
        return html.join('');
    },
    selRemove:function(){
        var _this=this;
        $('body').off('click','.sel_remove');
        $('body').on('click','.sel_remove',function(){
            _this.eleP=$(this).closest('.select_checkbox');
            var activeArr=$('.sel_checkbox .active',_this.eleP);
            if(activeArr.length>0){
                $(activeArr).remove();
            }else{
                alert('请先填写左测内容');
            }
        });
    },
    selCheckbox:function(){
        $('body').off('click','.sel_checkbox_li');
        $('body').on('click','.sel_checkbox_li',function(){
            $(this).toggleClass('active');
        });
    }
}
/*proxySelect 模拟Select start*/
/*
//html 代码
<div class="proxy_select"><i></i>
    <input class="proxy-txt form-control control-sm bor-c-green w-100" placeholder="职位"  type="text" readonly value="">
    <input class="proxy-val" placeholder=""  type="hidden"  value="">
    <ul class="option_group">
        <li val="1">公司1</li>
        <li val="2">公司2</li>
        <li val="3">公司3</li>
        <li val="4">公司4</li>
        <li val="5">公司5</li>
        <li val="6">公司6</li>
        <li val="7">公司7</li>
        <li val="8">公司8</li>
        <li val="9">公司9</li>
        <li val="10">公司10</li>
        <li val="11">公司11</li>
        <li val="12">公司12</li>
    </ul>
</div>
//模拟Select
proxySelectFun();
*/
function proxySelectFun(){
    function Selhtml(selOjb){

        var eventCode= $('select',selOjb).attr('eventCode');
        if(eventCode!=undefined){
            eventCode='onclick="'+eventCode+'"';
        }else{
            eventCode='';
        }
        var options=$('select option',selOjb);
        var selectedTxt=$('select option:selected',selOjb).text();
        var selectedVal=$('select option:selected',selOjb).val();
        var placeholder="";
        if($(selOjb).attr("placeholder")!=""&&$(selOjb).attr("placeholder")){
            placeholder=$(selOjb).attr("placeholder");
        }else{
            if($(options[0]).val()==""){
                placeholder=$(options[0]).text();
            }
        }
        if(selectedVal==""){
            selectedTxt="";
        }
        if(!selectedVal){
            selectedVal="";
        }
        var html = [];
        html.push('');
        html.push('<input class="proxy-txt form-control js_vali_agent js_no_error" placeholder="'+placeholder+'"  type="text"  value="'+selectedTxt+'" readonly>');
        html.push('<input class="proxy-val" type="hidden"  value="'+selectedVal+'">');
        html.push('<ul class="option_group">');
        for(var i=0; i<options.length; i++){
            if($(options[i]).val()!=""){
                if($(options[i]).val()==selectedVal){
                    html.push('    <li '+eventCode+' class="cur"  val="'+$(options[i]).val()+'">'+$(options[i]).text()+'</li>');
                }else{
                    html.push('    <li  '+eventCode+' val="'+$(options[i]).val()+'">'+$(options[i]).text()+'</li>');
                }
            }
        }
        html.push('</ul>');
        return html.join('');
    }
    var zIndex=1000;
    $('.proxy_select').each(function(index, el) {
        var proxySelect=$(this);

        $(proxySelect).css({"z-index":zIndex});
        zIndex--;
        if($(".proxy-txt",proxySelect).length==0){
            $(".proxy_sel_hide",proxySelect).before(Selhtml(proxySelect));
            //取消滚动冒泡事件
            $(".proxy_select .option_group").preventScroll();
             //placeholder
             placeholderFun();
        }
        var proxyTxtObj=$(".proxy-txt",proxySelect);
        var proxyValObj=$(".proxy-val",proxySelect);

        var selectValue=$('select',proxySelect).attr("selectValue");
        if(selectValue&&selectValue!=""){
            var selectText=$('select option:selected',proxySelect).text();
        }else{
            var selectText="";
        }
        $(proxyTxtObj).val(selectText);
        $(proxyValObj).val(selectValue);
        //样式
        $(".option_group",proxySelect).css({
            "border":'1px solid '+$(proxyTxtObj).css("border-color"),
            "width":$(proxyTxtObj).outerWidth()
        })
        if($(proxySelect).attr("showState")=='hide'){
           // $(proxySelect).css({"display":"none"});
        }
    });
    $("body").off('click', '.proxy_select .proxy-txt');
    $("body").on('click', '.proxy_select .proxy-txt', function(event) {
        var proxySelect=$(this).closest('.proxy_select');
        $(proxySelect).removeClass("proxy-un");
        $(".proxy-un .option_group").css({"display":"none"});
        var proxyTxtObj=$(".proxy-txt",proxySelect);
        var proxyValObj=$(".proxy-val",proxySelect);
        var aniTime=1;
        //默认值
        var curProxyVal =$(proxyValObj).val();
        if(curProxyVal!=""){
            $(".option_group li",proxySelect).removeClass("cur");
            $('.option_group li[val="'+curProxyVal+'"]',proxySelect).addClass("cur");
        }
        $(this).toggleClass("arrow-up");
        if($(".option_group li",proxySelect).length==0){
            return;
        }
        //slideToggle
        $(".option_group",proxySelect).slideToggle(aniTime,function(){
            var animSelVal=$('.proxy-val',proxySelect).val();
            var selectScrollTop=$('.option_group li[val="'+animSelVal+'"]',proxySelect)>0 ? $('.option_group li[val="'+selectValue+'"]',proxySelect).position().top-20 : 0;
            $('.option_group',proxySelect).scrollTop(selectScrollTop);
        });
        $(".option_group li",proxySelect).off("click");
        $(".option_group li",proxySelect).on("click",function(event){
            var proxyTxt=$(this).text();
            var proxyVal=$(this).attr("val");
            $(proxyTxtObj).val(proxyTxt);
            $(proxyValObj).val(proxyVal);
            var curselOjb=$(this).closest('.proxy_select');
            $('select',curselOjb).val(proxyVal);
            $(".option_group",curselOjb).slideUp(aniTime);
            $(".proxy-txt",curselOjb).removeClass("arrow-up");
            $(".proxy-txt",curselOjb).removeClass("placeholder");
            //js_validate验证
            $(".js_no_error",curselOjb).removeClass("no_error");
            //代理验证
            if( typeof agentValidate === 'function'){
                agentValidate({
                    "valiEle":$('select',curselOjb),
                    "agentEle":$(".proxy-txt",curselOjb)
                });
            }
            //onchange 回调
            $('select',curselOjb).trigger('change');
/*            var onchangeCall=$('select',curselOjb).attr('onchange');
            if(onchangeCall){
                onchangeCall=eval(onchangeCall);
            }*/
        });
    });
    $("body").off('blur','.proxy_select .proxy-txt');
    $("body").on('blur','.proxy_select .proxy-txt', function(event) {
        var proxySelect=$(this).closest('.proxy_select');
        $(proxySelect).addClass("proxy-un");
    });
    $("body").click(function(event){
        var proxy_select=$(event.target).closest('.proxy_select').length;
        var curselOjb=$(event.target).closest('.proxy_select');
        if(proxy_select==0){
           $(".proxy-un .option_group").css({"display":"none"});
        }
    })
}

 /*proxySelect 模拟Select end*/
/*模拟 radio checkbox  样式  注意label 的for属性 与  radio checkbox  一一对应； start*/
/*
//checkbox
<div class="proxyinput_group">
    <label class="proxyinput">
        <span class="h0hidden"><input type="checkbox" name="checkbox1" checked="checked"></span>张丰丰
    </label>
    <label class="proxyinput">
        <span class="h0hidden"><input type="checkbox" name="checkbox1" value="2"></span>张丰丰
    </label>
    <label class="proxyinput">
        <span class="h0hidden"><input type="checkbox" name="checkbox1" value="3"></span>张丰丰
    </label>
</div>
//radio
<div class="proxyinput_group">
    <label class="proxyinput " for="sex_m">
         <span class="h0hidden"><input class="js_validate" type="radio" name="sex" id="sex_m" value="M"></span>男
    </label>
    <label class="proxyinput" for="sex_f">
        <span class="h0hidden"><input type="radio" name="sex" id="sex_f" value="F" checked="checked"></span>女
    </label>
</div>
*/
function proxyInput(){
    $('.proxyinput [type="radio"]').each(function(index, el) {
        if($(this).prop("checked")){
            var proxyinput=$(this).closest('.proxyinput');
            var radioArr=$(this).closest('.proxyinput_group');
            $('.proxyinput',radioArr).removeClass('checked');
            $(proxyinput).addClass('checked');
        }

    });
    $('.proxyinput [type="radio"]').off('click');
    $('.proxyinput [type="radio"]').on('click', function(event) {
        var proxyinput=$(this).closest('.proxyinput');
        var radioArr=$(this).closest('.proxyinput_group');
        if($(radioArr).hasClass('radiocancel')){
            //可取消radio radiocancel
            if($(proxyinput).hasClass('checked')){
                $('.proxyinput',radioArr).removeClass('checked');
                $(this).prop('checked',false);
            }else{
                $('.proxyinput',radioArr).removeClass('checked');
                $(proxyinput).addClass('checked');
            }
        }else{
            //普通radio
            $('.proxyinput',radioArr).removeClass('checked');
            $(proxyinput).addClass('checked');
        }

    });

    $('.proxyinput [type="checkbox"]').each(function(index, el) {
        if($(this).prop("checked")){
            var proxyinput=$(this).closest('.proxyinput');
            $(proxyinput).addClass('checked');
        }

    });
    /*.proxyinput_group 可以设置 maxlength="3"*/
    $('.proxyinput [type="checkbox"]').off('click');
    $('.proxyinput [type="checkbox"]').on('click', function(event) {
        var checkboxArr=$(this).closest('.proxyinput_group');
        var proxyinput=$(this).closest('.proxyinput');

        var maxselectcount=$(checkboxArr).attr('maxselectcount');
        if($(this).prop("checked")){
            if(maxselectcount){
                maxselectcount=parseInt(maxselectcount);
                var checkCount=$('.proxyinput [type="checkbox"]:checked',checkboxArr).length;
                if(checkCount>maxselectcount){
                    $(this).prop("checked",false);
                    //小提示层;
                    validatePop({
                        "popconMsg":'最多选择'+maxselectcount+'个'
                    });
                }else{
                    $(proxyinput).addClass('checked');
                }
            }else{
                $(proxyinput).addClass('checked');
            }
        }else{
            $(proxyinput).removeClass('checked');
        }
    });

}
/*模拟 radio checkbox  样式 end*/

/*小提示层 validatePop start*/
/*
    //小提示层;
    validatePop({
        "eventEle":"#a1",//点击事件元素（不定义：立即弹出）
        "popconMsg":"成功",//Msg
        "popCallbackFun":function(args){
            //自动关闭时的操作
            console.log(args);
        }
    });
*/
var validatePop=function(args){
    var popup=function(args){
        if($(".validatePop").length>0){
            $(".validatePop").remove();
        }
        var validatePop='<div class="validatePop">'+args.popconMsg+'</div>';
        $("body").append(validatePop);
        var validatePopW=$(".validatePop").width()+parseFloat($(".validatePop").css('padding-left'))+parseFloat($(".validatePop").css('padding-right'));
        var validatePopH=$(".validatePop").height()+parseFloat($(".validatePop").css('padding-top'))+parseFloat($(".validatePop").css('padding-bottom'));
        $(".validatePop").css({"opacity": 0,"left":"50%","top":"50%","margin": "-"+(validatePopH/2)+"px 0 0 -"+(validatePopW/2)+"px"});
        $(".validatePop").stop().animate({"opacity": 1},350,function() {
            setTimeout(function(){
                if($(".validatePop").length>0){
                    $(".validatePop").fadeOut(100, function() {
                        if(args.popCallbackFun){
                            args.popCallbackFun(args);
                        }
                        $(this).remove();

                    });
                }
            },500);
        });
    }
    if(args.eventEle){
        $(args.eventEle).on("click",function(){
            args.eventEle=$(this);
            popup(args);
        });
    }else{
        popup(args);
    }
}
/*小提示层 validatePop end*/
/*popsel end*/


//animFun animated css3动画调用
/*
    animCss3Fun({
      "animObj":".animationsbox",//动画对象 class
      "animOption":"bounceInLeft",//动画方式
        "CallbackFun":function(animArgs){
            if(args.animCallbackFun){
                args.animCallbackFun(args);
            }
        }
    });
*/
function animCss3Fun(args) {
    $(args.animObj).removeClass("hidden").addClass(args.animOption+" animated").one('webkitAnimationEnd mozAnimationEnd MSAnimationEnd oanimationend animationend',function(){
        $(this).removeClass(args.animOption+" animated block");
        if(args.CallbackFun){
            args.CallbackFun(args);
        }
    });
}

//取消滚动冒泡事件
$.fn.extend({
    "preventScroll":function(){
        $(this).each(function(index, el) {
            var _this=this;
            $(this).scroll(function (event) {
                var self=this;
                var h=$(this).height();
                var st=this.scrollTop;
                var sh=this.scrollHeight;

                //console.log('h:'+ h+';st:'+ st+';sh:'+sh);
                function dwfDefaultFun(e){
                    e.preventDefault();
                }
                if(navigator.userAgent.indexOf('Firefox') >= 0){
                     //firefox
                     function dwfMouseScrollFun(e){
                        //top
                        if(st<=0&&e.detail<0){
                            //console.log("t");
                            e.preventDefault();
                        }else{
                            //bottom
                            if((h+st)>=sh&&e.detail>0){
                                //console.log("b");
                                e.preventDefault();
                            }else{
                                if (document.removeEventListener) {
                                    _this.removeEventListener('DOMMouseScroll', dwfMouseScrollFun, false);
                                } else {
                                    _this.detachEvent('DOMMouseScroll', dwfMouseScrollFun);
                                }
                            }
                        }

                     }

                    _this.addEventListener('DOMMouseScroll',dwfMouseScrollFun,false);
                }else{
                    _this.onmousewheel = function(e){
                        //console.log(e.wheelDeltaY);
                        e = e || window.event;
                        //top
                        if(st<=0&&e.wheelDeltaY>0){
                            return false;
                        }else{
                            //bottom
                            if((h+st)>=sh&&e.wheelDeltaY<0){
                                return false;
                            }
                        }

                    };
                }
            });

        });
    }
});
//取消滚动冒泡事件
$.fn.extend({
    "preventWheel":function(){
        $(this).each(function(index, el) {
            var _this=this;
            if(navigator.userAgent.indexOf('Firefox') >= 0){
                 //firefox
                 function dwfMouseScrollFun(e){
                    e.preventDefault();
                 }
                _this.addEventListener('DOMMouseScroll',dwfMouseScrollFun,false);
            }else{
                _this.onmousewheel = function(e){
                    //console.log(e.wheelDeltaY);
                    e = e || window.event;
                    //top
                    return false;
                };
            }
        });
    }
});




/*cookie start*/

function setCookie_g(name,value,expiredays){
    var exdate=new Date()
    exdate.setDate(exdate.getDate()+expiredays)
    document.cookie=name+ "=" +escape(value)+
    ((expiredays==null) ? "" : ";expires="+exdate.toGMTString())
}
function getCookie_g(name){
    if (document.cookie.length>0)
      {
      start=document.cookie.indexOf(name + "=")
      if (start!=-1)
        {
        start=start + name.length+1
        end=document.cookie.indexOf(";",start)
        if (end==-1) end=document.cookie.length
        return unescape(document.cookie.substring(start,end))
        }
      }
    return ""
}
//删除cookies
function delCookie_g(name){
    var exp = new Date();
    exp.setTime(exp.getTime() - 1);
    var cval=getCookie_g(name);
    if(cval!=null&&cval!='') document.cookie= name + "="+cval+";expires="+exp.toGMTString();
}
//列子
/*function checkCookie(){
  username=getCookie_g('username')
  if (username!=null && username!="")
    {alert('Welcome again '+username+'!')}
  else
    {
    username=prompt('Please enter your name:',"")
    if (username!=null && username!="")
      {
      setCookie_g('username',username,365)
      }
    }
}*/

/*cookie end*/

//是否存在指定函数
function isExitsFunction(funcName) {
    try {
        if (typeof(eval(funcName)) == "function") {
            return true;
        }
    } catch(e) {}
    return false;
}
//是否存在指定变量
function isExitsVariable(variableName) {
    try {
        if (typeof(variableName) == "undefined") {
            //alert("value is undefined");
            return false;
        } else {
            //alert("value is true");
            return true;
        }
    } catch(e) {}
    return false;
}
//moreInitOperFun 展开更多
function moreInitOperFun(){
    $('.js_moreOper').each(function(index, el) {
        var initOperLt=parseInt($(this).attr('initOper'));
        var initOperGt=initOperLt-1;
        var moreOper=$(this);
        var operCell=$(this).attr('operCell');
        var operList=$(this).attr('operList');
        if($(operList+' '+operCell,moreOper).length>initOperLt){
            $('.js_btn_down',moreOper).removeClass('hidden');
        }
        $(operList+' '+operCell+':lt('+initOperLt+')',moreOper).removeClass('hidden');
        //展开
        $('.js_btn_down',moreOper).off('click');
        $('.js_btn_down',moreOper).on('click', function(event) {
            $(this).addClass('hidden');
            $(operList+' '+operCell+'',moreOper).removeClass('hidden');
            $('.js_btn_up',moreOper).removeClass('hidden');
        });
        //收起
        $('.js_btn_up',moreOper).off('click');
        $('.js_btn_up',moreOper).on('click', function(event) {
            $(this).addClass('hidden');
            $(operList+' '+operCell+':gt('+initOperGt+')',moreOper).addClass('hidden');
            $('.js_btn_down',moreOper).removeClass('hidden');
        });
    });

}