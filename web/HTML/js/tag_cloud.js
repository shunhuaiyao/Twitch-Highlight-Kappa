var fill = d3.scale.category20();

function getWC(id){
  $.getJSON("http://140.114.77.126:5000/api/v1.0/vodKeyword/"+id, function(data) {
    if(data.status == "true"){
      $.colorbox({
        inline:true,
        href:"#Wordcloud",
        onComplete:function(){
          var keyword = [];
          var wc_data = JSON.parse(data.content);
          var order = [];
          for(var obj in wc_data){
            size = 0
              if (wc_data[obj] < 0.3)
                 size = wc_data[obj]*150;
              else if (wc_data[obj] < 0.5) {
                size = wc_data[obj]*100;
              }
              else
                 size = wc_data[obj]*30
              keyword.push({'text': obj, 'size': size});
          }
          addTagCloud(keyword);
        },
        onCleanup:function(){
          $("#tag_vis").empty();
        }
      });
    }
    else{
      swal("There is no Highlight now!", "We are adding this VOD to the queue of processing.", "warning");
    }
  });
}


var addTagCloud = function(keyword) {
  d3.layout.cloud().size([854, 480])
      .words(keyword)
      .rotate(function() { return ~~(Math.random() * 2) * 0; })
      .font("Impact")
      .padding(5)
      .fontSize(function(d) { return d.size; })
      .on("end", draw)
      .start();
};

