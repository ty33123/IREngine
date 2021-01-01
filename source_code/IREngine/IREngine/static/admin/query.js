$(document).ready(function() {
	if (document.getElementById("search_text").value !== '') {
		search_news(1)
	}
	$(function() {
		data = $.ajax({
			url: "/get_readtop.json",
			async: true,
			dataType: "json",
			success: function(result) {
				var dataObj = result.items,
				//返回的result为json格式的数据
				con = "";
				$.each(dataObj,
				function(index, item) {
					title = item.title.substr(0, 10) + "...";
                    con += "<p><a target='_blank' href='/re_direct?url=" + item.url + "' title='" + item.title + "'>" + title + " &nbsp;&nbsp; <font size='1' >阅读量：" + item.read_counts + "</font></a></p>"
				});
				//console.log(con);    //可以在控制台打印一下看看，这是拼起来的标签和数据
				$("#hot_read").html(con); //把内容入到这个div中即完成
			}
		});
	});
});
function get_rel_words(query_words) {
	data = $.ajax({
		url: "/rel_query.json",
		async: true,
		dataType: "json",
		type: 'POST',
		data: JSON.stringify({
			"qw": query_words
		}),
		contentType: "application/json; charset=utf-8",
		success: function(result) {
			var dataObj = result.items,
			//返回的result为json格式的数据
			con = "";
			$.each(dataObj,
			function(index, item) {
				con += "<p><a target='_self' href='" + item.link + "' title='" + item.title + "'>" + item.title + "</a></p>"
			});
			//console.log(con);    //可以在控制台打印一下看看，这是拼起来的标签和数据
			$("#rel_query").html(con); //把内容入到这个div中即完成
		}
	});
}
function get_results(){
	var thisSearch = '/s?wd=';
	var search_text = document.getElementById("search_text").value;
	window.open(thisSearch + search_text, '_self');
}

function search_news(page_num, type) {
	var search_text = document.getElementById("search_text").value;
	var url = "/search?q=" + search_text + "&page=" + page_num +"&type=" + type;
	data = $.ajax({
		url: url,
		async: true,
		dataType: "json",
		success: function(result) {
			var dataObj = result.items; //返回的result为json格式的数据
			resultTotal = "<span class='info'>找到约&nbsp;<span class='totalResult'>" + result.news_num + "</span>&nbsp;条结果(用时<span class='time'>" + result.used_time + "</span>秒)，共约<span class='totalPage'>" + result.total_page + "</span>页</span>";
			var by_time_url = url + "&type=by_time";
			var by_hot_url = url + "&type=by_hot"
			resultTotal += "<span class='orderOpt'\">" +
				"                    \t<a onclick=\"search_news("+ page_num + ",'byTime')\" class='byTime'>按时间排序</a>\n" +
				"                        <a onclick=\"search_news("+ page_num + ",'byHot')\" class='byHot'>按热度排序</a>\n" +
				"                    </span>";
			$(".resultTotal").html(resultTotal);
			if (dataObj.length == 0) {
				$(".resultList").html("");
			} else {
				get_rel_words(search_text);
				resItems = "";
				$.each(dataObj,
				function(index, item) {
					resItems += "<div class='resultItem'><div class='itemHead'>";
					title = item.title.substr(0, 25) + "...";
					resItems += "<a target=\"_blank\" href='/re_direct?url=" + item.url + "' class='title' title='" + item.title + "'>" + title + "</a>";
					resItems += "<span class='divsion'>-<a class='title' onclick='show_news(" + item.id + ")'>离线</a></span>";
					resItems += "<span class='dependValue'><span class='label'> 阅读量： ";
					resItems += "<span class='value'>" + item.read_counts + "</span></span></span></div>";
					if (item.context !== '') {
						resItems += "<div class='itemBody'>" + item.content + "</div>";
					}
					resItems += "<div class=\"itemFoot\">";
					resItems += "<span class='info'><label> 采集源： </label>";
					resItems += "<span class='value'>" + item.acq_source + "</span></span>";
					resItems += "<span class='info'><label> 采集时间： </label>";
					resItems += "<span class='value'>" + item.collect_time + "</span></span>";
					resItems += "<span class='info'><label> 发布时间： </label>";
					resItems += "<span class='value'>" + item.publish_time + "</span></span>";
					resItems += "<span class='info' style='color:blue;' onclick='sim_news(" + item.id + ")'><a style='color:blue;'> 相关推荐 </a>"+"</span></div></div>";
				});
				$(".resultList").html(resItems);
				createPageHTML(result.total_page, page_num, type);
				$('html').scrollTop(0);
			}
		}
	});

}
function createPageHTML(_nPageCount, _nCurrIndex, search_type) {
	var split_page = ''
	if (_nPageCount == null || _nPageCount <= 1) {
		$(".pageing").html(split_page);
		return;
	}
	var nCurrIndex = _nCurrIndex || 1;
	// 1 输出首页和上一页
	// 1.1 当前页是首页
	if (nCurrIndex == 1) {
		split_page += ("<span>当前第1/" + _nPageCount + "页</span>");
		split_page += ("<span><a onclick='search_news(1,\""+search_type+"\")'>首页</a></span>");
		// split_page+=("<span><a onclick=\"javascript:void(0)\">上一页</a></span>");
	}
	//1.2 当前页不是首页
	else {

		var nPreIndex = nCurrIndex - 1;
		split_page += ("<span>当前第" + (_nCurrIndex) + "/" + _nPageCount + "页</span>");
		split_page += ("<span><a onclick='search_news(1,\""+search_type+"\")'>首页</a></span>");
		split_page += ("<span><a onclick='search_news(" + nPreIndex + ",\""+search_type+"\")'>上一页</a></span>");
	}

	// 3 输出下一页和尾页
	// 3.1 当前页是尾页
	if (nCurrIndex == (_nPageCount)) {

}
	// 3.2 当前页不是尾页
	else {
		var nNextIndex = nCurrIndex + 1;
		split_page += ("<span><a onclick='search_news(" + nNextIndex + ",\""+search_type+"\")'>下一页</a>&nbsp;</span>");
		split_page += ("<span><a onclick='search_news(" + _nPageCount + ",\""+search_type+"\")'>尾页</a></span>");
	}
	$(".pageing").html(split_page);
}

