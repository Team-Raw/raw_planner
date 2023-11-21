console.log('test');

$('#head_search_btn').click(function(){
  $.ajax({
    url: '/result',
    data: {
      input : $('#header_search_data').val()
    },
    type: 'post',
    success: function(result){
      document.write(result)
      // $('#output1').text(result);
    },
    error: function(){
      alert('ajax 통신 실패');		
    },
    complete: function(){
      console.log('asdgawe4rg');
      
    }
  });
});
