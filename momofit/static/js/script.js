$(document).ready(function(){
    $('.modal').modal();
  });

  document.addEventListener('DOMContentLoaded', function() {
    var elems = document.querySelectorAll('.datepicker');
    var instances = M.Datepicker.init(elems, options);
  });

  document.addEventListener('DOMContentLoaded', function() {
    var elems = document.querySelectorAll('.datepicker');
    var options = {format:'yyyy-mm-dd',
                   setDefaultDate:true};
    var instances = M.Datepicker.init(elems, options)
  });