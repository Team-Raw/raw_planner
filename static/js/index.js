function getCurrentDate() {
  const today = new Date();
  const year = today.getFullYear() - 1; // 1년 전
  const month = (today.getMonth() + 1).toString().padStart(2, '0');
  const day = (today.getDate() - 1).toString().padStart(2, '0');
  return `${year}-${month}-${day}`;
}

function getLastDate() {
  const endDate = new Date();
  endDate.setDate(endDate.getDate() - 1); // 오늘보다 하루 전
  const endYear = endDate.getFullYear();
  const endMonth = (endDate.getMonth() + 1).toString().padStart(2, '0');
  const endDay = endDate.getDate().toString().padStart(2, '0');
  return `${endYear}-${endMonth}-${endDay}`;
}

document.getElementById('start_date').value = getCurrentDate();
document.getElementById('end_date').value = getLastDate();

$('#search_btn').click(function(e){
  if(check_text() == true){
    if(check_date() == true){
      search_data(e)
    }
  }
});

document.querySelector('#search_data').addEventListener('keyup', (e)=>{
  if (e.keyCode === 13) {
    if(check_text() == true){
      if(check_date() == true){
        search_data(e)
      }
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
    alert('기간은 최소 1년 이상 차이가 나야 합니다. 다시 입력해주세요.');
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
      start_date : $("#start_date").val(),
      end_date : $("#end_date").val(),
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
  document.getElementById('loading-modal').style.display = 'flex';
}

function hideLoadingModal() {
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