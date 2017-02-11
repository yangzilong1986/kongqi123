$(document).ready(function() {
    //字符时时统计
    countStrCheck(); 	
});

/*
//publish_demand_form 验证 说明  
PublishFormCheck({
    "formId":"#demand_userinfo_form",//form id
    "parentEleTagName":".li",//提示语append位置
    "errorMethod":"validatePop",//可选项  第一个条目报错 用小层弹出 3秒后消失 
    "validateOption":{
       "user_name":{
          "requiredCheck":{"msg":"必填项不能为空"},//必填项不能为空 必选项必须选择一项

          "lengthCheck":{"rangelength":[5,10,"字符个数必须大于5小于10"]},//长度区间 
          "lengthCheck":{"maxlength":[10,"最大不能超过10个字符"]},//最大长度
          "lengthCheck":{"minlength":[10,"最小不能少于10个字符"]},//最小长度

          "digitsCheck":{"msg":"只能输入整数且大于0"},//整数 验证

          "emailCheck":{"rangelength":[5,10,"邮箱个数必须大于5小于10"]},//长度区间 邮箱
          "emailCheck":{"maxlength":[10,"最大不能超过10个邮箱"]},//最大长度 邮箱
          "emailCheck":{"minlength":[10,"最小不能少于10个邮箱"]},//最小长度 邮箱

          "phoneCheck":{"msg":"你输入的手机号码不正确"},//你输入的手机号码不正确
          "noPhoneCheck":{"msg":"输入内容不能含手机电话"},//输入内容不能含手机电话

          "usernameCheck":{"msg":"账号格式有误，请输入正确的邮箱或手机号!"},//必须是邮箱或手机号

          "passwordCheck":{"msg":"6-16个字符，不能有空格!"},//6-16个字符，不能有空格!

          "httpCheck":{"msg":"请输入含“http”的正确网址！"},//请输入含“http”的正确网址！

          "ajaxCheck":{
            "ajaxFun":{
                  url: "../ajax/ajaxCheck_error.html",
                  type: 'POST',                   
                  data:{
                    "username":function(){return $("#username").val();},
                    "password":function(){return $("#password").val();}
                  },
                  success:function(data){
                    if(data!="true"){
                      var msg="报错内容";
                      return msg;
                    }
                  },//可选项
            		msg:'fafrar'//可选项
              }
          }

       },
       "mobile_phone":{
           "requiredCheck":{},
           "phoneCheck":{}
       },
       "mobile_code":{
           "requiredCheck":{}
       }
    },
    "submitType":"ajax",//ajax 提交方式（ 表单 post get方式 均不需要该项）
    "ajaxFun":function(args){//ajax 提交方式（ 表单 post get方式 均不需要该项）
        var ajaxUrl=$("#js_demand_userinfo_submit").attr("ajaxUrl");
        $.ajax({
            url: ajaxUrl,
            type: 'GET',
            dataType: 'json',
            data:$(args.formId).serialize(),
            beforeSend: function () {                           
                $("#js_demand_userinfo_submit").prop("disabled",true);
            },
            success: function(data){
                $("#js_demand_userinfo_submit").prop("disabled",false);
                if(data.status){
                    //需求表单 提交
                    $("#publish_demand_form").submit();
                }else{
                    //小提示层;
                    validatePop({                            
                        "popconMsg":data.message
                    }); 
                }
            }
        })   
    }  
}); 
*/

 /*#publish_form 验证提交*/
