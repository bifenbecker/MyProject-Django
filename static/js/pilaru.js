
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


const csrftoken = getCookie('csrftoken');
const API_URL_PREFIX = '/pilaru';


function api_add_item_to_order(btn, item_id) {
    let $btn = $(btn)
    let $span = $btn.find('span');

    let qty = parseInt($btn.parent().parent().find('input[name="item_qty"]')[0].value);

    $.ajax({
        url: API_URL_PREFIX + '/orders/api/add_item_to_order',
        type: 'post',
        data: { 'item_id': item_id, 'quantity': qty },
        headers: {
            'X-CSRFToken': csrftoken,
        },
        dataType: 'json',
        success: function (data) {
            if (data['result'] !== 'ok'){
                alert(data['result'])
            }else{
                let current_qty = parseInt($span.attr('data-count'));
                if (isNaN(current_qty)) {
                    current_qty = 0;
                }
                $span.attr('data-count', current_qty + qty);
            }

        },
        error: function (e) {
            alert('Ошибка запроса к серверу: ' + e.toString());
        }
    });
}


function api_remove_item_from_order(item_to_order_id) {
    console.log(item_to_order_id);
    $.ajax({
        url: API_URL_PREFIX + '/orders/api/remove_item_from_order',
        type: 'post',
        data: { 'item_to_order_id': item_to_order_id },
        headers: {
            'X-CSRFToken': csrftoken,
        },
        dataType: 'json',
        success: function (data) {
            document.location.reload();
        },
        error: function (e) {
            alert('Ошибка запроса к серверу: ' + e.toString());
        }
    });
}


function api_change_item_qty_in_order(input, item_to_order_id) {
    let quantity = input.value;
    $.ajax({
        url: API_URL_PREFIX + '/orders/api/change_item_qty_in_order',
        type: 'post',
        data: { 'item_to_order_id': item_to_order_id, 'quantity': quantity },
        headers: {
            'X-CSRFToken': csrftoken,
        },
        dataType: 'json',
        success: function (data) { },
        error: function (e) {
            alert('Ошибка запроса к серверу: ' + e.toString());
        }
    });
}


function api_close_order(order_id) {
    $.ajax({
        url: API_URL_PREFIX + '/orders/api/close_order',
        type: 'post',
        data: { 'order_id': order_id },
        headers: {
            'X-CSRFToken': csrftoken,
        },
        dataType: 'json',
        success: function (data) { },
        error: function (e) {
            alert('Ошибка запроса к серверу: ' + e.toString());
        }
    });

}

$(document).on('click', function(e) {
    var target = e.target;
    if(target.className === 'dropdown-item d-flex align-items-center' && target.onclick != null){
        var div_status = target.getElementsByClassName('badge badge-pill badge-secondary');
          
        if(div_status.length != 0){
            console.log(div_status[0].innerHTML);  
            div_status[0].innerHTML = 'Активный';
            div_status[0].className = 'badge badge-pill badge-success';
        }
    }
});

function filterElements(element){
    return element.getElementsByClassName('badge badge-pill badge-success').length != 0;
}

$(document.body).on("change", 'select[name="select_stage"]', function(){
    console.log(1);
    var product_stage_id = this.value;
    var item_to_order_id = this['children'][0]['id'];
    $.ajax({
        // TODO:Need To change
        url: '/pilaru/items/api/set_stage',
        type: 'post',
        data: { 'product_stage_id': product_stage_id, 'item_to_order_id': item_to_order_id },
        headers: {
            'X-CSRFToken': csrftoken,
        },
        dataType: 'json',
        success: function (data) { 
            
        },
        error: function (e) {
            alert('Ошибка запроса к серверу: ' + e['error']);
        }
    });
});

function replaceItem(btn, item_id, item_to_order_id){
    api_remove_item_from_order(item_to_order_id);
    api_add_item_to_order(btn, item_id);
}


$(document).on('click', 'button[name="btn-choose-similar"]', function () {
    let $btn = $(this);
    var item_id = $btn.attr('data-item-to-order-id');
    var item_to_order_item_id = $btn.attr('data-item-id');
    var remove_trs = Array.from(this.parentElement.parentElement.parentElement.children).filter(function(tr){
        return tr.className === 'remove-row_' + item_to_order_item_id;
    })
    if(remove_trs.length !== 0){
        remove_trs.forEach(function(item, i, arr){
            $(item).remove();
        })
    }else{
        $.ajax({
            // TODO:Need To change
            url: '/pilaru/items/api/get_similar',
            type: 'get',
            data: { 'item_to_order_item_id': item_to_order_item_id },
            headers: {
                'X-CSRFToken': csrftoken,
            },
            dataType: 'json',
            success: function (data) {
                data['similars'].forEach(function(item, i, arr){
                    $('#' + item_to_order_item_id + '_item').after('<tr class=remove-row_' + item_to_order_item_id + ' style="border:2px solid #ffccff"><td>' + item['id'] + '</td><td>' + item['name'] + '</td><td>-</td><td>' + item['supplier'] + '</td><td>' + item['unit_measurement'] + '</td><td><input class="form-control" type="number" name="item_qty" min="1" step="1" value="1"></td><td></td><td></td><td></td><td><button class="btn btn-info" onclick="replaceItem(this, ' + item['id'] + ', ' + item_id + ')">Заменить</button></td><td></td></tr>');
                })
            },
            error: function (e) {
                alert('Ошибка запроса к серверу: ' + e['error']);
            }
        });
    }
});