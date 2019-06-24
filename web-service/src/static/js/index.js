$('#empty_doc').click(function () {
    $('#btnGroupDrop1').text("Пустой документ");
    $('#requirements').hide('slow');
    $('#requirements').empty();
});

$('#lab_doc').click(function(){
$('#btnGroupDrop1').text("Лабораторная работа");
if($('#requirements').is(':hidden') || $('*').is('#field_for_course'))
{
$('#requirements').empty();
$('#requirements').append('<div class="row" id="field_for_lab"</div>')
$('#field_for_lab').append("<div class='col-md-6 mb-3'><label for='teacher'>Преподаватель</label><input type='text' class='form-control' id='teacher'></div>");
$('#field_for_lab').append("<div class='col-md-6 mb-3'><label for='student'>Студент</label><input type='text' class='form-control' id='student' placeholder='' value=''></div>");
$('#field_for_lab').append("<div class='col-md-6 mb-3'><label for='number_group'>Номер группы</label><input type='text' class='form-control' id='number_group' placeholder='' value=''></div>");
$('#field_for_lab').append("<div class='col-md-6 mb-3'><label for='theme'>Тема лабораторной работы</label><input type='text' class='form-control' id='theme' placeholder='' value=''></div>");
$('#field_for_lab').append("<div class='col-md-6 mb-3'><label for='discipline'>Название предмета</label><input type='text' class='form-control' id='discipline' placeholder='' value=''></div>");
$('#field_for_lab').append("<div class='col-md-6 mb-3'><label for='cathedra'>Кафедра</label><input type='text' class='form-control' id='cathedra' placeholder='' value=''></div>");
$('#requirements').show("slow")
}
});

$('#course_doc').click(function(){
$('#btnGroupDrop1').text("Курсовая работа");

if($('#requirements').is(':hidden') || $('*').is('#field_for_lab'))
{
$('#requirements').empty();
$('#requirements').append('<div class="row" id="field_for_course"</div>');
$('#field_for_course').append("<div class='col-md-6 mb-3'><label for='teacher'>Преподаватель</label><input type='text' class='form-control' id='teacher' placeholder='' value=''></div>");
$('#field_for_course').append("<div class='col-md-6 mb-3'><label for='student'>Студент</label><input type='text' class='form-control' id='student' placeholder='' value=''></div>");
$('#field_for_course').append("<div class='col-md-6 mb-3'><label for='number_group'>Номер группы</label><input type='text' class='form-control' id='number_group' placeholder='' value=''></div>");
$('#field_for_course').append("<div class='col-md-6 mb-3'><label for='theme'>Тема курсовой работы</label><input type='text' class='form-control' id='theme' placeholder='' value=''></div>");
$('#field_for_course').append("<div class='col-md-6 mb-3'><label for='discipline'>Название предмета</label><input type='text' class='form-control' id='discipline' placeholder='' value=''></div>");
$('#field_for_course').append("<div class='col-md-6 mb-3'><label for='cathedra'>Кафедра</label><input type='text' class='form-control' id='cathedra' placeholder='' value=''></div>");
$('#field_for_course').append("<div class='col-md-6 mb-3'><label for='min_pages'>Минимальное количество страниц</label><input type='text' class='form-control' id='min_pages' placeholder='' value=''></div>");
$('#field_for_course').append("<div class='col-md-6 mb-3'><label for='date_start'>Дата начала</label><input type='text' class='form-control' id='date_start' placeholder='' value=''></div>");
$('#field_for_course').append("<div class='col-md-6 mb-3'><label for='date_finish'>Дата сдачи</label><input type='text' class='form-control' id='date_finish' placeholder='' value=''></div>");
$('#field_for_course').append("<div class='col-md-6 mb-3'><label for='date_defend'>Дата защиты</label><input type='text' class='form-control' id='date_defend' placeholder='' value=''></div>");
$('#requirements').show('show');
}
});


function checkImportantData(){
    return $('#wiki_name').val() != '' && $('#repo_name').val() != '' && $('#branch').val() != ''
}

