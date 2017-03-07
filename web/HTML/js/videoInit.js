function addLatest(vodid,imgurl,title,author,time,row){
  var content = "<div class=\"col-sm-4 sm-margin-b-50\"><div class=\"margin-b-20\"><img class=\"img-responsive wow fadeIn test-popup-link\" style=\"width:100%;cursor: pointer;\"  onClick=getHL("+vodid+") src=\""+imgurl+"\" alt=\"Latest Products Image\" data-wow-duration=\".3\" data-wow-delay=\".1s\"></div><div style=\"margin:10px\"><h4 style=\"width:100%;text-overflow:ellipsis;overflow:hidden;white-space:nowrap;\"><a style=\"cursor: pointer;\" onClick=getHL("+vodid+")>"+title+"</a></h4><p>"+author+"<span class=\"text-uppercase margin-l-20\">"+time+"</span></p><a class=\"link\" style=\"cursor: pointer;\" onClick=getWC('"+vodid+"')>Read More</a></div></div>";
  if(row == 1)
    $(content).appendTo('#latest1');
  else
    $(content).appendTo('#latest2');
}

function addPopular(vodid,imgurl,title,author,time,row){
  var content = "<div class=\"col-sm-4 sm-margin-b-50\"><div class=\"margin-b-20\"><img class=\"img-responsive wow fadeIn test-popup-link\" style=\"width:100%;cursor: pointer;\"  onClick=getHL("+vodid+") src=\""+imgurl+"\" alt=\"Latest Products Image\" data-wow-duration=\".3\" data-wow-delay=\".1s\"></div><div style=\"margin:10px\"><h4 style=\"width:100%;text-overflow:ellipsis;overflow:hidden;white-space:nowrap;\"><a style=\"cursor: pointer;\" onClick=getHL("+vodid+")>"+title+"</a></h4><p>"+author+"<span class=\"text-uppercase margin-l-20\">"+time+"</span></p><a class=\"link\" style=\"cursor: pointer;\" onClick=getWC('"+vodid+"')>Read More</a></div></div>";
  if(row == 1)
    $(content).appendTo('#popular1');
  else
    $(content).appendTo('#popular2');
}

function JustAdd(){
  imgurl = "../img/3.0.png";
  var content = "<img class=\"img-responsive wow fadeIn test-popup-link\" style=\"width:10px;display:none\"  src=\""+imgurl+"\">";
  $(content).appendTo('#popular1');
}


function clickCount(id){
  $.getJSON("http://140.114.77.126:4000/api/v1.0/updateClick/"+id);
}
