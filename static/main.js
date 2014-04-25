
  $(function() {
    $('#datetimepicker4').datetimepicker({
      pickTime: false
    });

    $('.nav li a').on('click', function() {
    alert('clicked');
    $(this).parent().parent().find('.active').removeClass('active');
    $(this).parent().addClass('active');
	});

  });