function draw(words) {
  d3.select("#tag_vis").append("svg")
      .attr("width", 854)
      .attr("height", 480)
    .append("g")
      // .attr("transform", "translate(250,150)")
      .attr("transform", "translate(" + 426 + "," + 240 + ")")
      .attr("xmlns", "http://www.w3.org/2000/svg")
      .attr("xmlns:xlink", "http://www.w3.org/1999/xlink")
    .selectAll("text")
      .data(words)
    .enter().append("text")
      .style("font-size", function(d) { return d.size + "px"; })
      .style("font-family", "Impact")
      .style("fill", function(d, i) { return fill(i); })
      .attr("text-anchor", "middle")
      .attr("transform", function(d) {
        return "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")";
      })
      .text(function(d) { return d.text; });

  $('text').each(function(){
    if($(this).text()=='BibleThump'){
      var test = $(this).get(0);
      var xforms = test.getAttribute('transform');
      var parts  = /translate\(\s*([^\s,)]+)[ ,]([^\s,)]+)/.exec(xforms);
      var firstX = parts[1]-parseInt($(this).css("font-size"))/2,
          firstY = parts[2]-parseInt($(this).css("font-size"))/2;
      // alert($(this).position().left- $(this).parent().parent().position().left);
      $(this).text("");
      d3.select("g").append("svg:image")
         .attr("transform",'translate('+firstX+','+firstY+')rotate(0)')
        //  .attr('x',$(this).position().left - $(this).parent().position().left - 150)
        //  .attr('y',$(this).position().top - $(this).parent().position().top - 150)
         .attr('width', parseInt($(this).css("font-size")))
         .attr('height', parseInt($(this).css("font-size")))
         .attr("xlink:href","../img/emoji/BibleThump.png")
    }
    else if($(this).text()=='MingLee'){
      var test = $(this).get(0);
      var xforms = test.getAttribute('transform');
      var parts  = /translate\(\s*([^\s,)]+)[ ,]([^\s,)]+)/.exec(xforms);
      var firstX = parts[1]-parseInt($(this).css("font-size"))/2,
          firstY = parts[2]-parseInt($(this).css("font-size"))/2;
      // alert($(this).position().left- $(this).parent().parent().position().left);
      $(this).text("");
      d3.select("g").append("svg:image")
         .attr("transform",'translate('+firstX+','+firstY+')rotate(0)')
        //  .attr('x',$(this).position().left - $(this).parent().position().left - 150)
        //  .attr('y',$(this).position().top - $(this).parent().position().top - 150)
         .attr('width', parseInt($(this).css("font-size")))
         .attr('height', parseInt($(this).css("font-size")))
         .attr("xlink:href","../img/emoji/MingLee.png")
    }
    else if($(this).text()=='SwiftRage'){
      var test = $(this).get(0);
      var xforms = test.getAttribute('transform');
      var parts  = /translate\(\s*([^\s,)]+)[ ,]([^\s,)]+)/.exec(xforms);
      var firstX = parts[1]-parseInt($(this).css("font-size"))/2,
          firstY = parts[2]-parseInt($(this).css("font-size"));
      // alert($(this).position().left- $(this).parent().parent().position().left);
      $(this).text("");
      d3.select("g").append("svg:image")
         .attr("transform",'translate('+firstX+','+firstY+')rotate(0)')
        //  .attr('x',$(this).position().left - $(this).parent().position().left - 150)
        //  .attr('y',$(this).position().top - $(this).parent().position().top - 150)
         .attr('width', parseInt($(this).css("font-size")))
         .attr('height', parseInt($(this).css("font-size")))
         .attr("xlink:href","../img/emoji/SwiftRage.png")
    }
    else if($(this).text()=='BabyRage'){
      var test = $(this).get(0);
      var xforms = test.getAttribute('transform');
      var parts  = /translate\(\s*([^\s,)]+)[ ,]([^\s,)]+)/.exec(xforms);
      var firstX = parts[1]-parseInt($(this).css("font-size"))/2,
          firstY = parts[2]-parseInt($(this).css("font-size"));
      // alert($(this).position().left- $(this).parent().parent().position().left);
      $(this).text("");
      d3.select("g").append("svg:image")
         .attr("transform",'translate('+firstX+','+firstY+')rotate(0)')
        //  .attr('x',$(this).position().left - $(this).parent().position().left - 150)
        //  .attr('y',$(this).position().top - $(this).parent().position().top - 150)
         .attr('width', parseInt($(this).css("font-size")))
         .attr('height', parseInt($(this).css("font-size")))
         .attr("xlink:href","../img/emoji/BabyRage.png")
    }
    else if($(this).text()=='godtoneGOD'){
      var test = $(this).get(0);
      var xforms = test.getAttribute('transform');
      var parts  = /translate\(\s*([^\s,)]+)[ ,]([^\s,)]+)/.exec(xforms);
      var firstX = parts[1]-parseInt($(this).css("font-size"))/2,
          firstY = parts[2]-parseInt($(this).css("font-size"));
      // alert($(this).position().left- $(this).parent().parent().position().left);
      $(this).text("");
      d3.select("g").append("svg:image")
         .attr("transform",'translate('+firstX+','+firstY+')rotate(0)')
        //  .attr('x',$(this).position().left - $(this).parent().position().left - 150)
        //  .attr('y',$(this).position().top - $(this).parent().position().top - 150)
         .attr('width', parseInt($(this).css("font-size")))
         .attr('height', parseInt($(this).css("font-size")))
         .attr("xlink:href","../img/emoji/godtoneGOD.png")
    }
    else if($(this).text()=='PeteZarollTie'){
      var test = $(this).get(0);
      var xforms = test.getAttribute('transform');
      var parts  = /translate\(\s*([^\s,)]+)[ ,]([^\s,)]+)/.exec(xforms);
      var firstX = parts[1]-parseInt($(this).css("font-size"))/2,
          firstY = parts[2]-parseInt($(this).css("font-size"));
      // alert($(this).position().left- $(this).parent().parent().position().left);
      $(this).text("");
      d3.select("g").append("svg:image")
         .attr("transform",'translate('+firstX+','+firstY+')rotate(0)')
        //  .attr('x',$(this).position().left - $(this).parent().position().left - 150)
        //  .attr('y',$(this).position().top - $(this).parent().position().top - 150)
         .attr('width', parseInt($(this).css("font-size")))
         .attr('height', parseInt($(this).css("font-size")))
         .attr("xlink:href","../img/emoji/PeteZarollTie.png")
    }
  });
}