function show_news(id) {
	var item = '';
	data = $.ajax({
		url: "/query/news_id.json",
		async: false,
		dataType: "json",
		type: 'POST',
		data: JSON.stringify({
			"id": id
		}),
		contentType: "application/json; charset=utf-8",
		success: function(result) {
			item = result.item

		}
	});

	context = '';
	context += "<tr><th width='100' class='text-r'> 标题：</th>";
	context += "<td><a target='_blank' href='/re_direct?url=" + item.url + "' title='" + item.title + "'>" + item.title + "</a></td></tr>";
	context += "<tr><th width='100' class='text-r'> 采集源：</th>";
	context += "<td>" + item.acq_source + "</td></tr>";
	context += "<tr><th width='100' class='text-r'> 采集日期：</th>";
	context += "<td>" + item.collect_time + "</td></tr>";
	context += "<tr><th width='100' class='text-r'> 发布日期：</th>";
	context += "<td>" + item.publish_time + "</td></tr>";
	context += "<tr><th width='100' class='text-r'> 阅读量</th>";
	context += "<td>" + item.read_counts + "</td></tr>";
	context += "<tr><th width='100' class='text-r'> 全文</th>";
	context += "<td><textarea class='input-text' style='height:200px;width:400px;' readonly='readonly'>" + item.content + "</textarea></td></tr>";
	$('#detail_news').html(context);
	$("#show_news").modal("show")
}


function sim_news(id) {
    var item='';
    data = $.ajax({
        url: "/recom_news",
        async: true,
        dataType: "json",
        type: 'POST',
        data: JSON.stringify({
            "id": id
        }),
		contentType: "application/json; charset=utf-8",
		success: function(result) {
			var dataObj = result.items,
			//返回的result为json格式的数据
			con = '';
			$.each(dataObj,
			function(index, item) {
				title = item.title.substr(0, 30) + "...";
				con += "<p><a target=\"_blank\" href='/re_direct?url=" + item.url + "' title='" + item.title + "'>" + title + " &nbsp;&nbsp; <font size='1' >阅读量：" + item.read_counts + "</font></a></p>"
				console.log(con);
			});
			console.log(con);    //可以在控制台打印一下看看，这是拼起来的标签和数据
			//$("#simi_news").html(con);//把内容入到这个div中即完成
			$('#sim_show').html(con);

		}
    });
    $("#sim_news").modal("show")
}