var PublishFormCheck=function(args){
	if (typeof args.validateOption === 'function') {
		args.validateOption=args.validateOption(args);
	}
    $("body").on("focus",".js_no_error",function(event) {
        $(this).addClass("no_error");
    });
	//disabled 取消验证 start
	$(".js_validate",$(args.formId)).each(function(index, el) {
		if($(this).prop("disabled")){
			$(this).removeClass("js_validate");
		}		
	});
	//disabled 取消验证 end
	var parentEleTagName=args.parentEleTagName;
	if(args.errorMethod){
		$(args.formId).addClass("unblur-error");
	}
	//checkSuccess init false
	$(".js_validate",$(args.formId)).closest(parentEleTagName).attr("checkSuccess","false");
	/*form 验证开始*/
	/*blur:失去焦点 验证*/
	$("body").on("blur",args.formId+" .js_validate",function(){
		//var val = $(this).val();
		var parentLi = $(this).closest(parentEleTagName);
		//checkSuccess init false
		$(parentLi).attr("checkSuccess","false");
		if($(this).hasClass("no_error")){
			return ;
		}		
		$(this).addClass("error");
		if($(this).attr("valiname")!=undefined){
			var curOjbAttrName=$(this).attr("valiname");
		}else{
			var curOjbAttrName=$(this).attr("name");
		}


		validateOption({
			"validateOption":args.validateOption,
			"parentEle":parentLi,
			"curOjb":$(this),
			"curOjbAttrName":curOjbAttrName

		});
	})
	//click:点击 checkbox  
	$("body").on("change",args.formId+" .js_validate",function(){
		var curOjbTagName=$(this)[0].tagName;
		var curOjbType;
		switch(curOjbTagName){
			case "INPUT":
				curOjbType=$(this).attr("type");
			break;
			case "SELECT":
				curOjbType="select";
			break;						
			default:;		
		}	
		
		switch(curOjbType){
			case "checkbox":
				var parentLi = $(this).closest(parentEleTagName);
				//checkSuccess init false
				$(parentLi).attr("checkSuccess","false");	

				$(this).addClass("error");
				var curOjbAttrName=$(this).attr("name");
				validateOption({
					"validateOption":args.validateOption,
					"parentEle":parentLi,
					"curOjb":$(this),
					"curOjbAttrName":curOjbAttrName

				});			
			break;
			case "select":
				var parentLi = $(this).closest(parentEleTagName);
				//checkSuccess init false
				$(parentLi).attr("checkSuccess","false");	

				$(this).addClass("error");
				var curOjbAttrName=$(this).attr("name");
				validateOption({
					"validateOption":args.validateOption,
					"parentEle":parentLi,
					"curOjb":$(this),
					"curOjbAttrName":curOjbAttrName

				});			
			break;			
		}	
	});
	//焦点事件
	focusCheck({
		"formId":args.formId,
		"parentEleTagName":args.parentEleTagName
	});
	if(args.submitType=="ajax"){
		//表单提交
		$(args.formId).on('submit',function(event){
			
			var checkResult = formSubmitCheck({
				"formId":args.formId,
				"parentEleTagName":args.parentEleTagName
			});
			//checkResult=true;
			

			if(checkResult){
				args.ajaxFun.call(this,args);
			}
			return false;
		});
	}else{
		//表单提交
		$(args.formId).on('submit',function(event) {
			return formSubmitCheck({
				"formId":args.formId,
				"parentEleTagName":args.parentEleTagName
			});
		});   		
	}

}	
	/*form 操作方法 start*/