$('#btn_submit').click(function () {
if(checkImportantData())
{
$( "div" ).remove( "#spinner_for_answer" );
$('#buttons_field').append('<div id="spinner_for_answer" class="spinner-border text-success" role="status"></div>')
}
})

$('#style_setter').click(function(){
if ($('#style_settings').is(':hidden'))
   {
   $('#style_settings').show("slow")
   $("#style_setter").css("background","#FF2400");
   }
else
   {
   $('#style_settings').hide("slow")
   $("#style_setter").css("background","#007bff");
   }
});


function submitForm(){
$.ajax({
                type: "POST",
                crossDomain: true,
                data: get_data_from_form(),
                success: function(json, status) {
                    console.log('Success for submit form');
                    location.reload();
                },
        })
}

function get_data_from_form(){
        var repo_name = $('#repo_name').val();
        var wiki_name = $('#wiki_name').val();
        var branch_name = $('#branch_name').val();
        var general_font = $('#general_font').val();
        var general_size = $('#general_size').val();
        var code_font = $('#code_font').val();
        var code_size = $('#code_size').val();
        var for_h1 = $('#for_h1').val();
        var for_h2 = $('#for_h2').val();
        var for_h3 = $('#for_h3').val();
        var for_h4 = $('#for_h4').val();
        var for_h5 = $('#for_h6').val();
        var for_h6 = $('#for_h6').val();


        var result = `repo_name=${repo_name}`;
        result += `&wiki_name=${wiki_name}`;
        result += `&branch_name=${branch_name}`;
 		result += `&general_font=${general_font}`;
 		result += `&general_size=${general_size}`;
 		result += `&code_font=${code_font}`;
 		result += `&code_size=${code_size}`;
 		result += `&h1=${for_h1}`;
 		result += `&h2=${for_h2}`;
 		result += `&h3=${for_h3}`;
 		result += `&h4=${for_h4}`;
 		result += `&h5=${for_h5}`;
 		result += `&h6=${for_h6}`;

 		if($("*").is("#teacher")){
 			var teacher = $('#teacher').val();
 			result += `&teacher=${teacher}`;
 			};
 		if($("*").is("#student")){
 			var student = $('#student').val();
 			result += `&student=${student}`;
 			};
 		if($("*").is("#number_group")){
 			var number_group = $('#number_group').val();
 			result += `&number_group=${number_group}`;
 			};
 		if($("*").is("#theme")){
 			var theme = $('#theme').val();
 			result += `&theme=${theme}`;
 			};
 		if($("*").is("#discipline")){
 			var discipline = $('#discipline').val();
 			result += `&discipline=${discipline}`;
 			};
 		if($("*").is("#cathedra")){
 			var cathedra = $('#cathedra').val();
 			result += `&cathedra=${cathedra}`;
 			};
 		if($("*").is("#min_pages")){
 			var min_pages = $('#min_pages').val();
 			result += `&min_pages=${min_pages}`;
 			};
 		if($("*").is("#date_start")){
 			var date_start = $('#date_start').val();
 			result += `&date_start=${date_start}`;
 			};
 		if($("*").is("#date_finish")){
 			var date_finish = $('#date_finish').val();
 			result += `&date_finish=${date_finish}`;
 			};
 		if($("*").is("#date_defend")){
 			var date_defend = $('#date_defend').val();
 			result += `&date_defend=${date_defend}`;
 			};

        return result;
    }

var _a = document.getElementById('repo_menu');

_a.addEventListener('click', changeRepo);
function changeRepo(e)
{
var ssh_str = 'git@github.com:' + event.target.href.substring(19) + '.git'
$("#repo_name").val(ssh_str);
e.preventDefault();
}

var _b = document.getElementById('wiki_menu');

_b.addEventListener('click', changeWiki);
function changeWiki(e)
{
var wiki_str = event.target.href + '.wiki.git'
$("#wiki_name").val(wiki_str);
e.preventDefault();
}



