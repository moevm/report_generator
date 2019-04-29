$('#empty_doc').click(function () {
    $('#requirements').empty();
});

$('#lab_doc').click(function(){
$('#requirements').empty();
});

$('#course_doc').click(function(){
$('#requirements').empty();
var teacher_field = '<div class="col-md-6 mb-3"><label for="teacher">Преподаватель</label><input type="text" class="form-control" id="teacher" placeholder="" name="teacher" value="{{ request.args.get(\'teacher\',\'\') }}"></div>'
$('#requirements').append(teacher_field);
});

$('#empty_doc').click(function(){
    $('#btnGroupDrop1').text("пустой документ");
})

$('#course_doc').click(function(){
    $('#btnGroupDrop1').text("Курсовая работа");
})

$('#lab_doc').click(function(){
    $('#btnGroupDrop1').text("лабораторная работа");
})