/*args:{"parentEle":,"msg":}*/
var setErrormsg=function(args){	
	var pErrorLength=$(args.parentEle).has('p.error').length;
	/*是否已经含有错信息*/
	if(pErrorLength>0){
		$("p.error",$(args.parentEle)).html(args.msg);
	}else{
		$(args.parentEle).append('<p class="error">'+args.msg+'</p>');
	}	
	
}	
/*通过验证 do*/
/*args:{"parentEle":,"curOjb":,"msg"}*/
var checkSuccDo=function(args){
	$(args.curOjb).removeClass("error");
	$(args.parentEle).removeClass("error");
	$("p.error",$(args.parentEle)).remove();
	//checkSuccess  true;
	if($(".js_validate",args.parentEle).length==1){
		$(args.parentEle).attr("checkSuccess","true");
	}
	if($(".js_validate",args.parentEle).length>1){		
		$(":input.error.js_validate",args.parentEle).each(function(index, el) {
			$(this).trigger("blur");
		});
	}

}
/*form 操作方法 end*/
//焦点事件
var focusCheck=function(args){
	$(".js_validate",$(args.formId)).on("focus",function(event) {
		var val = $(this).val();
		var parentLi = $(this).closest(args.parentEleTagName);
		//checkSuccess init false
		$(parentLi).attr("checkSuccess",false);		
		$(this).removeClass("error");
		$("p.error",$(parentLi)).remove();
		$(parentLi).removeClass("error");
		//pop_valierror
		$(this).removeClass("pop_valierror");
		//select_pop 特殊验证
		if($(this).hasClass("js_pop_val")){
	       var elect_pop_text=$(".js_pop_text",$(this).closest(".select_pop"));
	       $(elect_pop_text).removeClass('pop_valierror');
		}
		//代理验证
		if($(this).hasClass("js_vali_ele")){
	       var elect_vali_agent=$(".js_vali_agent",$(this).closest(".js_vali_elep"));
	       $(elect_vali_agent).removeClass('pop_valierror');
		}

		
	});

}	
//提交表单验证
var formSubmitCheck=function(args){
	var allSuccess = true;	
	$(".js_validate",$(args.formId)).each(function(){
    	//js_validate验证
    	$(this).removeClass("no_error"); 

		var parentLi = $(this).closest(args.parentEleTagName);		
		if($(parentLi).attr("checkSuccess")!="true"){
			if($(".js_validate",$(parentLi)).length==1){
				$(this).trigger('blur');	
				//console.log("验证打开");						
				if($(parentLi).attr("checkSuccess")!="true"){
					allSuccess = false;
				}
			}
			if($(".js_validate",$(parentLi)).length>1){				
				$(".js_validate",$(parentLi)).trigger('blur');				
				if($(":input.error.js_validate",$(parentLi)).length==0){
					$(parentLi).attr("checkSuccess",true);
				}else{
					allSuccess = false;					
				}				
			}
			//select_pop 特殊验证
			if($(this).hasClass("js_pop_val")){
		       var elect_pop_text=$(".js_pop_text",$(this).closest(".select_pop"));	
		       if($(this).hasClass('error')){
		            $(elect_pop_text).addClass('error');
		       }else{
		            $(elect_pop_text).removeClass('error');
		       }
			}
			//代理验证
			if($(this).hasClass("js_vali_ele")){
		       var elect_vali_agent=$(".js_vali_agent",$(this).closest(".js_vali_elep"));	
		       if($(this).hasClass('error')){
		            $(elect_vali_agent).addClass('error');
		       }else{
		            $(elect_vali_agent).removeClass('error');
		       }
			}
			//
			if($(this).attr("ajaxCheck")=="ready"){
				$(this).attr("ajaxCheck","submit");
			}			
		}
	})
	
	if(!allSuccess){	
		var firstFalseEle=$('[checksuccess="false"]',$(args.formId))[0];
		if(args.parentEleTagitem==1){
			var firstFalseEle=$(args.formId);
		}
		/*定位第一个 报错 start*/
		var firstFalseEleTop=$(firstFalseEle).offset().top;
		if($(".head-h").length>0){
			firstFalseEleTop=$(firstFalseEle).offset().top-118;			
		}
		if($(".pagewrap").length>0){
			var mheaderH=$(".header").height();
			firstFalseEleTop=$(firstFalseEle).offset().top-mheaderH-2;
			$(firstFalseEle).addClass('error');
			
		}
		if(args.parentEleTagitem!=1){
		$("html,body").animate({scrollTop: firstFalseEleTop}, 300);	
		}
		/*定位第一个 报错 end*/
		/*弹出第一个 报错 start*/
		if($(firstFalseEle).closest("form").hasClass("unblur-error")){			
			if($(".validatePop").length>0){
				$(".validatePop").remove();
			}
			var errorTxt=$("p.error",$(firstFalseEle)).text();
			if(errorTxt.length>0){
				//pop_valierror
				$(".js_validate.error",firstFalseEle).addClass("pop_valierror");
				//select_pop 特殊验证
				if($(".js_validate.error",firstFalseEle).hasClass("js_pop_val")){
			       var elect_pop_text=$(".js_pop_text",$(".js_validate.error",firstFalseEle).closest(".select_pop"));
			       $(elect_pop_text).addClass('pop_valierror');
				}
				//代理验证
				if($(".js_validate.error",firstFalseEle).hasClass("js_vali_ele")){
			       var elect_vali_agent=$(".js_vali_agent",$(".js_validate.error",firstFalseEle).closest(".js_vali_elep"));
			       $(elect_vali_agent).addClass('pop_valierror');
				}
				var validatePop='<div class="validatePop">'+errorTxt+'</div>';
				$("body").append(validatePop);
				var validatePopW=$(".validatePop").width()+parseFloat($('.validatePop').css('padding-top'))+parseFloat($('.validatePop').css('padding-bottom'));	
				var validatePopH=$(".validatePop").height();
				$(".validatePop").css({"opacity": 0,"left":"50%","top":"50%","margin": "-"+(validatePopH/2)+"px 0 0 -"+(validatePopW/2)+"px"});
				$(".validatePop").animate({"opacity": 1},350,function() {
					setTimeout(function(){
						if($(".validatePop").length>0){											
							$(".validatePop").fadeOut(100, function() {
								$(this).remove();
							});
						}
					},500);
				});
			}

		}	
		/*弹出第一个 报错 end*/		
	}	
	return allSuccess;
}
/*args:{
	"validateOption":args.validateOption,
	"parentEle":parentLi,
	"curOjb":$(this),
	"curOjbAttrName":curOjbAttrName

}*/
var validateOption=function(args){
	var validateOption=args.validateOption;
	var checkOption = validateOption[args.curOjbAttrName];
	
	var checkState=false;
	if(checkOption!=false){
		for(var checkOptionVal in checkOption){
			switch(checkOptionVal){
				case "requiredCheck":
				case "lengthCheck":
				case "digitsCheck":
				case "rangeCheck":
				case "emailCheck":
				case "phoneCheck":
				case "noPhoneCheck":				
				case "salaryCheck":
				case "usernameCheck":
				case "passwordCheck":
				case "httpCheck":
				case "ajaxCheck":
				
				
				var checkFunName=checkOptionVal;
				
				var checkArgs=checkOption[checkOptionVal];
				var newcheckArgs={"parentEle":args.parentEle,"curOjb":args.curOjb};				
				//参数追加
				for(var t in checkOption[checkOptionVal]){
					newcheckArgs[t]=checkOption[checkOptionVal][t];
				}
				
				
				var checkFun=eval(checkFunName);
				
				var checkState=checkFun.call(null,newcheckArgs);//当前函数名
				
				if(checkState){
					return;
				}
			}
		}		

	}else{
		
		//checkState=true;
	}

	if(!checkState){		
		checkSuccDo({"parentEle":args.parentEle,"curOjb":args.curOjb});
	}	
}


 //是否含有中文（也包含日文和韩文）
