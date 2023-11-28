$('#search_btn').click(function(e){
  if(check_text() == true){
    search_data(e)
  }
});

document.querySelector('#search_data').addEventListener('keyup', (e)=>{
  if (e.keyCode === 13) {
    if(check_text() == true){
      search_data(e)
    }
  }  
});

function search_data(e){
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
      alert('데이터가 존재하지 않습니다. 다시 입력해주세요.');		
    },
    complete: function(){
      hideLoadingModal();
      console.log('검색 조회 완료');
    }
  });
}

function showLoadingModal() {
  // 모달을 보이게 하는 부분
  document.getElementById('loading-modal').style.display = 'flex';
}

function hideLoadingModal() {
  // 모달을 숨기는 부분
  document.getElementById('loading-modal').style.display = 'none';
}

function check_text(){
  let input_data = document.getElementById('search_data');
  if(input_data.value.length == 0){
    alert("텍스트를 입력해주세요.");
    input_data.focus();
    return false;
  } else{
    return true
  }
}