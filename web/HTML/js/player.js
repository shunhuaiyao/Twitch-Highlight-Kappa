var player=null;
var VideoInfo;
var nowIndex = 0;
var myVar;

function playerInitial(id){
  var options = {
      width: 854,
      height: 480,
      video: "v"+id
  };
  player = new Twitch.Player("Highlight", options);
  player.setVolume(0.5);
  $('#prevHL').css('visibility','hidden');
  $('#nextHL').css('visibility','visible');
  $('#HLtitle').text('Twitch Hight #1');
  player.seek(VideoInfo[0].start);
  myVar = setInterval(checkUpdate, 1000);
}

function nextHL(){
  var numHL = VideoInfo.length;
  if(nowIndex < numHL-1){
    nowIndex++;
    player.seek(VideoInfo[nowIndex].start);
    $('#HLtitle').text('Twitch Hight #'+(nowIndex+1));
    $('#prevHL').css('visibility', 'visible');
    if(nowIndex==numHL-1)
      $('#nextHL').css('visibility','hidden')
  }
}

function prevHL(){
  if(nowIndex > 0){
    nowIndex--;
    player.seek(VideoInfo[nowIndex].start);
    $('#HLtitle').text('Twitch Hight #'+(nowIndex+1));
    $('#nextHL').css('visibility', 'visible');
    if(nowIndex==0)
      $('#prevHL').css('visibility','hidden');
  }
}

function checkUpdate(){
  var nowtime = player.getCurrentTime();
  var start = VideoInfo[nowIndex].start;
  var end = VideoInfo[nowIndex].end;
  //End of Highlight
  if(nowIndex == VideoInfo.length-1 && nowtime >= end){
    clearInterval(myVar);
    player.pause();
  }
  //New Highlight Start
  else if(nowtime < start){
    player.seek(start);
  }
  //Highlight Interval
  else if(nowtime >= start && nowtime <= end)
    return;
  //Next Highlight
  else if(nowtime > end && nowIndex < VideoInfo.length-1){
    nowIndex++;
    $('#prevHL').css('visibility', 'visible');
    $('#HLtitle').text('Twitch Hight #'+(nowIndex+1));
    if(nowIndex == VideoInfo.length-1){
      $('#nextHL').css('visibility','hidden');
    }
  }
}

function getHL(id) {
  clickCount(id);
  $.getJSON("http://140.114.77.126:5000/api/v1.0/vodHighlight/"+id, function(data) {
    if(data.status == "true"){
      VideoInfo = data.videos;
      $.colorbox({
          inline:true,
          href:"#Highlight_div",
          onComplete:function(){
            nowIndex = 0;
            playerInitial(id);
          },
          onCleanup:function(){
            player.destroy();
            clearInterval(myVar);
          }
        });
      }
    else{
      swal("There is no Highlight now!", "We are adding this VOD to the queue of processing.", "warning");
    }
  });
}

function getlatestVOD(){
  $.getJSON("http://140.114.77.126:4000/api/v1.0/getlatestVOD", function(data) {
      for(i=0 ; i<data.length; i++){
          var d = new Date(data[i].video_time);
          var temp = d.toDateString().split(" ");
          var new_d = temp[1] + " " + temp[2] + ", " + temp[3];
          addLatest(data[i].vodid, data[i].prev_url, data[i].title, data[i].author, new_d, Math.floor(i/3)+1);
      }
  });
}

function getpopularVOD(){
  $.getJSON("http://140.114.77.126:4000/api/v1.0/getpopularVOD", function(data) {
      for(i=0 ; i<data.length; i++){
          var d = new Date(data[i].video_time);
          var temp = d.toDateString().split(" ");
          var new_d = temp[1] + " " + temp[2] + ", " + temp[3];
          addPopular(data[i].vodid, data[i].prev_url, data[i].title, data[i].author, new_d, Math.floor(i/3)+1);
      }
  });
}



$(document).ready(function() {
	$("#keyword").keypress(function(event) {
	    if (event.which == 13) {
          	var url = $('#keyword').val();
          	var token = url.split("/");
          	getHL(token[token.length-1]);
		$('#keyword').val("");
	        event.preventDefault();
	    }
	});
  getlatestVOD();
  getpopularVOD();
  JustAdd();
});
