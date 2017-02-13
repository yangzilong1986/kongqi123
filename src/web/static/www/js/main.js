var windowW;
var windowH;
var currentNum = 0;
var totalNum;
var interval;
var currentEvtNum = 0;
var evtNum;
var interval2;
var countNum = 0;
var scrollPosition = [ "0" , "700" , "2100" ];    // html , body scrollTop의 값

$(function()
{
	$(window).resize ( function ()
	{	
		windowW = $(window).width();
		windwH = $(window).height();

		//Main_visual
		$(".visual li").each(function(i)
		{	
			$(this).css ( { left:windowW * i } );
		});
		$(".visual").stop().css( { width:windowW*5, left:-currentNum*windowW } );
		$(".roll").stop().css( {width:windowW } );
		$(".visual li").stop().css( {width:windowW } );

		//Event
		$(".evt_lst li").each(function(i)
		{	
			$(this).css ( { left:windowW * i } );
		});
		$(".evt_lst").stop().css( { width:windowW*5, left:-currentEvtNum*windowW } );
		$(".evt_box").stop().css( {width:windowW } );
		$(".evt_lst li").stop().css( {width:windowW } );

		$(".mov").find("a").each(function(i)
		{
			$(this).bind( "click" , movPopStart );
		});
		
		resizeImages();

	}).resize();

	function movPopStart()
	{
		clearTimeout ( interval );
	}
	
	function resizeImages()
	{
		var ratio1 = 1920/960;
		var ratio2 = 960/1920;

		var ww = parseInt(windowW);
		var hh = parseInt(windwH * ratio1);

		if ( ww > hh )
		{
			ww = windowW;
			hh = windowW * ratio2;
		}
		else
		{
			ww = windwH * ratio1;
			hh = windwH;
		}

	}

	totalNum = $(".visual").find("li").length;
	evtNum = $(".evt_lst").find("li").length;

	for ( var i = 0; i < totalNum; i++ )
	{
		$(".btn_area").append ( '<a href="javascript:bltwrap()"><img src="../images/common/btn/btn_bn_off.png" /></a>' );
	}
//	moveBanner();
	moveEvent();
	bltwrap();
});

function btnLft()
{
	currentNum--;
	
	if( currentNum < 0 )
	{
		currentNum = 0;
	}
//	moveBanner();
}

function btnRgt()
{
	currentNum++;

	if( currentNum > totalNum-1 )
	{
		currentNum = totalNum-1
	}
	
//	moveBanner();
}

function bltwrap()
{
	$(".btn_area a").click ( pageMove );
}

function pageMove(element)
{
	currentNum = $(element).index();
//	moveBanner();
}

function pageAutoCount()
{
	currentNum++;
//	moveBanner();
}

/*
function moveBanner()
{
	if ( currentNum < 0 ) currentNum = totalNum-1;
	if ( currentNum > totalNum-1 ) currentNum = 0;

	$(".btn_area a").each ( function (i)
	{
		if ( i == currentNum )
		{
			$(this).find("img").attr("src" , "../images/common/btn/btn_bn_on.png");
		}
		else
		{
			$(this).find("img").attr("src" , "../images/common/btn/btn_bn_off.png");
		}
	});	
	
	if( currentNum == 0 )
	{
		$(".visual").stop().animate ( { left:-currentNum * windowW } );
		clearTimeout ( interval );
		interval = setTimeout ( pageAutoCount , 10000 );
	}

	else
	{
		$(".visual").stop().animate ( { left:-currentNum * windowW } );
		clearTimeout ( interval );
		interval = setTimeout ( pageAutoCount , 3500 );
	}
	
	
}
*/

function moveEvent()
{

	$(".evt_lst").stop().animate ( { left:-currentEvtNum * windowW } );	

	currentEvtNum++;
	
	if ( currentEvtNum > evtNum-1 ) currentEvtNum = 0;
	clearTimeout ( interval2 );
	interval2 = setTimeout ( moveEvent , 3500 );
}

/////////////////////////////////////////////////////////////////////////////
// 추가 150701~
var duration = 400;
var motionFlag = false;
var currentIndex = 0;
var tartgetIndex = 0;
var currentBanner;
var targetBanner;

var selectedIndex = 0;

var BANNER_WIDTH = 291;
var SPEED = 500;
var banner_length;
var selectedBanner;
var $selectedIndicator;
var rollingTimer;

$(document).ready(setupRolling);

//$(".indicator").css("background", "url('/images/common/main/navigation_n.png')");

function setupRolling(){
    init();
    rollingTimer = setInterval(changeBanner, 3000);
    $("#indicator_area div").bind("mouseenter", mOverIndicator);
    $("#indicator_area div").bind("mouseleave", autoRolling);
}

function init(){
    banner_length = $("#phone_banner").children("img").length;
//    banner_length = $("#phone_banner").children("div").length;
    $("#phone_banner").width(banner_length*BANNER_WIDTH);
    selectedBanner = 0;
    changeIndicator();
    rollingTimer = 0;            
}

function autoRolling(){
    rollingTimer = setInterval(changeBanner, 3000);
}      

function mOverIndicator(e){
    clearInterval(rollingTimer);
    rollingTimer = 0;
    $(".indicator").css("background","url(images/navigation_n.png) center no-repeat");
    $selectedIndicator = $(e.target);
    $selectedIndicator.css("background","url(images/navigation_p.png) center no-repeat");
    selectedBanner = $selectedIndicator.index();
    
    showBanner();
}

function changeIndicator(){
	$(".indicator").css("background","url(images/navigation_n.png) center no-repeat");
    $selectedIndicator = $("#indicator_area div:eq("+selectedBanner+")");
    $selectedIndicator.css("background","url(images/navigation_p.png) center no-repeat");
}

function showBanner(){
	$("#text_banner").children().hide();
	$($("#text_banner").children()[selectedBanner]).show();
	
    var mPosition = selectedBanner*BANNER_WIDTH*-1;
    
    
    //$("#phone_banner").css("left",mPosition);
    selectedBanner = (selectedBanner+1)%banner_length;
    $("#phone_banner").stop();
    $("#phone_banner").animate({left: mPosition}, SPEED, "easeOutQuint");
}

function changeBanner(){
    changeIndicator();
    showBanner();
}

function showPopupCommingsoonKo() {
	openModalPopup("pop_commingsoon_ko.html" , 1000, 600 ,false );
}

function showPopupCommingsoonEn() {
	openModalPopup("/pop_commingsoon_en.html" , 1000, 600 ,false );
}

//bannerTimer = setInterval(bannerSlideRight, 3000);

// 추가 150701~
/////////////////////////////////////////////////////////////////////////////
