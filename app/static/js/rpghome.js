/*
https://stackoverflow.com/questions/1051061/convert-json-array-to-an-html-table-in-jquery

https://stackoverflow.com/questions/26079754/flask-how-to-return-a-success-status-code-for-ajax-call
https://stackoverflow.com/questions/5589420/select-tr-by-id-with-jquery
https://roytuts.com/delete-multiple-rows-from-table-using-flask-ajax-jquery-mysql/
https://stackoverflow.com/questions/22437514/how-to-keep-elements-on-same-line-with-overflow

$.getJSON('/'+home+'/sheets', function(data) {
    $.each(data['sheets'], function(index, element) {
        console.log(element)
        $('body').append($('<div>', {
            text: element.id
        }));
    });
});
*/

function createButtonGroup (name, id) {
    var btnG = '<div class="sheet-stat button"><a class="btn btn-secondary btn-block" href="/'+home+'/edit/'+id+'" role="button">Edit</a></div>';
    return btnG+= '<div class="sheet-stat button last"><button class="btn btn-danger btn-block" name="delete" onclick="deleteSheet(\''+name+'\',\''+id+'\')">Delete</button></div>';
}

function formatName(name){
    if (name.length > 30) {
        name = name.substring(0,30)+"...";
    };
    return name;
};

function addSheetHitPoints(ch,mh){
    var hstr = '<div class="sheet-stat hp">';
    hstr += '<span class="green">'+ch+'</span>';
    hstr += ' / ';
    hstr += '<span class="green">'+mh+'</span>';
    return hstr += '</div>'
}

function appendUserRow (data){
    $('#no-user-sheets').remove();
    var rowString = '<div id=row_'+data['id']+' class="sheet"><div class="block">';
    rowString += '<div class="wrap sheet-stats"><a class="sheet-show" href="/'+home+'/sheet/'+data['id']+'"><div class="wrap justify-content-left">';
    rowString += '<div class="sheet-stat name">'+formatName(data['name'])+'</div>';
    rowString += '<div class="sheet-stat class">'+data['character_class']+'</div>';
    rowString += '<div class="sheet-stat background">'+data['background']+'</div>';
    rowString += '<div class="sheet-stat level">'+data['level']+'</div>';
    rowString += addSheetHitPoints(data['current_hp'],data['max_hp']);
    rowString += '</div></a></div>';
    rowString += createButtonGroup(data['name'], data['id']);
    rowString += '</div></div>';
    $('.user-sheets').append(rowString);
}

function appendPlayerRow (data){
    $('#no-player-sheets').remove();
    var rowString = '<div id=row_'+data['id']+' class="sheet"><div class="block">';
    rowString += '<div class="wrap sheet-stats"><a class="sheet-show" href="/'+home+'/sheet/'+data['id']+'"><div class="wrap justify-content-left">';
    rowString += '<div class="sheet-stat name">'+formatName(data['name'])+'</div>';
    rowString += '<div class="sheet-stat class">'+data['character_class']+'</div>';
    rowString += '<div class="sheet-stat background">'+data['background']+'</div>';
    rowString += '<div class="sheet-stat level">'+data['level']+'</div>';
    rowString += addSheetHitPoints(data['current_hp'],data['max_hp']);
    rowString += '<div class="sheet-stat user">'+data['user'][0]['username']+'</div>'
    rowString += '</div></a></div>';
    rowString += '</div></div>';
    $('.player-sheets').append(rowString);
}

function removeRow (id){
    $('#row_'+id).remove();
};

function createNewSheet () {
    $.ajax({
    type: "POST",
    url: '/'+home+'/create',
    dataType: 'json',
    success: function(data) {
        appendUserRow(data['sheets']);
    }});
};

function deleteSheet(name, id) {
    if (!window.confirm("Are you sure you want to delete: "+name+" ?" )) {
        return false
    };
    $.ajax({
    type: "DELETE",
    url: '/'+home+'/delete/'+id,
    dataType: 'json',
    success: function() {
        removeRow(id);
    }});
};


function queryUserSheets () {
    $.ajax({
        type: "GET",
        url: '/'+home+'/usersheets',
        dataType: 'json',
        success: function(data) {
            if (data['sheets'].length == 0){
                $('.user-sheets').append('<div id="no-user-sheets" class="justify-content-center"><p>You have no characters saved!</p></div>')
            } else {
                $.each(data['sheets'], function(index, element) {
                    appendUserRow(element);
                });
            };
        },
        error: function() {
            $('.user-sheets').append('<div id="no-user-sheets" class="justify-content-center"><p>You have no characters saved!</p></div>')
        }
    })
}

function queryPlayerSheets () {
    $.ajax({
        type: "GET",
        url: '/'+home+'/playersheets',
        dataType: 'json',
        success: function(data) {
            console.log(data);
            if (data['sheets'].length == 0){
                $('.player-sheets').append('<div id="no-player-sheets" class="justify-content-center"><p>There are no other player sheets!</p></div>')
            } else {
                $.each(data['sheets'], function(index, element) {
                appendPlayerRow(element);
                });
            };
            $('#player-paginate').append(generatePaginate(data['iter']))
        },
        error: function() {
            $('.player-sheets').append('<div id="no-player-sheets" class="justify-content-center"><p>There are no other player sheets!</p></div>')
        }
    })
}

/* 
*/ 
function generatePaginate(iter) {
    var pagStr = '<nav aria-label="..."><ul class="pagination">';
    if (!iter['has_prev']) {
        pagStr += '<li class="page-item disabled"><span class="page-link">Previous</span></li></li>';
    } else {
        pagStr += '<li class="page-item"><a class="page-link" href="/'+home+'/playersheets?page='+iter['prev_num']+'">Previous</a></li>';
    };
    for (let i = 0; i < iter['iter'].length;i ++) {
        if (i == iter['page'] ) {
            pagStr += '<li class="page-item active"><span class="page-link">'+i+'<span class="sr-only">(current)</span></span></li>';
        } else if (!i) {
            null
        } else {
            pagStr += '<li class="page-item"><a class="page-link" href="/'+home+'/playersheets?page='+i+'">'+i+'</a></li>';
        };
    };
    if (!iter['next_num']) {
        pagStr += '<li class="page-item disabled"><span class="page-link">Next</span></li></li>';
    } else {
        pagStr += '<li class="page-item"><a class="page-link" href="/'+home+'/playersheets?page='+iter['next_num']+'">next</a></li>';
    };
    return pagStr += '</ul></nav>'
}

/*
When the document is ready, query the backend to get all character sheets
*/
$( document ).ready(function() {
    queryUserSheets(); 
    queryPlayerSheets();
});
