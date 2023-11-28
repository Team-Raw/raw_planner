$('#search_btn').click(function(e){
  if(check_text() == true){
    console.log(check_date())
    // search_data(e)
  }
});

document.querySelector('#search_data').addEventListener('keyup', (e)=>{
  if (e.keyCode === 13) {
    if(check_text() == true){
      search_data(e)
    }
  }  
});

function check_date() {
  let today = new Date();
  let start_date = $('#start_date').val();
  let end_date = $('#end_date').val();

  if (start_date == '' || end_date == '') {
    alert('조회 날짜를 입력해주세요.');
    return false;
  }

  start_date = new Date(start_date);
  end_date = new Date(end_date);

  if (end_date <= start_date) {
    alert('시작 날짜는 마지막 날짜보다 클 수 없습니다. 다시 입력해주세요.');
    return false;
  }

  const oneYearInMillis = 365 * 24 * 60 * 60 * 1000; // milliseconds in a year
  if (end_date - start_date < oneYearInMillis) {
    alert('시작 날짜와 마지막 날짜는 최소 1년 이상 차이가 나야 합니다. 다시 입력해주세요.');
    return false;
  }

  if (start_date > today || end_date > today) {
    alert('조회 날짜는 오늘보다 클 수 없습니다. 다시 입력해주세요.');
    return false;
  }

  return true;
}

function search_data(e){
  showLoadingModal();
  $.ajax({
    url: '/search_result',
    data: {
      input : $('#search_data').val(),
      startDate : $(".from_date")[0].value,
      endDate : $(".to_date")[0].value
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