var isChineseChar= function(args){
   var reg = /[\u4E00-\u9FA5\uF900-\uFA2D]/;
   return reg.test(args);	
}
//同理，是否含有全角符号的函数
var isFullwidthChar=function(args){
   	//全角符号
   	var reg=/[^\x00-\xff]/g;
   return reg.test(args);
}  
var isFullwidthChar2=function(args){
	//匹配这些中文标点符号 。 ？ ！ ， 、 ； ： “ ” ‘ ’ （ ） 《 》 〈 〉 【 】 『 』 「 」 ﹃ ﹄ 〔 〕 … — ～ ?
   var reg = /[\u3002|\uff1f|\uff01|\uff0c|\u3001|\uff1b|\uff1a|\u201c|\u201d|\u2018|\u2019|\uff08|\uff09|\u300a|\u300b|\u3008|\u3009|\u3010|\u3011|\u300e|\u300f|\u300c|\u300d|\ufe43|\ufe44|\u3014|\u3015|\u2026|\u2014|\uff5e|\ufe4f|\uffe5]/;
   return reg.test(args);
}
/*验证方法stat*/

var errorStrNull='必填项不能为空';
var errorSelNull="必选项必须选择一项";
var errorMaxLength="最大长度为";
var errorMinLength="最小长度为";
var errorDigits="只能输入整数且大于0";
var errorPhone="你输入的手机号码不正确";
var errorUsername="账号格式有误，请输入正确的邮箱或手机号!"
var errorPassword="6-16个字符，不能有空格!"
var errorHttp="请输入含“http”的正确网址！";
//var errorrangelength="请输入 一个长度介于 {0} 和 {1} 之间的字符串";
/*必填项 验证*/
/*args:{"parentEle":,"curOjb":,"msg"}*/
var requiredCheck=function(args){
	var checkState= false;	
	var curOjbTagName=$(args.curOjb)[0].tagName;
	var curOjbType;
	switch(curOjbTagName){
		case "INPUT":
			curOjbType=$(args.curOjb).attr("type");
		break;
		case "SELECT":
			curOjbType="select";
		break;
		default:;		
	}
	
	switch(curOjbType){
		case "radio":/*radio*/
			var radioName=$(args.curOjb).attr("name");
			var checkedLength=$('input[name="'+ radioName+'"]:checked').length;				
            if(checkedLength==0){
                //什么也没选中!
				if (args.msg != undefined) {
					setErrormsg({"parentEle":args.parentEle,"msg":args.msg});
				}else{
					setErrormsg({"parentEle":args.parentEle,"msg":errorSelNull});
				}
				checkState=true;
            }
		break;	
		case "checkbox":
			var checkboxName=$(args.curOjb).attr("name");
			var checkedLength=$('input[name="'+ checkboxName+'"]:checked').length;
            if(checkedLength==0){
                //什么也没选中!
				if (args.msg != undefined) {
					setErrormsg({"parentEle":args.parentEle,"msg":args.msg});
				}else{
					setErrormsg({"parentEle":args.parentEle,"msg":errorSelNull});
				}
				checkState=true;
            }			
		break;
		case "select":
			//var selectName=$(args.curOjb).attr("name");
			var curVal=$(":selected",args.curOjb).attr("value");
            if(curVal==""||curVal==undefined){
                //什么也没选中!
				if (args.msg != undefined) {
					setErrormsg({"parentEle":args.parentEle,"msg":args.msg});
				}else{
					setErrormsg({"parentEle":args.parentEle,"msg":errorSelNull});
				}
				checkState=true;
            }	

		break;				
		default:/*input: text password tle email url number Date pickers (date, month, week, time, datetime, datetime-local) search color;textarea:; */
			var placeholderval=$(args.curOjb).attr("placeholder");
			var defulttxt=$(args.curOjb).attr("defulttxt");
			var defultval=iGetInnerText($(args.curOjb).val());			
			var vallength=$(args.curOjb).val().length;
			if(defulttxt==defultval){
				vallength=0;
			}
			if(placeholderval==$(args.curOjb).val()){
				vallength=0;
			}

			if($(".js_pop_other",args.parentEle).length>0){
				if($(".js_pop_other",args.parentEle).val().length>0){
					vallength=$(".js_pop_other",args.parentEle).val().length;
				}
			}
			if(vallength==0){
				if (args.msg != undefined) {						
					setErrormsg({"parentEle":args.parentEle,"msg":args.msg});
				}else{						
					setErrormsg({"parentEle":args.parentEle,"msg":errorStrNull});
				}
				checkState=true;				
			}else{
				
			}				
	}
	
	return checkState;
	
}
function iGetInnerText(testStr) {
        var resultStr = testStr.replace(/\ +/g, ""); //去掉空格
        resultStr = testStr.replace(/[ ]/g, "");    //去掉空格
        resultStr = testStr.replace(/[\r\n]/g, ""); //去掉回车换行
        return resultStr;
}
/*checkbox选择长度,字符长度 验证*/
/*args:{
"parentEle":parentLi,
"curOjb":$(this),
"minlength":[2,"dfafa"],
"maxlength":[5,"dfafa"],						
"rangelength":[5,10,"5255"],
"vallength":
}*/	
var lengthCheck=function(args){
	
	var checkState= false;
	var curOjbTagName=$(args.curOjb)[0].tagName;		
	var curOjbType;
	var vallength;
	switch(curOjbTagName){
		case "INPUT":
			curOjbType=$(args.curOjb).attr("type");
		break;		
		default:;		
	}
	switch(curOjbType){
		case "checkbox":
			var checkboxName=$(args.curOjb).attr("name");			
			vallength=$('input[name="'+ checkboxName+'"]:checked').length;

		break;
		default:/*字符*/
			
			vallength=$(args.curOjb).val().length;
	}	

	if (args.vallength != undefined) {
		vallength=args.vallength;

	}
	if (args.rangelength != undefined) {

		/*长度区间*/
		if(!(vallength>args.rangelength[0]&&vallength<args.rangelength[1])){
			if(args.rangelength.length==3){
				setErrormsg({"parentEle":args.parentEle,"msg":args.rangelength[2]});
			}else{
				var curmsg='请输入一个长度介于'+args.rangelength[0]+' 和'+args.rangelength[1]+'之间的字符串';
				setErrormsg({"parentEle":args.parentEle,"msg":curmsg});
			}
			checkState=true;				
		}

	}else{

		/*最小长度*/
		if (args.minlength != undefined) {
			if(vallength<args.minlength[0]){
				if(args.minlength.length==2){
					var curmsg=args.minlength[1];
					setErrormsg({"parentEle":args.parentEle,"msg":curmsg});
					
				}else{
					var curmsg=errorMinLength+args.minlength[0];
					setErrormsg({"parentEle":args.parentEle,"msg":curmsg});
				}
				checkState=true;
			}
		}
		/*最大长度*/
		if (args.maxlength != undefined) {
			
			if(vallength>args.maxlength[0]){
				if($(args.curOjb).attr("type")=="checkbox"){
					$(args.curOjb).prop("checked",false);
				}
				
				if(args.maxlength.length==2){
					var curmsg=args.maxlength[1];
					setErrormsg({"parentEle":args.parentEle,"msg":curmsg});						
				}else{
					
					var curmsg=errorMaxLength+args.maxlength[0];
					setErrormsg({"parentEle":args.parentEle,"msg":curmsg});							
				}
				checkState=true;
				
			}else{
				
			}
		}		
		

	}
	return checkState;
}
/*整数 验证*/
/*args:{"parentEle":,"curOjb":,"msg"}*/
var digitsCheck=function(args){
	var checkState= false;
	var numberRegex= /^[0-9]*[1-9][0-9]*$/;	//不包括0
	var val=$(args.curOjb).val();
	
	if(!(numberRegex.test(val))){
		if (args.msg != undefined) {
			setErrormsg({"parentEle":args.parentEle,"msg":args.msg});
		}else{
			setErrormsg({"parentEle":args.parentEle,"msg":errorDigits});
		}
		checkState=true;
	}
	return checkState;
	
}

