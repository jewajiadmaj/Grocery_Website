$('.show__account--number').mouseup(function(){
  
    if($('.account-number').attr('type') == 'password'){
      $('.account-number').attr('type', 'text');
      $('.pword_icon').removeClass('fa-eye-slash');
      $('.pword_icon').addClass('fa-eye');
    }
    else{
      $('.account-number').attr('type', 'password');
      $('.pword_icon').removeClass('fa-eye');
      $('.pword_icon').addClass('fa-eye-slash');
    }
  });