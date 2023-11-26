console.log("conn")
$('#search_btn').click(function(){
  console.log('ok')
  $.ajax({
    url: '/search_result',
    data: {
      input : $('#search_data').val()
    },
    type: 'post',
    success: function(result){
      document.body.innerHTML = '';
      document.write(result)
      // $('#output1').text(result);
    },
    error: function(){
      alert('ajax 통신 실패');		
    },
    complete: function(){
      console.log('api 호출 완료');
    }
  });
});
