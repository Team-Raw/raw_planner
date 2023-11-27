$('#search_btn').click(function(){
  showLoadingModal();
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
      hideLoadingModal();
      console.log('검색 조회 완료');
    }
  });
});


function showLoadingModal() {
  // 모달을 보이게 하는 부분
  document.getElementById('loading-modal').style.display = 'flex';
}

function hideLoadingModal() {
  // 모달을 숨기는 부분
  document.getElementById('loading-modal').style.display = 'none';
}
