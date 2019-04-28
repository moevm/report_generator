$('#btn_start').click(function() {
	$('#message')
	.html('Message')
});
$('#btn_reset').click(function(){
	location.reload();
});

$('h1').css('color','green');

$('#empty_doc').click(function () {
    $('#requirements').empty();
});

$('#lab_doc').click(function(){
$('#requirements').empty();
$('#requirements').append('<div class="row" id="field_for_lab"</div>')
$('#field_for_lab').append("<div class='col-md-6 mb-3'><label for='teacher'>Преподаватель</label><input type='text' class='form-control' id='teacher' placeholder='' value=''>");
$('#field_for_lab').append("<div class='col-md-6 mb-3'><label for='student'>Студент</label><input type='text' class='form-control' id='student' placeholder='' value=''>");
$('#field_for_lab').append("<div class='col-md-6 mb-3'><label for='number_group'>Номер группы</label><input type='text' class='form-control' id='number_group' placeholder='' value=''>");
$('#field_for_lab').append("<div class='col-md-6 mb-3'><label for='theme'>Тема лабораторной работы</label><input type='text' class='form-control' id='theme' placeholder='' value=''>");
$('#field_for_lab').append("<div class='col-md-6 mb-3'><label for='discipline'>Название предмета</label><input type='text' class='form-control' id='discipline' placeholder='' value=''>");
$('#field_for_lab').append("<div class='col-md-6 mb-3'><label for='cathedra'>Кафедра</label><input type='text' class='form-control' id='cathedra' placeholder='' value=''>");
});

$('#course_doc').click(function(){
$('#requirements').empty();
$('#requirements').append('<div class="row" id="field_for_course"</div>')
$('#field_for_course').append("<div class='col-md-6 mb-3'><label for='teacher'>Преподаватель</label><input type='text' class='form-control' id='teacher' placeholder='' value=''>");
$('#field_for_course').append("<div class='col-md-6 mb-3'><label for='student'>Студент</label><input type='text' class='form-control' id='student' placeholder='' value=''>");
$('#field_for_course').append("<div class='col-md-6 mb-3'><label for='number_group'>Номер группы</label><input type='text' class='form-control' id='number_group' placeholder='' value=''>");
$('#field_for_course').append("<div class='col-md-6 mb-3'><label for='theme'>Тема курсовой работы</label><input type='text' class='form-control' id='theme' placeholder='' value=''>");
$('#field_for_course').append("<div class='col-md-6 mb-3'><label for='discipline'>Название предмета</label><input type='text' class='form-control' id='discipline' placeholder='' value=''>");
$('#field_for_course').append("<div class='col-md-6 mb-3'><label for='cathedra'>Кафедра</label><input type='text' class='form-control' id='cathedra' placeholder='' value=''>");

$('#field_for_course').append("<div class='col-md-6 mb-3'><label for='content'>Содержание</label><input type='text' class='form-control' id='content' placeholder='' value=''>");
$('#field_for_course').append("<div class='col-md-6 mb-3'><label for='min_pages'>Минимальное количество страниц</label><input type='text' class='form-control' id='min_pages' placeholder='' value=''>");
$('#field_for_course').append("<div class='col-md-6 mb-3'><label for='date_start'>Дата начала</label><input type='text' class='form-control' id='date_start' placeholder='' value=''>");
$('#field_for_course').append("<div class='col-md-6 mb-3'><label for='date_finish'>Дата сдачи</label><input type='text' class='form-control' id='date_finish' placeholder='' value=''>");
$('#field_for_course').append("<div class='col-md-6 mb-3'><label for='date_defend'>Дата защиты</label><input type='text' class='form-control' id='date_defend' placeholder='' value=''>");


});

$('#empty_doc').click(function(){
    $('#btnGroupDrop1').html("пустой документ");
})

$('#course_doc').click(function(){
    $('#btnGroupDrop1').html("Курсовая работа");
})

$('#lab_doc').click(function(){
    $('#btnGroupDrop1').html("лабораторная работа");
})