/*range 数字的区间*/
var rangeCheck=function(args){

}
//邮件验证	
/*args:{
"parentEle":parentLi,
"curOjb":$(this),
"minlength":[2,"dfafa"],
"maxlength":[5,"dfafa"],						
"rangelength":[5,10,"5255"]
}*/			
var emailCheck = function(args){
	var checkState= false;
	var emailRegex =/^[a-zA-Z0-9.!#$%&'*+\/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$/;//邮箱
	var quanjiaoRegex=/[^\x00-\xff]/g;//全角
	var val=$(args.curOjb).val();
	if(quanjiaoRegex.test(val)){
		
		var curmsg="输入的不能含中文全角字符";
		setErrormsg({"parentEle":args.parentEle,"msg":curmsg});	
		checkState=true;			
	}else{
		var varArray=val.split(";");
		var varArrayLength=varArray.length;
		if(varArray[varArrayLength-1]==""){
			varArray.pop();
			varArrayLength=varArray.length;
		}
		var mailSucc=true;
		var errorMail="";
		for(var i=0; i<varArray.length;i++){
			if(!emailRegex.test(varArray[i])){
				mailSucc=false;
				errorMail=errorMail+varArray[i]+";";
			}
		}
		if(mailSucc){
			//长度验证
			var curArgs=args;
				curArgs.vallength=varArrayLength;		
				checkState=lengthCheck(curArgs);
		}else{
			
			//var curmsg= errorMail+"不是正确的邮箱地址";
			var curmsg= "邮箱地址格式不正确";
			setErrormsg({"parentEle":args.parentEle,"msg":curmsg});	
			checkState=true;		
		}
	}	
	return checkState;		
	
}
var phoneCheck = function(args){
	
	var checkState= false;
	var phoneRegex = /^1[34578]\d{9}$/;//手机号码
	var quanjiaoRegex=/[^\x00-\xff]/g;//全角
	var curVal=$(args.curOjb).val();
	
	if(quanjiaoRegex.test(curVal)){
		var curmsg="输入的不能含中文全角字符";
		setErrormsg({"parentEle":args.parentEle,"msg":curmsg});	
		checkState=true;			
	}else{
		if(!phoneRegex.test(curVal)){	
			if (args.msg != undefined) {
				setErrormsg({"parentEle":args.parentEle,"msg":args.msg});
			}else{
				setErrormsg({"parentEle":args.parentEle,"msg":errorPhone});
			}
			checkState=true;			
		}		

	}	
	return checkState;		
	
}
var noPhoneCheck = function(args){	
	var checkState= false;
    var mobilephoneRegex=/(13[0-9]|14[0-9]|15[0-9]|18[0-9])\d{8}/;
    var phoneRegex=/(([0\+]\d{2,3}-)?(0\d{2,3})-)?(\d{7,8})(-(\d{3,}))?/;
	var curVal=$(args.curOjb).val();	
	if(mobilephoneRegex.test(curVal)||phoneRegex.test(curVal)){
		if (args.msg != undefined) {
			setErrormsg({"parentEle":args.parentEle,"msg":args.msg});
		}else{
			setErrormsg({"parentEle":args.parentEle,"msg":errorPhone});
		}
		checkState=true;			
	}	
	return checkState;
}
var usernameCheck = function(args){
	
	var checkState= false;
	var emailRegex =/^[a-zA-Z0-9.!#$%&'*+\/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$/;//邮箱
	var phoneRegex = /^1[34578]\d{9}$/;//手机号码
	var quanjiaoRegex=/[^\x00-\xff]/g;//全角
	var curVal=$(args.curOjb).val();
	if(quanjiaoRegex.test(curVal)){
		var curmsg="输入的不能含中文全角字符";
		setErrormsg({"parentEle":args.parentEle,"msg":curmsg});	
		checkState=true;			
	}else{
		if(emailRegex.test(curVal)||phoneRegex.test(curVal)){
		}else{
			if (args.msg != undefined) {
				setErrormsg({"parentEle":args.parentEle,"msg":args.msg});
			}else{
				setErrormsg({"parentEle":args.parentEle,"msg":errorUsername});
			}
			checkState=true;				
		}
	}	
	return checkState;
}
var passwordCheck = function(args){
	var checkState= false;
	var passwordRegex = /^[^\s]{6,16}$/;
	var curVal=$(args.curOjb).val();
	if(!passwordRegex.test(curVal)){	
		if (args.msg != undefined) {
			setErrormsg({"parentEle":args.parentEle,"msg":args.msg});
		}else{
			setErrormsg({"parentEle":args.parentEle,"msg":errorPassword});
		}
		checkState=true;			
	}
	return checkState;	
}
var httpCheck = function(args){
	var checkState= false;
	var httpRegex = /(http|ftp|https):\/\//;
	var curVal=$(args.curOjb).val();
	if(!httpRegex.test(curVal)||curVal=="http://"){	
		if (args.msg != undefined) {
			setErrormsg({"parentEle":args.parentEle,"msg":args.msg});
		}else{
			setErrormsg({"parentEle":args.parentEle,"msg":errorHttp});
		}
		checkState=true;			
	}
	return checkState;	
}
/*
   	"ajaxCheck":{
   		"ajaxFun":{
            url: "../ajax/ajaxCheck_error.html",
            type: 'POST',		                
            data:{
            	"username":function(){return $("#username").val();},
            	"password":function(){return $("#password").val();}
            },
            success:function(data){
            	if(data!="true"){
            		var msg="报错内容";
            		return msg;
            	}
            }
        }//,
        //"msg":"不对"
    }
*/
var ajaxCheck = function(args){
	var checkState= false;
	if(args.ajaxFun!=undefined&&$(args.curOjb).attr("ajaxCheck")!="submit"){
		var ajaxFun=args.ajaxFun;
		var args_url=ajaxFun.url;
		var args_type=ajaxFun.type;
		var args_dataType="";
		if(ajaxFun.dataType!=undefined){
			args_dataType=ajaxFun.dataType;
		}		
		var args_data=ajaxFun.data;
		var dataobj={};
		for(i in args_data){			
			dataobj[i]=args_data[i].call(null);
		}
		var args_success=ajaxFun.success;
		var args_msg=ajaxFun.msg;
        $.ajax({
            url: args_url,
            type: args_type,
            dataType: args_dataType,
            data:dataobj,
            success: function(data){
            	var callbackAgrs={};
            	if(args_success!=undefined){
            		callbackAgrs=args_success.call(null,data);
            		if(callbackAgrs!=undefined){
            			setErrormsg({"parentEle":args.parentEle,"msg":callbackAgrs});     
            			checkState=true;     
            			//validatePop			
            			if($(args.curOjb).closest("form").hasClass("unblur-error")){
            				var curForm= $(args.curOjb).closest("form");
            				var curFirstFalseEleIndex=$($('[checksuccess="false"]',$(curForm))[0]).index();
            				var curIndex=$(args.curOjb).index();
            				if(curFirstFalseEleIndex==curIndex){
								if($(".validatePop").length>0){
									$(".validatePop").remove();
								}
								validatePop({
									"popconMsg":callbackAgrs
								}); 
            				} 
            			} 			
            		}else{
            			checkState=false;  
            			$(args.parentEle).removeClass('error');        			 
            		}
            	}else{
            		//默认报错           		
            		if(data!="true"){            			
            			var msg=data;
            			if(args_msg!=undefined){
            				msg=args_msg;
            			}
			 			setErrormsg({"parentEle":args.parentEle,"msg":msg});
						checkState=true;  
						//validatePop
            			if($(args.curOjb).closest("form").hasClass("unblur-error")){
            				var curForm= $(args.curOjb).closest("form");
            				var curFirstFalseEleIndex=$($('[checksuccess="false"]',$(curForm))[0]).index();
            				var curIndex=$(args.curOjb).index();
            				if(curFirstFalseEleIndex==curIndex){
								if($(".validatePop").length>0){
									$(".validatePop").remove();
								}
								validatePop({
									"popconMsg":msg
								}); 
            				} 
            			}        			
            		}else{
            			checkState=false;   
            			$(args.parentEle).removeClass('error');  			
            		}
            	}
            	if(checkState==true){            		
            		args.parentEle.attr("checkSuccess","false");
            		args.curOjb.addClass("error");
            		$(args.curOjb).attr("ajaxCheck","false");
            	}else{
        			$(args.parentEle).attr("checksuccess","true");
        			$(args.curOjb).removeClass('error');
        			if($(args.curOjb).attr("ajaxCheck")=="submit"){ 
        				$(args.curOjb).closest('form').submit();      				
        			} 
        			$(args.curOjb).attr("ajaxCheck","true");           		
            	}
				return checkState;
            }

        })
		$(args.curOjb).attr("ajaxCheck","ready"); 
		$(args.curOjb).removeClass("error");
    	return checkState=true;
	}

}
/*私有验证方法*/
/*salary薪资范围*/
var salaryCheck=function(args){		
	var salaryFrom=parseInt($("#salary_from").val());
	var salaryTo=parseInt($("#salary_to").val());	
	var checkState= false;	
	if(salaryFrom<1000||salaryFrom>1000000||salaryTo<1000||salaryTo>1000000){
		var curmsg="请输入有效的月薪范围，1000—1000000";
		setErrormsg({"parentEle":args.parentEle,"msg":curmsg});	
		checkState=true;
	}else{
		if((salaryTo-salaryFrom)<=0){
			var curmsg="薪资范围第二项必须大于第一项";
			setErrormsg({"parentEle":args.parentEle,"msg":curmsg});	
			checkState=true;
		}else if((salaryTo/salaryFrom)>2){
			var curmsg="薪资范围不能相差超过2倍";
			setErrormsg({"parentEle":args.parentEle,"msg":curmsg});				
			checkState=true;
		}		
	}

	return checkState;		
}
/*验证方法 end*/
/*特殊验证*/
var likeRadioCheck=function(args){
    $("body").on('click',args.likeParentEle+' [likename="'+args.likename+'"][likeradio="0"]', function(event) {   	
    	var val = $(this).prop('checked');


    	/*1：隐藏 ，取消验证*/ 
    	if(val){    	
    		//1隐藏
            $(args.likeParentEle+' [likename="'+args.likename+'"][likeradio="1"]').parent().addClass("hidden"); 
            
            //1取消验证
            $(args.likeParentEle+' [likename="'+args.likename+'"][likeradio="1"]').removeClass("js_validate");
            $(args.likeParentEle+' [likename="'+args.likename+'"][likeradio="1"]').removeClass("error");
            $('p.error',$(args.likeParentEle+' [likename="'+args.likename+'"][likeradio="1"]').closest('[checksuccess]')).remove();

            //3显示
            $(args.likeParentEle+' [likename="'+args.likename+'"][likeradio="3"]').parent().removeClass("hidden"); 
            $(args.likeParentEle+' [likename="'+args.likename+'"][likeradio="3"]').addClass("js_validate");                              		
    	}else{
    		$(this).removeClass("js_validate");
    		//1显示
            $(args.likeParentEle+' [likename="'+args.likename+'"][likeradio="1"]').parent().removeClass("hidden"); 
            $(args.likeParentEle+' [likename="'+args.likename+'"][likeradio="1"]').addClass("js_validate");  

    		//3隐藏
            $(args.likeParentEle+' [likename="'+args.likename+'"][likeradio="3"]').parent().addClass("hidden"); 
            //3取消验证
            $(args.likeParentEle+' [likename="'+args.likename+'"][likeradio="3"]').removeClass("js_validate");
            $(args.likeParentEle+' [likename="'+args.likename+'"][likeradio="3"]').removeClass("error");
            $('p.error',$(args.likeParentEle+' [likename="'+args.likename+'"][likeradio="3"]').closest('[checksuccess]')).remove();              		
    	}
        /*2：设置空，取消验证*/
        if(val){
        	//2取消验证
            $(args.likeParentEle+' [likename="'+args.likename+'"][likeradio="2"]').removeClass("js_validate");
            $(args.likeParentEle+' [likename="'+args.likename+'"][likeradio="2"]').removeClass("error");
            $('p.error',$(args.likeParentEle+' [likename="'+args.likename+'"][likeradio="2"]').closest('[checksuccess]')).remove();
            //2置空
            $(args.likeParentEle+' [likename="'+args.likename+'"][likeradio="2"]').val("");        	
        }else{
        	$(this).removeClass("js_validate");
        	$(args.likeParentEle+' [likename="'+args.likename+'"][likeradio="2"]').addClass("js_validate");

        }       
 
    });

}  

var countStrCheck=function(){
	countStrFun=function(args){
		var countname=args.countname;
		var countvalobj=args.countvalobj;
		var curojb=args.curojb;
        var testStr = curojb.val().replace(/\n/g, "\r\n");
        var testStr2 = testStr.replace(/\r\r\n/g, "\r\n");   //兼容IE7,8,FF
        var testStr3 = testStr2.replace(/\r\n\r/g, "\r\n");  //兼容IE9
		countvalobj.html(testStr3.length);
	}
	$('[countname]').each(function(index, el) {
        var countname=$(this).attr("countname");
        var countvalobj=$(this).next().find('[countval="'+countname+'"]');
        if(countvalobj.length==0){
        	countvalobj=$(this).parent().next().find('[countval="'+countname+'"]');
        }  
        var curojb=$(this);
		new countStrFun({
			"countname":countname,
			"countvalobj":countvalobj,
			"curojb":curojb
		});
	});
	$("body").off('keyup','[countname]');
	$("body").on('keyup','[countname]', function(event) {
        var countname=$(this).attr("countname");
        var countvalobj=$(this).next().find('[countval="'+countname+'"]'); 
        if(countvalobj.length==0){
        	countvalobj=$(this).parent().next().find('[countval="'+countname+'"]');
        }              
        var curojb=$(this);
        //调用
		new countStrFun({
			"countname":countname,
			"countvalobj":countvalobj,
			"curojb":curojb
		});
	});	
}
//代理验证
//agentValidate({"valiEle":,"agentEle":});
function agentValidate(args){
    //js_validate验证
    $(args.valiEle).trigger('blur');
    if($(args.valiEle).hasClass("error")){
        $(args.agentEle).addClass("error");
    }else{
        $(args.agentEle).removeClass("error");
        $(args.agentEle).removeClass("pop_valierror");
    }
}