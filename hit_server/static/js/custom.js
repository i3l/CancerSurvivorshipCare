$(function(){
  console.log("Loaded custom js");
  $('#newlabel').click(function(e)
  {
    // e.preventDefault();
    console.log("You clicked foo! good work");
  });

  $(".lblname2").click(function(e){

    console.log("clicked");
    // console.log($(this).text());
    var txt = $(this).text().replace(/\s+/g, '');
    console.log(txt);

    url = "http://"+ window.location.host + "/patients/" + "label/" + txt + "/";
    console.log(url);
    window.open(url,"_self")


  });

  // $("body").on('click', ".lblname2",function(){
  //   window.alert("it works");
  // });

  $('#homelink').click(function(e){
    url = "http://"+ window.location.host + "/patients/label/all/";
    console.log(url);
    window.open(url,"_self")
  });
  $('#modalsave').click(function(e){

    var label = $('#newlabelname').val();
    var pid = $('#pid').text().replace(/\s+/g, '');
    console.log(label);
    console.log(pid);
    // url(r'^patients/label/(?P<lbl_name>.+)/(?P<patient_id>.+)/$', 'hit_server.views.addLabelToPatient', name='addLabelToPatient'),
    url = "http://"+ window.location.host + "/patients/" + label + "/label/" + pid + "/";
    console.log(url);
    var saveData = $.ajax({
      type: 'GET',
      url: url,
      data: {},
      dataType: "text",
      success: function (resultData) {
        location.reload();
        // callback(resultData); // need to get the <h2> text here..
      }
    });
  });
});
