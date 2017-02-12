$(document).ready(function() {
        $('#fullpage').fullpage({
            'verticalCentered': false,
            'css3': true,
            'navigation': true,
            'navigationPosition': 'right',
            //'scrollingSpeed': 500,
            'afterLoad': function(anchorLink, index){
                var winH=$(window).height();
                var headH=$(".head-wrap").height();
                var headT=winH-headH;
                var headCW=$(".head-wrap .wrap").width();
                var goML=(headCW-56)/2;
                if(index==1){
                    $(".head-wrap,.head").css({"top":headT+"px"});
                    $("#fp-nav").addClass("h0hidden");
                    $(".btn-go-top").addClass("hidden");
                    $(".go-down,.go-up").css({"margin-right":"-"+goML+"px"});
                    if($("#fp-nav .page_next").length==0){
                        $("#fp-nav ul").before('<i class="page_prve"></i>');
                        $("#fp-nav ul").after('<i class="page_next"></i>');
                    }
                }
                /* #section4*/
                var s3PT=winH*0.19;
                $("#section3 .wrap").css({"padding-top":s3PT+"px"});
                /*#section4 */
                var s4PT=winH*0.14;
                $("#section4 .wrap").css({"padding-top":s4PT+"px"});
                /*#section5 */
                var s5PT=winH*0.16;
                $("#section5 .wrap").css({"padding-top":s5PT+"px"});
                //.btn-go-top 事件
                $(".btn-go-top").off('click');
                $(".btn-go-top").on('click',function(event) {
                    $('#fp-nav ul li:eq(0) a').trigger('click');
                });
                //.go-down 事件
                $(".go-down").off('click');
                $(".go-down").on('click',function(event) {
                    $('#fp-nav ul li:eq(1) a').trigger('click');
                });
                //.go-up 事件
                $(".go-up").off('click');
                $(".go-up").on('click',function(event) {
                    $('#fp-nav ul li:eq(0) a').trigger('click');
                });
                //.ico-more 事件
                $("#section2 .ico-more").off('click');
                $("#section2 .ico-more").on('click',function(event) {
                    $('#fp-nav ul li:eq(2) a').trigger('click');
                });
                //.page_next 事件
                $("#fp-nav .page_next").off('click');
                $("#fp-nav .page_next").on('click',function(event) {
                    var curLi=$('#fp-nav ul li a.active').closest('li');
                    var nextIndex=curLi.index()+1;
                    $('#fp-nav ul li:eq('+nextIndex+') a').trigger('click');
                });
                //.page_next 事件
                $("#fp-nav .page_prve").off('click');
                $("#fp-nav .page_prve").on('click',function(event) {
                    var curLi=$('#fp-nav ul li a.active').closest('li');
                    var prveIndex=curLi.index()-1;
                    $('#fp-nav ul li:eq('+prveIndex+') a').trigger('click');
                });

                /*section3 section4 section5 anim */
                if(index==3||index==4||index==5){
                    var anim1="#section"+index+" .anim-p-1";
                    var anim2="#section"+index+" .anim-p-2";
                    animCss3Fun({
                        "animObj":anim1,//动画对象 class
                        "animOption":"slideInUp",//动画方式
                        "CallbackFun":function(animArgs){
                            animCss3Fun({
                                "animObj":anim2,//动画对象 class
                                "animOption":"zoomIn"
                            });
                        }
                    });
                }
            },
            'onLeave': function(index, nextIndex, direction){
                var winH=$(window).height();
                var headH=$(".head-wrap").height();
                var headT=winH-headH;

                if(nextIndex==1){
                    $(".head-wrap,.head").css({"top":headT+"px"});
                    $("#fp-nav").addClass("h0hidden");

                    $(".go-down").removeClass("hidden");
                    $(".go-up").addClass("hidden");
                }
                if(nextIndex==2){
                    $(".head-wrap,.head").css({"top":"0px"});
                    $("#fp-nav").removeClass("h0hidden");

                    $(".go-down").addClass("hidden");
                    $(".go-up").removeClass("hidden");
                }
                if(nextIndex>2){
                    $(".go-down").addClass("hidden");
                    $(".go-up").addClass("hidden");
                    $(".btn-go-top").removeClass("hidden");
                }else{
                    $(".btn-go-top").addClass("hidden");
                }
                if(nextIndex==7){
                    $(".footer").css({"position":"fixed","bottom":"0px"});
                }else{
                    $(".footer").css({"position":"","bottom":""});
                }
                /*section4 section5 section6 anim */
                if(nextIndex!=3){
                    $("#section3 .anim-p-1").addClass("hidden");
                    $("#section3 .anim-p-2").addClass("hidden");
                }
                if(nextIndex!=4){
                    $("#section4 .anim-p-1").addClass("hidden");
                    $("#section4 .anim-p-2").addClass("hidden");
                }
                if(nextIndex!=5){
                    $("#section5 .anim-p-1").addClass("hidden");
                    $("#section5 .anim-p-2").addClass("hidden");
                }
            }
        });

    });
$(window).resize(function(){
    location.reload();
});